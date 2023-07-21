# 总结技术报告

## 主要贡献

负责“中传放心传”基于网页的文件上传加密与数字签名系统部分内容

## 技术工作

未完成什么太具有技术性的工作

## bug&方法

### 验证文件完整性

    from docopt import docopt

上述代码报错，在终端安装  `pip install docopot`  后报错消除

    if os.path.exists(filename):
        if confirm("[warning] remake data integrity file \'%s\'?" % filename):
            os.remove(filename)
            print "[successful] data integrity file \'%s\' has been remade." % filename
            sys.exit(0)
        else:
            print "[warning] data integrity file \'%s\'is not remade." % filename
            sys.exit(0)
    else:
        print >> sys.stderr, "[error] data integrity file \'%s\'is not exist." % filename

`"[successful] data integrity file \'%s\' has been remade."`  报错提示  `Statements must be separated by newlines or semicolons`  加括号后报错消除

    def makeDataIntegrity(path):
    path = unicode(path, 'utf8')  # For Chinese Non-ASCII character

`path = unicode(path, 'utf8')`  报错提示  `"unicode" is not defined` 加入语句  `import unicodedata`  并将原语句改为  `path = unicodedata(path, 'utf8')`  后报错消除

    while True:
            response = input("%s [%s] " % (question, suffix)).lower()

` response = raw_input("%s [%s] " % (question, suffix)).lower()`  代码报错，提示  `"raw_input" is not defined`  查询资料得知  Python3  将 `raw_input`  改为  `input`，遂将此处修改，报错消除

    print docopt(__doc__, argv="--help")

上述代码报错，提示  `Statements must be separated by newlines or semicolons`，仔细审查发现，忘加  `>>`，遂将此处修改，报错消除

运行之后提示异常，显示  `TypeError: expected string or bytes-like object`，查询资料未发现有效的办法，遂放弃。
