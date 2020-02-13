#!/usr/bin/env bash
#
# Adapted from https://github.com/facebookresearch/MIXER/blob/master/prepareData.sh

# Training Set     用来训练模型
# Validation Set   用来做model selection
# Test set         用来评估所选出来的model的实际性能


function parm_err(){
	echo "Please input -l -m -moses -subword parms\n such as ./myprepare.sh -l no -m 0 -e ~/moses/mosesdecoder/scripts -s ~/subword-nmt/subword_nmt"
	echo "-l <protection>     <protection> can be 'no' 'tok' 'bpe' "
	echo "-m <model>          <model> can be 0 or 1 or 2  "
    echo "-e <path>           <path> is the path of moses scripts  "
    echo "-s <path>           <path> is the path of subword      "
	exit
	exit
}

LABLE=""
MODEL=""
# ~/moses/mosesdecoder/scripts
MOSESROOT=""
# ~/subword-nmt/subword_nmt
BPEROOT=""
BPE_TOKENS=10000
while getopts 'l:m:e:s:' opt
do
	case $opt in
		l)
			LABLE=$OPTARG;;
		m)
			MODEL=$OPTARG;;
        e)
            MOSESROOT=$OPTARG;;
        s)
            BPEROOT=$OPTARG;;
		*)
			parm_err
	esac
done
# echo $LABLE $MODEL

if  [ "$LABLE" != "no" ] && [ "$LABLE" != "tok" ] && [ "$LABLE" != "bpe" ]; then
	parm_err
fi

if  [ "$MODEL" != "0" ] && [ "$MODEL" != "1" ] && [ "$MODEL" != "2" ]; then  
	parm_err
fi

# script path
# 以.sh为中心,
# SCRIPTS 可设计成依赖上层参数,感觉设计成绝对路径比较好
SCRIPTS=$MOSESROOT
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
LC=$SCRIPTS/tokenizer/lowercase.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
CN_TOKENIZER=cn_tokenizer.py


src=cn
tgt=en
lang=cn-en
prep=../preprocess
tmp=$prep/tmp
orig=../orig
# rawdata 和 testdata也依赖上层参数
CREATDATA=../creat_data/data
rawprefix=out_test
testprefix=out_test
mkdir -p $orig $tmp $prep

# 最开始假设所需的资料都和脚本同目录,并且名字为$rawprefix.* $testprefix.*
for l in $src $tgt; do
    python lable_process.py $MODEL $CREATDATA/$rawprefix.$l  $l > $orig/$rawprefix.$l
    python lable_process.py $MODEL $CREATDATA/$testprefix.$l $l > $orig/$testprefix.$l
done

# 进行分词和清理
echo "pre-processing train data..."
for l in $src $tgt; do
    tok=train.tok.$l
    if [ "$l" == "$src" ];
    then 
	  python $CN_TOKENIZER $orig/$rawprefix.$l | perl $TOKENIZER -l cn > $tmp/$tok
	  echo "cn tokenizer finished"
    else
      perl $TOKENIZER -l en < $orig/$rawprefix.$l  >  $tmp/$tok 
	  echo "en tokenizer finished"
    fi
done

# CLEAN 会导致此处不好对应
perl $CLEAN -ratio 1.5 $tmp/train.tok $src $tgt $tmp/train.clean 1 175

# 跳过CLEAN
# cp $tmp/train.tok.$src $tmp/train.clean.$src
# cp $tmp/train.tok.$tgt $tmp/train.clean.$tgt

for l in $src $tgt; do
    perl $LC < $tmp/train.clean.$l > $tmp/train.tags.$l
done
echo "finished tokenize , clean , lowercase"

echo "creating train, valid, test..."
perl $TOKENIZER -l en < $orig/$testprefix.en | perl $LC > $tmp/test.en
python $CN_TOKENIZER $orig/$testprefix.cn  | perl $TOKENIZER -l cn | perl $LC > $tmp/test.cn 

# 在分词时不切分
if [ "$LABLE" != "no" ]; then
    for l in $src $tgt; do
        cp $tmp/test.$l $tmp/test.bak.$l
        cp $tmp/train.tags.$l $tmp/train.tags.bak.$l
    done

    for l in $src $tgt; do
        python restore_token.py $LABLE $MODEL $tmp/test.bak.$l > $tmp/test.$l
        python restore_token.py $LABLE $MODEL $tmp/train.tags.bak.$l > $tmp/train.tags.$l
    done
fi

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

if [ "$LABLE" == "bpe" ]; then # 仅BPE时保留
    for l in $src $tgt; do
        for f in train.$l valid.$l test.$l; do
            cp $prep/$f $prep/$f.bpebak
        done
    done

    for l in $src $tgt; do
        for f in train.$l valid.$l test.$l; do
            python restore_token.py $LABLE $MODEL $prep/$f.bpebak > $prep/$f
        done
    done
fi

TEXT=$prep
DATADIR=../preprocess_data
rm -rf $DATADIR
mkdir -p $DATADIR
fairseq-preprocess --source-lang $src --target-lang $tgt \
    --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test \
    --destdir $DATADIR \
    --workers 20