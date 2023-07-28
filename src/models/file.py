from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, and_
from os import remove, path, mkdir
import re
from database import db
from config import storage_path
import secret

filename_pattern = re.compile(r'[^\u4e00-\u9fa5]+')


class File(db.Model):
    #创建表单'file'
    __tablename__ = 'files'
    creator_id = Column(Integer, ForeignKey('users.id_', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    filename = Column(String(64), primary_key=True)
    hash_value = Column(String(128))
    shared = Column(Boolean, default=False)

    @classmethod
    def upload_file(cls, user, data):
        from hashlib import sha512
        from config import allowed_file_suffix_list
        filename = data.filename
        # 文件名长度限制。
        assert len(filename) <= 64, 'Filename is too long (>filename.length>64B)'
        # 对文件.之后的部分进行拆分（后缀名），将后缀名赋值给filename_suffix。
        assert filename_pattern.fullmatch(filename), 'No unicode character allowed'
        filename_suffix = filename.rsplit('.', maxsplit=1)[-1]
        # 限制文件类型，只有后缀名为config中自定义的变量allowed_file_suffix_list中定义的类型，才能上传。
        assert filename_suffix in allowed_file_suffix_list, 'Unsupported file format'
        # 查询数据库，通过查询本地的create_id、filename和线上的user_id、filename判定文件名是否重复。
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert not f, 'Please do not upload the same file'
        # 读取文件，转为字符串，判定字符串的长度是否小于10*1024^2，若大于则不允许上传。
        content = data.read()
        assert len(content) < 10*1024*1024, 'The file size exceeds the limit (>=10MB)'
        # 创建存储用户名的文件
        user_id = str(user.id_)+'/'
        if not path.exists(storage_path+user_id):
            if not path.exists(storage_path):
                mkdir(storage_path)
            mkdir(storage_path+user_id)
        # 计算原文件的哈希
        hash_value = sha512(content).hexdigest()
        # 判断文件是否存在
        if not path.exists(storage_path+user_id+hash_value):
            # 对称加密。加密前得先还原出对称密钥。
            content = secret.symmetric_encrypt(secret.decrypt(user.encrypted_symmetric_key), content)
            # 同时计算签名，利用了secret中的sign计算签名
            signature = secret.sign(content)
            # 保存密文与签名
            with open(storage_path+user_id+hash_value, 'wb') as f:
                f.write(content)
            with open(storage_path+user_id+hash_value+'.sig', 'wb') as f:
                f.write(signature)
        creator_id = user.id_
        file = File(creator_id=creator_id, filename=filename, hash_value=hash_value)
        db.session.add(file)
        db.session.commit()

    @classmethod
    def delete_file(cls, user, filename):
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        db.session.delete(f)
        db.session.commit()
        files = File.query.filter(File.hash_value == hash_value).all()
        if not len(files):
            remove(storage_path+str(user.id_)+'/'+hash_value)
            remove(storage_path+str(user.id_)+'/'+hash_value+'.sig')

    @classmethod
    def download_file(cls, user, filename, type_):
        from flask import make_response
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        if type_ == 'hashvalue':
            content = hash_value
            filename = filename + '.hash'
        elif type_ == 'signature':
            # 读取签名
            with open(storage_path+str(user.id_)+'/'+hash_value+'.sig', 'rb') as f_:
                content = f_.read()
                filename = filename+'.sig'
        else:
            with open(storage_path+str(user.id_)+'/'+hash_value, 'rb') as f_:
                content = f_.read()
            # 读取明文
            if type_ == 'plaintext':
                content = secret.symmetric_decrypt(secret.decrypt(user.encrypted_symmetric_key), content)
            # 读取密文
            elif type_ == 'encrypted':
                filename = filename + '.encrypted'
   

        
        response = make_response(content)
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    @classmethod
    def share_file(cls, user, filename):
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        f.shared = not f.shared
        db.session.commit()
