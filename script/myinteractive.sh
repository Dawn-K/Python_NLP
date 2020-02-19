function parm_err(){
	echo "Please input -l -m -moses -subword parms\n such as ./myinteractive.sh -l no -m 0 -r 6"
	echo "-l <protection>     <protection> can be 'no' 'tok' 'bpe' "
	echo "-m <model>          <model> can be 0 or 1 or 2  "
    echo "-r <record_num>     <record_num> is the num of recorded lables  "
	exit
}

MODEL_DIR=../checkpoints/fconv_wmt_cn_en
src=cn
tgt=en
orig=../orig
DATA=../creat_data/data
REFIN=$DATA/test_splitce.cn
REFOUT=$DATA/test_splitce.en
RECORD_NUM=""
cslxprefix=test_splitce
GEN_INPUT=$orig/$cslxprefix.$src
GEN_OUTPUT=$orig/$cslxprefix.$tgt
ANTI_GEN_INPUT=anti_gen_input
ANTI_GEN_OUTPUT=anti_gen_output
PROTECT_MODEL=""
GENERALIATE_MODEL=""

while getopts 'l:m:r:' opt
do
	case $opt in
		l)
			PROTECT_MODEL=$OPTARG;;
		m)
			GENERALIATE_MODEL=$OPTARG;;
        r)
            RECORD_NUM=$OPTARG;;
		*)
			parm_err
	esac
done

# 翻译
DATADIR=../preprocess_data
fairseq-generate  $DATADIR \
    --path $MODEL_DIR/checkpoint_best.pt \
    --beam 5 --remove-bpe  | tee out.tmp

grep ^H out.tmp | cut -f3- | sed 's/@@ //g' > gen.out.sys
# grep ^T out.tmp | cut -f2- | sed 's/@@ //g' > gen.out.ref

# 恢复标签
python3 anti-generalize.py $GEN_INPUT  gen_record $GENERALIATE_MODEL > $ANTI_GEN_INPUT
python3 anti-generalize.py gen.out.sys gen_record $GENERALIATE_MODEL > $ANTI_GEN_OUTPUT

# 评估模型
cd ../evaluate_model
python3 evaluate.py $REFIN ../script/$ANTI_GEN_OUTPUT $REFOUT
cd ../script  
