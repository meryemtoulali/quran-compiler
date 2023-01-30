from datetime import datetime

def logevent(s): #log event type with date and time
    f = open("log.txt", "a", encoding='utf-8')
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    string = '\n' + date + ' - ' + s
    f.write(string)
    f.close()

def logeventinfo(s): #log event info
    f = open("log.txt", "a", encoding='utf-8')
    f.write(s)
    f.close()

logevent('starting app\n')