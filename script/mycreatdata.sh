# 构造数据

function parm_err(){
	echo "Please input -f -l -t -k -e and -a parms\n such as ./mycreatdata.sh -f wmt2018.zh2en-Registry -l 100 -t cslx-dataset-zh2en -k 6 -e ~/moses/mosesdecoder/scripts -a ~/fast_align/fast_align-master/build"
	echo "-f <file>        <file> is the path of wmt2018  "
	echo "-l <line_num>    <line_num> is the num of line to read "
	echo "-t <file>        <file> is the path of cslx "
    echo "-k <record_num>  <record_num> is the num of lable to record"
	echo "-e <path>        <path> is the path of moses scripts  "
	echo "-a <path>        <path> is the path of fast_align  "
	exit
}
CN2EN_SOURCE_FILE=wmt2018.zh2en-Registry 
READ_FILE_NUM=100 
CSLX_FILE=cslx-dataset-zh2en
RECORD_NUM=6
MOSESPATH=""
FASTPATH=""
while getopts 'f:l:t:k:e:a:' opt
do
	case $opt in
		f)
			CN2EN_SOURCE_FILE=$OPTARG;;
		l)
			READ_FILE_NUM=$OPTARG;;
		t)
			CSLX_FILE=$OPTARG;;
        k)
            RECORD_NUM=$OPTARG;;
		e)
			MOSESPATH=$OPTARG;;
		a)
			FASTPATH=$OPTARG;;
		*)
			parm_err
	esac
done
cd ../creat_data
python3 main.py $CN2EN_SOURCE_FILE $READ_FILE_NUM $CSLX_FILE $RECORD_NUM $MOSESPATH $FASTPATH
cd ..
