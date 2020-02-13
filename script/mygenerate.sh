DATADIR=../preprocess_data
fairseq-generate $DATADIR \
    --cpu \
    --path checkpoints/fconv_wmt_cn_en/checkpoint_best.pt \
    --beam 5 --remove-bpe