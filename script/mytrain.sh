DATADIR=preprocess_data
# Train the model
mkdir -p checkpoints/fconv_wmt_cn_en
fairseq-train $DATADIR \
    --cpu \
    --lr 0.25 --clip-norm 0.1 --dropout 0.2 --max-tokens 4000 \
    --arch fconv --save-dir checkpoints/fconv_wmt_cn_en