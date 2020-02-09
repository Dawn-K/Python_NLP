#!/usr/bin/env bash
#
# Adapted from https://github.com/facebookresearch/MIXER/blob/master/prepareData.sh

# Training Set     用来训练模型
# Validation Set   用来做model selection
# Test set         用来评估所选出来的model的实际性能


# script path
SCRIPTS=moses/mosesdecoder/scripts
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
CN_TOKENIZER=cn_tokenizer.py
LC=$SCRIPTS/tokenizer/lowercase.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
BPEROOT=subword-nmt/subword_nmt
BPE_TOKENS=10000

# check moses path
if [ ! -d "$SCRIPTS" ]; then
    echo "Please set SCRIPTS variable correctly to point to Moses scripts."
    exit
fi

src=cn
tgt=en
lang=cn-en
prep=preprocess
tmp=$prep/tmp
orig=orig
rawprefix=rawdata
testprefix=testdata
mkdir -p $orig $tmp $prep

# 最开始假设所需的资料都和脚本同目录,并且名字为$rawprefix.* $testprefix.*
for l in $src $tgt; do
    cp $rawprefix.$l $orig/
    cp $testprefix.$l $orig/
done

# 进行分词和清理
echo "pre-processing train data..."
for l in $src $tgt; do
    tok=train.tok.$l
    if [ "$l" == "$src" ];
    then 
	  python $CN_TOKENIZER $orig/$rawprefix.$l > $tmp/$tok
	  echo "cn tokenizer finished"
    else
      perl $TOKENIZER -l en < $orig/$rawprefix.$l  >  $tmp/$tok 
	  echo "en tokenizer finished"
    fi
done
perl $CLEAN -ratio 1.5 $tmp/train.tok $src $tgt $tmp/train.clean 1 175
for l in $src $tgt; do
    perl $LC < $tmp/train.clean.$l > $tmp/train.tags.$l
done
echo "finished tokenize , clean , lowercase"

echo "creating train, valid, test..."
perl $TOKENIZER -l en < $orig/$testprefix.en | perl $LC > $tmp/test.en
python $CN_TOKENIZER $orig/$testprefix.cn  | perl $LC > $tmp/test.cn 

# 每23条抽一条放到valid.*,剩下的放到train.*
for l in $src $tgt; do
    awk '{if (NR%23 == 0)  print $0; }' $tmp/train.tags.$l > $tmp/valid.$l
    awk '{if (NR%23 != 0)  print $0; }' $tmp/train.tags.$l > $tmp/train.$l
done
echo "finish creating train, valid, test"

TRAIN=$tmp/train.en-cn
> $TRAIN 
BPE_CODE=$prep/code
for l in $src $tgt; do
    cat $tmp/train.$l >> $TRAIN
done

echo "learn_bpe.py on ${TRAIN}..."
python $BPEROOT/learn_bpe.py -s $BPE_TOKENS < $TRAIN > $BPE_CODE

# 将train.$L valid.$L test.$L 子词切分后移动到$prep/下
for L in $src $tgt; do
    for f in train.$L valid.$L test.$L; do
        echo "apply_bpe.py to ${f}..."
        python $BPEROOT/apply_bpe.py -c $BPE_CODE < $tmp/$f > $prep/$f
    done
done