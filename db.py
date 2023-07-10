
from mysql.connector import connect
import config

#path_bot = config.path_bot
#if path_bot[-1] != "/":
    #path_bot += "/"

db_host = config.host_db
db_login = config.login_db
db_pass = config.password_db
db_name = config.database_name


def rec(record):
    resp = 0
    with connect(
        host=db_host,
        # port=3306,
        user=db_login,
        password=db_pass,
        database=db_name,
    ) as connection:

        with connection.cursor(buffered=True) as cursor:
            cursor.execute(record)
            connection.commit()
            if record[:6] == "SELECT":
                resp = cursor.fetchall()
    return resp


def get_user(user_id, user_name):
    record = "SELECT * FROM `users` WHERE `user_id` LIKE '" + user_id + "'"
    resp = rec(record)
    if len(resp) == 0 and user_name != 'stop':
        record = "INSERT INTO `users` (`user_id`, `user_name`) VALUES ('" + user_id + "', '" + user_name + "');"
        rec(record)
        
        return [(0, user_name, user_id, "Not", 0, "0", "0", 'user', 0)]
    elif len(resp) == 0 and user_name == 'stop':
        return 'stop'
    else:
        return resp
    

def get_org(user_id):
    record = "SELECT * FROM `organizations` WHERE `user_id` LIKE '" + user_id + "'"
    resp = rec(record)
    if len(resp) == 0:
        record = "INSERT INTO `organizations` (`user_id`) VALUES ('" + user_id + "');"
        rec(record)
        
        return [(0, user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
    else:
        return resp


def get_org_all():
    record = "SELECT * FROM `organizations` WHERE 1"
    resp = rec(record)
    return resp
    
def get_works(org_id):
    record = "SELECT * FROM `workers` WHERE `org_id` LIKE " + org_id + ";"
    resp = rec(record)
    return resp
    
def get_work(worker_id):
    record = "SELECT * FROM `workers` WHERE `id` LIKE " + worker_id + ";"
    resp = rec(record)
    return resp
    
def upd_org(user_id, table, field, val):
    record = "UPDATE `" + table + "` SET `" + field + "` = '" + str(val) + "' WHERE `user_id` = '" + str(user_id) + "';"
    # print(record)
    rec(record)

def upd_progress(user_id, table, val):
    record = "UPDATE `" + table + "` SET `progress` = " + str(val) + " WHERE `user_id` = '" + str(user_id) + "';"
    # print(record)
    rec(record)


def add_worker(org, form_list6):
    # del form_list6[0]
    orgs = ""
    try:
        orgs = int(org)
    except:
        orgs = org[0][0]
    record = "INSERT INTO `workers` (`id`, `org_id`, `date_add`, `date_upd`, `active`, `name`, `jtitle`, `bet_size`, `jlocation`, `salary`, `date`, `passport_s_num`, `passport_who`, `division_code`, `adress`, `snils`, `inn`, `date_birth`, `employment_history`, `current_account`, `correspondent_account`, `bik_bank`) VALUES (NULL, '" + str(orgs) + "', current_timestamp(), current_timestamp(), '1', '" + str(form_list6[0]) + "', '" + form_list6[1] + "', '" + form_list6[2] + "', '" + form_list6[3] + "', '" + form_list6[4] + "', '" + form_list6[5] + "', '" + form_list6[6] + "', '" + form_list6[7] + "', '" + form_list6[8] + "', '" + form_list6[9] + "', '" + form_list6[10] + "', '" + form_list6[11] + "', '" + form_list6[12] + "', '" + form_list6[13] + "', '" + form_list6[14] + "', '" + form_list6[15] + "', '" + form_list6[16] + "');"
    # print(record)
    rec(record)

def upd_worker(user_id, val):
    # record = "UPDATE `workers` SET `name` = " + val[0] + ", `passport_s_num` = " + val[1] + ", `passport_who` = " + val[2] + ", `division_code` = " + val[3] + ", `adress` = " + val[4] + ", `snils` = " + val[5] + ", `inn` = " + val[6] + ", `current_account` = " + val[7] + ", `correspondent_account` = " + val[8] + ", `bik_bank` = " + val[9] + " WHERE `org_id` = '" + user_id + "';"
    
    record = "UPDATE `workers` SET `name` = '" + val[0] + "', `passport_s_num` = '" + val[1] + "', `passport_who` = '" + val[2] + "', `division_code` = '" + val[3] + "', `adress` = '" + val[4] + "', `snils` = '" + val[5] + "', `inn` = '" + val[6] + "', `current_account` = '" + val[7] + "', `correspondent_account` = '" + val[8] + "', `bik_bank` = '" + val[9] + "' WHERE `org_id` = '" + user_id + "';"
    # print(record)
    rec(record)
    
def upd_worker02(user_id, val):
    # print(val)
    record = "UPDATE `workers` SET `name` = '" + val[0] + "', `passport_s_num` = '" + val[1] + "', `passport_who` = '" + val[2] + "', `division_code` = '" + val[3] + "', `adress` = '" + val[4] + "', `snils` = '" + val[5] + "', `inn` = '" + val[6] + "', `current_account` = '" + val[7] + "', `correspondent_account` = '" + val[8] + "', `bik_bank` = '" + val[9] + "' WHERE `id` = '" + user_id + "';"
    # print(record)
    rec(record)

def upd_worker2(user_id, table, field, val):
    record = "UPDATE `" + table + "` SET `" + field + "` = '" + str(val) + "' WHERE `id` = '" + str(user_id) + "';"
    # print(record)
    rec(record)

def del_worker(user_id):
    record = "DELETE FROM `workers` WHERE `id` = " + user_id + ";"
    # print(record)
    rec(record)

def get_worker2(user_id):
    record = "SELECT * FROM `workers` WHERE `id` = " + str(user_id) + ";"
    # print(record)
    resp = rec(record)
    return resp

def add_log(command, err):
    record = "INSERT INTO `logs` (`id`, `date`, `command`, `errs`) VALUES (NULL, current_timestamp(), '" + command + "', '" + str(err) + "');"
    rec(record)

# INSERT INTO `workers` (`id`, `date_add`, `date_upd`, `active`, `name`, `jtitle`, `bet_size`, `jlocation`, `salary`, `date`, `passport_s_num`, `passport_who`, `division_code`, `adress`, `snils`, `inn`, `date_birth`, `employment_history`, `current_account`, `correspondent_account`, `bik_bank`) VALUES (NULL, current_timestamp(), current_timestamp(), '1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);


def get_usersdfg(user_id, user_name):
    record = "SELECT * FROM `users` WHERE `user_id` LIKE '" + user_id + "'"
    resp = rec(record)
    if len(resp) == 0:
        record = "INSERT INTO `users` (`id`, `user_name`, `user_id`, `class`) VALUES (NULL, '" + user_name + "', '" + user_id + "', 'member');"
        rec(record)
        
        return [(0, user_name, user_id, 0, 0, 0, 'member')]
    else:
        return resp

def wr_mess(chat_name, user_name, user_id, chat_id, message_id, links, text, keywords):
    record = "INSERT INTO `messages_log` (`id`, `date`, `chat_name`, `user_name`, `user_id`, `chat_id`, `message_id`, `links`, `text`, `keywords`) VALUES (NULL, current_timestamp(), '" + chat_name + "', '" + user_name + "', '" + user_id + "', '" + chat_id + "', '" + message_id + "', '" + links + "', '" + text + "', '" + keywords + "');"
    # print(record)
    rec(record)

def add_admin(user_id):
    record = "UPDATE `users` SET `class` = 'admin' WHERE `user_id` = '" + user_id + "';"
    # print(record)
    rec(record)