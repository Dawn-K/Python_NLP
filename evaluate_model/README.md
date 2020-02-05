## 结果评估脚本

### 使用方法

#### 直接调用脚本
```python
python evaluate.py  CN_SOURCE_FILE EN_SOURCE_FILE EN_REF_FILE
```

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