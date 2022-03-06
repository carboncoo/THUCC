from .translate import solve_translate, solve_tselect
from .microwrite import (
    solve_microwrite, 
    solve_wholebookreading_with_microwrite,
    solve_poem_shortanswer_with_microwrite,
    solve_cc_shortanswer_with_microwrite,
    solve_analects_with_microwrite
)
from .wsd import (
    solve_wsd
)
from .poem_retrieval import (
    solve_dictation,
    solve_dictation_v1
)
from .poem_appreciation import solve_poem_shortanswer_with_appreciation
from .poem_answer import solve_poem_shortanswer
from .poem_uselect import solve_poem_uselect

from .translate import translate as api_translate
from .microwrite import microwrite as api_microwrite
from .wsd import wsd_translate_align as api_wsd_translate_align
from .wsd import get_sense as api_get_sense
from .poem_retrieval import api_dictation

from thucc.engine.utils import log_solve

def empty_solve(default_answer=''):
    @log_solve('empty')
    def solve_func(*args, **kwargs):
        outputs = {
            'ans': default_answer
        }
        return outputs
    return solve_func