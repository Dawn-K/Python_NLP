## 结果评估脚本

### 使用之前

#### 环境要求

- Linux / MacOS
- python3
- pynlpir
- perl 

注: 为保证输出美观,执行perl脚本时出现的**任何错误输出都被重定向到了data/log**下

### 使用方法
如果tools下的perl脚本无执行权限,请先 `chmod +x tools/*.perl`

#### 直接调用脚本
```python
python evaluate.py  CN_SOURCE_FILE EN_SOURCE_FILE EN_REF_FILE
```
举例`python evaluate.py out_test.cn out_test.en out_ref_test.en `由于后两个文件内容相同,所以测出的结果就是
```bash
precision :  1.0
recall :  1.0
F1 value :  1.000
BLEU = 100.00, 100.0/100.0/100.0/100.0 (BP=1.000, ratio=1.000, hyp_len=3926, ref_len=3926)
```
可通过修改 out_test.en 以验证正确性

#### 以函数形式调用
``` python
import evaluate

evaluate.evaluate(CN_file, EN_file, EN_ref_file)
```


### 目录结构

```bash
.
├── BLEU.py
├── data        # 存放临时数据文件
├── evaluate.py
├── PRF.py
├── __pycache__ # 存放缓存文件
├── README.md
├── share       # 英文分词所需的依赖
│   └── nonbreaking_prefixes
│       └── nonbreaking_prefix.en
└── tools       # 用到的脚本
    ├── multi-bleu.perl
    ├── tokenizer.perl
    ├── train-truecaser.perl
    └── truecase.perl
```

`tools` 中的文件在moses的对应位置:

```bash
 moses/mosesdecoder/scripts/generic/multi-bleu.perl
 moses/mosesdecoder/scripts/recaser/train-truecaser.perl
 moses/mosesdecoder/scripts/recaser/truecase.perl
 moses/mosesdecoder/scripts/tokenizer/tokenizer.perl
```