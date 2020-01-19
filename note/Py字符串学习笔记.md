# Python 字符串学习笔记

## 编码
**Unicode编码**,其采用两字节表示字符(四字节表示非常偏僻的字符),将所有语言的文字都编码到了统一规则下.

但是它非常的浪费空间,所以后来推出的**UTF-8**就是用来解决这个问题,它采用变长的方式,根据不同的数字大小编码成1-6个字节.

**常用的英文字母被编码成1个字节，汉字通常是3个字节**，只有很生僻的字符才会被编码成4-6个字节.

非常方便的是,UTF-8完全兼容ASCII.

在计算机**内存中，统一使用Unicode编码**，当需要**保存到硬盘或者需要传输的时候，就转换为UTF-8编码**。

--- 
## Python中的字符串
### 编码转化
```python
# ord(ch)获取ch的整数表示
>>> ord('A')
65
>>> ord('中')
20013

# chr(i)获取以i为编码的字符
>>> chr(66)
'B'
>>> chr(25991)
'文'

# 上述两个操作互为逆运算
>>> ord(chr(66))
66
>>> chr(ord('B'))
'B'

# 用十六进制直接输出也可(4e2d的十进制就是20013)
>>> '\u4e2d\u6587'
'中文'
```

除此之外,还有编码与二进制数据之间的转化,此处廖雪峰写的不是很详细.以下掺杂着我个人的猜想

```python
# bytes类型是一个 0 <= x < 256 区间内的整数不可变序列。也就是每个元素就是一字节的二进制
>>> s2=b'ABC'
>>> type(s2)
<class 'bytes'>

# encode可以将字符串以特定的编码形式的规范转化成bytes类型
>>> 'ABC'.encode('ascii')
b'ABC'
>>> '中文'.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'
>>> '中文'.encode('ascii') # 溢出
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)

# decode恰恰相反,其是将bytes类型转化成字符串类型
>>> b'ABC'.decode('ascii')
'ABC'
>>> b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
'中文'

# 如果bytes中包含无法解码的字节，decode()方法会报错：
# 如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节：
>>> b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
'中'
```
一般在文件开头,我们都会加上
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```
第一行注释是为了告诉**Linux/OS X**系统，这是一个Python可执行程序，**Windows系统会忽略这个注释**

第二行注释是为了告诉Python解释器，按照UTF-8编码读取源代码，否则，你在源代码中写的中文输出可能会有乱码,并且首先保证文件真的是UTF-8的

### 输入输出
python的字符串格式化和c语言的相似,也是占位符+参数的形式,不过是以'%'+参数实现的,一个参数的时候可以不加括号,%s是万能输出格式(甚至数组字典都可以打印)
```python
# %d    整数
# %f	浮点数(同样可以控制尾数长度以及总体长度等)
# %s	字符串
# %x	十六进制整数
# %%    非转义,单纯打一个'%'
s = 'Hello,%s %d %%' % ("world", 2333)
print(s)
```
**format()**

另一种格式化字符串的方法是使用字符串的format()方法，它会用传入的参数依次替换字符串内的占位符{0}、{1}……，不过这种方式写起来比%要麻烦得多：
```python
>>> 'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125)
'Hello, 小明, 成绩提升了 17.1%'
```

```python
# ljust(len，str) 字符向左对齐，用str补齐长度
print 'bbb'.ljust(10,'a')
# bbbaaaaaaa

# rjust(len，str) 字符向右对齐，用str补齐长度
print 'bbb'.rjust(10,'a')
# aaaaaaabbb

# center(len，str)字符中间对齐，用str补齐长度
print 'bbb'.center(10,'a')
# aaabbbaaaa

# zfill(width)指定字符串长度，右对齐，前面补充0
print '2'.zfill(5)
# 00002
```
