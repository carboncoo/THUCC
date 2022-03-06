script_dir=$(cd $(dirname $0);pwd)
base_dir=$(dirname $(dirname $script_dir))

cd $base_dir

systems=""

for sub_system in wsd translate cc_answer poem_uselect poem_retrieval dictation poem_appreciation poem_answer ;
do
    systems="$systems thucc/systems/$sub_system/src"
done

tar zcvf thucc-systems.tar.gz $systems