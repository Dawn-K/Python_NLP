# 以下5个需要自己填写

# wmt文件的绝对路径
WMTPATH=~/wmt2018.zh2en-Registry 
# CSLX文件的绝对路径
CSLXPATH=~/cslx-dataset-zh2en
# 读取wmt的前几行,为空则为全读,1w行大概需要两分钟
READLINE=100000
# 记录标签中的前几个
RECORDNUM=3
# mosesdecoder:/script的绝对路径 例如 ~/moses/mosesdecoder/scripts
MOSESPATH=~/moses/mosesdecoder/scripts
# subword-nmt/subword_nmt的绝对路径 例如 ~/subword-nmt/subword_nmt
SUBWORDPATH=~/subword-nmt/subword_nmt
# fast_align/fast_align-master/build的绝对路径,例如~/fast_align/fast_align-master/build
FASTPATH=~/fast_align/fast_align-master/build

function main_err(){
	echo "Please input -l  -m -c parms\n such as ./main.sh -l no -m 0 -c 0"
	echo "-l <protection>     <protection> can be 'no' 'tok' 'bpe' "
	echo "-m <model>          <model> can be 0 or 1 or 2 or 3 "
	exit
}
# 标签保护模式
PROTECT_MODEL=""
# 标签泛化模式
GENERALIATE_MODEL=""

GPU_NUM=0
while getopts 'l:m:c:' opt
do
	case $opt in
		l)
			PROTECT_MODEL=$OPTARG;;
		m)
			GENERALIATE_MODEL=$OPTARG;;
		c)
			GPU_NUM=$OPTARG;;
		*)
			parm_err
	esac
done

if [ ! -d "$MOSESPATH" ]; then
    echo "Please set MOSESPATH variable correctly to point to Moses scripts."
    exit
fi

if [ ! -d "$SUBWORDPATH" ]; then
    echo "Please set SUBWORDPATH variable correctly to point to subword."
    exit
fi

if [ ! -f "$WMTPATH" ]; then
    echo "Please set WMTPATH variable correctly to point to wmt file."
fi

if [ "$RECORDNUM" = "" ]; then
    echo "Please set RECORDNUM variable"
fi

if [ "$READLINE" = "" ]; then
    echo READLINE=7471638
fi

chmod +x *.sh
chmod +x evaluate_model/tools/*.perl
./clean.sh
# 开始流程
cd script
chmod +x *.sh
./mycreatdata.sh -f $WMTPATH -l $READLINE -t $CSLXPATH -k $RECORDNUM -e $MOSESPATH -a $FASTPATH
./myprepare.sh -l $PROTECT_MODEL -m $GENERALIATE_MODEL -k $RECORDNUM -e $MOSESPATH -s $SUBWORDPATH -c $GPU_NUM

# 模型最后存放为checkpoints/fconv_wmt_cn_en/checkpoint_best.pt
./mytrain.sh -c $GPU_NUM
./myinteractive.sh -l $PROTECT_MODEL -m $GENERALIATE_MODEL -r $RECORDNUM -c $GPU_NUM


# 以下部分是复制数据和模型到别处,自行修改
cd ~/LESS_LABLE
LESS_LABLE=res_${PROTECT_MODEL}_${GENERALIATE_MODEL}
mkdir -p  $LESS_LABLE/script
PRE=preprocess
SC=script
cp checkpoints/fconv_wmt_cn_en/checkpoint_best.pt $LESS_LABLE/LESS_lable_best.pt
cp $PRE/*n   $LESS_LABLE/
cp $SC/*     $LESS_LABLE/script
rm $LESS_LABLE/script/*.py
rm $LESS_LABLE/script/*.sh
