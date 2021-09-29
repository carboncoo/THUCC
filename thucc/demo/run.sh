#!/bin/bash 
project_path=$(cd `dirname $0`; pwd)
export PYTHONPATH=$PYTHONPATH:$project_path/../../

cd $project_path
streamlit run app.py