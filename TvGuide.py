from cgi import print_arguments
from queue import PriorityQueue
from sys import maxsize
# from datetime import datetime, timedelta
import datetime 
# from datetime import timedelta

# print("__________________________ ")
# print("|                          |")
# print("|__________________________|")


# class canalTv()


####
# esta funcion llena espacios para coincidir con el formato de salida de la matriz
########

def llenarEspacios(frase, maxSize):
    tamOracion = int(len(frase))
    if tamOracion<maxSize :
        diferencia = maxSize - tamOracion
        return '| ' + frase + ' '*(diferencia -1)
    else:
        return '| ' + frase[:(maxSize-1)]
# frase = "Batman Dark Knight y algo mas para que corte"
# maxSize = 25
# print( llenarEspacios(frase, maxSize))

tamColum= 35
nroColum= 5
####
# aca se agrega una division a la pantalla
def filadiv():
    print(("+" + "-"*tamColum)*nroColum + "+")
####
# esta funcion llena crea los bloques de horas dependiendo de lo que se necesite
########

def filaHoras(horaSolicitada):
    filadiv()
    if int(horaSolicitada.minute) < 30 :
        bloque1 =  horaSolicitada.replace(minute = 0, second=0)     
    else:
        bloque1 =  horaSolicitada.replace(minute = 30, second=0)
    bloque2 = bloque1 + datetime.timedelta(minutes=30)
    bloque3 = bloque1 + datetime.timedelta(minutes=60)
    bloque4 = bloque1 + datetime.timedelta(minutes=90)
    b1 = bloque1.strftime("%H:%M")
    b2 = bloque2.strftime("%H:%M")
    b3 = bloque3.strftime("%H:%M")
    b4 = bloque4.strftime("%H:%M")
    print( llenarEspacios("CANAL // HORARIO",tamColum) + llenarEspacios(b1,tamColum)  +llenarEspacios(b2,tamColum)  + llenarEspacios(b3,tamColum)  + llenarEspacios(b4,tamColum) +'|' ) 
    filadiv()

# ahora = datetime.datetime.now()
# cuatroAm = datetime.datetime(1,1,1,4,0)
# filaHoras(ahora)
# filaHoras(cuatroAm)

# ######## #se lee el archivo que contiene los datos de la programacion de tv
def leerBD(): 
    arc1 = open("bd20221001.txt", "r")

    x=arc1.readline()
    while(x):
        palab = x.split('//')
        print("Programa: ", palab[0])         
        print("canal: ", palab[1])     
        print("hora ininicio: ", palab[2])        
        print("hora final: ", palab[3])     
        x=arc1.readline()    
        arc1.close()      
    
#importante, recorre todo el archivo y recopila los canales que se encuentran en el indice [1]
def crearlistaCanales():
    arc1 = open("bd20221001.txt", "r")
    listaCanales = []
    Prg1  = arc1.readline()
    atrP1 = Prg1.split('//')
    listaCanales.append(atrP1[1])

    for programa in arc1.readlines():   
        atributoPrograma = programa.split('//')
        bool1 = False
        i=0
        while bool1==False and i <= (len(listaCanales)-1):
            if atributoPrograma[1] == listaCanales[i]:
                bool=True
            else:
                if i==len(listaCanales)-1:
                    listaCanales.append(atributoPrograma[1])
            i += 1 
             
    arc1.close()
    return listaCanales

class programaTv:
    def __init__(self, title, canal, hIni, hFin):
        self.title = title
        self.canal = canal
        self.hIni = hIni
        self.hFin = hFin
        # self.fecha = fecha
        

def programasImp(fechaHora):
    arc1 = open("bd20221001.txt", "r")
    x=arc1.readline()
    listPImprimir = []
    b0 = fechaHora
    b1 = b0 +datetime.timedelta(minutes=30)
    b2 = b0 +datetime.timedelta(minutes=60)  # aca se crean los bloques de media hora para la impresion, con referencia a la hora solicitada
    b3 = b0 +datetime.timedelta(minutes=90)
    b4 = b0 +datetime.timedelta(minutes=120)
    while(x):
        
        atrP = x.split('//')
        fiSF = atrP[2]
        ffSF = atrP[3]
        
        #print(int(fiSF[0:4:1]), int(fiSF[4:6:1]),int(fiSF[6:8:1]),int(fiSF[8:10:1]),int(fiSF[-2:]))
        f0 = datetime.datetime(int(fiSF[0:4:1]), int(fiSF[4:6:1]),int(fiSF[6:8:1]),int(fiSF[8:10:1]),int(fiSF[-2:])) 
        ff = datetime.datetime(int(ffSF[0:4:1]), int(ffSF[4:6:1]),int(ffSF[6:8:1]),int(ffSF[8:10:1]),int(ffSF[-3:]))
        x = arc1.readline()
        
        #limites inferiores y superiores de bloques
        a = f0<= b0 and ff<= b0
        b = f0>= b4 and ff>= b4
        if not(a or b):
            programaGuardar = programaTv(str(atrP[0]),str(atrP[1]),f0,ff)
            
            listPImprimir.append(programaGuardar) 
     
   
    listaCanales = crearlistaCanales()
    for canal in listaCanales:  
        print((llenarEspacios(canal, tamColum) ), end='')
        for i in range(0,4):    
            for obj in listPImprimir:
                if str(obj.canal)==str(canal):
                    
                        bi = b0 + datetime.timedelta(minutes=(i*30))
                        bf = b0 + datetime.timedelta(minutes=(30 + i*30))
                        c = obj.hIni<= bi and obj.hFin<= bi
                        d = obj.hIni>= bf and obj.hFin>= bf
                        if not(c or d):
                            print(( llenarEspacios(obj.title, tamColum) ), end='')
        print('|')
        filadiv()
    arc1.close()    

        
    #partir el atributo de las horas y convertirlo a fechas para comparar con el bloque

anio= 2022
mes = 10
dia=0
hora=0
salir = False
print("\nPrograma: Programacion Fin de Semana v 1.0")
print("\nInstrucciones: \nSe le presentaran dos fechas a elegir, una vez escogida, debe seleccionar el bloque horario a Consultar.")
while not salir:
    c1= False
    while not(c1):
        seleccion = input("\nSeleccione dia: \n(1) Sabado\n(2) Domingo \n:")
        if seleccion == "1" :
            dia = 1
            c1= True
        elif seleccion == "2":
            dia = 2
            c1= True
        else:
            print("Seleccion no valida")
            c1= False
    c1= False
    while not(c1):
        seleccion = input("\nSeleccione la Hora(de 0 a 22, 0 es media noche y 22 las 10:00pm) \n:")
        if seleccion== '0':	
            hora=0
            c1=True
        elif seleccion== '1':	
            hora=1
            c1=True
        elif seleccion== '2':	
            hora=2
            c1=True
        elif seleccion== '3':	
            hora=3
            c1=True
        elif seleccion== '4':	
            hora=4
            c1=True
        elif seleccion== '5':	
            hora=5
            c1=True
        elif seleccion== '6':	
            hora=6
            c1=True
        elif seleccion== '7':	
            hora=7
            c1=True
        elif seleccion== '8':	
            hora=8
            c1=True
        elif seleccion== '9':	
            hora=9
            c1=True
        elif seleccion== '10':	
            hora=10
            c1=True
        elif seleccion== '11':	
            hora=11
            c1=True
        elif seleccion== '12':	
            hora=12
            c1=True
        elif seleccion== '13':	
            hora=13
            c1=True
        elif seleccion== '14':	
            hora=14
            c1=True
        elif seleccion== '15':	
            hora=15
            c1=True
        elif seleccion== '16':	
            hora=16
            c1=True
        elif seleccion== '17':	
            hora=17
            c1=True
        elif seleccion== '18':	
            hora=18
            c1=True
        elif seleccion== '19':	
            hora=19
            c1=True
        elif seleccion== '20':	
            hora=20
            c1=True
        elif seleccion== '21':	
            hora=21
            c1=True
        elif seleccion== '22':	
            hora=22
            c1=True
        else:
            print("seleccion no valida")
            c1= False

    fechaHora = datetime.datetime(anio,mes,dia,hora,0)
    print(f"\nLa programacion del dia {fechaHora} es:\n\n")
    filaHoras(fechaHora)
    programasImp(fechaHora)
    c1= False
    while not(c1):
        seleccion = input("\nSiguiente accion: \n(1) Consultar Otro Horario\n(2) Salir \n:")
        if seleccion == "1" :
            salir = False
            c1= True
        elif seleccion == "2":
            dia = 2
            c1= True
            salir = True
        else:
            print("Seleccion no valida")
            c1= False


