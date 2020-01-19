# Google

问题：

```html
谷歌翻译<b>可以</b>识别不同种标签
Google Translate <b> Yes </ b> identify different kinds of tags


人类破坏环境
Humans destroy the environment

人类破坏<b>环境</b>
Humans destroy the <b> environment </ b>

人类<b>破坏</b><b>环境</b>
Humans <b> destroy </ b> <b> environment </ b>


<!和上句对比就发现了严重问题，感觉谷歌应该不是泛化标签，根据大小写可以看出它确实是将p看做文本的分隔>
人类<p>破坏</p><b>环境</b>
Human <p> Destruction </ p> <b> Environment </ b>

人类<p>毁坏</p><b>环境</b>
Humans <p> Destroy </ p> <b> Environment </ b>


<!发现‘破坏’会出问题，很让我疑惑>
<p>人类破坏环境</p>
<p> Human destruction of the environment </ p>

<p>人类毁坏环境</p>
<p> Humans destroy the environment </ p>

点击图标以下载软件
Click on the icon to download the software

点击图标<b>以下载软件</b>
Click the icon <b> to download the software </ b>

点击图标下载软件
Click the icon to download the software

<!发现这个也有问题,'下载软件'看样子会被识别成一个短语整体翻译,而上文的'以下载软件',就不会被认为成一个短语>
点击图标<b>下载软件</b>
Click the icon <b> Download Software </ b>


<!基本上可以确定,谷歌会将标签内部的单独翻译(这个从句子的大小写就能看出来),但是它也尽量尝试去和标签外的进行联合翻译,这个还是结合上述的问题,就是/b会尝试联合翻译,/p则会尝试分隔进行翻译>
大家如果有需要翻译的文本,第一个也会想起谷歌翻译.
If you have text that needs to be translated, the first one will also think of Google Translate.


大家<b>如果有需要翻译的文本</b>,第一个也会想起谷歌翻译.
Everyone <b> If there is text that needs translation </ b>, the first one will also think of Google Translate.


<!在同一个词出现多次的情况下,谷歌可以正确翻译>
我们不仅要热爱<b>环境</b>,更要保护环境,珍惜<b>环境</b>
We must not only love the <b> environment </ b>, but also protect the environment and cherish the <b> environment </ b>

<!--谷歌也没考虑到语义问题,下面的例子应该是不翻译的-->
<code>声明</code>
<code> declaration </ code>


<!--标签错位问题-->
图像可被<b>文本编辑器创建</b>。
Images can be created by <b> text editors </ b>.
```
