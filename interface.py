import settings
from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from utils import formatter
from engine import lexical, syntax_lines



def start():

    def inputText():
        # reset analysis results
        settings.lex_state["output"] = ""
        settings.lex_state["is_error"] = False

        settings.syn_state["output"] = ""
        settings.syn_state["is_error"] = False

        settings.sem_state["output"] = ""
        settings.sem_state["is_error"] = False
        # manually reset lex line number
        settings.lineno = 0

        inp = input_area.get(1.0, "end-1c")
        with open('input.txt', 'w', encoding='utf-8') as f:
            f.write(inp)
        f = open('input.txt', encoding='utf-8')
        lines=f.read()

        lexical(lines)
        syntax_lines(lines)


        if (settings.lex_state["is_error"] == True) :
            lex_error.config(image = img_error)
        else :
            lex_error.config(image = img_success)


        if (settings.syn_state["is_error"] == True):
            syn_error.config(image = img_error)
        else:
            syn_error.config(image = img_success)


        if (settings.sem_state["is_error"] == True):
            sem_error.config(image = img_error)
        else:
            sem_error.config(image = img_success)

        lex_canvas.itemconfig(lex_output, text=settings.lex_state["output"])
        lex_canvas.config(scrollregion=lex_canvas.bbox("all"))
        syn_canvas.itemconfig(syn_output, text=settings.syn_state["output"])
        syn_canvas.config(scrollregion=syn_canvas.bbox("all"))
        sem_canvas.itemconfig(sem_output, text=settings.sem_state["output"])
        sem_canvas.config(scrollregion=sem_canvas.bbox("all"))


    f = open('input.txt', encoding='utf-8')
    lines=f.read()

    main_window = ThemedTk(theme="breeze")
    main_window.title('Quran Compiler')

    outer_frame = ttk.Frame(main_window)
    outer_frame.pack()
    img_header = ImageTk.PhotoImage(Image.open("header.jpg"))
    header = ttk.Label(outer_frame, image=img_header)
    header.pack()

    frame = ttk.Frame(outer_frame)
    frame.pack(pady=(10, 30), padx=50)


    input_miniframe = Frame(frame, height=50, width=750)
    input_label = ttk.Label(input_miniframe, text = "Input", font=('Segoe 12 bold'))
    run_button = ttk.Button(input_miniframe ,text="Run", command=inputText)
    input_area = Text(frame, height=6, bg="white", relief="groove", padx=10, pady=5)
    input_area.tag_configure('tag-right', justify='right')

    
    # lexical area
    lex_miniframe = ttk.Frame(frame, height=50, width=250)
    lex_label = ttk.Label(lex_miniframe, text = "Lexical analysis", font=('Segoe 12 bold'))
    img_error = ImageTk.PhotoImage(Image.open("error.png"))
    img_success = ImageTk.PhotoImage(Image.open("success.png"))
    lex_error = ttk.Label(lex_miniframe)

    lex_frame = ttk.Frame(frame, width=250, height=300)
    lex_frame.grid(column=0, row=3)
    lex_canvas = Canvas(lex_frame, bg="white", height=300, width=250)
    lex_output = lex_canvas.create_text(20, 20, width=220, text="", font=('Consolas 10'))

    lex_scroll=ttk.Scrollbar(lex_frame, orient=VERTICAL)
    lex_scroll.pack(side=RIGHT,fill=Y)
    lex_scroll.config(command = lex_canvas.yview )
    lex_canvas.config(scrollregion=lex_canvas.bbox("all"), yscrollcommand=lex_scroll.set)

    # syntactic area

    syn_miniframe = ttk.Frame(frame, height=50, width=250)
    syn_label = ttk.Label(syn_miniframe, text = "Syntactic analysis" ,font=('Segoe 12 bold'))
    syn_error = ttk.Label(syn_miniframe)

    syn_frame = ttk.Frame(frame, width=250, height=300)
    syn_frame.grid(column=1, row=3)
    syn_canvas = Canvas(syn_frame, bg="white", height=300, width=250)
    syn_output = syn_canvas.create_text(20, 20, width=220, text="")

    syn_scroll=ttk.Scrollbar(syn_frame, orient=VERTICAL)
    syn_scroll.pack(side=RIGHT,fill=Y)
    syn_scroll.config(command = syn_canvas.yview )
    syn_canvas.config(scrollregion=syn_canvas.bbox("all"), yscrollcommand=syn_scroll.set)

    # semantic area

    sem_miniframe = ttk.Frame(frame, height=50, width=250)
    sem_label = ttk.Label(sem_miniframe, text = "Semantic analysis", font=('Segoe 12 bold'))
    sem_error = ttk.Label(sem_miniframe)

    sem_frame = ttk.Frame(frame, width=250, height=300)
    sem_frame.grid(column=2, row=3)

    sem_canvas = Canvas(sem_frame, bg="white", height=300, width=250)
    sem_output = sem_canvas.create_text(20, 20, width=220, text="")

    sem_scroll=ttk.Scrollbar(sem_frame, orient=VERTICAL)
    sem_scroll.pack(side=RIGHT,fill=Y)
    sem_scroll.config(command = sem_canvas.yview )
    sem_canvas.config(scrollregion=sem_canvas.bbox("all"), yscrollcommand=sem_scroll.set)


    # display
    input_miniframe.grid(column=0, row=0, columnspan=3)
    input_miniframe.columnconfigure(0, minsize=290)
    input_miniframe.columnconfigure(1, minsize=290)
    input_label.grid(column=0, row=0, pady = 2, sticky=W)
    run_button.grid(column=1, row=0, pady = 5, sticky=E)

    input_area.grid(column=0, row=1, columnspan=3)

    lex_miniframe.grid(column=0, row=2)

    lex_label.grid(column=0, row=0, sticky=W)
    lex_error.grid(column=1, row=0, sticky=E)
    lex_miniframe.columnconfigure(0, minsize=125)
    lex_miniframe.columnconfigure(1, minsize=125)
    lex_miniframe.rowconfigure(0, minsize=50)
    lex_canvas.pack(padx=10)


    syn_miniframe.grid(column=1, row=2, padx=10)

    syn_label.grid(column=0, row=0, sticky=W)
    syn_error.grid(column=1, row=0, sticky=E)
    syn_miniframe.columnconfigure(0, minsize=125)
    syn_miniframe.columnconfigure(1, minsize=125)
    syn_miniframe.rowconfigure(0, minsize=50)

    syn_canvas.pack(padx=10)

    sem_miniframe.grid(column=2, row=2)

    sem_label.grid(column=0, row=0, sticky=W)
    sem_error.grid(column=1, row=0, sticky=E)
    sem_miniframe.columnconfigure(0, minsize=125)
    sem_miniframe.columnconfigure(1, minsize=125)
    sem_miniframe.rowconfigure(0, minsize=50)
    sem_canvas.pack(padx=10)


    main_window.mainloop()