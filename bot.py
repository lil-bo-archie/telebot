import telebot
import sqlite3

bot=telebot.TeleBot('1001877138:AAHefrzspeT5CLisWsv9kdQfP-zQnjuWr6Q')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Чия черга?', 'Треба прибрати(((','виніс')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Чия черга?', 'Треба прибрати(((')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.row('Чия черга?', 'виніс')

'''
keyboard0 = telebot.types.ReplyKeyboardMarkup(True)
keyboard0.row('yes', 'no')
'''

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'вотсап ти написав мені /start, давай своримо тобі кімнату! кст якщо ти до цього створив одну, вона зникне)) щоб перейти до режиму створення кімнати введи команду /reg.')
    # print("yo dude")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, "Тикаєш на великі клавіші й отримуєш інфу, що неясно? /reg - свторити нову кімнату")
    # print("yo dude")

@bot.message_handler(commands=['reg'])
def registration(message):

    conn = sqlite3.connect('bot_database.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT members FROM Rooms ''')
    n = cur.fetchall()
    conn.commit()
    myname = '@' + message.chat.username
    for room in n:
        if myname in room[0]:
            kimn = (n[n.index(room)][0])
            bot.send_message(message.from_user.id, "Чувак, що я можу тобі сказати ти вже є в кімнатах!! Тому просто тикай на клавіші великі й буде тобі щастя.")
    try:
        print(kimn)
    except:
        msg = bot.send_message(message.from_user.id, "Введи ім'я кімнати:")
        bot.register_next_step_handler(msg, name)

lis = []
guys = []

def name(message):
    lis.append(message.text)
    room_number = message.text
    msg = bot.send_message(message.chat.id, 'Скіки вас у кімнаті пацанів?')
    bot.register_next_step_handler(msg, number)

def number(message):
    try:
        lis.append(message.text)
        room_number = int(message.text)
        room_number = abs(room_number)
        msg = bot.send_message(message.chat.id, 'Тепер введи nicknames pls, якщо що - ось так, бо зі звичайною фігньою не вийде, тре нікнейм для нагадувань ось так: - {0}'.format('@' + message.chat.username))
        
        # the next line is a musthave for a final product as it'll ease the room reg process
        #guys.append('@'+message.chat.username)
        bot.register_next_step_handler(msg, names)
    except:
        msg = bot.send_message(message.chat.id, 'Ну, сам розумієш, що {0} людей вас бути не може - ботові треба ціле додатнє число'.format(message.text))       
        bot.register_next_step_handler(msg, number)



def names(message):
    
    if (message.text).startswith('@'):
        guys.append(message.text)
        num = len(guys)
        num = len(guys)
        print(num)
        # print(guys)
        if num != (int(lis[1])):    
            print(num)
            print((int(lis[1])))
            msg = bot.send_message(message.chat.id, 'Окей, додав я туди {0} чувака - {1}.'.format(num, message.text), reply_markup=keyboard2)
            bot.register_next_step_handler(msg, names)
        else:
            msg = bot.send_message(message.chat.id, 'Ну всьо, зарегав цю діч для тебе!!! нажимай великі кнопочки тепер і зможеш дізнатися чия черга прибирати й виносити сміття!')
            lis.append(guys)
            # guys = str(guys)
            print(name)
            conn = sqlite3.connect('bot_database.sqlite')
            cur = conn.cursor()

            cur.execute('''SELECT members FROM Rooms ''')
            cur.execute('''INSERT OR IGNORE INTO Rooms (name, members, l2)
            VALUES ( ?, ?, ?)''', ( str(lis[0]), str(guys), 0) )
            conn.commit()
    else:
            msg = bot.send_message(message.chat.id, 'Ти повинен ввести нік чувака, що починається з "@" ', reply_markup=keyboard2)       
            bot.register_next_step_handler(msg, names)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    l2 = []

    conn = sqlite3.connect('bot_database.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Rooms''')

    n = cur.fetchall()
    conn.commit()

    myname = '@' + message.chat.username

    for room in n:
        # print(room[2])
        if myname in room[2]:
            kimn = (n[n.index(room)][2])
            l2 = (n[n.index(room)][3])
            print('osio kimnata - ',kimn)
    try:

        l1 = kimn.strip('][').split(', ') 

        print(type(l1))
        # if not l2:
        #     l2 = []
        # else:
        #     l2 = l2.strip('][').split(', ') 
        print(l2)
        l2 = []
        if message.text == "Чия черга?":
            if len(l2) <= 1:
                l2.extend(l1)
            # print(l2[0], 'cleans')
            print(message.chat.username,'opa i tut', l2[0].strip("'"))
            if (l2[0]).strip("'") == ('@'+message.chat.username):
                bot.send_message(message.from_user.id, "Ти повинен прибрати!",  reply_markup=keyboard3)
            else:
                bot.send_message(message.from_user.id, "{0} повинен прибрати".format((l2[0]).strip("'")))
        elif message.text == "Треба прибрати(((":
            if len(l2) <= 1:
                l2.extend(l1)
            bot.send_message(message.from_user.id, "Запускаю нагадування {0}".format((l2[0]).strip("'")))

        elif message.text == "виніс":
            print('1 tut nema pomylky')
            if len(l2) <= 1:
                # print('2/1 tut nema pomylky')
                l2.extend(l1)
                # conn = sqlite3.connect('bot_database.sqlite')
                # cur = conn.cursor()
                # cur.execute('''SELECT members FROM Rooms ''')
                # # print( str(l2), str(l1))
                # cur.execute('''INSERT INTO Rooms (l2) VALUES (?) WHERE members = (?)''', ( str(l2), str(l1), ) )
                # conn.commit()
                # print(' 2 tut nema pomylky')

            del(l2[0])
            print(l2[0], 'cleans')



            bot.send_message(message.from_user.id, "Уважаю, тепер {0} повинен прибирати".format((l2[0].strip("'"))), reply_markup=keyboard2) 

        else:
            # bot.send_message(message.from_user.id, "шо? ти лох")
            myname = '@' + message.chat.username
            print('My name is ', myname)
            bot.send_message(message.from_user.id, "шо? тебе звати хаха {0}".format(myname))
    except:

        bot.send_message(message.from_user.id, "Чувак, що я можу тобі сказати - тебе нема в кімнатах! ось так от, нажми /reg щоб зареєструвати нову!")
    
       


bot.polling(none_stop=True, interval=0)

# to get a username we use:
# myname = '@' + message.chat.username
