set -ex

cd thucc-systems-docker

# docker load -i thucc-ccanswer:v0.0.1.tar
# docker load -i thucc-wsd:v0.0.1.tar
# docker load -i thucc-translate:v0.0.1.tar
# docker load -i thucc-microwrite:v0.0.1.tar
# docker load -i thucc-poemuselect:v0.0.1.tar
# docker load -i thucc-poemanswer:v0.0.1.tar
# docker load -i thucc-dictation:v0.0.2.tar
# docker load -i thucc-poemretrieval:v0.0.1.tar

may_restart_docker(){
    docker_name=$1
    image_name=$2
    port=$3

    if [[ -n $(sudo docker ps -q -f "name=${docker_name}") ]];then
        echo "docker $docker_name running, continue"
        return
    else
        if [[ -n $(sudo docker ps -a -q -f "name=${docker_name}") ]];then
            sudo docker rm $docker_name
            echo "stopped docker $docker_name exists, remove it"
        fi
        sudo docker run -d -p $port:80 --name $docker_name $image_name
    fi
}

may_restart_docker thucc-ccanswer thucc-ccanswer:v0.0.1 36800
# may_restart_docker thucc-dictation thucc-dictation:v0.0.2 36794
# may_restart_docker thucc-microwrite thucc-microwrite:v0.0.1 36790
# may_restart_docker thucc-poemanswer thucc-poemanswer:v0.0.1 36795
may_restart_docker thucc-dictation thucc-dictation:v0.0.1 36793
# may_restart_docker thucc-poemuselect thucc-poemuselect:v0.0.1 36796
# may_restart_docker thucc-translate thucc-translate:v0.0.1 36789
# may_restart_docker thucc-wsd thucc-wsd:v0.0.1 36792


# sudo docker run -d -p 36794:80 --name thucc-ccanswer thucc-ccanswer:v0.0.1
# sudo docker run -d -p 36794:80 --name thucc-dictation thucc-dictation:v0.0.2
# sudo docker run -d -p 36790:80 --name thucc-microwrite thucc-microwrite:v0.0.1
# sudo docker run -d -p 36795:80 --name thucc-poemanswer thucc-poemanswer:v0.0.1
# sudo docker run -d -p 36793:80 --name thucc-poemretrieval thucc-poemretrieval:v0.0.1
# sudo docker run -d -p 36796:80 --name thucc-poemuselect thucc-poemuselect:v0.0.1
# sudo docker run -d -p 36789:80 --name thucc-translate thucc-translate:v0.0.1
# sudo docker run -d -p 36792:80 --name thucc-wsd thucc-wsd:v0.0.1