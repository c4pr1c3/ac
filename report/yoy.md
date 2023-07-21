# 「中传放心传」总结技术报告

负责人：吴晓晓 2020212063026

## 项目介绍

小组协作开发完成“**中传放心传**”项目，在示例代码上进行二次开发，可以实现用户登录注册及文件上传共享以及基于网页的加解密工作，其中本人在项目中主要负责完成”**基于网页的注册与登录系统**“，对示例代码给出的文件上传加密与数字签名系统及加密文件下载与解密功能进行分析运用，通过屏幕操作录像回答相关知识运用问题，在开发过程中积累经验，提高水平。

## 实验过程

- ### 查看示例代码，确定二次开发方案，安装docker环境

![docke01](C:\Users\wxxiao\Desktop\docke01.bmp)

![docker02](C:\Users\wxxiao\Desktop\docker02.bmp)

在这步中不知道如何打开网站安装docker，一开始下载最新版本的docker，在命令行里无法运行，docker-compose无法运行，在网上查找相关情况建议降低版本，重新下载4.4版的docker，并下载wsl_update，成功运行代码进入网站。

- ### 配置openssl环境，自签发证书

要自己建一个CA，然后对自己的请求文件进行认证然后生成证书，私钥和证书，一共俩

ubuntu上一般都自带安装了OpenSSL

```ruby
ubuntu:~$ openssl
OpenSSL> version
OpenSSL 1.1.1  11 Sep 2018
OpenSSL>
```

#### 基本概念

- **CA**：认证机构。有自己的**证书**，可以拿自己的证书给别人签名然后收钱，这个星球上的CA被几家说英语的人垄断了。在这里我们会虚拟出一个CA机构，然后用他来给自己的证书认证签名。
- **(网站)证书** ：发送给客户端的证书，其中大部分是公钥。是一个包含自己网站的公钥、认证、签名等信息的文件。
- **(网站)私钥** ：服务器留存的解密私钥(server)

#### 基本流程

1. 搞一个虚拟的CA机构，生成一个证书
2. 生成一个自己的密钥，然后填写证书认证申请，拿给上面的CA机构去签名
3. 于是就得到了**自（自建CA机构认证的）签名证书**

#### 首先，虚构一个CA认证机构出来

```csharp
# 生成CA认证机构的证书密钥key
# 需要设置密码，输入两次
openssl> genrsa -des3 -out ca.key 1024

# 去除密钥里的密码(可选)
# 这里需要再输入一次原来设的密码
openssl> rsa -in ca.key -out ca.key

# 用私钥ca.key生成CA认证机构的证书ca.crt
# 其实就是相当于用私钥生成公钥，再把公钥包装成证书
openssl> req -new -x509 -key ca.key -out ca.crt -days 365
# 这个证书ca.crt有的又称为"根证书",因为可以用来认证其他证书
```

#### 其次，才是生成网站的证书

```css
# 生成自己网站的密钥server.key
openssl> genrsa -des3 -out server.key 1024

# 生成自己网站证书的请求文件
# 如果找外面的CA机构认证，也是发个请求文件给他们
# 这个私钥就包含在请求文件中了，认证机构要用它来生成网站的公钥，然后包装成一个证书
openssl> req -new -key server.key -out server.csr

# 使用虚拟的CA认证机构的证书ca.crt，来对自己网站的证书请求文件server.csr进行处理，生成签名后的证书server.crt
# 注意设置序列号和有效期（一般都设1年）
openssl> x509 -req -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt -days 365
```

至此，私钥`server.key`和证书`server.crt`已全部生成完毕，可以放到网站源代码中去用了。

![crt](C:\Users\wxxiao\Desktop\crt.bmp)

- ### 网页前端界面改善



