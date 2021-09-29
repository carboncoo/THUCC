import time
import argparse

from thucc.engine.parse import parse
from thucc.engine.api import (
    solve_wsd,
    solve_translate,
    solve_tselect,
    solve_microwrite,
    solve_wholebookreading_with_microwrite,
    solve_poem_shortanswer_with_microwrite,
    solve_cc_shortanswer_with_microwrite,
    solve_analects_with_microwrite,
    solve_dictation
)

question_types = ['wsd',                # 题型：词义消歧 (6, 7)
                  'cc_tselect',         # 题型：翻译选择 (8)
                  'cc_uselect',         # 题型：文言文理解性选择 (9)
                  'translate',          # 题型：翻译 (10)
                  'cc_shortanswer',     # 题型：文言文简答（11）
                  'analects',           # 题型：论语（12）
                  
                  'poem_uselect',       # 题型：诗歌理解性选择 (13, 14)
                  'poem_shortanswer',   # 题型：诗歌简答 (15)
                  'dictation',          # 题型：默写 (16)
                  'whole_book_reading', # 题型：整本书阅读（17）
                  
                  'microwrite'          # 题型：微写作（23）
                  ]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        type=str,
        help="path to the input xml test file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="path to the output xml answer file",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="save answers in a more readable format",
    )
    return parser.parse_args()

def main(args):
    root, tq_mapping = parse(args.input)
    
    print("========= THUCC Start ========\n")

    # for q in tq_mapping['wsd']:
    #     outputs = solve_wsd(q)

    # for q in tq_mapping['translate']:
    #     outputs = solve_translate(q)
    # for q in tq_mapping['cc_tselect']:
    #     outputs = solve_tselect(q)

    # for q in tq_mapping['microwrite']:
    #     outputs = solve_microwrite(q)
    # for q in tq_mapping['whole_book_reading']:
    #     outputs = solve_wholebookreading_with_microwrite(q)
    # for q in tq_mapping['poem_shortanswer']:
    #     outputs = solve_poem_shortanswer_with_microwrite(q)
    # for q in tq_mapping['cc_shortanswer']:
    #     outputs = solve_cc_shortanswer_with_microwrite(q)
    # for q in tq_mapping['analects']:
    #     outputs = solve_analects_with_microwrite(q)
    for q in tq_mapping['dictation']:
        outputs = solve_dictation(q)
    
    # save answers to the output xml file
    if args.output:
        root.write(args.output, xml_declaration=True, encoding="UTF-8")

    # save answers in more readable format
    if args.output and args.simple:
        all_answers = ""
        for k, questions in tq_mapping.items():
            for q in questions:
                all_answers += f"Question:\t{q.qid} [{k}]\n"
                all_answers += f"Answer:\t{q.answer}\n\n"
        print("========= THUCC Results ========\n")
        print(all_answers)
        with open(args.output.replace('.xml', '.txt'), 'w') as fout:
            fout.write(all_answers)
    
if __name__ == '__main__':
    start = time.time()
    main(parse_args())
    end = time.time()
    print(f'Total time: {end-start}s')