import MySQLdb
import socket
import sys
import threading
import marshal
import select
import uuid
import hashlib

data=[]
def coneccion(sql):
    db = MySQLdb.connect(host="localhost",    # tu host, usualmente localhost
                     user="root",         # tu usuario
                     passwd="123456789",  # tu password
                     db="Users")        # el nombre de la base de datos
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    for row in cur.fetchall():
        global data
        data = [row[0]]
        print data
    return data
def conexiones(socket_cliente):
    peticion = marshal.loads(socket_cliente.recv(1024))
    print "[*] Mensaje recibido: %s" % peticion
    PASS = peticion[2]
    if peticion[0]=="A":
        PASS2= hash_password(PASS)
        querry = ("insert into users (login,hash) values ('{0}','{1}')".format(peticion[1],PASS2))
        coneccion(querry)
        tenviar=["Usuario y password almacenados"]
        enviar=marshal.dumps(tenviar)
        socket_cliente.send(enviar)
        socket_cliente.close()
    if peticion[0]=="V":
        querry=("select hash from users where login= '%s'"%peticion[1])
        consultarHash1=coneccion(querry)
        consultarHash=consultarHash1[0]
        if check_password(consultarHash, PASS):
            tenviar=["Password Verificado"]
            enviar=marshal.dumps(tenviar)
            socket_cliente.send(enviar)
        else:
            tenviar=["Password no se pudo verificar porque no coincide"]
            enviar=marshal.dumps(tenviar)
            socket_cliente.send(enviar)
        socket_cliente.close()

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    print password
    print salt
    print hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
if __name__ == "__main__":

    HOST = ''
    PORT = 8864
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        SERVER_SOCKET.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    SERVER_SOCKET.listen(10)
    print "[*] Esperando conexiones en %s:%d" % (HOST, PORT)
    while True:
        cliente, address = SERVER_SOCKET.accept()
        print "[*] Conexion establecida con %s:%d" % (address[0] , address[1])
        threading.Thread(target=conexiones, args=(cliente,)).start()
