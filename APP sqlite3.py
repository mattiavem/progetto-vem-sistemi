import sqlite3
import socket
import threading
import time

#IP computer locale
UDP_IP_ADDR = "192.168.179.60"
#Porta computer locale
UDP_PORT_NUMBER = 20006

ip_port_Data = (UDP_IP_ADDR, UDP_PORT_NUMBER)
   
def client_Receive_Data():
    print("Avvio THREAD Receive Data...")
    serversocket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket1.bind(("192.168.179.60", 20006))
    msgToSend = str.encode("DB_OK")
    
    #crea connessione al database
    connection = sqlite3.connect('lopro.db')
    cursor = connection.cursor()
        
    try:            
        while True:            
            data, address = serversocket1.recvfrom(1024)
            strData = bytes.decode(data).split(":")
         
            sql = """ INSERT INTO tbl_log(Temperatura, Umidita) VALUES ('{}', '{}');""".format(strData[0], strData[1])
            
            print(sql)
            
            cursor.execute(sql)
            connection.commit()

            #invia al device una risposta
            serversocket1.sendto(msgToSend, ip_port_Data)
            time.sleep(1)
    except:
        print("errore")
        msgToSend = str.encode("ERRORE")
        serversocket1.sendto(msgToSend, ip_port_Data)
        connection.close()

def crea_tabella():
    #una volta creata la tabella possiamo evitare di chiamare
    #questa funzione ad ogni esecuzione del programma
    #crea connessione al database
    connection = sqlite3.connect('lopro.db')
    cursor = connection.cursor()
 
    #Se esiste la tabella cancellala
    #cursor.execute("DROP TABLE IF EXISTS tbl_log")
 
    # Crea la tabella se non esiste
    table = """ CREATE TABLE IF NOT EXISTS tbl_log (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Temperatura VARCHAR(50) NOT NULL,
            Umidita VARCHAR(50) NOT NULL      
        ); """
 
    cursor.execute(table)
    cursor.close()
    connection.close()

 
def list_rows():
    print("list rows..")
    #crea connessione al database
    connection = sqlite3.connect('lopro.db')

    sql = """ SELECT * FROM tbl_log;"""

    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    # Close the connection
    connection.close()

if __name__=="__main__":
    
    print("Start program")
    t1 = threading.Thread(target=client_Receive_Data)
    t1.start()