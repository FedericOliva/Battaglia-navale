import socket
import facilities
import random
import threading as th
import time

def inGame(player,current,lock):
    ris1='n'
    ris2='n'
    while(True):
        time.sleep(0.1)
        with lock:
            if player[current][2]:
                mossa=facilities.bytes_to_list(player[current][0].recv(1024))
                print(mossa)
                hitted=controllaMossa(player,current,mossa)
                if(len(player[current-1][1])==0):
                    ris1='v'
                    ris2='p'
                player[current][0].send(facilities.tuple_to_bytes((hitted,mossa,ris1)))

                
                player[current-1][0].send(facilities.tuple_to_bytes((hitted,mossa,ris2)))
                player[current][2]=not player[current][2]
                player[current-1][2]=not player[current][2]

def controllaMossa(player,current,mossa):
    for pos in player[current-1][1]:
        if(pos==mossa[0]):
            player[current-1][1].remove(pos)
            print(player[current-1][1])
            return 't'
    return 'f'


host="localhost"
porta=50003
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,porta))
s.listen(2)
p1Turn=bool(random.getrandbits(1))
p2Turn=not p1Turn
conn,addr=s.accept()
print('connessione 1 avviata')
if(p1Turn):t='t'
else:t='f'
conn.send(t.encode())
conn2,addr2=s.accept()
print('connessione 2 avviata')
if(p2Turn):t='t'
else:t='f'
conn2.send(t.encode())

player=[]

temp=conn.recv(1024)
p1Navi=facilities.bytes_to_list(temp)

temp=conn2.recv(1024)
p2Navi=facilities.bytes_to_list(temp)

player.append([conn,p1Navi,p1Turn])
player.append([conn2,p2Navi,p2Turn])

lock=th.Lock()

th1=th.Thread(target=inGame,args=(player,0,lock))
th2=th.Thread(target=inGame,args=(player,1,lock))


th1.start()
th2.start()

th1.join()
th2.join()
