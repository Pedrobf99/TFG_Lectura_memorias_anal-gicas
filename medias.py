# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 00:04:34 2022

@author: Admin
"""
#import matplotlib.pylab as plt
import os
import numpy as np
import pandas as pd
import shutil
#import regresion2 as r

#carpeta="prueba"
#ajstr=1
#def grafiquita(carpetas,ajstr):
def medias(nombre):
    ajstr=1
    folder="Datos/"
    ajst="ajust/"
    medias="MEDIAS/"
    archivos=[]

    for carpeta in os.listdir(folder+ajst):
        if nombre in carpeta and carpeta[0]!="T" and ".png" not in carpeta and ".csv" not in carpeta:
            #print(carpeta)
            path=folder+ajst+carpeta+'/'
            # CARACTERISTICAS MEMORIAS
            wes=[[0.5,0.5,0.5,0.5],[4,2,1,6],[0.5,0.5,0.5,0.5],[0.5,1,2,4],
                 [1,1,1,1],[1,1,1,1],[0.5,1,2,4],[4,2,1,6]]
            les=[[4,2,1,0.5],[0.5,0.5,0.5,0.5],[2,1,0.5,4],[0.5,0.5,0.5,0.5],
                 [0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[1,1,1,1],[0.5,0.5,0.5,0.5]]
            mims=[[160,160,160,160],[160,160,160,160],[160,160,160,160],[160,160,160,160],
                 [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[160,160,160,160],[160,160,160,160]]
            #wps=[[0,0,0,0],[0,0,0,0],[0.5,0.5,0.5,0.5],[1,1,1,1],[1,1,1,1],[0,0,0,0],[1,1,1,1],[4,2,1,6]]
            #wns=[[0.5,0.5,0.5,0.5],[4,2,1,6],[0,0,0,0],[0.5,1,2,4],[1,1,1,1],[1,1,1,1],[0.5,1,2,4],[0,0,0,0]]   
            #lns=[[4,2,1,0.5],[0.5,0.5,0.5,0.5],[0,0,0,0],[0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[1,1,1,1],[0,0,0,0]]
            #lps=[[0,0,0,0],[0,0,0,0],[2,1,0.5,4],[0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[0,0,0,0],[1,1,1,1],[0.5,0.5,0.5,0.5]]
            
            #bloques de memorias separadas por la variable que cambia en cada caso
            ws=[1,3,6,7]
            ls=[0,2]
            mim=[4,5]
            
            #Variable que cambia en cada caso
            #var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
            #dts=[]
            #times=[]
            
            Vin=[]
            sVin=[]
            a=[]
            sa=[]
            Vhold=[]
            sVhold=[]
            c=[]
            sc=[]
            n=0
            #Leemos todos los archivos de la carpeta para 
            #hacer una media de los valores de cada chip
            for i in os.listdir(path):
                if 'csv' in i and i[15]!='_':
                    # and i[14]!='7' and i[14]!='8' and i[14]!='4' and i[14]!='5' and i[14]!='1':
                    #and "4500" not in i and i[14]!='7' and i[14]!='8':
                        
                    #if (len(carpeta)==6 and len(i)>37) or (len(carpeta)>6 and len(i)>49):                     
                    #print(i)
                    #Leemos cada archivo y almacenamos los datos
                    dft=pd.read_csv(path+i)
                    arrt=dft.to_numpy()
                        
                    for data in arrt[:,0]:
                        Vin.append(data)
                    for data in arrt[:,1]:
                        sVin.append(data)
                    for data in arrt[:,2]:
                        a.append(data)
                    for data in arrt[:,3]:
                        sa.append(data)
                    for data in arrt[:,4]:
                        Vhold.append(data)
                    for data in arrt[:,5]:
                        sVhold.append(data)    
                    if ajstr==1:
                        for data in arrt[:,6]:
                            c.append(data)
                        for data in arrt[:,7]:
                            sc.append(data)    
                    n=n+1
                    archivos.append(i)
            
            
            if ajstr==1:
                valores=[Vin,sVin,a,sa,Vhold,sVhold,c,sc]
            if ajstr==0:
                valores=[Vin,sVin,a,sa,Vhold,sVhold]
                
            #Reorganizamos los datos haciendo una media para la memoria correspondiente
            bux=[]
            sbux=[]
            for h in range(0,ajstr+3):
                aux=[]
                saux=[]
                for j in range(0,32):
                    for i in range(0,n):
                        aux.append(valores[2*h][i*32+j])
                        saux.append(1/(valores[2*h+1][i*32+j])**2)
                    pesos=sum(saux[j*n:j*n+n])
                    bux.append(np.average(aux[j*n:j*n+n],weights=saux[j*n:j*n+n]))
                    sbux.append(1/pesos**0.5)
            if not os.path.exists(folder+ajst+medias+'T_'+nombre+'_masv/'):
                        os.makedirs(folder+ajst+medias+'T_'+nombre+'_masv/')   
                        

                
            #Las matrices bux y sbux tienen los valores medios de cada memoria y sus inceridumbres
            file = open(folder+ajst+medias+'T_'+nombre+'_masv/'+carpeta+'.csv', "a") #añadimos informacion al archivo
            file.write("Vin,sVin,a,sa,Vhold,sVhold,c,sc\n")
            
            for i in range(0,32):
                file.write(str(bux[i])+','+str(sbux[i])+','+str(bux[i+32])+','+str(sbux[i+32])+','+str(bux[i+64])+','+str(sbux[i+64])+','+str(bux[i+96])+','+str(sbux[i+96])+'\n')
        
            file.close()
    archivo = open(folder+ajst+medias+'T_'+nombre+'_masv/'+nombre+'_archivos_usados.txt', "a") #añadimos informacion al archivo
    for i in range(0,len(archivos)):
            archivo.write(archivos[i]+"\n")
    print("Nombre de la carpeta: "+'T_'+nombre+'_masv')
    
name=input("Nombre de la carpeta destino: (con T_ delante) ")
medias(name)


























'''
  
def organizador():
    folder="Datos/"
    ajst="ajust/"
    for carpeta in os.listdir(folder+ajst):
        if 'NCAP' in carpeta:
            for i in os.listdir(carpeta):
                if i[0:4]=='NCAP' and i[-7]=='V':
                    if not os.path.exists(folder+ajst):
                        os.makedirs(folder+ajst+'NCAP/')
                    shutil.move(folder+ajst+carpeta+i,folder+ajst+'NCAP/'+i)

    #fig, axs = plt.subplots(4, 3, sharex='col', sharey='row')
    fig = plt.figure()
    gs = fig.add_gridspec(4, 3, hspace=0, wspace=0)
    axs=gs.subplots(sharey='row')
    ylabels=['V','tiempo (ms)','V','V/s'] 
    #si queremos ver el resto de variables cambaimos j y la matriz varis (y en fig,axs cambiamos el nº de gráficas en el 1º eje)
    varis=[0,1,2,3]
    for j in range(0,4):
        #print(varis[j])
        colores=['g','b','k','r']
        h=0
        labels=['NMOS','PMOS','TG','TG']
        for i in ws:
            axs[j,0].errorbar(wes[i],bux[varis[j]*32+i*4:varis[j]*32+i*4+4],sbux[varis[j]*32+i*4:varis[j]*32+i*4+4],0,
                                    ls='',marker='o',color=colores[h], label=labels[h]+' L='+str(les[i][0]), capsize=3)
            h=h+1
        axs[j,0].set(xlabel='W $(\mu m)$')
        if j==0:
            axs[j,0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),ncol=2, fancybox=True, shadow=True,fontsize=8)
        
        h=0
        labels=['NMOS','PMOS']
        for i in ls:
            axs[j,1].errorbar(les[i],bux[varis[j]*32+i*4:varis[j]*32+i*4+4],sbux[varis[j]*32+i*4:varis[j]*32+i*4+4],0,
                                    ls='',marker='o',color=colores[h], label=labels[h]+' W='+str(wes[i][0]), capsize=3)
            h=h+1
        axs[j,1].set(xlabel='L $(\mu m)$')
        if j==0:
            axs[j,1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),ncol=1, fancybox=True, shadow=True,fontsize=8)    
        h=0
        colores=['g','k','r']
        labels=['NMOS W=1 L=0.5','TG W=1 L=0.5']
        for i in mim:
            axs[j,2].errorbar(mims[i],bux[varis[j]*32+i*4:varis[j]*32+i*4+4],sbux[varis[j]*32+i*4:varis[j]*32+i*4+4],0,
                                    ls='',marker='o',color=colores[h], label=labels[h], capsize=3)
            h=h+1
        axs[j,2].set(xlabel='C $(mF)$')
        if j==0:
            axs[j,2].legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),ncol=1, fancybox=True, shadow=True,fontsize=8) 
        
        for ax in axs[j].flat:
            ax.set(ylabel=ylabels[j])
        
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        fig.set_size_inches(10, 10)
    
    fig.savefig(path+carpeta+'_medias.png')
    fig.savefig(path+carpeta+'_medias.svg',format='svg',transparent=True)
'''
