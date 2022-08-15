from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, and_
from os import remove, path, mkdir
import re
from database import db
from config import storage_path
import secret
from asyncio import exceptions
from hashlib import sha512
import os

filename_pattern = re.compile(r'[^\u4e00-\u9fa5]+')


class File(db.Model):
    __tablename__ = 'files'
    creator_id = Column(Integer, ForeignKey('users.id_', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    filename = Column(String(64), primary_key=True)
    hash_value = Column(String(128))
    shared = Column(Boolean, default=False)

    @classmethod
    def upload_file(cls,user,data):
        # 判断文件格式是否符合
        filename = data.filename
        # file_postfix = filename.split('.')[1]
        suffix = filename.rfind('.')
        if suffix == -1:
            raise exceptions.APIException('图片不正确')
        file_postfix = filename.name[suffix + 1:]
        if file_postfix not in ['jpg', 'png', 'gif', 'bmp', 'jpeg', 'JPG', 'PNG','BMP', 'JPEG', 'doc''docx', 'xls', 'xlsx', 'ppt', 'pptx']:
            raise exceptions.APIException('文件格式不正确')

        #判断文件大小是否大于10MB
        content = data.read()
        size = len(content) /1024 /1024
        assert size < 10, '文件过大'

        #判断文件是否存在
        file = File.query.filter_by(File.filename == filename).first()
        assert not file,'文件已经存在'

        #文件添加路径
        if not os.path.exist(file):
            user_id = str(user.id_)+'/'
            mkdir(storage_path+user_id)

            #对用户对称密钥解密
            user_symmetric_key = secret.decrypt(user.encrypted_symmetric_key)
            #用系统对称密钥对文件内容加密
            content = secret.symmetric_encrypt(user_symmetric_key, content)

            #对加密文件签名
            signature = signature = secret.sign(content)

            #计算文件哈希值
            hash_value = sha512(content).hexdigest()

            #保存密文和签名
            with open(storage_path+user_id+hash_value, 'wb') as f:
                f.write(content)
            with open(storage_path+user_id+hash_value+'.sig', 'wb') as f:
                f.write(signature)

        creator_id = user.id_
        file = File(creator_id=creator_id, filename=filename, hash_value=hash_value)
        db.session.add(file)
        db.session.commit()
        return "上传成功"

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
            # 读取密文
            with open(storage_path+str(user.id_)+'/'+hash_value, 'rb') as f_:
                content = f_.read()
            if type_ == 'plaintext':
                content = secret.symmetric_decrypt(secret.decrypt(user.encrypted_symmetric_key), content)
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
