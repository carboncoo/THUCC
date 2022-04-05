import sys
from PoemAppreciationAPI import PoemAppreciationAPI
from train import defaultdictFunc

def run(poem):
    p = PoemAppreciationAPI()
    res = p.appreciate(poem, 3, False, False)
    print(res)

if __name__ == '__main__':
    run(sys.argv[1])