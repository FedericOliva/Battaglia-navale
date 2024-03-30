import socket
import facilities

class connessione:
    def __init__(self):
        host="localhost"
        porta=50003
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self.s.connect((host,porta))

    def mandaPosizioniNavi(self,posizioni):
        posB=facilities.list_to_bytes(posizioni)
        self.s.send(posB)
    
    def aspettaMossa(self, ):
        data=self.s.recv(1024)
        return facilities.bytes_to_tuple(data)
    
    def getTurno(self):
        return self.s.recv(1024).decode()
    
    def mandaMossa(self,mossa):
        self.s.send(facilities.list_to_bytes(mossa))
