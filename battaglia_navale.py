import pygame
import pygame_utilities
import threading
import time
import clienteBattagliaNavale
    

def aspetta(conn,mossa):
    temp=conn.aspettaMossa()
    mossa[0]=temp

    

def getPosizioniNavi(listaCaselle,nave1,nave2,nave3,nave4,nave5):
    listaPos=[]
    for i in range(len(listaCaselle)):
        for j in range(len(listaCaselle[i])):
            if(listaCaselle[i][j].rect.colliderect(nave1.rect)):
                listaPos.append((i,j))
            if(listaCaselle[i][j].rect.colliderect(nave2.rect)):
               listaPos.append((i,j))
            if(listaCaselle[i][j].rect.colliderect(nave3.rect)):
               listaPos.append((i,j))
            if(listaCaselle[i][j].rect.colliderect(nave4.rect)):
               listaPos.append((i,j))
            if(listaCaselle[i][j].rect.colliderect(nave5.rect)):
               listaPos.append((i,j))
    return listaPos
pygame.init()
#altezza e larghezza finestra
info=pygame.display.Info()
SCREEN_HEIGHT,SCREEN_WIDTH=info.current_h-100,info.current_w-100

#istanzio la finestra
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('battaglia navale')

#carico e allargo l'immagine per lo sfondo
bg_img = pygame.image.load('bg_battagliaNavale.jpg')
bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH+1500,SCREEN_HEIGHT+1500))


#font per le scrite
fontTitle=pygame.font.SysFont("Arial", 60)
font_style=pygame.font.SysFont("Arial", 50)

#scritte
inizioImg = font_style.render('Inizia partita', True, (0,0,0))
inizio=pygame_utilities.Button(SCREEN_WIDTH*0.4,SCREEN_HEIGHT/2,inizioImg)

esciImg = font_style.render('Esci', True, (0,0,0))
esci=pygame_utilities.Button(SCREEN_WIDTH*0.45,SCREEN_HEIGHT/3*2,esciImg)

esciImg2 = font_style.render('Esci', True, (0,0,0))
esci2=pygame_utilities.Button(SCREEN_WIDTH*0.9,SCREEN_HEIGHT*0.9,esciImg)

iniziaImg = font_style.render('Inizia',True,(0,0,0))
iniz=pygame_utilities.Button(SCREEN_WIDTH*0.9,SCREEN_HEIGHT*0.8,iniziaImg)



#variabili per il main loop
inGame=False
inPrep=False
ready=False
turno=False
run=True
flag=True
campoMandato=False
mossa=[]
tuplav=(),(),()
mossa.append(())
ris=[]
ris.append(tuplav)
ris2=[]
ris2.append(tuplav)
fine=False
#vettore caselle
lista_caselle=[] 

#creo la connessione con il server

conn=clienteBattagliaNavale.connessione()

#costante per la posizione delle caselle
CONST_POS=60

#creo la griglia di caselle
for i in range(10):
    lista_caselle.append([])
    for j in range(10):
        lista_caselle[i].append(pygame_utilities.box(SCREEN_WIDTH*0.35+j*CONST_POS,SCREEN_HEIGHT*0.3+i*CONST_POS,60))


#immagini navi

nave1 = pygame.image.load('boat1.png').convert_alpha()
nave1X,nave1Y=nave1.get_size()
nave1 = pygame.transform.scale(nave1, (nave1X/2 ,nave1Y/2))


nave2 = pygame.image.load('boat2.png').convert_alpha()
nave2X,nave2Y=nave2.get_size()
nave2 = pygame.transform.scale(nave2, (nave2X ,nave2Y))

nave3 = pygame.transform.scale(nave2, (nave2X*0.75,nave2Y))

nave4 = pygame.transform.scale(nave2, (nave2X ,nave2Y))

nave5 = pygame.transform.scale(nave2, (nave2X*0.75,nave2Y))
#oggetti navi

boat1=pygame_utilities.nave(SCREEN_WIDTH*0.1,SCREEN_HEIGHT*0.2,nave1,lista_caselle)
boat2=pygame_utilities.nave(SCREEN_WIDTH*0.1,SCREEN_HEIGHT*0.3,nave2,lista_caselle)
boat3=pygame_utilities.nave(SCREEN_WIDTH*0.1,SCREEN_HEIGHT*0.4,nave3,lista_caselle)
boat4=pygame_utilities.nave(SCREEN_WIDTH*0.1,SCREEN_HEIGHT*0.5,nave2,lista_caselle)
boat5=pygame_utilities.nave(SCREEN_WIDTH*0.1,SCREEN_HEIGHT*0.6,nave3,lista_caselle)

turno=conn.getTurno()

#main loop
while(run):
    screen.blit(bg_img,(i,0))
    #finchè l'utente non sta giocando:
    if(not inPrep and not fine):
        #metto a schermo la finestra di benvenuto
        pygame_utilities.draw_text("Benvenuto su battaglia navale!",fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.2,screen)
        #metto a schermo un bottone per iniziare la partita
        if(inizio.drawWithBorder(screen)):
            inPrep=True
        #pulsante uscita gioco
        if(esci.drawWithBorder(screen)):
            run=False


   #se l'utente è in preparazionepr
    if(inPrep and not inGame and not fine):
        #metto a schermo la tabella delle caselle
        ready=True
        if(not boat1.draw(screen,inPrep)):
            ready=False
        if(not boat2.draw(screen,inPrep)):
            ready=False
        if(not boat3.draw(screen,inPrep)):
            ready=False
        if(not boat4.draw(screen,inPrep)):
            ready=False
        if(not boat5.draw(screen,inPrep)):
            ready=False
        if(esci2.drawWithBorder(screen)):
            run=False
        if(iniz.drawWithBorder(screen) and ready):
            inGame=True
        pygame_utilities.draw_text('metti le navi in posizione e premi inizia',font_style,(0,0,0),SCREEN_WIDTH*0.325,SCREEN_HEIGHT*0.1,screen)
        for i in range (10):
            for j in range(10):
                lista_caselle[i][j].draw(screen)
        
    if(not campoMandato and inGame):
        conn.mandaPosizioniNavi(getPosizioniNavi(lista_caselle,boat1,boat2,boat3,boat4,boat5))
        campoMandato=True

    if(inGame):
        if(turno=='t'):
            pygame_utilities.draw_text("scegli una casella da bombardare",fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.1,screen)
            for i in range (10):
                for j in range(10):
                    lista_caselle[i][j].draw(screen)
    
            if(ris[0]==()):
                pass
            elif(ris[0][0] == 't'):
                pygame_utilities.draw_text('sei stato colpito in '+str(ris[0][1]),fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.2,screen)
            elif(ris[0][0] == 'f'):
                pygame_utilities.draw_text('l\'avversario ha mancato',fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.2,screen)
            if(mossa[0]==()):
                pos=pygame.mouse.get_pos()
                for i in range(len(lista_caselle)):
                    for j in range(len(lista_caselle[i])):
                        if lista_caselle[i][j].rect.collidepoint(pos):
                                if pygame.mouse.get_pressed()[0] == True and mossa[0]==():
                                    mossa[0]=(i,j)
                                    conn.mandaMossa(mossa)
                                    turno='f'

            if(mossa[0]!=()):
                ris2[0]=conn.aspettaMossa()
                mossa[0]=()

        else:
            
            pygame_utilities.draw_text("Aspetta che l'avversario faccia una mossa",fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.2,screen)
            if ris2[0]==():
                pass
            elif ris2[0][0]=='t':
                pygame_utilities.draw_text("hai centrato una nave in"+str(ris2[0][1]),fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.3,screen)
            elif ris2[0][0]=='f':
                pygame_utilities.draw_text("hai mancato",fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.3,screen)
            if flag:
                thA=threading.Thread(target=aspetta,args=(conn,mossa))
                thA.start()
                flag=False     
            
            if not thA.is_alive():
                thA.join()
                ris=mossa[:]
                print(ris)     
                mossa[0]=()
                flag=True
                turno='t'
                print(ris)
    #controllo se l'utente chiude la finestra
    if(ris[0]==()):
        pass
    elif(ris[0][2]=='p'):
        inGame=False
        fine=True
        pygame_utilities.draw_text("hai perso",fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.3,screen)
    elif(ris2[0][2]=='v'):
         inGame=False
         fine=True
         pygame_utilities.draw_text("hai vinto",fontTitle,(0,0,0),SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.3,screen)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run=False

    #update della finestra
    pygame.display.update()




pygame.quit()