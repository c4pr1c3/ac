
# 中传放心传

----

#### 作品简介
 
完成一个集基于网页的用户注册与登录系统、文件上传加密与数字签名系统和加密文件下载与解密一体的作品

#### 技术使用

HTML + CSS

#### 个人贡献

我在本次项目中担当的主要作用是：完成网页前端网页的设计和给予用户的注册与登录系统的设计与完善、理解半成品python代码的结构和内容、帮助大家完善配置环境

#### 重要代码

对编写的代码中印象比较深刻的部分：

* 通过正则表达式对注册的用户邮箱进行限制：
```python
username_pattern = re.compile(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
```
* 页面确认弹窗：
```python
 <button class="btn" onclick="{if(confirm('确认跳转嘛？'))location.href='/login'}">登 录</button>
```
* 主页的左侧导航栏：
    * html部分
```python
<div class="wrap">
        <div class="nav">
            <div class="btn">
                <div class="btn-item"></div>
                <div class="btn-item"></div>
                <div class="btn-item"></div>
            </div>
            <div class="icon">
                <div class="icon-img"><img src="static/img/photo.jpg" alt="" /></div>
                <div class="icon-con">
                    <p>中传放心传</p>
                    <h4>{{username}}</h4>
                </div>
            </div>
            <div class="line"></div>
            <div class="title">
                <p>公开</p>
            </div>
            <div class="menu">
                <div class="item">
                    <div class="light"></div>
                    <div class="licon"><span class="iconfont icon-wenjian"></span></div>
                    <div class="con"><a href="/shared_file">共享文件</a></div>
                    <div class="ricon"><span class="iconfont icon-share"></span></div>
                </div>                
            </div>
            <div class="line"></div>
            <div class="title">
                <p>个人</p>
            </div>
            <div class="menu">
                <div class="item">
                    <div class="light"></div>
                    <div class="licon"><span class="iconfont icon-mine"></span></div>
                    <div class="con"><a href="/file">我的文件</a></div>
                    <div class="ricon">
                        <span class="iconfont icon-myfile"></span>
                    </div>
                </div>                
            </div>
            <div class="line"></div>
            <div class="title">
                <p>更多</p>
            </div>
            <div class="menu">
                <div class="item">
                    <div class="light"></div>
                    <div class="licon"><span class="iconfont icon-exit"></span></div>
                    <div class="con"><a href="/logout">退出登录</a></div>
                    <div class="ricon">
                        <span class="iconfont icon-logout"></span>
                    </div>
                </div>                
            </div>
            <div class="line"></div>
            <div class="title">
                <p>关于</p>
            </div>
            <div class="menu">
                <div class="item">
                    <div class="light"></div>
                    <div class="licon"><span class="iconfont icon-caidan"></span></div>
                    <div class="con">
                        <h5>这是由陈锦兰、吴晓晓、钟佳欣、方诗棋完成的中传放心传</h5>
                    </div>
                    <div class="ricon">
                        <span class="iconfont icon-Dashboard"></span>
                    </div>
                </div>                
            </div>
        </div>    
```
*    * CSS部分
```css
.wrap {
        width:100%;
        height: 100vh;
        background: url(img/bg.jpg) center no-repeat;
        background-size: cover;
        display: flex;
        padding-left: 20px;
    }
.nav {
        width: 110px;
        height: 820px;
        background: #a6c1ee;
        border-radius: 20px;
        overflow: hidden;
        transition: 0.5s;
    }

    .nav:hover {
        width: 280px;
    }

    .btn {
        width: 60px;
        height: 10px;
        display: flex;
        justify-content: space-around;
        margin-left: 25px;
        margin-top: 25px;
    }

    .btn-item {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }

    .btn-item:nth-child(1) {
        background: palevioletred;
    }

    .btn-item:nth-child(2) {
        background: beige;
    }

    .btn-item:nth-child(3) {
        background: rgb(112, 128, 144);
    }

    .icon {
        width: 250px;
        height: 60px;
        margin-left: 25px;
        margin-top: 20px;
        display: flex;
    }   

    .icon-img {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 4px solid #fff;
        overflow: hidden;
    }

    .icon-img img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
    }

    .icon-con {
        height: 60px;
        margin-left: 25px;
    }

    .icon-con p {
        padding-top: 5px;
    }

    .icon-con h4 {
        font-weight: 300;
    }

    .line {
        width: 60px;
        height: 1px;
        background: #fff;
        margin: 20px 25px;
        transition: 0.5s;
    }

    .nav:hover .line {
        width: 230px;
    }

    .title {
        width: 60px;
        margin-left: 25px;
        margin-bottom: 20px;
    }

    .title p {
        font-size: 16px;
    }

    .item {
        display: flex;
        position: relative;
        transition: 0.5s;
        border-radius: 6px;
    }

    .item:hover {
        background: #f0c4e4;
    }

    .licon {
        width: 60px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .con {
        width: 0px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: 0.5s;
        overflow: hidden;
        position: relative;
        left: -20px;
        opacity: 0;
    }

    .nav:hover .con {
        width: 160px;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 1;
    }

    .ricon {
        width: 0px;
        height: 50px;
        transition: 0.5s;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        position: relative;
        opacity: 0;
    }

    .nav:hover .ricon {
        width: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 1;
    }

    .iconfont {
        font-size: 26px;
    }

    .ricon .iconfont {
        font-size: 20px;
        color: #62cb44;
    }

    .light {
        width: 6px;
        height: 50px;
        background: #fbc2eb;
        position: absolute;
        left: -25px;
        transition: 0.5s;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
        opacity: 0;
    }

    .item:hover .light {
        opacity: 1;
    }  

    .menu {
        width: 230px;
        margin-left: 25px;
    }

    .nav:hover .serve {
        width: 230px;
    }
```
#### 遇到的困难

本次网页的设计超出了我的css水平，编写过程中参考了许多资料，并且对于网页布局不断地调试，最终得到这个页面设计。并且通过查询资料加深了对正则表达式、文件加密上传等内容的理解。