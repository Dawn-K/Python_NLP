DATADIR=../preprocess_data
# Train the model
rm -rf ../checkpoints/fconv_wmt_cn_en 
SAVEDIR=../checkpoints/fconv_wmt_cn_en
mkdir -p $SAVEDIR
GPU_NUM=0

function parm_err(){
	echo "Please input -c parm\n such as ./mytrain.sh -c 0"
        echo "-c <GPU_NUM>         "
	exit
}

while getopts 'c:' opt
do
	case $opt in
		c)
			GPU_NUM=$OPTARG;;
		*)
			parm_err
	esac
done
CUDA_VISIBLE_DEVICES=$GPU_NUM    fairseq-train \
              $DATADIR \
              --arch transformer --save-dir $SAVEDIR \
              --num-workers 20 --max-epoch 10 \
              --share-decoder-input-output-embed \
              --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
              --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
              --dropout 0.3 --weight-decay 0.0001 \
              --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
              --max-tokens 4096 
