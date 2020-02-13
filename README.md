# Python_NLP

![](https://img.shields.io/badge/license-MIT-blue)

本仓库记录寒假在小牛翻译实验室编写的一些程序


## creat_data

构造带标签的双语语料

### 环境要求

 - Linux
 - Python >= 3.6
 - torch >= 1.3.0                       
 - torchvision >= 0.4.2    
 - PyNLPIR           
 - perl        

### 使用方法

首先编辑 `main.sh` ,配置好文件

```bash
chmod +x main.sh
./main.sh  -l <protection> -m <model>
```
`<protection> 只能是 'no' 'tok' 'bpe'中的一种 `
`<model> 只能是 0 或 1 或 2`
```
0 : 不泛化
1 : 标签两端加$copy
2 : 完全泛化
```

举例
```
./main.sh -l bpe -m 1 
```
**2/13/2020 :**

制造出的带标签数据存在`orig/`里面

`process_data/`存放 fairseq-preprocess 生成的文件

`test.sh`可以调用`main.sh`生成所有九种数据