rm -rf test
mkdir test
for l in no tok bpe; do
	for m in 0 1 2; do
		./main.sh -l $l -m $m >/dev/null 2>&1
		cp preprocess/train.cn test/cn.$l.$m
		cp preprocess/train.en test/en.$l.$m
	done
done
