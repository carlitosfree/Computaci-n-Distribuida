import socket
import sys
import select
import marshal

if __name__=="__main__":
    if len(sys.argv)<6:
        #Tipo se refiere si quiere almacenar el usuario y la contrasenia 
        #O si quiere verificar una ya registrada
        print ('Usage: python Cliente.py IP PORT TIPO USUARIO PASSWORD')
        sys.exit()
    HOST= sys.argv[1]
    PORT= int(sys.argv[2])
    LOGIN=sys.argv[4]
    PASSWORD=sys.argv[5]
    TIPO=sys.argv[3]
    CLIENT= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        CLIENT.connect((HOST,PORT))
    except socket.error as msg:
        print('Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    enviar=[]
    enviarSerializado=[TIPO,LOGIN,PASSWORD]
    enviar=marshal.dumps(enviarSerializado)
    CLIENT.send(enviar)
    respuesta= marshal.loads(CLIENT.recv(4096))
    print respuesta[0]
    CLIENT.close()
