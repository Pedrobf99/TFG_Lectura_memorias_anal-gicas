# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:28:28 2022

@author: Admin
"""
import serial
import time
from graficas import graf
#from analisis2 import an
from analisis3 import an3
import matplotlib.pylab as plt
import os

plt.close('all')

folder="Datos/"

port="COM19" #nombre del puerto al que se conecta el arduino
baud=115200 #ratio del arduino

ser=serial.Serial(port,baud) #conexion con el arduino

ajstr=1 #Utilizamos siempre el mismo tipo de ajuste

#Preguntas para guardar los datos de forma ordenada
chip=input("¿Que chip estamos midiendo? ")
condiciones=input("¿Bajo iluminación? (Y/N) ")
'''
if condiciones=="Y" or condiciones=="Si" or condiciones=="y" or condiciones=="si":
        dist="65"
        voltaje=input("Voltaje de la fuente: ")
        if int(voltaje)<22:
            #voltaje='0'+voltaje
            filtro="N"
        if int(voltaje)>22:
            filtro=input("Filtros: (N/nombre del filtro) ")
            
else:
    voltaje="0"
    filtro="N"   
'''         
def medir(chip,condiciones,estructura,voltaje,filtro,num):
    
    #En función del bloque de memorias establecemos unos límites para los parámetros
    if estructura=="1":
        estructura="NCAP"
        pin="15"
        boundes=[[0.1,100,0,-2],[2,8000,2,2]]
    elif estructura=="2":
        estructura="MIM"
        pin="16"
        boundes=[[0.001,300,0,-2],[2,12000,2,2]]
    elif estructura=="11":
        estructura="PCAP"
        pin="14"
        boundes=[[0.001,300,0,-2],[2,12000,2,2]]
        
    #estructura=input("¿NCAP, MIM, PCAP? (Out en 1,2,11) ")
    #Construir el nombre del archivo donde guardar los datos
    
     
    if condiciones=="Y" or condiciones=="Si" or condiciones=="y" or condiciones=="si":    
        ser.write(bytes(pin, 'utf-8'))   
        time.sleep(2)
        if int(voltaje)<10:
            voltaje='0'+voltaje
        if int(voltaje)>22:
            filename="Datos_"+chip+"_"+estructura+"_T"+num+"_d"+dist+"cm_V"+voltaje+"V_filtro"+filtro+".csv" #Archivo guardar datos
        else:
            filename="Datos_"+chip+"_"+estructura+"_T"+num+"_d"+dist+"cm_V"+voltaje+"V_filtroN.csv" #Archivo guardar datos

        ajstr=1
        
    else:     
        ser.write(bytes(pin, 'utf-8'))   
        time.sleep(2)
        
        filename="Datos_"+chip+"_"+estructura+"_T"+num+"_sinluz.csv"  #Archivo guardar datos
        ajstr=1
    
    #print(pin)
    
    ser.write(bytes(num, 'utf-8'))   
    
    #file=open(folder+filename,"w")
    
    t_measures=0
    measures=0
    fallito=0
    fallos=[]
    filas=[]
    dts=[]
    times=[]
    
    #Para almacenar los datos los guardamos en una carpeta con el nombre del chip
    path=folder+chip+'/'
    if not os.path.exists(path):
        os.makedirs(path)
    
    #Eliminamos un archivo en caso de que se repita el nombre
    for i in os.listdir(folder+chip+'/'):
        if i==filename:
            os.remove(folder+chip+'/'+i)
            print('Archivo eliminado')
            
    
    file = open(folder+chip+'/'+filename, "a") #añadimos informacion al archivo
    file.write("Lectura analógica,Tiempo\n")
    
    #siguiente mensaje será el comienzo de datos de la primera medida
    start=str(ser.readline().decode())
    while "Inicio" not in start:
        start=str(ser.readline().decode())
    print(start[0:-2])
    
    time_start=time.time()
    
    tiempos=0
    n_filas=50000 #Límite en el caso de que el tiempo del Arduino sea demasiado largo
    #Ahora almacenamos los valores que el arduino envía durante un ciclo completo    
    while t_measures<n_filas:
    
        getData=ser.readline()
        #print(getData)
        fila=getData.decode()[0:][0:-2]
        #print(fila)  
        
    
        if str(getData).find('Final')==-1:
            #Cada fila representa el valor de una MEMORIA 
            
            filas.append(fila)
            if t_measures%33==0:
                #print(fila)
                
                try:
                    times.append(float(filas[t_measures]))    #en esta matriz almacenamos los valores de tiempo
                except:
                    times.append(2*float(filas[t_measures-33])-float(filas[t_measures-65])) #en el caso de que haya un error tomamos aprox del tiempo
                    fallito=fallito+1
                    fallos.append(t_measures)
                    
                tiempos=tiempos+1
                t_measures=t_measures+1
                
            else:
                try:
                    dts.append(float(filas[t_measures]))    #en esta matriz almacenamos los valores de todas las memorias (cada memoria esta separada por 32 valores)
                except:
                    dts.append(float(filas[t_measures-33]))    #en el caso de que haya un error tomamos el último valor que hayamos medido de esa memoria
                    fallito=fallito+1
                    fallos.append(t_measures)
                #print(str(dts[t_measures-tiempos])+","+str(times[int(t_measures/33)])+"\n")
                file.write(str(dts[t_measures-tiempos])+","+str(times[int(t_measures/33)])+"\n") #escribimos cada linea
                t_measures=t_measures+1
                
        else: 
            t_measures=n_filas
    
    
    n=int(len(dts)/32)
    print("Medidas para cada set de memorias: "+str(n))
    print("Total de medidas: "+str(len(dts)))
    print("Hubo "+str(fallito)+" fallito(s) en la(s) posicion(es): "+ str(fallos))
    print("El archivo de datos es: " + filename+"\n")
    
    file.write(str(n)+","+str(n) + "\n") #escribimos numero de medidas por memoria
    
    file.close() #cerramos el archivo
    return boundes,filename

#Por si queremos graficar ya los datos al tomarlos
#grafi=input("Ver gráficas: (Y/N) ") 

#Bucle para medir los tres bloques, y medir período más largo para PCAP y MIM
grafi='Nooooo' 
if condiciones=="Y" or condiciones=="Si" or condiciones=="y" or condiciones=="si":
    medimos=19
else:
    medimos=1
for i in range(medimos):
    if condiciones=="Y" or condiciones=="Si" or condiciones=="y" or condiciones=="si":
        dist="65"
        voltaje=input("Voltaje de la fuente: ")
        if int(voltaje)<22:
            #voltaje='0'+voltaje
            filtro="N"
        if int(voltaje)>22:
            filtro=input("Filtros: (N/nombre del filtro) ")
                    
    else:
        voltaje="0"
        filtro="N" 
    for estructura in ("1","2","11","2_","11_"):
        if estructura=="1":
            num = "1500" #Período de lectura de memorias
        elif estructura=="2":
            num = "4500" 
        elif estructura=="11":
            num = "4500"  
        elif estructura=="2_":
            estructura="2"
            num = "8500" 
        elif estructura=="11_":
            estructura="11"
            num = "8500"      
        boundes,filename=medir(chip,condiciones,estructura,voltaje,filtro,num)
        if grafi=='Y' or grafi=='Yes' or grafi=='si' or grafi=='y' or grafi=='Si' or grafi=='yes':
            graf(filename)
            bound=boundes
            an3(filename,bound,ajstr)
          
    
    
ser.close() #cerramos el puerto



























'''
grafi=input("Ver las graficas: (Y/N) ")
if grafi=='Y' or grafi=='Yes' or grafi=='si' or grafi=='y' or grafi=='Si' or grafi=='yes':
    graf(filename)

    ajust=input("Ver los ajustes: (Y/N) ")
    if ajust=='Y' or ajust=='Yes' or ajust=='si' or ajust=='y' or ajust=='Si' or ajust=='yes':
        
        bound=boundes
        an(filename,bound,ajstr)
        
        
        b=input("Cambiar límites de los ajustes: (Y/N) ")
        if b=='Y' or b=='Yes' or b=='si' or b=='y' or b=='Si' or b=='yes':
            bound=input('Límites: ')
            an(filename,bound,ajstr)
        else:
            bound=boundes
            an(filename,bound,ajstr)
'''

