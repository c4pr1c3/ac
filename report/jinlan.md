# 中传放心传

## 陈锦兰 2020212063030

</br>

- 基于网页的文件上传加密与数字签名系统


- [x] 已完成《基于网页的用户注册与登录系统》所有要求
- [x] 限制文件大小：小于 10MB
- [x] 限制文件类型：office文档、常见图片类型
- [x] 匿名用户禁止上传文件
- [x] 对文件进行对称加密存储到文件系统，禁止明文存储文件 【 对称加密 密钥管理（如何安全存储对称加密密钥） 对称加密密文的PADDING问题 】
- [x] 系统对加密后文件进行数字签名 【 数字签名（多种签名工作模式差异） 】
- [ ] (可选）文件秒传：服务器上已有的文件，客户端可以不必再重复上传了

</br>

代码实现

```

from asyncio import exceptions
from hashlib import sha512
import os

def upload_file(cls,user,data):

    # 判断文件格式是否符合
    filename = data.filename
    suffix = filename.rfind('.')
    if suffix == -1
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
    if not os.path.exist(file)
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
    file = File(creator_id=creator_id, filename=filename， hash_value=hash_value)
    db.session.add(file)
    db.session.commit()
    return "上传成功"

```

在学习的过程中遇到了很多问题，比如文件格式的限制，因为包括了图片和文档都需要考虑进去。



