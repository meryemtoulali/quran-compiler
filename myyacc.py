import ply.yacc as yacc
from mylex import tokens
from pyarabic import *
import re
from utils import correct_verses_list, translated_verses_list
import settings
from logger import logevent, logeventinfo

def semantic_check(p, verse_n):
    logeventinfo('Semantic check for:' + verse_n + '\n')
    settings.sem_state["output"] += '\nSemantic check for: ' + verse_n + '\n'
    number = re.findall(r'\d+', verse_n)
    number = int(number[0])
    verse = split_lines =re.split('(\d+)', verse_n)
    # will return verse is  ['وَ وَالِدٍ وَ مَا وَلَدَ ', '3', '']
    all_correct_verses = [item[0] for item in correct_verses_list]
    possible_correct_verse = correct_verses_list[number-1][0]
    # turn verse into list
    verse = verse[0].split()
    possible_correct_verse = possible_correct_verse.split()
    all_correct_verses = [item.split() for item in all_correct_verses]

    if (''.join(verse) == ''.join(possible_correct_verse)): 
        logeventinfo('=> Semantically correct, verse ' + str(number) + ':\n')
        settings.sem_state["output"] += '=> Semantically correct, verse '+ str(number) + ':\n'

        logeventinfo(' '.join(possible_correct_verse) + '\n')
        settings.sem_state["output"] += ' '.join(possible_correct_verse) + '\n'
        
        logeventinfo('Translation : ')
        settings.sem_state["output"] += 'Translation : '

        logeventinfo(translated_verses_list[number-1] + '\n')
        settings.sem_state["output"] += translated_verses_list[number-1] + '\n'
        return
    
    # if not, check if it's just the wrong number. 
    # compare against every correct verse :
    for i in range(len(all_correct_verses)):
        if(''.join(verse) == ''.join(all_correct_verses[i])):
            settings.sem_state["is_error"] = True            
            logeventinfo('=> Semantically correct, but with the wrong number. Did you mean verse number ' + str(i+1) + ' ?\n')
            settings.sem_state["output"] += '=> Semantically correct, but with the wrong number. Did you mean verse number ' + str(i+1) + ' ?\n'
            return
    
    # if not, semantic error. find the culprit :
    for i in range (len(verse)):
        if(verse[i] != possible_correct_verse[i]):
            settings.sem_state["is_error"] = True
            logeventinfo('=> Semantic error at verse ' + str(number) + ': ' + verse[i] + '. Did you mean: ' + possible_correct_verse[i] + ' ?\n')
            settings.sem_state["output"] += '=> Semantic error at verse '+ str(number) + ': '+ verse[i]+ '. Did you mean: '+ possible_correct_verse[i]+ ' ?\n'

            return

def p_surah(p):
    '''surah : verse_n
    | surah verse_n'''
    p[0] = ' '.join(p[1:])
    #print("surah -> ", p[0])
    logeventinfo("\n-------------------------------------\n")
    settings.syn_state["output"] += "\n-------------------------------------\n"

def p_verse_n(p):
    '''verse_n : verse DIVIDER'''
    p[0] = ' '.join(p[1:])
    #print('Verse_n -> ', p[0])
    #settings.syn_state["output"] += 'Verse_n -> '+ p[0] + "\n"

    semantic_check(p, p[0])

def p_verse(p):
    '''verse : vs
    | ns 
    | CONJ ns pp object 
    | CONJ UNDEF_N CONJ vs 
    | VERB object 
    | CONJ UNDEF_N CONJ UNDEF_N 
    | CONJ ns '''
    p[0] = ' '.join(p[1:])
    logeventinfo('Verse -> ' + p[0] + '\n')
    settings.syn_state["output"] += 'Verse -> '+ p[0] + "\n"


def p_ns(p):
    '''ns : PRON UNDEF_N
    | UNDEF_N UNDEF_N
    | CONJ UNDEF_N  pp UNDEF_N UNDEF_N
    | UNDEF_N UNDEF_N UNDEF_N
    | CONJ UNDEF_N UNDEF_N UNDEF_N
    | VERB pp VERB subject CONJ vs CONJ vs
    | DEM UNDEF_N DEF_N
    | REL vs ns
    | PRON_PLURAL UNDEF_N DEF_N
    | pp UNDEF_N adj'''
    p[0] = ' '.join(p[1:])
    logeventinfo('Nominal sentence -> '+ ' '.join(p[1:]) + "\n")
    settings.syn_state["output"] += 'Nominal sentence -> '+ ' '.join(p[1:]) + "\n"

def p_vs(p):
    '''vs : NEG VERB pp object 
    | REL VERB
    | EMPH CERT VERB subject object pp
    | INTG VERB object
    | NEG VERB pp subject
    | VERB subject object adj
    | NEG VERB object subject
    | INTG NEG VERB pp object
    | CONJ VERB subject object object
    | REM NEG VERB object
    | CONJ REL VERB PRON REL DEF_N
    | VERB subject pp'''
    p[0] = ' '.join(p[1:])
    logeventinfo('Verbal sentence -> '+ ' '.join(p[1:]) + "\n")
    settings.syn_state["output"] += 'Verbal sentence -> '+ ' '.join(p[1:]) + "\n"

def p_pp(p):
    '''pp : PREP DEM 
    | PREP UNDEF_N
    | PREP PRON
    | PREP DEF_N
    | PREP REL
    | PREP UNDEF_N PRON'''
    p[0] = ' '.join(p[1:])
    logeventinfo('Preposition phrase -> '+ ' '.join(p[1:]) + "\n")
    settings.syn_state["output"] += 'Preposition phrase -> '+ ' '.join(p[1:]) + "\n"

def p_sc(p):
    '''sc : SUB vs'''
    p[0] = ' '.join(p[1:])
    logeventinfo('Subordinate clause -> '+ ' '.join(p[1:]) + "\n")
    settings.syn_state["output"] += 'Subordinate clause -> '+ ' '.join(p[1:]) + "\n"


def p_object(p):
    '''object : DEF_N
    | UNDEF_N
    | sc
    | vs
    | PRON'''
    p[0] = ' '.join(p[1:])
    logeventinfo('Object -> '+ ' '.join(p[1:]) + "\n")
    settings.syn_state["output"] += 'Object -> '+ ' '.join(p[1:]) + "\n"


def p_subject (p):
    '''subject : PRON
    | UNDEF_N'''
    p[0] = ' '.join(p[1:])
    logeventinfo('Subject -> '+ ' '.join(p[1:]) + "\n")
    settings.syn_state["output"] += 'Subject -> '+ ' '.join(p[1:]) + "\n"


def p_adj(p):
    '''adj : UNDEF_N'''
    p[0] = ' '.join(p[1:])
    logeventinfo('Adjective -> '+ ' '.join(p[1:]) + "\n")
    settings.syn_state["output"] += 'Adjective -> '+ ' '.join(p[1:]) + "\n"



def p_error(p):
    settings.syn_state["is_error"] = True
    settings.sem_state["is_error"] = True
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"
    logeventinfo(f"\nSyntax error: Unexpected {token}" + "\n")
    settings.syn_state["output"] += f"\nSyntax error: Unexpected {token}" + "\n"



parser = yacc.yacc(debug=True)
