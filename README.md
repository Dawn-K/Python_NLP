# Python_NLP

![](https://img.shields.io/badge/license-MIT-blue)

本仓库记录寒假在小牛翻译实验室编写的一些程序

---

## count_HTML

项目进行初期对HTML的统计脚本及统计结果

---

## creat_data

构造带标签的双语语料

### 环境要求

 - Linux
 - Python >= 3.6
 - torch >= 1.3.0                       
 - torchvision >= 0.4.2    
 - PyNLPIR         
 - numpy           

### 使用方法


#### 产生对齐信息

```python
    python main.py
```

main.py默认读取同目录下的wmt2018文件(在文件中可修改),会自动在同目录下生成data文件夹,其中的final.align 即对齐信息

#### 产生对齐语料

```python
    python Lable.py
```

Lable.py会读取data/cn,data/en,data/final.align文件,然后生成out_test.cn, out_test.en,即最后的语料

