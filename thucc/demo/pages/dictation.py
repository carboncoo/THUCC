import random
from thucc.engine.api.poem_retrieval import dictation
import streamlit as st
from thucc.engine.api import api_dictation

sample_inputs = [
    "《子路、曾皙、冉有、公西华侍坐》中冉有认为自己能治理小国，使百姓富足，但他又用“________，________”表明自己还不能以礼乐教化百姓。",
    "《短歌行》中曹操借“明月”比喻贤才求而不得的诗句是“________，________”。",
    "陶渊明身在宦海，心系田园，因此他在《归园田居》中运用比喻、对偶手法，写出了“________，________”的诗句。",
    "《论语·子路、曾皙、冉有、公西华侍坐》中，写孔子哂笑子路的原因的句子是：“________，________。”",
    "白居易《琵琶行》第二段末，通过描写听众的反应和景物来侧面突出琵琶女演奏技艺高超的句子是：“________，________。”",
    "苏轼《念奴娇·赤壁怀古》中“________，________”两句，收束了对赤壁雄奇景物的描写，引起后面对历史的缅怀。",
    "荀子《劝学》中，“________，________” 通过“木”与“金”的变化来进一步说明客观事物经过人工改造，可以改变原来的状况。",
    "李白在《蜀道难》一诗中引用神话传说为其增添了浪漫气息，如引用“五丁开山”这一神话的句子是“________，________。”",
    "黑格尔的“人类从历史中学到的唯一的教训，就是没有从历史中吸取到任何教训” 佐证了杜牧在《阿房宫赋》中的“________，________”观点。",
    "《山居秋暝》中由写景转为写人，采用了“未见其人，先闻其声”的写法的诗句是“________，________”。",
    "辛弃疾在《永遇乐 · 京口北固亭怀古》的上阕中用“________，________” 展现了刘裕的北伐赫赫武功；可虎父偏有犬子，刘义隆在面对北方敌人时却落得“赢得仓皇北顾”的下场。",
    "当我们来到乡村，见到“鸡犬相闻”的景象，会联想到陶渊明在《归园田居》中“________，________”来表达对田园生活的赞美。",
    "当我们想表达做事情需要多多寻求外在的帮助这一观点时，可引用《荀子·劝学》中的“________，________”两句来增强说服力。",
    "当人们满怀愁情地伫立江边时，常常会借用李煜《虞美人》中“________ ， ________”这两句来表达。"
]

def app():
    st.title("古诗文默写系统")

    # instructions = '请使用 "_________" 标注空位'
    instructions = ''

    if "dictation_inputs" not in st.session_state:
        st.session_state.dictation_inputs = "当人们满怀愁情地伫立江边时，常常会借用李煜《虞美人》中“________ ， ________”这两句来表达。"
    if st.session_state.get("sample", False):
        st.session_state.dictation_inputs = sample = random.sample(sample_inputs, 1)[0]

    inputs = st.text_area(instructions, value=st.session_state.dictation_inputs, key="initial_text_area")
    display = ""

    col1, col2, _ = st.columns([1.4, 2.0, 10])
    with col1:
        submit_button = st.button('提交', key='submit')
    with col2:
        try_button = st.button('随机输入', key='sample')
    
    with st.expander("输入说明", expanded=True):
         st.write("""
                &emsp;&emsp;为保证最佳质量，请使用 "\_\_\_\_\_\_\_\_" 标注要填写的位置。
         """)

    st.write("### 系统输入")
    st.write(inputs)

    display = api_dictation(inputs)
    if not display:
        display = '未检索到相关诗词'
    else:
        display = f'“{display}”'


    st.write("### 作答结果")
    
    st.write(display)