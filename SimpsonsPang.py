import simplegui
import random
import math

#Variables globales

anP = 800 # Ancho Pantalla
alP = 600 # Alto Pantalla
VELOCIDAD = 5
VELOCIDAD_DISPARO = 6
VELOCIDAD_DONUT = 5
ACELERACION = .6
DIVISIONES = 2
TIEMPO = 5000
GRAVEDAD = .04
NUEVO_DONUT = 5000
INVULNERABLE = 100

VIDAS_TOTALES = 3

VIDAS = 3
PUNTOS = 0
FIN_JUEGO = False

lista_donuts = []
lista_disparos = []
tiempoPasado = 0


#CLASES

class Homer:

    pos =[0,0]
    tam = (0,0) 
    radio = 60
    
    imgI = None
    imgD = None
    imgE = None
 
    mov = 'quieto'
    vel = 0
    
    def __init__(self,imgI,imgD,imgE,pos,tam,vel):
 
        self.imgI = imgI
        self.imgD = imgD
        self.imgE = imgE
        self.tam = tam
        self.pos = [pos[0],pos[1]]
        self.vel = vel
        
        self.radio = 5
 
    def get_radio(self):
        
        return self.radio
    
    def get_posicion(self):
        
        return self.pos
 
    def update(self):
 
        if self.mov == 'izq':
            self.pos[0] -= self.vel
 
        elif self.mov == 'der':           
            self.pos[0] += self.vel
 
        if (self.pos[0] - self.tam[0]/2) < 0:
            self.pos[0] = self.tam[0]/2
            
        elif (self.pos[0] + self.tam[0]/2) > anP:
            self.pos[0] = anP - self.tam[0]/2
 
    def dibujar(self,canvas):
 
        self.update()

        if self.mov == 'izq':
            self.imgI.dibujar(canvas,self.pos,self.tam)
            
        elif self.mov == 'der':
            self.imgD.dibujar(canvas,self.pos,self.tam)
            
        else:
            self.imgE.dibujar(canvas,self.pos,(self.tam[0]-25,self.tam[1]))
 
    def movimiento(self,movimiento):
 
        self.mov = movimiento
        
       
    
class Donut:
    
    pos = [0,0]
    vel = [0,0]
    imagen = None
    tam = (0,0)
    radio = 0
    divisiones = 0
 
    def __init__(self, imagen, pos, tam, vel, divisiones = 0):
 
        self.pos = [pos[0],pos[1]]
        self.tam = tam
        self.vel = [vel[0],vel[1]]
        self.imagen = imagen
        self.radio = self.tam[0]/2
 #para ver si debe o no volver a dividirse
        self.divisiones = divisiones
 #conseguimos que la altura alcanzada este en funcion del tama�o del donut
        self.aceleracion = ACELERACION * (divisiones+1)
 
 #Para el calculo de colisiones 
 
    def get_radio(self):
        return self.radio
 #Para el calculo de colisiones
    def get_posicion(self):
        return self.pos

    def update(self): 
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[1] += GRAVEDAD
        self.rebote()
        

    def rebote(self): 
        if self.pos[1] >= alP-self.radio:
            

            self.vel[1] = -VELOCIDAD_DONUT - self.aceleracion
            
        elif self.pos[0] >= anP-self.radio:
            
            self.vel[0] = -self.vel[0]
            
        elif self.pos[0] <= self.radio:
            
            self.vel[0] = -self.vel[0]
        

    def dibujar(self, canvas):
        self.imagen.dibujar(canvas,self.pos,self.tam)
        
        
class Disparo:
    imagen = None
    pos = [0,0]
    tam = (0,0)
    vel = 0
    radio = 0
 
    def __init__(self, imagen, pos, tam, vel):

        self.pos = [pos[0],pos[1]]
        self.vel = vel
        self.imagen = imagen
        self.tam = tam
 #igual que en los casos anteriores, o lo pasamos por parametros o lo calculamos 
 #en funcion del tama�o de la imagen
 
        self.radio = 5
            
          #Para lagestion delascolisiones
 
    def get_radio(self):
 
        return self.radio
 
    def get_posicion(self):
        
        return self.pos
 
    def dibujar(self, canvas):

        self.imagen.dibujar(canvas,self.pos,self.tam)
 
#actualizamos la posicion, no necesitamos rebotes, al llegar a la parte superior de 
#la pantalla devolvemos True para eliminar el objeto de la lista de disparos
 
    def update(self):

        self.pos[1]-=self.vel
        
        if self.pos[1] == 0 :
            return True

        return False
        
               
class Imagen:
    tamanio = None
    centro = None
    img = None
    angulo = None
    
    def __init__(self,img,tamanio,centro,angulo = 0):
        self.img = img
        self.tamanio = tamanio
        self.centro = centro
        self.angulo = angulo
    
    def get_tamanio(self):
        return self.tamanio
    
    def set_tamanio(self,tamanio):
        self.tamanio = tamanio
    
    def get_centro(self):
        return self.centro
    
    def set_centro(self,centro):
        self.centro = centro
    
    def dibujar(self,canvas,pos,tam):
        canvas.draw_image(self.img,self.centro,self.tamanio,pos,tam,self.angulo)

#Funciones Auxiliares

def actualizarDonuts():
    
    global PUNTOS,tiempoPasado,INVULNERABLE
    
    if tiempoPasado<=INVULNERABLE:
        tiempoPasado+=1
    
    for i in range (len(lista_donuts)):	

        Actualizar = True
            
        lista_donuts[i].update()
        
        if colision(homer.pos,homer.radio,lista_donuts[i].pos,lista_donuts[i].radio):
            
            if(INVULNERABLE<tiempoPasado):
                lista_donuts.remove(lista_donuts[i])
                print "ouch"
                homerTocado()
                break
            
        else:
            
           for j in range (len(lista_disparos)):
                
               if colision(lista_disparos[j].pos,lista_disparos[j].radio,lista_donuts[i].pos,lista_donuts[i].radio): 
                    
                    PUNTOS+=1
                    
                    if lista_donuts[i].divisiones<DIVISIONES:
                        
                        nuevoDonut (lista_donuts[i].pos,(-1,-1),(lista_donuts[i].radio,lista_donuts[i].radio),lista_donuts[i].divisiones+1)
                        nuevoDonut (lista_donuts[i].pos,(1,-1),(lista_donuts[i].radio,lista_donuts[i].radio),lista_donuts[i].divisiones+1)                        
                        
                    lista_donuts.remove(lista_donuts[i])
                    lista_disparos.remove(lista_disparos[j])
                    Actualizar = False
                    break
        
        if Actualizar==False:
            break
        
        
def nuevoDonut (posicion,velocidad,tamanno,divisiones):
    
    global PUNTOS, lista_donuts
    lista_donuts.append(Donut(donut1,posicion,tamanno,velocidad,divisiones))

    
def donut_aleatorios():

    nuevoDonut((random.randrange(40, anP-40),random.randrange(40, alP/2)),(random.randrange(-3,3),0),(80,80),0)
    
def nuevoDisparo():
    
    lista_disparos.append(Disparo(disparoRojo1,(homer.pos[0],alP-90),(10,10),VELOCIDAD_DISPARO))
    
def actualizarDisparo():

    
    
    for i in range (len(lista_disparos)):	
       
        
        if lista_disparos[i].update():
            
            lista_disparos.remove(lista_disparos[i])
            break

def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def colision(p1,r1,p2,r2):
    return distancia(p1,p2) <= (r1+r2)        
 
def homerTocado():

    global VIDAS, FIN_JUEGO, tiempoPasado

    VIDAS-=1
    tiempoPasado = 0
    
    if(VIDAS == 0):
        
        FIN_JUEGO = True
        timerDonutNuevo.stop()
        timerDonutMovimiento.stop()
        
def reset():
    
    global lista_donuts,FIN_JUEGO,VIDAS
    
    lista_donuts = []
    
    FIN_JUEGO = False
    VIDAS = VIDAS_TOTALES
    timerDonutNuevo.start()
    timerDonutMovimiento.start()
    

        
         
 
#Imagenes     
        
fondo = simplegui.load_image('http://imagizer.imageshack.us/a/img843/6822/8zon.jpg')      
homer_izq = simplegui.load_image('http://imagizer.imageshack.us/a/img853/3831/k2xu.png')
homer_der = simplegui.load_image('http://imagizer.imageshack.us/a/img196/3630/k82m.png')
homer_espalda = simplegui.load_image('http://imagizer.imageshack.us/a/img845/7682/kail.png')
donut_img = simplegui.load_image('http://imagizer.imageshack.us/a/img845/8408/l6z6.png')
disparoRojo = simplegui.load_image('http://imagizer.imageshack.us/a/img89/8283/mwhh.png')

#Instancias de clase

fondo1 = Imagen(fondo,(anP,alP),(anP/2,alP/2))
hi = Imagen(homer_izq,(125,225),(125/2,225/2))
hd = Imagen(homer_der,(125,225),(125/2,225/2))
he = Imagen(homer_espalda,(75,225),(75/2,225/2))
donut1 = Imagen(donut_img,(80, 80),(80/2,80/2))
disparoRojo1= Imagen(disparoRojo,(10,10),(5,5))

homer = Homer(hi,hd,he,(anP/2,alP-60),(125/2,225/2),2)

#Manejador de dibujo

def dibujar(canvas):
    

    
    fondo1.dibujar(canvas,(anP/2,alP/2),(anP,alP))
    homer.dibujar(canvas)
 
    
    
    for i in range (len(lista_disparos)):

        lista_disparos[i].dibujar(canvas)

    vidas = 'Vidas:' + str(VIDAS)   
    puntos = 'Puntos: ' + str(PUNTOS)
    
    canvas.draw_text(vidas ,(30,50),25,'Black') 
    canvas.draw_text(puntos ,(anP-110,50),25,'Black')     
    
    for i in range (len(lista_donuts)):

        lista_donuts[i].dibujar(canvas)
        
    if FIN_JUEGO == True:
        
        canvas.draw_line((0,alP/2),(anP,alP/2),70,'Black')
        canvas.draw_text('GAME OVER',(anP/2-120,alP/2+15),40,'Red')
    

#Ejecucion de manejadores de teclado
    
def pulsar_tecla(tecla):

    if FIN_JUEGO == False:
        
        if tecla == simplegui.KEY_MAP['left']:

            homer.movimiento('izq')

        elif tecla == simplegui.KEY_MAP['right']:
 
            homer.movimiento('der')
        
        elif tecla == simplegui.KEY_MAP['space']:
        
            nuevoDisparo()


def soltar_tecla(tecla):
    
   homer.movimiento('quieto')
                

#Ventana

frame = simplegui.create_frame('Homer Pang', anP,alP)

#Manejadores

frame.set_keydown_handler(pulsar_tecla)
frame.set_keyup_handler(soltar_tecla)
frame.set_draw_handler(dibujar)

#Inicializacion
    
frame.start()

#Botones

frame.add_button("Reiniciar", reset, 100)

#Timers
    
timerDonutMovimiento = simplegui.create_timer(20.0, actualizarDonuts)
timerDonutMovimiento.start()
timerDonutNuevo = simplegui.create_timer(NUEVO_DONUT, donut_aleatorios)
timerDonutNuevo.start()
timerAvanzarDisparo = simplegui.create_timer(20.0, actualizarDisparo)
timerAvanzarDisparo.start()