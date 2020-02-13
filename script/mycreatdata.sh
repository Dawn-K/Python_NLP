
function parm_err(){
	echo "Please input -f -l and -k parms\n such as ./mycreatdata.sh -f wmt2018.zh2en-Registry -l 100 -k 6 "
	echo "-f <file>        <file> is the path of wmt2018  "
	echo "-l <line_num>    <line_num> is the num of line to read "
    echo "-k <record_num>  <record_num> is the num of lable to record"
	exit
}
CN2EN_SOURCE_FILE=wmt2018.zh2en-Registry 
READ_FILE_NUM=100 
RECORD_NUM=6
while getopts 'f:l:k:' opt
do
	case $opt in
		f)
			CN2EN_SOURCE_FILE=$OPTARG;;
		l)
			READ_FILE_NUM=$OPTARG;;
        k)
            RECORD_NUM=$OPTARG;;
		*)
			parm_err
	esac
done
cd ../creat_data
python main.py $CN2EN_SOURCE_FILE $READ_FILE_NUM $RECORD_NUM
cd ..
