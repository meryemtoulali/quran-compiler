from mylex import lex
from myyacc import parser
import settings
from logger import logevent, logeventinfo

def lexical(lines):
    logevent('Starting Lexical analysis...\n')
    settings.lex_state["output"] += "| LINE | COL |  TYPE  | TOKEN\n-------------------------------\n"
    logeventinfo("\n| LINE | COL |  TYPE  | TOKEN\n-------------------------------\n")

    lex.lineno = 0
    lex.input(lines)
    while 1:
        tok = lex.token()        if not tok: break
        logeventinfo("|{2: <6}|{3: <5}|{1: <8}|{0: <9}\n".format(tok.value, tok.type, settings.lineno, tok.lexpos))
        settings.lex_state["output"] += "|{2: <6}|{3: <5}|{1: <8}|{0: <9}\n".format(tok.value, tok.type, settings.lineno, tok.lexpos)
        if (tok.type == 'DIVIDER'): 
            logeventinfo("-------------------------------\n")
            settings.lex_state["output"] += "-------------------------------"


def syntax_lines(lines):
    logevent('Starting syntactic and semantic analysis...\n')
    res = parser.parse(lines, tracking=True)
    print("parser result :\n", res)
    if(res != None):
        settings.syn_state["output"] += "parser result:\n" + res + "\n"
        logeventinfo("parser result:\n" + res + "\n")
