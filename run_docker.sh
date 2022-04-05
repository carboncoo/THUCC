set -ex

cd thucc-systems-docker

docker load -i thucc-ccanswer:v0.0.1.tar
docker load -i thucc-wsd:v0.0.1.tar
docker load -i thucc-translate:v0.0.1.tar
docker load -i thucc-microwrite:v0.0.1.tar
docker load -i thucc-poemuselect:v0.0.1.tar
docker load -i thucc-poemanswer:v0.0.1.tar
docker load -i thucc-dictation:v0.0.1.tar
docker load -i thucc-poemretrieval:v0.0.1.tar

docker run -d -p 36800:80 --name thucc-ccanswer thucc-ccanswer:v0.0.1
docker run -d -p 36794:80 --name thucc-dictation thucc-dictation:v0.0.1
docker run -d -p 36790:80 --name thucc-microwrite thucc-microwrite:v0.0.1
docker run -d -p 36795:80 --name thucc-poemanswer thucc-poemanswer:v0.0.1
docker run -d -p 36793:80 --name thucc-poemretrieval thucc-poemretrieval:v0.0.1
docker run -d -p 36796:80 --name thucc-poemuselect thucc-poemuselect:v0.0.1
docker run -d -p 36789:80 --name thucc-translate thucc-translate:v0.0.1
docker run -d -p 36792:80 --name thucc-wsd thucc-wsd:v0.0.1