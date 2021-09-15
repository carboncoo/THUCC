from thucc.engine.parse import parse
from thucc.engine.api import (
    solve_translate,
    solve_tselect
)

def main():
    tq_mapping = parse("/data/private/cc/experiment/guwen_831/I.xml")
    import ipdb; ipdb.set_trace()
    for q in tq_mapping['translate']:
        outputs = solve_translate(q)
    for q in tq_mapping['cc_tselect']:
        outputs = solve_tselect(q)

if __name__ == '__main__':
    main()