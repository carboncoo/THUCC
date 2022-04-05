set -ex

sudo docker save thucc-ccanswer:v0.0.1 > thucc-ccanswer:v0.0.1.tar
sudo docker save thucc-wsd:v0.0.1 > thucc-wsd:v0.0.1.tar
sudo docker save thucc-translate:v0.0.1 > thucc-translate:v0.0.1.tar
sudo docker save thucc-microwrite:v0.0.1 > thucc-microwrite:v0.0.1.tar
sudo docker save thucc-poemuselect:v0.0.1 > thucc-poemuselect:v0.0.1.tar
sudo docker save thucc-poemanswer:v0.0.1 > thucc-poemanswer:v0.0.1.tar
sudo docker save thucc-dictation:v0.0.1 > thucc-dictation:v0.0.1.tar
sudo docker save thucc-poemretrieval:v0.0.1 > thucc-poemretrieval:v0.0.1.tar

mkdir thucc-systems-docker
mv *.tar thucc-systems-docker
