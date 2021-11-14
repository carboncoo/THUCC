import time
import argparse

from thucc.engine.parse import parse
from thucc.engine.api import (
    empty_solve,
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

question_api_mapping = {'wsd': solve_wsd,                                             # 题型：词义消歧 (6, 7)
                        'cc_tselect': solve_tselect,                                  # 题型：翻译选择 (8)
                        'cc_uselect': empty_solve,                                    # 题型：文言文理解性选择 (9)
                        'translate': solve_translate,                                 # 题型：翻译 (10)
                        'cc_shortanswer': solve_cc_shortanswer_with_microwrite,       # 题型：文言文简答（11）
                        'analects': solve_analects_with_microwrite,                   # 题型：论语（12）
                        
                        'poem_uselect': empty_solve,                                  # 题型：诗歌理解性选择 (13, 14)
                        'poem_shortanswer': solve_poem_shortanswer_with_microwrite,   # 题型：诗歌简答 (15)
                        'dictation': solve_dictation,                                 # 题型：默写 (16)
                        'whole_book_reading': solve_wholebookreading_with_microwrite, # 题型：整本书阅读（17）
                        
                        'microwrite': solve_microwrite                                # 题型：微写作（23）
                        }

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
        "-q",
        "--qtypes",
        nargs='*',
        choices=question_api_mapping.keys(),
        help="only answer these types of questions",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="save answers in a more readable format",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debugging mode: no files will be saved",
    )
    parser.add_argument(
        "--no_exp",
        action="store_true",
        help="don't output explainations",
    )
    parser.add_argument(
        "--stage",
        type=str,
        choices=['first, second'],
        help="development stage",
    )
    return parser.parse_args()

def main(args):
    root, tq_mapping = parse(args.input)
    
    print("========= THUCC Start ========\n")

    qtypes = args.qtypes or question_api_mapping.keys()

    for qtype in qtypes:
        for q in tq_mapping[qtype]:
            output = question_api_mapping[qtype](q)
    
    if args.debug:
        import ipdb; ipdb.set_trace()
        exit(0)
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
                if q.explain:
                    all_answers += f"Explain:\t{q.explain}\n\n"
        print("========= THUCC Results ========\n")
        print(all_answers)
        with open(args.output.replace('.xml', '.txt'), 'w') as fout:
            fout.write(all_answers)
    
if __name__ == '__main__':
    start = time.time()
    main(parse_args())
    end = time.time()
    print(f'Total time: {end-start}s')