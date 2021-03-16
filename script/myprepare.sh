#!/usr/bin/env bash

#对数据进行预处理


function parm_err(){
	echo "Please input -l -m -k -moses -subword  -c parms\n such as ./myprepare.sh -l no -m 0 -k 6 -e ~/moses/mosesdecoder/scripts -s ~/subword-nmt/subword_nmt -c 0"
	echo "-l <protection>     <protection> can be 'no' 'tok' 'bpe' "
	echo "-m <model>          <model> can be 0 or 1 or 2 or 3 "
    echo "-k <record_num>     <record_num> is the num of lable to record"
    echo "-e <path>           <path> is the path of moses scripts  "
    echo "-s <path>           <path> is the path of subword      "
	echo "-c <GPU_NUM>    <GPU_NUM> is the path of GPU    "
	exit
	exit
}

LABLE=""
MODEL=""
# ~/moses/mosesdecoder/scripts
MOSESROOT=""
# ~/subword-nmt/subword_nmt
BPEROOT=""
RECORD_NUM=""
BPE_TOKENS=10000
GPU_NUM=0
while getopts 'l:m:k:e:s:c:' opt
do
	case $opt in
		l)
			LABLE=$OPTARG;;
		m)
			MODEL=$OPTARG;;
        k)
            RECORD_NUM=$OPTARG;;
        e)
            MOSESROOT=$OPTARG;;
        s)
            BPEROOT=$OPTARG;;
	c)
	    GPU_NUM=$OPTARG;;
	*)
			parm_err
	esac
done
# echo $LABLE $MODEL

if  [ "$LABLE" != "no" ] && [ "$LABLE" != "tok" ] && [ "$LABLE" != "bpe" ]; then
	parm_err
fi

if  [ "$MODEL" != "0" ] && [ "$MODEL" != "1" ] && [ "$MODEL" != "2" ] && [ "$MODEL" != "3" ]; then  
	parm_err
fi


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
testprefix=test_splitce
# cslxprefix=test_splitce
mkdir -p $orig $tmp $prep
# 最开始假设所需的资料都和脚本同目录,并且名字为$rawprefix.* $testprefix.*
for l in $src $tgt; do
    python3 lable_process.py $MODEL $CREATDATA/$rawprefix.$l  $l > $orig/$rawprefix.$l
done

#for l in $src $tgt; do
    #python3 restore_token.py $LABLE 0 $CREATDATA/${testprefix}.$l > $CREATDATA/${testprefix}.restore.$l
#done

if [ "$MODEL" != "2" ] && [ "$MODEL" != "3" ];
then
    python3 lable_process.py $MODEL $CREATDATA/${testprefix}.$src $src > $orig/${testprefix}.$src
    python3 lable_process.py $MODEL $CREATDATA/${testprefix}.$tgt $tgt > $orig/${testprefix}.$tgt
else
    python3 generalize_file.py $CREATDATA/${testprefix}.$src  $RECORD_NUM $MODEL > $orig/${testprefix}.$src
    mv $CREATDATA/${testprefix}.$tgt $orig/${testprefix}.$tgt
fi

# 进行分词和清理
echo "pre-processing train data..."
for l in $src $tgt; do
    tok=train.tok.$l
    if [ "$l" == "$src" ];
    then 
	  python3 $CN_TOKENIZER $orig/$rawprefix.$l | perl $TOKENIZER -l cn > $tmp/$tok
	  echo "cn tokenizer finished"
    else
      perl $TOKENIZER  -threads 8 -l en < $orig/$rawprefix.$l  >  $tmp/$tok 
	  echo "en tokenizer finished"
    fi
done

# CLEAN 会导致此处不好对应
# perl $CLEAN -ratio 1.5 $tmp/train.tok $src $tgt $tmp/train.clean 1 175

# 跳过CLEAN
mv $tmp/train.tok.$src $tmp/train.clean.$src
mv $tmp/train.tok.$tgt $tmp/train.clean.$tgt

for l in $src $tgt; do
    perl $LC < $tmp/train.clean.$l > $tmp/train.tags.$l
done
echo "finished tokenize , clean , lowercase"

echo "creating train, valid, test..."
perl $TOKENIZER  -threads 8 -l en < $orig/$testprefix.en | perl $LC > $tmp/test.en
python3 $CN_TOKENIZER $orig/$testprefix.cn  | perl $TOKENIZER  -threads 8 -l cn | perl $LC > $tmp/test.cn 

# 在分词时不切分
if [ "$LABLE" != "no" ]; then
    for l in $src $tgt; do
        mv $tmp/test.$l $tmp/test.bak.$l
        mv $tmp/train.tags.$l $tmp/train.tags.bak.$l
    done

    for l in $src $tgt; do
        python3 restore_token.py $LABLE $MODEL $tmp/train.tags.bak.$l > $tmp/train.tags.$l
    done
    
    python3 restore_token.py $LABLE $MODEL $tmp/test.bak.$src > $tmp/test.$src
    if [ "$MODEL" == "0" ] || [ "$MODEL" == "1" ]; then
        python3 restore_token.py $LABLE $MODEL $tmp/test.bak.$tgt > $tmp/test.$tgt
    else
        python3 restore_token.py $LABLE 0 $tmp/test.bak.$tgt > $tmp/test.$tgt
    fi
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
python3 $BPEROOT/learn_bpe.py -s $BPE_TOKENS < $TRAIN > $BPE_CODE

# 将train.$L valid.$L test.$L 子词切分后移动到$prep/下
for L in $src $tgt; do
    for f in train.$L valid.$L test.$L; do
        echo "apply_bpe.py to ${f}..."
        python3 $BPEROOT/apply_bpe.py -c $BPE_CODE < $tmp/$f > $prep/$f
    done
done

if [ "$LABLE" == "bpe" ]; then # 仅BPE时保留
    for l in $src $tgt; do
        for f in train.$l valid.$l test.$l; do
            mv $prep/$f $prep/${f}.bpebak
        done
    done

    for l in $src $tgt; do
        for f in train.$l valid.$l; do
            python3 restore_token.py $LABLE $MODEL $prep/${f}.bpebak > $prep/$f
        done
    done

    python3 restore_token.py $LABLE $MODEL $prep/test.${src}.bpebak > $prep/test.$src
    if [ "$MODEL" != "3" ] && [ "$MODEL" != "2" ]; then
        python3 restore_token.py $LABLE $MODEL $prep/test.${tgt}.bpebak > $prep/test.$tgt
    else
        python3 restore_token.py $LABLE 0 $prep/test.${tgt}.bpebak > $prep/test.$tgt
    fi
fi


DATA_DIR=../orig
python3 remove_test.py $DATA_DIR/test_splitce.$src $DATA_DIR/test_splitce.$tgt $prep/test.$src $prep/test.$tgt gen_record $MODEL
cp new_RC $orig/
cp new_RE $orig/
cp new_C $prep/test.$src
cp new_E $prep/test.$tgt
cp new_R gen_record
TEXT=$prep
DATADIR=../preprocess_data
rm -rf $DATADIR
mkdir -p $DATADIR
   fairseq-preprocess --source-lang $src --target-lang $tgt \
    --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test  \
    --destdir $DATADIR \
    --workers 20
