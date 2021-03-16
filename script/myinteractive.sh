function parm_err(){
	echo "Please input -l -m -moses -subword -c parms\n such as ./myinteractive.sh -l no -m 0 -r 6 -c GPU_NUM -i MODEL_ID "
	echo "-l <protection>     <protection> can be 'no' 'tok' 'bpe' "
	echo "-m <model>          <model> can be 0 or 1 or 2  "
    echo "-r <record_num>     <record_num> is the num of recorded lables  "
	echo "-c <GPU_NUM>         "
    echo "-i <CHECK_ID>       <MODEL_ID> is the index of checkpoints "
	exit
}

MODEL_DIR=../checkpoints/fconv_wmt_cn_en
src=cn
tgt=en
orig=../orig
REFIN=new_RC
REFOUT=new_RE
RECORD_NUM=""
ANTI_GEN_INPUT=anti_gen_input
ANTI_GEN_OUTPUT=anti_gen_output
PROTECT_MODEL=""
GENERALIATE_MODEL=""
GPU_NUM=0
CHECK_ID=_best
while getopts 'l:m:r:c:i:' opt
do
	case $opt in
		l)
			PROTECT_MODEL=$OPTARG;;
		m)
			GENERALIATE_MODEL=$OPTARG;;
	    r)
        	RECORD_NUM=$OPTARG;;
		c)
			GPU_NUM=$OPTARG;;
        i)
            CHECK_ID=$OPTARG;;
		*)
			parm_err
	esac
done

# 翻译
DATADIR=../preprocess_data
CUDA_VISIBLE_DEVICES=$GPU_NUM    fairseq-generate  $DATADIR \
    --path $MODEL_DIR/checkpoint${CHECK_ID}.pt \
    --batch-size 128  --beam 5 --remove-bpe  > out.tmp
     
# --beam 5 --remove-bpe
python3 sort_out.py

# 恢复标签
# 此处产生疑问,此处应该用未泛化的,但是删减过的原文,new_RC再翻译可能会带来问题,也可能不会
python3 anti-generalize.py new_RC  new_R $GENERALIATE_MODEL > $ANTI_GEN_INPUT
python3 anti-generalize.py gen.out.sys new_R $GENERALIATE_MODEL > $ANTI_GEN_OUTPUT

# 评估模型
cd ../evaluate_model
echo "evaluate the model..."
echo "$PROTECT_MODEL $GENERALIATE_MODEL $CHECK_ID " >>  ../script/result
python3 evaluate.py ../script/$ANTI_GEN_INPUT ../script/$ANTI_GEN_OUTPUT ../script/new_RE  >>  ../script/result
cd ../script  
