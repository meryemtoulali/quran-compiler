import ply.lex as lex
import settings
import difflib
from utils import dictionary
from logger import logeventinfo
import settings

tokens=['DIVIDER', 'UNDEF_N', 'DEF_N', 'VERB', 'PRON', 'SUB', 'NEG', 'PREP', 'CONJ', 'EMPH', 'CERT', 'DEM', 'REL', 'REM', 'INTG','PRON_PLURAL']

t_ignore = ' \t'
t_DEF_N = r'النَّجْدَيْنِ | الْبَلَدِ | الْإِنْسانَ | الْعَقَبَةُ | الصَّبْرِ| الْمَرْحَمَةِ | الْمَيْمَنَةِ |الْعَقَبَةَ| الْمَشْأَمَةِ'
t_NEG = r'لَمْ | لَا | لَنْ'
t_PREP = r'لَّ | بِ | فِي | عَلَى | مِنَ | عَلَيْ'
t_CONJ = r'وَ | أَوْ | ثُمَّ'
t_EMPH = r'لَ'
t_CERT = r'قَدْ'
t_DEM = r'هَذَا | أُوْلَئِكَ'
t_REL = r'مَا | الَّذِينَ'
t_REM = r'فَ'
t_INTG = r'أَ | مَا'

def t_VERB(t):
    r'يَقُولُ | أَهْلَكْ | يَحْسَبُ | يَرَ | نَجْعَل | هَدَيْ | أُقْسِمُ | وَلَدَ | خَلَقْ | يَقْدِرَ | اقْتَحَمَ | أَدْرَا |  كَانَ | آمَنُ | تَوَاصَ | كَفَرُ'
    return t

def t_UNDEF_N(t):
    r'مَالًا | لُبَداً | أَحَدٌ | عَيْنَيْنِ | لِسَانًا | شَفَتَيْنِ | حِلٌّ | وَالِدٍ | كَبَدٍ | فَكُّ | رَقَبَةٍ | إِطْعَامٌ | يَوْمٍ | ذِي | مَسْغَبَةٍ | يَتِيمًا | ذَا | مَقْرَبَةٍ |  مِسْكِينًا | مَتْرَبَةٍ | أَصْحَابُ | آيَاتِ | مُّؤْصَدَةٌ | نَارٌ'
    return t
    
def t_PRON_PLURAL(t):
    r'هُمْ'
    return t

def t_PRON(t):
    r'تُ | هُ | نَا | أَنْتَ | وا | وْا | هِمْ | كَ | هِ'
    return t
    
def t_SUB(t):
     r'أَنْ'
     return t
    
def t_DIVIDER(t):
    r'\d+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    # using a global variable for lineno because
    # lex.input() does not automatically reset the line number
    settings.lineno += len(t.value)

def t_error(t):
    bad_tok = t.value.split()[0]
    settings.lex_state["is_error"] = True
    possible_correct_word = difflib.get_close_matches(bad_tok, dictionary, 1, 0.5)
    logeventinfo("Illegal token '%s' at line %s col %s !\n" % (bad_tok, settings.lineno, t.lexpos))
    settings.lex_state["output"] += "Illegal token '%s' at line %s col %s !\n" % (bad_tok, settings.lineno, t.lexpos)
    if(possible_correct_word):
        logeventinfo("Did you mean: " + possible_correct_word[0] + "?\n")
        settings.lex_state["output"] += "Did you mean: " + possible_correct_word[0] + "?\n"

    t.lexer.skip(len(bad_tok))

lex.lex()
