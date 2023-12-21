import os
import sys
import psycopg2
from psycopg2 import sql, OperationalError, errorcodes, errors
from app import user, pwd
def print_postgresql_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    
def connect(usr, pwd):
    try:
        conn = psycopg2.connect(
                host="localhost",
                database="cyberdefender",
                user=usr,
                password=pwd)
    except OperationalError as err:
        print_postgresql_exception(err)
        conn = None
    return conn

def create_table():
    conn = connect(user, pwd)
    if conn != None:
        
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(table_name) FROM information_schema.tables WHERE table_name = 'grupos_telegram';")
            
        except Exception as err:
            print_postgresql_exception(err)
            conn.rollback()

        if cur.fetchone()[0] == 0:
            try:    
                cur.execute('CREATE TABLE grupos_telegram (id_grupo bigint PRIMARY KEY, '
                                            'ids_responsables bigint[]);'
                                            )
            except Exception as err:
                print_postgresql_exception(err)
                conn.rollback()

        conn.commit()

        cur.close()
        conn.close()
    
#returns a list with the responsibles and the   
def get_responsibles(chatId):
    conn = connect(user, pwd)
    if conn != None:
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT ids_responsables FROM grupos_telegram WHERE id_grupo = (%s);",(chatId,))
        except Exception as err:
            print_postgresql_exception(err)
            conn.rollback()
        
        conn.commit()
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result

        
        
        
            
#registers a list of chats with a list of responsibles
def register(chatId, responsible_list):
        
    conn = connect(user, pwd)   
    if conn!= None:
        cur = conn.cursor()
        for id in chatId:
            try:
                
                cur.execute("SELECT COUNT(id_grupo) FROM grupos_telegram WHERE id_grupo = (%s);", (id))
                
                # if the group hasn't been registered yet, a new row is inserted into the table with the new id
                if cur.fetchone()[0] == 0:
                    try:
                        cur.execute("INSERT INTO grupos_telegram(id_grupo, ids_responsables) VALUES((%s), (%s));", (id, responsible_list))
                    except Exception as err:
                        print_postgresql_exception(err)
                        conn.rollback()
                
                # if the group is already registered, we obtain the list of responsibles associated and add the new responsibles to the list
                else:
                    try:
                        cur.execute("SELECT ids_responsables FROM grupos_telegram WHERE id_grupo = (%s);", (id,))
                    except Exception as err:
                        print_postgresql_exception(err)
                        conn.rollback()
                    current_list = cur.fetchone()[0]
                    current_list.extend(responsible_list)
                    current_list = list(dict.fromkeys(current_list))
                    try:
                        cur.execute("UPDATE grupos_telegram SET ids_responsables = (%s) WHERE id_grupo = (%s);", (current_list, id))
                    except Exception as err:
                        print_postgresql_exception(err)
                        conn.rollback()
                    

            except Exception as err:
                print_postgresql_exception(err)
                conn.rollback()

            conn.commit()

        cur.close()
        conn.close()
        #ver si retornar algo
    