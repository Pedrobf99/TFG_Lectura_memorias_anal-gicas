
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 00:04:34 2022

@author: Admin
"""
#import matplotlib.pylab as plt
import os
import pandas as pd
import regresion2 as r

#an4("16/","Datos_16_NCAP_T1500_sinluz.csv",[[0.1,100,0,-2],[2,8000,2,2]],1)

def an4(chip,filename,boundes,ajstr):
    dts=[]
    times=[]
    
    folder="Datos/"
    ajust="Ajustes/"
    ajst="ajust/"
    
    #Leemos todos el archivo filename para representar los datos
    dft=pd.read_csv(folder+chip+filename)
    arrt=dft.to_numpy()
    n=int(arrt[-1,0]) #numero de medidas por memoria
    
    for data in arrt[:-1,0]:
        dts.append(data)
    for data in arrt[:-1,1]:
        times.append(data)
    
    a=[] #Matriz auxiliar
    b=[] #Datos de cada memoria ordenados fila a fila
    t1=[] #Matriz auxiliar
    t_final=[] #Tiempos de cada memoria ordenados fila a fila
    
    #Para probar con 4 memorias cambiar los 32 por 4 y debería funcionar
    for j in range(0,32):
        for i in range(0,n):
            a.append(dts[i*32+j]*5/1024)
            t1.append(times[i*32+j])
        b.append(a[j*n:j*n+n])
        t_final.append(t1[j*n:j*n+n])
    #matriz donde almacenaremos todos los datos ordenados
    valores=[]
    file = open(folder+ajst+'ajustes_'+filename, "a") #añadimos informacion al archivo
    file.write("Vin,sVin,a,sa,Vhold,sVhold,c,sc\n")
    #Matrices auxiliares para recoger los datos
    Vin=[]
    sVin=[]
    a=[]
    sa=[]
    Vhold=[]
    sVhold=[]
    c=[]
    sc=[]
    for j in range(0,8):
        Vin=[]
        sVin=[]
        a=[]
        sa=[]
        Vhold=[]
        sVhold=[]
        c=[]
        sc=[]
        for i in range(0,4):
            
            #Ajustamos cada memoria a una exponencial decreciente + una recta
            coefs,scoef=r.ajuste(t_final[i+j*4][1:], b[i+j*4][1:], boundes,i+j*4,ajstr)
            if ajstr==1:
                c.append(coefs[3])
                sc.append(scoef[3])
                #Escribimos los valores en un excel
                file.write(str(coefs[0])+','+str(scoef[0])+','+str(coefs[1])+','+str(scoef[1])+','+str(coefs[2])+','+str(scoef[2])+','+str(coefs[3])+','+str(scoef[3])+"\n") #escribimos cada linea
            if ajstr==0:
                file.write(str(coefs[0])+','+str(scoef[0])+','+str(coefs[1])+','+str(scoef[1])+','+str(coefs[2])+','+str(scoef[2])+"\n") #escribimos cada linea
            #Recogemos los valores obtenidos
            Vin.append(coefs[0])
            a.append(coefs[1])
            Vhold.append(coefs[2])
            
            sVin.append(scoef[0])
            sa.append(scoef[1])
            sVhold.append(scoef[2])
        if ajstr==0:
            valores.append([Vin,sVin,a,sa,Vhold,sVhold])

        if ajstr==1:
            valores.append([Vin,sVin,a,sa,Vhold,sVhold,c,sc])
            #print(Vin)

    #comparamos las caract de las memorias con los valores obtenidos del ajuste
    #regres=r.regs(caract,valores,ajstr)    
    #Esta función nos da las rectas del ajuste anterior para representarlas
    #plots=r.plotss(caract,regres,var,ajstr)
    
    file.close()
    '''
    path=ajust+filename[:-4]+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    '''
    
    r.ajuste_graph(t_final, b, ajust+filename[:-4],boundes,ajstr)
