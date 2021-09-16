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
                  'analects',           # 题型：论语（12, 13）
                  
                  'poem_uselect',       # 题型：诗歌理解性选择 (13, 14)
                  'poem_shortanswer',   # 题型：诗歌简答 (15)
                  'dictation',          # 题型：默写 (16)
                  'whole_book_reading', # 题型：整本书阅读（17）
                  
                  'microwrite'          # 题型：微写作（23）
                  ]

def main():
    tq_mapping = parse("/data1/private/cc/THUCC/I.xml")
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
    for q in tq_mapping['cc_shortanswer']:
        outputs = solve_cc_shortanswer_with_microwrite(q)
        print(outputs)
    for q in tq_mapping['analects']:
        outputs = solve_analects_with_microwrite(q)
        print(outputs)
    
    # for q in tq_mapping['dictation']:
    #     outputs = solve_dictation(q)
    #     print(outputs)
    

if __name__ == '__main__':
    main()