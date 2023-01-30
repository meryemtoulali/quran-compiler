def init():
    global lex_state
    global syn_state
    global sem_state
    global lineno
    
    lex_state = {
        'output' : '',
        'is_error' : False
    }
    syn_state = {
        'output' : '',
        'is_error' : False
    }
    sem_state = {
        'output' : '',
        'is_error' : False
    }
    # using a global variable for lineno because
    # lex.input() does not automatically reset the line number
    lineno = 1