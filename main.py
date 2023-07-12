from datetime import datetime
import telebot
from telebot import types
from mysql.connector import connect, Error
import os
import traceback

import config
import database as db
import rr
import cl
import gdrive
from admin import generate_key

# accbot112211@gmail.com
# qwerty12Aa

answ = cl.Anwers()
menu = cl.Menu()
qmsg1 = answ.qmsg1

bot = telebot.TeleBot(config.token)
path_bot = config.path_bot
if path_bot[-1] != "/":
    path_bot += "/"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        now = datetime.now().strftime("%H:%M:%S")
        print(now + " - " + message.from_user.username + " - " + str(message.from_user.id) + " - start")

        user_name = message.from_user.username
        user_id = str(message.from_user.id)
        if message.chat.id > 0:
            user = db.get_user(user_id, user_name)
            print(user)

            bot.send_message(message.from_user.id, answ.start_for_lead[0] + answ.pavel_consultant_link)
            # markup = menu.markup(menu.start2)
            # bot.send_message(message.chat.id, answ.start1[0], reply_markup=markup)
            # bot.send_message(message.chat.id, answ.start1[1], reply_markup=markup)
    except:
        err = traceback.format_exc().replace('"', '')
        err = err.replace("'", "")
        print(err)
        bot.send_message(message.chat.id, "Ошибка", reply_markup=None)
        command = message.from_user.username + " - " + str(message.chat.id) + " - start"
        db.add_log(command, err)


@bot.message_handler(content_types=['text'])
def work_acc(message: types.Message):
    try:
        now = datetime.now().strftime("%H:%M:%S")
        requests_bot = message.text.lower()
        user_name = message.from_user.username
        user_id = str(message.from_user.id)
        chat_id = str(message.chat.id)

        print(now + " - " + message.from_user.username + " - " + str(message.chat.id) + " - " + requests_bot)
        user = db.get_user(user_id, user_name)
        org = db.get_org(user_id)
        st = 0

        if user[0][7] == "lead":
            users_token = db.check_token(user_id)
            if users_token != 0:
                if message.text == users_token:
                    db.upd_org(user_id, "users", "status", "user")
                    markup = menu.markup(menu.start2)
                    bot.send_message(message.chat.id, answ.start1[0], reply_markup=markup)
                    bot.send_message(message.chat.id, answ.start1[1], reply_markup=markup)
                    return
                else:
                    bot.send_message(message.from_user.id, answ.start_for_lead[3])
                    return
            else:
                bot.send_message(message.from_user.id, answ.start_for_lead[1] + answ.pavel_consultant_link +
                                 answ.start_for_lead[2])
                return

        if user[0][7] == "admin":
            if message.text == "Пользователь зарегистрирован":
                markup = menu.markup(menu.admin_kb_1)
                bot.send_message(message.from_user.id, answ.admin_msg[1], reply_markup=markup)
            elif message.text.isdigit():
                markup = menu.markup(menu.admin_kb_1)
                token = generate_key()
                resp = db.update_user_token(message.text, token)
                bot.send_message(message.from_user.id, answ.admin_msg[2] + message.text + resp + token,
                                 reply_markup=markup)
            else:
                markup = menu.markup(menu.admin_kb_2)
                bot.send_message(message.from_user.id, answ.admin_msg[0], reply_markup=markup)

        elif message.chat.id > 0 and user[0][7] != "assistant":

            if message.text == config.assistants_password:
                db.upd_org(user_id, "users", "status", "assistant")
                # db.del_org(user_id) - нужно ли чистить организации?
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.from_user.id, answ.assistant_msg[0], reply_markup=markup)
                bot.send_message(message.chat.id, answ.help_a, reply_markup=markup)
                return

            elif message.text == "К обзору!":
                if user[0][8] == 0:
                    db.upd_progress(user_id, "users", "9999")
                else:
                    db.upd_progress(user_id, "users", "9998")
                # user = db.get_user(user_id, user_name)
                markup = menu.markup([menu.start1[0]])
                bot.send_message(message.chat.id, answ.start2[0], reply_markup=markup)
            elif message.text == "Понятно, далее":
                markup = menu.markup([menu.start1[1]])
                bot.send_message(message.chat.id, answ.start2[1], reply_markup=markup)
            elif message.text == "Классно, далее":
                markup = menu.markup([menu.start1[2]])
                bot.send_message(message.chat.id, answ.start2[2], reply_markup=markup)
                bot.send_message(message.chat.id, answ.start2[3], reply_markup=markup)
            elif message.text == "Понял, буду отправлять первичку вовремя":
                markup = menu.markup([menu.start1[3]])
                bot.send_message(message.chat.id, answ.start2[4], reply_markup=markup)
            elif message.text == "Понял, далее":
                markup = menu.markup([menu.start1[4]])
                bot.send_message(message.chat.id, answ.start2[5], reply_markup=markup)
            elif message.text == "Понятно":
                markup = menu.markup([menu.start1[5]])
                bot.send_message(message.chat.id, answ.start2[6], reply_markup=markup)
            elif message.text == "Ага, хорошо":
                if user[0][8] == 9999:
                    db.upd_progress(user_id, "users", "0")
                else:
                    db.upd_progress(user_id, "users", "1")
                user = db.get_user(user_id, user_name)
                st = 1
                if user[0][8] == 0:
                    markup = menu.markup([menu.start2[1]])
                    bot.send_message(message.chat.id, answ.start2[7], reply_markup=markup)
                else:
                    # ===========================================================================================================================================
                    # markup = menu.markup(menu.cancel)
                    markup = menu.markup(menu.mainmenu)
                    bot.send_message(message.chat.id, answ.start2[7], reply_markup=markup)
                    # bot.send_message(message.chat.id, answ.start3[0], reply_markup=None)
                    # bot.send_message(message.chat.id, answ.start3[1], reply_markup=None)
                    # bot.send_message(message.chat.id, answ.form1[org[0][19]], reply_markup=markup)

            if int(chat_id) < 0:
                None

            elif user[0][8] == 0 and st == 0:
                if message.text == menu.cancel[0]:
                    markup = menu.markup(menu.start2)
                    bot.send_message(message.chat.id, answ.start1[0], reply_markup=markup)
                    bot.send_message(message.chat.id, answ.start1[1], reply_markup=markup)

                elif message.text == "К работе!":
                    markup = menu.markup(menu.cancel)
                    bot.send_message(message.chat.id, answ.start3[0], reply_markup=None)
                    bot.send_message(message.chat.id, answ.start3[1], reply_markup=None)
                    bot.send_message(message.chat.id, answ.form1[org[0][19]], reply_markup=markup)

                elif org[0][19] <= 12:
                    if message.text == "Отмена":
                        markup = menu.markup(menu.start2)
                        # db.upd_progress(user_id, "users", "0")
                        db.upd_progress(user_id, "organizations", "0")

                        bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                        bot.send_message(message.chat.id, answ.start3[1], reply_markup=markup)
                        bot.send_message(message.chat.id, answ.form1[org[0][19]], reply_markup=markup)
                    else:
                        if message.text != config.assistants_password:
                            db.upd_org(user_id, "organizations", answ.form1db[org[0][19]], str(message.text))
                            db.upd_progress(user_id, "organizations", str(org[0][19] + 1))

                            markup = menu.markup(menu.cancel)
                            bot.send_message(message.chat.id, answ.form1[org[0][19] + 1], reply_markup=markup)

                elif org[0][19] == 13:
                    markup = menu.markup(menu.start3)
                    bot.send_message(message.chat.id, answ.start4[0], reply_markup=markup)
                    bot.send_message(message.chat.id, answ.start4[1], reply_markup=markup)
                    db.upd_org(user_id, "organizations", answ.form1db[org[0][19]], str(message.text))
                    db.upd_progress(user_id, "organizations", str(org[0][19] + 1))
                    path_dr = gdrive.create_orgs_folder(org[0][5], config.folder_id)
                    db.upd_org(user_id, "organizations", "folder_id", str(path_dr))

                    path_dr2 = gdrive.create_orgs_folder("Трудоустройство", path_dr)
                    db.upd_org(user_id, "organizations", "folder_id2", str(path_dr2))

                    path_dr3 = gdrive.create_orgs_folder("Финансовые документы", path_dr)
                    db.upd_org(user_id, "organizations", "folder_id3", str(path_dr3))

                    path_dr4 = gdrive.create_orgs_folder("Отчёты", path_dr)
                    db.upd_org(user_id, "organizations", "folder_id4", str(path_dr4))

                    path_dr5 = gdrive.create_orgs_folder("ФНС", path_dr4)
                    db.upd_org(user_id, "organizations", "folder_id5", str(path_dr5))

                    path_dr6 = gdrive.create_orgs_folder("СФР", path_dr4)
                    db.upd_org(user_id, "organizations", "folder_id6", str(path_dr6))

                    path_dr7 = gdrive.create_orgs_folder("ФСС", path_dr4)
                    db.upd_org(user_id, "organizations", "folder_id7", str(path_dr7))

                    path_dr8 = gdrive.create_orgs_folder("other", path_dr)
                    db.upd_org(user_id, "organizations", "folder_id8", str(path_dr8))

                elif message.text == "Я буду загружать сам":
                    markup = menu.markup(menu.start4)
                    bot.send_message(message.chat.id, answ.start6, reply_markup=markup)
                    bot.send_photo(message.chat.id, open(os.path.abspath(__file__)[:-7] + 'image.png', 'rb'))

                elif message.text == "Хорошо, буду загружать":
                    markup = menu.markup(menu.mainmenu)
                    bot.send_message(message.chat.id, answ.start5end, reply_markup=markup)
                    db.upd_progress(user_id, "users", "1")

                elif message.text == "Я передумал, хочу автоматизировать процесс" or message.text == "Я хочу автоматизировать процесс":
                    markup = menu.markup(menu.mainmenu)
                    bot.send_message(message.chat.id, answ.start7, reply_markup=markup)
                    bot.send_message(message.chat.id, answ.start5end, reply_markup=markup)
                    db.upd_progress(user_id, "users", "1")

                    markup = menu.inline(user_id)
                    answer = "Клиент https://t.me/" + user_name + " хочет оформить доверенность\nact=1"
                    bot.send_message(config.assists_chat, answer, reply_markup=markup)
                    # ===========================================================================================================================================
                    # ссылка для ассистентов https://t.me/test_8979_bot

                # print(os.path.abspath(__file__)[:-7])

            elif message.text == "К работе!":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.start2[7], reply_markup=markup)

            elif user[0][8] == 91:
                markup = menu.inline(user_id)
                answer = "https://t.me/" + user_name + "\nКлиент " + org[0][
                    5] + " спрашивает:\n" + message.text + "\nact=2"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, "Через некоторое время специалист даст ответ", reply_markup=markup)
                db.upd_progress(user_id, "users", "1")

            elif user[0][8] == 102:
                markup = menu.inline(user_id)
                answer = "https://t.me/" + user_name + "\nКлиент " + org[0][
                    5] + " спрашивает:\n" + message.text + "\nact=2"
                bot.send_message(config.assists_chat_fsi, answer, reply_markup=markup)
                # ===========================================================================================================================================
                # ссылка для ассистентов
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.fsi2[1], reply_markup=markup)
                db.upd_progress(user_id, "users", "1")

            elif user[0][8] == 103:
                markup = menu.inline(user_id)
                answer = "https://t.me/" + user_name + "\nКлиент " + org[0][
                    5] + " спрашивает:\n" + message.text + "\nact=3"
                bot.send_message(config.assists_chat_fsi, answer, reply_markup=markup)
                # ===========================================================================================================================================
                # ссылка для ассистентов
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.fsi3[1], reply_markup=markup)
                db.upd_progress(user_id, "users", "1")

            elif 200 <= user[0][8] <= 208:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    wrt = user[0][9] + "@@$@@" + message.text
                    db.upd_org(user_id, "users", "stage", wrt)
                    markup = menu.markup(menu.cancel)
                    bot.send_message(message.chat.id, answ.doc1form2[user[0][8] + 1 - 200], reply_markup=markup)
            elif user[0][8] == 209:
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.docs1[3], reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                db.upd_org(user_id, "users", "stage", "")
                del form1_list[0]

                markup = menu.inline(user_id)
                # print(answ.doc1form2)
                # print(form1_list)
                # answer = "https://t.me/" + user_name + "\nКлиент " + org[0][5] + " запросил составление договора купли-продажи."
                answer = rr.company_list.format(user="https://t.me/" + user_name, org_name="Клиент " + org[0][5],
                                                items="составление договора купли-продажи.",
                                                q=org[0]) + "\n===================\n" + rr.contract_trade.format(
                    w=answ.doc1form2, q=form1_list) + "\nact=4"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Клиент "Название ООО" запросил составление договора купли-продажи.

            elif 300 <= user[0][8] <= 312:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    db.upd_org(user_id, "users", "stage", user[0][9] + "@@$@@" + message.text)
                    markup = menu.markup(menu.cancel)
                    bot.send_message(message.chat.id, answ.doc2form3[user[0][8] + 1 - 300], reply_markup=markup)
            elif user[0][8] == 313:
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.docs1[3], reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                db.upd_org(user_id, "users", "stage", "")
                del form1_list[0]

                markup = menu.inline(user_id)
                # answer = "https://t.me/" + user_name + "\nКлиент " + org[0][5] + " запросил составление договора купли-продажи."
                answer = rr.company_list.format(user="https://t.me/" + user_name, org_name="Клиент " + org[0][5],
                                                items="составление договора об оказании услуг плательщика НПД.",
                                                q=org[0]) + "\n===================\n" + rr.contract_NPD.format(
                    w=answ.doc2form3, q=form1_list) + "\nact=5"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)

                # markup = menu.inline(user_id)
                # answer = "https://t.me/" + user_name + "\nКлиент " + org[0][5] + " запросил составление договора об оказании услуг плательщика НПД."
                # bot.send_message(config.assists_chat, answer, reply_markup=markup)
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Клиент "Название ООО" запросил составление договора об оказании услуг плательщика НПД.

            elif 400 <= user[0][8] <= 412:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    wrt = user[0][9] + "@@$@@" + message.text
                    db.upd_org(user_id, "users", "stage", wrt)
                    markup = menu.markup(menu.cancel)
                    bot.send_message(message.chat.id, answ.doc3form4[user[0][8] + 1 - 400], reply_markup=markup)
            elif user[0][8] == 413:
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.docs1[3], reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                db.upd_org(user_id, "users", "stage", "")
                del form1_list[0]

                markup = menu.inline(user_id)
                # answer = "https://t.me/" + user_name + "\nКлиент " + org[0][5] + " запросил составление договора купли-продажи."
                answer = rr.company_list.format(user="https://t.me/" + user_name, org_name="Клиент " + org[0][5],
                                                items="составление договора ГПХ с физическим лицом.",
                                                q=org[0]) + "\n===================\n" + rr.contract_GPH_F.format(
                    w=answ.doc3form4, q=form1_list) + "\nact=6"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Клиент "Название ООО" запросил составление договора ГПХ с физическим лицом.

            elif 500 <= user[0][8] <= 509:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    wrt = user[0][9] + "@@$@@" + message.text
                    db.upd_org(user_id, "users", "stage", wrt)
                    markup = menu.markup(menu.cancel)
                    bot.send_message(message.chat.id, answ.doc3form5[user[0][8] + 1 - 500], reply_markup=markup)
            elif user[0][8] == 510:
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id,
                                 "Спасибо, я сделал договор, как свободный бухгалтер его проверит я сразу же отправлю его тебе",
                                 reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                db.upd_org(user_id, "users", "stage", "")
                del form1_list[0]

                markup = menu.inline(user_id)
                answer = rr.company_list.format(user="https://t.me/" + user_name, org_name="Клиент " + org[0][5],
                                                items="составление договора ГПХ с юридическим лицом.",
                                                q=org[0]) + "\n===================\n" + rr.contract_GPH_U.format(
                    w=answ.doc3form5, q=form1_list) + "\nact=7"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)

            elif 600 <= user[0][8] <= 615:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    wrt = user[0][9] + "@@$@@" + message.text
                    db.upd_org(user_id, "users", "stage", wrt)
                    markup = menu.markup(menu.cancel)
                    bot.send_message(message.chat.id, answ.worksform6[user[0][8] + 1 - 600], reply_markup=markup)
            elif user[0][8] == 616:
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id,
                                 "Спасибо, я сделал договор, как свободный бухгалтер его проверит я сразу же "
                                 "отправлю его тебе",
                                 reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                db.upd_org(user_id, "users", "stage", "")
                del form1_list[0]
                db.add_worker(org, form1_list)

                markup = menu.inline(user_id)
                answer = rr.company_list.format(user="https://t.me/" + user_name, org_name="Клиент " + org[0][5],
                                                items="составление договора найма нового сотрудника.",
                                                q=org[0]) + "\n===================\n" + rr.contract_hiring.format(
                    w=answ.worksform6, q=form1_list) + "\nact=8"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)
            elif user[0][8] == 50:
                summ = message.text

                summ = summ.replace("    ", "")
                summ = summ.replace("   ", "")
                summ = summ.replace("  ", "")
                summ = summ.replace(" ", "")

                # try:
                float(summ)

                db.upd_progress(user_id, "users", "1")
                worker = user[0][10]
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id,
                                 "Спасибо, я сделал дополнительное соглашение к трудовому договору, как свободный бухгалтер его проверит я сразу же отправлю его тебе",
                                 reply_markup=markup)
                work = db.get_work(worker)
                db.upd_worker2(str(work[0][0]), "workers", "bet_size", summ)
                db.upd_org(user_id, "users", "target1", "")

                markup = menu.inline(user_id)
                answer = "Клиент " + org[0][5] + " хочет изменить оклад сотрудника " + work[0][
                    5] + " на " + summ + "\nact=9"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)

            elif user[0][8] == 51:
                new_d = message.text

                db.upd_progress(user_id, "users", "1")
                worker = user[0][10]
                work = db.get_work(worker)
                markup = menu.inline(user_id)
                answer = "Клиент " + org[0][5] + " хочет изменить должность сотрудника " + work[0][
                    5] + " на " + new_d + "\nact=10"
                db.upd_worker2(str(work[0][0]), "workers", "jtitle", new_d)
                bot.send_message(config.assists_chat, answer, reply_markup=markup)
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id,
                                 "Спасибо, я сделал дополнительное соглашение к трудовому договору, как свободный бухгалтер его проверит я сразу же отправлю его тебе",
                                 reply_markup=markup)
                db.upd_org(user_id, "users", "target1", "")

            elif user[0][8] >= 700 and user[0][8] <= 708:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    wrt = user[0][9] + "@@$@@" + message.text
                    db.upd_org(user_id, "users", "stage", wrt)
                    markup = menu.markup(menu.cancel2)
                    if "Пропустить" == message.text:
                        bot.send_message(message.chat.id, "Пропущено: \n" + answ.worksform7[user[0][8] + 1 - 700],
                                         reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, "Данные изменены: \n" + answ.worksform7[user[0][8] + 1 - 700],
                                         reply_markup=markup)

            elif user[0][8] == 709:
                markup = menu.markup(menu.cancel2)
                bot.send_message(message.chat.id,
                                 "Спасибо, я сделал дополнительное соглашение к трудовому договору, как свободный бухгалтер его проверит я сразу же отправлю его тебе",
                                 reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                db.upd_org(user_id, "users", "stage", "")
                del form1_list[0]
                # db.upd_worker(org[0][0], form1_list)
                for i in range(len(form1_list)):
                    if "Пропустить" != form1_list[i]:
                        db.upd_worker2(org[0][0], "workers", answ.works_db_form[i], form1_list[i])

                markup = menu.inline(user_id)
                # answer = "Клиент " + org[0][5] + "хочет изменить личные данные сотрудника " + work[0][5] + "\n===================\n" + rr.contract_hiring.format(w = answ.worksform7, q = form1_list) + "\nact=11"
                # bot.send_message(config.assists_chat, answer, reply_markup=markup)

            elif message.text.lower() == "/помощь":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.help_m, reply_markup=markup)

            elif message.text.lower() == "/вопросы" or message.text == "Вернуться к вопросам":
                markup = menu.markup(menu.qs)
                bot.send_message(message.chat.id, answ.qmsg0, reply_markup=markup)

            # вопросы:
            elif message.text in menu.qs:
                markup = menu.markup(menu.questmenu)
                for x in answ.qmsg1[menu.qs.index(message.text)]:
                    bot.send_message(message.chat.id, x, reply_markup=markup)
                if menu.qs.index(message.text) == 11:
                    db.upd_progress(user_id, "users", "91")

            elif message.text.lower() == "/фси":
                markup = menu.markup(menu.fsi1)
                bot.send_message(message.chat.id, answ.fsi1[0], reply_markup=markup)

            elif message.text == "Мне нужно составить финансовый отчёт":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.fsi1[1], reply_markup=markup)
                answer = "Клиент " + org[0][5] + " хочет получить финансовый отчёт" + "\nact=12"
                bot.send_message(config.assists_chat_fsi, answer, reply_markup=None)
                # ===========================================================================================================================================
                # Клиент "Название ООО" хочет получить финансовый отчёт

            elif message.text == "У меня есть вопрос по работе с фондом.":
                markup = menu.markup(menu.fsi2)
                bot.send_message(message.chat.id, answ.fsi1[2], reply_markup=markup)

            elif message.text == "Письменную":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.fsi2[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "102")

            elif message.text == "Прямую консультацию":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.fsi3[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "103")

            elif message.text.lower() == "/документы":
                markup = menu.markup(menu.docs1)
                bot.send_message(message.chat.id, answ.docs0[0], reply_markup=markup)

            # !
            elif message.text == "Договор купли/продажи":
                markup = menu.markup(menu.docs21)
                bot.send_message(message.chat.id, answ.docs1[0], reply_markup=markup)

            elif message.text == "Хoчу шаблон":
                markup = menu.markup(menu.mainmenu)
                bot.send_document(message.chat.id, document=open(
                    os.path.abspath(__file__)[:-7] + 'Договор куплипродажи-продажи (шаблон).doc', 'rb'),
                                  reply_markup=markup)

            elif message.text == "Хочу весь дoговор":
                markup = menu.markup(menu.cancel)
                bot.send_message(message.chat.id, answ.docs1[1], reply_markup=markup)
                bot.send_message(message.chat.id, answ.docs1[2], reply_markup=markup)
                bot.send_message(message.chat.id, answ.doc1form2[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "200")

            # !
            elif message.text == "Договор для работы с самозанятыми":
                markup = menu.markup(menu.docs22)
                bot.send_message(message.chat.id, answ.docs1[0], reply_markup=markup)

            elif message.text == "Хочy шаблон":
                markup = menu.markup(menu.mainmenu)
                bot.send_document(message.chat.id, document=open(
                    os.path.abspath(__file__)[:-7] + 'Договор оказания услуг самозанятым (шаблон).doc', 'rb'),
                                  reply_markup=markup)

            elif message.text == "Хочу весь догoвор":
                markup = menu.markup(menu.cancel)
                bot.send_message(message.chat.id, answ.docs2[0], reply_markup=markup)
                bot.send_message(message.chat.id, answ.doc2form3[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "300")

            # !
            elif message.text == "Договoр ГПХ":
                markup = menu.markup(menu.docs23)
                bot.send_message(message.chat.id, answ.docs1[0], reply_markup=markup)

            elif message.text == "Хoчy шаблон":
                markup = menu.markup(menu.mainmenu)
                bot.send_document(message.chat.id,
                                  document=open(os.path.abspath(__file__)[:-7] + 'Договор ГПХ (шаблон).docx', 'rb'),
                                  reply_markup=markup)

            elif message.text == "Хочу весь договoр":
                markup = menu.markup(menu.docs3)
                bot.send_message(message.chat.id, "Договор на юридическое или физическое лицо?", reply_markup=markup)

            elif message.text == "Физ. лицо":
                markup = menu.markup(menu.cancel)
                bot.send_message(message.chat.id, "Заполни данную форму", reply_markup=markup)
                bot.send_message(message.chat.id, answ.doc3form4[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "400")

            elif message.text == "Юр. лицо":
                markup = menu.markup(menu.cancel)
                bot.send_message(message.chat.id, "Заполни данную форму", reply_markup=markup)
                bot.send_message(message.chat.id, answ.doc3form5[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "500")

            # !
            elif message.text.lower() == "/сотрудники":
                markup = menu.markup(menu.works1)
                bot.send_message(message.chat.id, answ.works1[0], reply_markup=markup)

            elif message.text == "Нанять нового сотрудника":
                markup = menu.markup(menu.cancel)
                bot.send_message(message.chat.id, answ.works1[1], reply_markup=markup)
                bot.send_message(message.chat.id, answ.worksform6[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "600")

            elif message.text == "Уволить сотрудника":
                inline_list = db.get_works(str(org[0][0]))
                markup = menu.inline_list(inline_list, "worker_list7")
                if len(inline_list) > 0:
                    bot.send_message(message.chat.id, "Какого сотрудника ты хочешь уволить?", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "Нет сотрудников", reply_markup=markup)

            # !
            elif message.text == "Изменить условия для сотрудника":
                inline_list = db.get_works(str(org[0][0]))
                markup = menu.inline_list(inline_list, "worker_list1")
                if len(inline_list) > 0:
                    bot.send_message(message.chat.id, "Для какого сотрудника ты хочешь внести изменения?",
                                     reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "Нет сотрудников", reply_markup=markup)

            elif message.text == "Изменить оклад":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id,
                                 "Какой месячный оклад ты хочешь установить для этого сотрудника?Помни, что \"На руки \" сотрудник получит суммы с вычетом 13%",
                                 reply_markup=markup)
                db.upd_progress(user_id, "users", "50")

            elif message.text == "Изменить должность":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, "Какую должность теперь занимает этот сотрудник?",
                                 reply_markup=markup)
                db.upd_progress(user_id, "users", "51")

            elif message.text == "Изменить личные данные":
                markup = menu.markup(menu.cancel2)
                bot.send_message(message.chat.id, answ.works1[1], reply_markup=markup)
                bot.send_message(message.chat.id, answ.worksform6[0], reply_markup=markup)
                db.upd_progress(user_id, "users", "700")

            # !
            elif message.text.lower() == "/моя компания":
                markup = menu.markup(menu.my_company)
                bot.send_message(message.chat.id, "Какую информацию ты хочешь узнать?", reply_markup=markup)

            elif message.text == "Данные о компании":
                markup = menu.markup(menu.my_company)
                bot.send_message(message.chat.id, answ.my_org(org), reply_markup=markup)

            elif message.text == "Данные сотрудников":
                inline_list = db.get_works(str(org[0][0]))
                markup = menu.inline_list(inline_list, "worker_list2")
                if len(inline_list) > 0:
                    bot.send_message(message.chat.id, "Данные какого сотрудника тебе нужны?", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "Нет сотрудников", reply_markup=markup)

            elif message.text == "Реквизиты счёта":
                markup = menu.markup(menu.my_company)
                answer = answ.req_acc.format(org[0][15], org[0][16], org[0][18], org[0][17], org[0][8])
                bot.send_message(message.chat.id, answer, reply_markup=markup)

            elif message.text == "Документооборот":

                inline_list = list()
                r = gdrive.drive_check_all(org[0][20])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append([x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append([x['name'], "2" + x['id']])
                r = gdrive.drive_check_all(org[0][21])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append([x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append([x['name'], "2" + x['id']])
                r = gdrive.drive_check_all(org[0][22])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append([x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append([x['name'], "2" + x['id']])

                markup = menu.inline_list2(inline_list, "worker_list3")

                if len(inline_list) > 0:
                    bot.send_message(message.chat.id, "Какой документ тебе отправить?", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "Нет документов", reply_markup=markup)

            # !
            elif message.text.lower() == "/1с":
                markup = menu.markup(menu.d_1c)
                bot.send_message(message.chat.id, "Какой документ ты хочешь загрузить?", reply_markup=markup)

            elif message.text in menu.d_1c:
                # print(menu.d_1c.index(message.text))
                markup = menu.markup(menu.mainmenu)
                ind = menu.d_1c.index(message.text)
                db.upd_progress(user_id, "users", str(40 + ind))
                bot.send_message(message.chat.id, answ.d_1c[ind], reply_markup=markup)

            # !
            elif message.text.lower() == "/1с_выгрузка":
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, "Формирую выгрузку, скоро я тебе её отправлю", reply_markup=markup)

                markup = menu.inline(user_id)
                answer = "https://t.me/" + user_name + "\nКлиент " + org[0][5] + " запросил выгрузку из 1С"
                bot.send_message(config.assists_chat, answer, reply_markup=markup)

            # !
            elif message.text == "Отчёты в налоговые органы":

                inline_list = list()
                r = gdrive.drive_check_all(org[0][24])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append(["ФНС - " + x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append(["ФНС - " + x['name'], "2" + x['id']])
                r = gdrive.drive_check_all(org[0][25])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append(["СФР - " + x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append(["СФР - " + x['name'], "2" + x['id']])
                r = gdrive.drive_check_all(org[0][26])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append(["ФСС - " + x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append(["ФСС - " + x['name'], "2" + x['id']])

                markup = menu.inline_list2(inline_list, "worker_list8")

                if len(inline_list) > 0:
                    bot.send_message(message.chat.id, "Какой документ тебе отправить?", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "Нет отчётов", reply_markup=markup)

            else:
                markup = None

        if message.chat.id > 0 and user[0][7] == "assistant":

            if message.reply_to_message:

                if user[0][7] == "assistant":
                    reply_text = message.reply_to_message.text
                    if "act=2" in reply_text[-30:] or "act=3" in reply_text[-30:]:
                        label = reply_text.find("user: ", -30) + 6
                        # print(reply_text[label:])
                        # print("requests_bot[label:]")
                        user_ids = reply_text[label:]
                        bot.send_message(user_ids, message.text)

            elif 4600 <= user[0][8] <= 4615:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    db.upd_org(user_id, "users", "target1", "")
                    db.upd_org(user_id, "users", "target2", "")
                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    wrt = user[0][9] + "@@$@@" + message.text
                    db.upd_org(user_id, "users", "stage", wrt)
                    markup = menu.markup(menu.cancel)
                    bot.send_message(message.chat.id, answ.worksform6[user[0][8] + 1 - 4600], reply_markup=markup)
            elif user[0][8] == 4616:
                markup = menu.markup(menu.mainmenu)
                # bot.send_message(message.chat.id, "Спасибо, я сделал договор, как свободный бухгалтер его проверит я сразу же отправлю его тебе", reply_markup=markup)
                bot.send_message(message.chat.id, "Сотрудник добавлен", reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                del form1_list[0]
                db.upd_org(user_id, "users", "stage", "")
                db.upd_org(user_id, "users", "target1", "")
                db.upd_org(user_id, "users", "target2", "")
                db.add_worker(user[0][11], form1_list)

            elif user[0][8] == 4001:
                summ = message.text
                summ = summ.replace("    ", "")
                summ = summ.replace("   ", "")
                summ = summ.replace("  ", "")
                summ = summ.replace(" ", "")
                markup = menu.markup(menu.mainmenu)

                try:
                    float(summ)

                    db.upd_progress(user_id, "users", "1")
                    db.upd_worker2(str(user[0][10]), "workers", "bet_size", summ)

                    bot.send_message(message.chat.id, "Оклад изменён", reply_markup=markup)
                    # db.upd_org(user_id, "users", "stage", "")
                    # db.upd_org(user_id, "users", "target1", "")
                    # db.upd_org(user_id, "users", "target2", "")
                except:
                    bot.send_message(message.chat.id, "Только цифры", reply_markup=markup)

            elif user[0][8] == 4003:
                markup = menu.markup(menu.mainmenu)
                new_d = message.text

                db.upd_progress(user_id, "users", "1")
                db.upd_worker2(str(user[0][10]), "workers", "jtitle", new_d)
                bot.send_message(message.chat.id, "Должность изменена", reply_markup=markup)
                db.upd_org(user_id, "users", "stage", "")
                db.upd_org(user_id, "users", "target1", "")
                db.upd_org(user_id, "users", "target2", "")

            elif 4050 <= user[0][8] <= 4058:
                if message.text == "Отмена":
                    markup = menu.markup(menu.mainmenu)
                    db.upd_progress(user_id, "users", "1")
                    db.upd_org(user_id, "users", "stage", "")
                    db.upd_org(user_id, "users", "target1", "")
                    db.upd_org(user_id, "users", "target2", "")

                    bot.send_message(message.chat.id, "Отменено", reply_markup=markup)
                else:
                    db.upd_progress(user_id, "users", str(user[0][8] + 1))
                    wrt = user[0][9] + "@@$@@" + message.text
                    db.upd_org(user_id, "users", "stage", wrt)
                    markup = menu.markup(menu.cancel2)
                    bot.send_message(message.chat.id, answ.worksform7[user[0][8] + 1 - 4050], reply_markup=markup)

            elif user[0][8] == 4059:
                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, "Данные обновлены", reply_markup=markup)
                db.upd_progress(user_id, "users", "1")
                form1_list = user[0][9].split('@@$@@')
                form1_list.append(message.text)
                del form1_list[0]
                db.upd_org(user_id, "users", "stage", "")
                db.upd_org(user_id, "users", "target1", "")
                db.upd_org(user_id, "users", "target2", "")
                # db.upd_worker02(user[0][10], form1_list)
                for i in range(len(form1_list)):
                    if "Пропустить" != form1_list[i]:
                        db.upd_worker2(user[0][10], "workers", answ.works_db_form[i], form1_list[i])

            elif message.text.lower() == "/помощь":

                markup = menu.markup(menu.mainmenu)
                bot.send_message(message.chat.id, answ.help_a, reply_markup=markup)

            elif message.text.lower() == "/чат":
                orgs = db.get_org_all()
                markup = menu.inline_list3(orgs, "orgs_list")
                bot.send_message(message.chat.id, "Руководителю какой компании ты хочешь написать?",
                                 reply_markup=markup)

            elif message.text.lower() == "/ооо":
                orgs = db.get_org_all()
                markup = menu.inline_list3(orgs, "2orgs_list")
                bot.send_message(message.chat.id, "Данные какой компании тебе нужны?", reply_markup=markup)

            elif message.text.lower() == "/сотрудники_б":
                markup = menu.markup(menu.assist_works_inf)
                bot.send_message(message.chat.id, "Что ты хочешь сделать?", reply_markup=markup)

            elif message.text == "Посмотреть данные сoтрудника":
                orgs = db.get_org_all()
                markup = menu.inline_list3(orgs, "3orgs_list")
                bot.send_message(message.chat.id, "Сотрудников какой компании ты хочешь посмотреть?",
                                 reply_markup=markup)

            elif message.text == "Устроить нового сoтрудника":
                orgs = db.get_org_all()
                markup = menu.inline_list3(orgs, "4orgs_list")
                bot.send_message(message.chat.id, "В какую компанию ты хочешь устроить сотрудника?",
                                 reply_markup=markup)

            elif message.text == "Уволить сoтрудника":
                orgs = db.get_org_all()
                markup = menu.inline_list3(orgs, "5orgs_list")
                bot.send_message(message.chat.id, "Сотрудника какой компании ты хочешь уволить?", reply_markup=markup)

            elif message.text == "Внести изменения в карточку сoтрудника":
                orgs = db.get_org_all()
                markup = menu.inline_list3(orgs, "6orgs_list")
                bot.send_message(message.chat.id, "В карточку сотрудника какой компании ты хочешь внести изменения?",
                                 reply_markup=markup)

            elif message.text.lower() == "/отчёты":
                orgs = db.get_org_all()
                markup = menu.inline_list3(orgs, "7orgs_list")
                bot.send_message(message.chat.id, "Отчёты для какой компании ты хочешь загрузить?", reply_markup=markup)

    except:
        err = traceback.format_exc().replace('"', '')
        err = err.replace("'", "")
        print(err)
        bot.send_message(message.chat.id, "Ошибка", reply_markup=None)
        command = message.from_user.username + " - " + str(message.chat.id) + " - start"
        db.add_log(command, err)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        now = datetime.now()
        now2 = now.strftime("%H:%M:%S")
        now3 = now.strftime("%M%S")
        chat_id = str(call.message.chat.id)
        user_id = str(call.from_user.id)
        mess_id = str(call.message.message_id)
        group_names = str(call.message.chat.title)
        user_name = str(call.from_user.username)
        print(now2 + " - " + call.from_user.username + " - " + str(call.message.chat.id) + " - " + call.data)

        user = db.get_user(user_id, user_name)
        org = db.get_org(user_id)

        if user[0][7] != "assistant":
            if call.data[:13] == 'worker_list1=':
                # print(call.data[12:])
                worker = db.get_work(call.data[13:])

                db.upd_org(user_id, "users", "target1", call.data[13:])

                answer = "Выбран: " + worker[0][5]
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)
                markup = menu.markup(menu.works2)
                bot.send_message(chat_id, "Что ты хочешь поменять?", reply_markup=markup)

            if call.data[:13] == 'worker_list7=':
                worker = db.get_work(call.data[13:])
                if len(worker) > 0:
                    db.del_worker(call.data[13:])
                    answer = "Сотрудник " + worker[0][5] + " уволен"
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                          reply_markup=None)

                    answer = "https://t.me/" + user_name + "\nКлиент " + org[0][5] + " уволил сотрудника " + worker[0][
                        5]
                    bot.send_message(config.assists_chat, answer, reply_markup=None)

            elif call.data[:13] == 'worker_list2=':
                markup = menu.markup(menu.mainmenu)
                # print(call.data[12:])
                worker = db.get_work(call.data[13:])
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answ.worker(worker),
                                      reply_markup=markup)

            elif call.data[:13] == "worker_list3=":
                markup = menu.markup(menu.mainmenu)
                if call.data[13] == "1":
                    answer = "https://drive.google.com/file/d/" + call.data[14:]
                elif call.data[13] == "2":
                    answer = "https://docs.google.com/document/d/" + call.data[14:]
                bot.send_message(chat_id, answer, reply_markup=markup)


            elif call.data[:13] == "worker_list8=":
                markup = menu.markup(menu.mainmenu)
                if call.data[13] == "1":
                    answer = "https://drive.google.com/file/d/" + call.data[14:]
                elif call.data[13] == "2":
                    answer = "https://docs.google.com/document/d/" + call.data[14:]
                bot.send_message(chat_id, answer, reply_markup=markup)

        if user[0][7] == "assistant":
            if call.data[:5] == 'take=':
                db.upd_org(user_id, "users", "status", "assistant")
                user_cl = db.get_user(call.data[5:], "stop")
                # print(call.data[5:])
                # print(user_cl)
                if user_cl != "stop":
                    org_cl = db.get_org(user_id)
                    answer = "от https://t.me/" + user_cl[0][
                        2] + "\nпринят следующий запрос:\n" + call.message.text + "\nuser: " + call.data[5:]

                    markup = menu.markup(menu.mainmenu)
                    # print(call.data[12:])
                    worker = db.get_work(call.data[13:])
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                          text=call.message.text + "\n взял: " + user_name, reply_markup=None)
                    bot.send_message(user_id, answer, reply_markup=markup)
                else:
                    print("не take=" + call.data)

            if call.data[:10] == 'orgs_list=':
                user_cl = db.get_user(call.data[10:], "stop")
                if user_cl != "stop":
                    org_cl = db.get_org(call.data[10:])
                    answer = "Передать сообщение " + str(org_cl[0][5]) + "\nhttps://t.me/" + user_cl[0][
                        2] + "\nact=3\nuser: " + call.data[10:]
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                          reply_markup=None)

            if call.data[:11] == '2orgs_list=':
                user_cl = db.get_user(call.data[11:], "stop")
                if user_cl != "stop":
                    org_cl = db.get_org(call.data[11:])
                    markup = menu.inline_list2(menu.assist_org_inf, "assistand_org_inf")
                    answer = "Какую информацию ты хочешь получить?\nВыбрано: " + str(
                        org_cl[0][5]) + "\n org_id - " + call.data[11:]
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                          reply_markup=markup)

            if call.data == 'assistand_org_inf=req':
                label = call.message.text.rfind("org_id - ") + 9
                org_cl = db.get_org(call.message.text[label:])
                answer = answ.req_acc.format(org_cl[0][15], org_cl[0][16], org_cl[0][18], org_cl[0][17], org_cl[0][8])
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)

            if call.data == 'assistand_org_inf=dat':
                label = call.message.text.rfind("org_id - ") + 9
                org_cl = db.get_org(call.message.text[label:])
                answer = answ.my_org(org_cl)
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)

            if call.data == 'assistand_org_inf=doc':
                label = call.message.text.rfind("org_id - ") + 9
                org_cl = db.get_org(call.message.text[label:])

                inline_list = list()
                r = gdrive.drive_check_all(org_cl[0][20])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append([x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append([x['name'], "2" + x['id']])
                r = gdrive.drive_check_all(org_cl[0][21])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append([x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append([x['name'], "2" + x['id']])
                r = gdrive.drive_check_all(org_cl[0][22])
                for x in r['files']:
                    if "plain" in x['mimeType']:
                        inline_list.append([x['name'], "1" + x['id']])
                    elif "document" in x['mimeType']:
                        inline_list.append([x['name'], "2" + x['id']])

                markup = menu.inline_list2(inline_list, "worker_list3")
                if len(inline_list) > 0:
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                          text="Какой документ тебе отправить?", reply_markup=markup)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Нет документов",
                                          reply_markup=markup)

            if call.data[:13] == "worker_list3=":
                markup = menu.markup(menu.mainmenu)
                if call.data[13] == "1":
                    answer = "https://drive.google.com/file/d/" + call.data[14:]
                elif call.data[13] == "2":
                    answer = "https://docs.google.com/document/d/" + call.data[14:]
                bot.send_message(chat_id, answer, reply_markup=markup)

            if call.data[:11] == "3orgs_list=":
                user_cl = db.get_user(call.data[11:], "stop")
                if user_cl != "stop":
                    org_cl = db.get_org(call.data[11:])
                    inline_list = db.get_works(str(org_cl[0][0]))
                    markup = menu.inline_list(inline_list, "worker_list4")
                    if len(inline_list) > 0:
                        answer = "Вот какие сотрудники есть в этой компании.\nВыбран: " + str(
                            org_cl[0][5]) + "\norg_id - " + str(org_cl[0][1])
                    else:
                        answer = "Нет сотрудников"
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                          reply_markup=markup)

            if call.data[:13] == "worker_list4=":
                worker = db.get_worker2(call.data[13:])
                markup = menu.markup(menu.mainmenu)
                answer = answ.worker(worker)
                bot.send_message(chat_id, answer, reply_markup=markup)

            if call.data[:11] == "4orgs_list=":
                user_cl = db.get_user(call.data[11:], "stop")
                if user_cl != "stop":
                    org_cl = db.get_org(call.data[11:])
                    markup = menu.markup(menu.cancel)
                    bot.send_message(call.message.chat.id, answ.works1[1], reply_markup=markup)
                    bot.send_message(call.message.chat.id, answ.worksform6[0], reply_markup=markup)
                    db.upd_progress(user_id, "users", "4600")

                    db.upd_org(user_id, "users", "target2", org_cl[0][0])

            if call.data[:11] == "5orgs_list=":
                user_cl = db.get_user(call.data[11:], "stop")
                if user_cl != "stop":
                    org_cl = db.get_org(call.data[11:])
                    inline_list = db.get_works(str(org_cl[0][0]))
                    markup = menu.inline_list(inline_list, "worker_list5")
                    if len(inline_list) > 0:
                        answer = "Вот какие сотрудники есть в этой компании.\nВыбран: " + str(
                            org_cl[0][5]) + "\norg_id - " + str(org_cl[0][1])
                    else:
                        answer = "Нет сотрудников"
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                          reply_markup=markup)

            if call.data[:13] == "worker_list5=":
                # worker = db.get_worker2(call.data[13:])
                db.del_worker(call.data[13:])
                markup = menu.markup(menu.mainmenu)
                answer = "Сотрудник удалён из карточки компании"
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)
                bot.send_message(chat_id, "Не забудь уведомить об этом клиента", reply_markup=markup)

            if call.data[:11] == "6orgs_list=":
                user_cl = db.get_user(call.data[11:], "stop")
                if user_cl != "stop":
                    org_cl = db.get_org(call.data[11:])
                    inline_list = db.get_works(str(org_cl[0][0]))
                    markup = menu.inline_list(inline_list, "worker_list6")
                    if len(inline_list) > 0:
                        answer = "Вот какие сотрудники есть в этой компании.\nВыбран: " + str(org_cl[0][5])
                    else:
                        answer = "Нет сотрудников"
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                          reply_markup=markup)

            if call.data[:11] == "7orgs_list=":
                user_cl = db.get_user(call.data[11:], "stop")
                if user_cl != "stop":
                    org_cl = db.get_org(call.data[11:])
                    db.upd_org(user_id, "users", "target1", call.data[11:])

                    markup = menu.inline_list2(menu.nalogi_1, "nalogi_list6")
                    # markup = menu.inline_list(inline_list, "worker_list6")

                    answer = "Отчёт для какого налогового органа ты загружаешь?"
                    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                          reply_markup=markup)

            if call.data == "nalogi_list6=FNS":
                answer = "Загружаю отчёт для ФНС:"
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)
            if call.data == "nalogi_list6=FSR":
                answer = "Загружаю отчёт для СФР:"
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)
            if call.data == "nalogi_list6=FSS":
                answer = "Загружаю отчёт для ФСС:"
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)

            if call.data[:13] == "worker_list6=":
                worker = db.get_worker2(call.data[13:])
                markup = menu.inline_list2(menu.works3, "assistant_worker_change")
                label = call.message.text.rfind("Выбран")
                db.upd_org(user_id, "users", "target1", call.data[13:])
                answer = "Что ты хочешь поменять?\n" + call.message.text[label:] + "\nСотрудник: " + str(worker[0][5])
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=markup)

            if call.data == "assistant_worker_change=okl":
                markup = menu.markup(menu.cancel)
                label = call.message.text.rfind("Выбран")
                answer = "Какой месячный оклад ты хочешь установить для этого сотрудника?\n" + call.message.text[label:]
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)

                label = call.message.text.rfind("worker_id") + 11

                db.upd_progress(user_id, "users", "4001")

            if call.data == "assistant_worker_change=dat":
                markup = menu.markup(menu.cancel2)
                label = call.message.text.rfind("Выбран")
                answer = "Какие данные ты хочешь поменять?\n" + call.message.text[label:]
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)
                bot.send_message(call.message.chat.id, answ.worksform6[0], reply_markup=markup)

                label = call.message.text.rfind("worker_id") + 11

                db.upd_progress(user_id, "users", "4050")

            if call.data == "assistant_worker_change=sta":
                markup = menu.markup(menu.cancel)
                label = call.message.text.rfind("Выбран")
                answer = "Какую должность теперь занимает этот сотрудник?\n" + call.message.text[label:]
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=answer,
                                      reply_markup=None)

                label = call.message.text.rfind("worker_id") + 11

                db.upd_progress(user_id, "users", "4003")

    except:
        err = traceback.format_exc().replace('"', '')
        err = err.replace("'", "")
        print(err)
        bot.send_message(call.message.chat.id, "Ошибка", reply_markup=None)
        command = call.message.from_user.username + " - " + str(call.message.chat.id) + " - start"
        db.add_log(command, err)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:

        user_id = str(message.from_user.id)

        user = db.get_user(user_id, "stop")
        if user[0][7] != "assistant":
            if user != 'stop' and user[0][8] >= 40 and user[0][8] <= 48:
                org = db.get_org(user_id)

                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = os.path.abspath(__file__)[:-7] + 'files\\' + user_id + "\\" + message.document.file_name
                try:
                    with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                        new_file.close()
                except:
                    os.mkdir(os.path.abspath(__file__)[:-7] + 'files\\' + user_id)
                    with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                        new_file.close()

                folder_id = org[0][20]
                if user[0][8] != 41 and user[0][8] != 47:
                    folder_id = org[0][22]
                elif user[0][8] == 41:
                    folder_id = org[0][21]
                elif user[0][8] == 47:
                    folder_id = org[0][20]
                gdrive.drive_upload(src, message.document.file_name, folder_id)

                answer = "Клиент " + org[0][5] + " загрузил на диск " + menu.d_1c[user[0][8] - 40]
                db.upd_progress(user_id, "users", "1")

                bot.send_message(config.assists_chat, answer, reply_markup=None)
                markup = menu.markup(menu.mainmenu)
                bot.reply_to(message, "Получено", reply_markup=markup)

        # bot.send_document(message.chat.id, bot.get_file(message.document.file_id))
        # bot.forward_message(message.chat.id, message.chat.id, message.id)

        if user[0][7] == "assistant":
            if message.reply_to_message:
                reply_text = message.reply_to_message.text
                # print(reply_text)
                if "act=" in reply_text[-30:]:
                    label = reply_text.find("user: ", -30) + 6
                    user_ids = reply_text[label:]
                    if "act=4" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=5" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=6" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=7" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=8" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=9" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=10" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=11" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)
                    elif "act=12" in reply_text[-30:]:
                        bot.reply_to(message, "Получено")
                        bot.forward_message(user_ids, message.chat.id, message.id)

                elif "запросил выгрузку из 1С" in reply_text:
                    label = reply_text.find("user: ", -30) + 6
                    user_ids = reply_text[label:]
                    bot.reply_to(message, "Получено")
                    bot.forward_message(user_ids, message.chat.id, message.id)
                    # user_cl = db.get_user(user_ids, "stop")
                    # if user_cl != "stop":
                    #     org_cl = db.get_org(user_id)
                    #     bot.forward_message(message.chat.id, message.chat.id, message.id)

                elif "Загружаю отчёт для " in reply_text:
                    user = db.get_user(user_id, "stop")
                    org = db.get_org(user[0][10])
                    folder_id = ""

                    file_info = bot.get_file(message.document.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)

                    src = os.path.abspath(__file__)[:-7] + 'files\\' + user_id + "\\" + message.document.file_name
                    try:
                        with open(src, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            new_file.close()
                    except:
                        os.mkdir(os.path.abspath(__file__)[:-7] + 'files\\' + user_id)
                        with open(src, 'wb') as new_file:
                            new_file.write(downloaded_file)
                            new_file.close()

                    if "ФНС" in reply_text:
                        folder_id = org[0][24]
                    if "СФР" in reply_text:
                        folder_id = org[0][25]
                    if "ФСС" in reply_text:
                        folder_id = org[0][26]

                    gdrive.drive_upload(src, message.document.file_name, folder_id)

                    answer = "Загружен" + reply_text[8:-1]
                    db.upd_progress(user_id, "users", "1")

                    bot.send_message(org[0][1], answer, reply_markup=None)
                    markup = menu.markup(menu.mainmenu)
                    bot.reply_to(message, "Получено", reply_markup=markup)


    except:
        err = traceback.format_exc().replace('"', '')
        err = err.replace("'", "")
        print(err)
        bot.send_message(message.chat.id, "Ошибка", reply_markup=None)
        command = message.from_user.username + " - " + str(message.chat.id) + " - start"
        db.add_log(command, err)

    # if "act=2" in reply_text[-30:] or  "act=3" in reply_text[-30:]:
    #     label = reply_text.find("user: ", -30) + 6
    #     # print(reply_text[label:])
    #     # print("requests_bot[label:]")
    #     user_ids = reply_text[label:]
    #     bot.send_message(user_ids, message.text)


def generate_token_for_accountant(message: types.Message):
    pass


bot.polling(none_stop=True)
