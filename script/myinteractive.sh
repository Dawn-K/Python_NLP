MODEL_DIR=../checkpoints/fconv_wmt_cn_en
BPECODE=../preprocess/code
# todo
TESTIN=
TESTOUT=
REFOUT=
fairseq-interactive \
    --path $MODEL_DIR/checkpoint_best.pt $MODEL_DIR \
    --beam 5 --source-lang cn --target-lang en \
    --tokenizer moses \
    --bpe subword_nmt --bpe-codes $BPECODE  --input $TESTIN --results-path  $TESTOUT

cd ../evaluate_model
python evaluate.py $TESTIN $TESTOUT $REFOUT
cd ../script  