DATADIR=../preprocess_data
# Train the model
SAVEDIR=../checkpoints/fconv_wmt_cn_en
mkdir -p $SAVEDIR
CUDA_VISIBLE_DEVICES=0  fairseq-train \
              $DATADIR \
              --lr 0.25 --clip-norm 0.1 --dropout 0.2 \
              --max-tokens 4000 --arch fconv --save-dir $SAVEDIR \
              --num-workers 20 --max-epoch 5
