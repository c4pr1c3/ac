from nacl.public import PrivateKey, SealedBox
from nacl.signing import SigningKey
from nacl.secret import SecretBox
from nacl.utils import random
from os.path import exists
from config import nacl_sk_path

if not exists(nacl_sk_path):
    # 生成私钥，用这个私钥可以推导出对应的公钥
    # PrivateKey 对象有一个属性叫做 .public_key，它是一个 PublicKey 对象，包含了公钥的信息。
    # 可以利用pk = sk.public_key还原出对应的公钥。
    sk = PrivateKey.generate()
    # 利用sk.encode将私钥导出为一个字符串
    sk_raw = sk.encode()
    with open(nacl_sk_path, 'wb') as f:
        f.write(sk_raw)
else:
    with open(nacl_sk_path, 'rb') as f:
        sk_raw = f.read()


def encrypt(plaintext: bytes):
    # 公钥加密
    # 利用密封盒类 实现公钥加密对应的消息plaintext
    return SealedBox(PrivateKey(sk_raw).public_key).encrypt(plaintext)


def decrypt(ciphertext: bytes):
    # 私钥解密
    # 利用密封盒类 实现私钥解密
    return SealedBox(PrivateKey(sk_raw)).decrypt(ciphertext)


def sign(message: bytes):
    # 公钥签名
    # 利用SigningKey类 生成一个源自sk-raw参数的私钥，并对message进行签名
    # .sign会返回一个SingnedMessage的对象，包含了消息和签名
    # 利用.signnature调用签名，作为返回值
    return SigningKey(sk_raw).sign(message).signature


def verify(message: bytes, signature: bytes):
    # 利用私钥对应的公钥验证签名
    # 利用SigningKey类 生成一个源自sk-raw参数的私钥
    # 利用.verify_key 获取这个私钥对应的公钥
    # 利用公钥的.verify来验证消息字节和签名字节
    return SigningKey(sk_raw).verify_key.verify(message, signature)

#以上为实现数字签名的函数，以下为实现对称加密的函数。

def new_symmetric_key():
    # 生成随机的256位对称密钥
    return random(SecretBox.KEY_SIZE)


def symmetric_encrypt(symmetric_key: bytes, plaintext: bytes):
    # 对称加密
    # 返回加密后的密文串
    return SecretBox(symmetric_key).encrypt(plaintext)


def symmetric_decrypt(symmetric_key: bytes, ciphertext: bytes):
    # 对称加密后的解密
    return SecretBox(symmetric_key).decrypt(ciphertext)


def get_pk_raw():
    # 获取公钥
    # 获取sk_raw对应的公钥
    return PrivateKey(sk_raw).public_key.encode()


def new_pair():
    # 产生新的公私钥对
    sk = PrivateKey.generate()
    return sk.encode(), sk.public_key.encode()
