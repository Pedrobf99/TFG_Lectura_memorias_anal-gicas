# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 00:04:34 2022

@author: Admin
"""
import matplotlib.pylab as plt
import os
import numpy as np
import pandas as pd
import regresion2 as r
from regresion2 import luz1,simple

#carpeta="MIM_d65"
#0 es Vin 1 es a 2 es Vhold y 3 es c
#variable=1
folder="Datos/"
ajst="ajust/"
medias="MEDIAS/"
bloques=['NMOS','NMOS_WIDTH','PMOS','TG','TG_VAR_MIM','NMOS_VAR_MIM','TG_L_1u','PMOS_WIDTH']

def potencia(V):
    return 1614.1e-4*V-9.9e-3


#la carpeta basicamentes es elegir NCAP, MIM o PCAP
path=folder+ajst+medias
#Representar datos frente a las características de cada memoria
def caracts(carpeta,variable):
        
    folder="Datos/"
    ajst="ajust/"
    medias="MEDIAS/"

    path=folder+ajst+medias+carpeta+'/'
    # CARACTERISTICAS MEMORIAS
    wes=[[0.5,0.5,0.5,0.5],[4,2,1,6],[0.5,0.5,0.5,0.5],[0.5,1,2,4],
         [1,1,1,1],[1,1,1,1],[0.5,1,2,4],[4,2,1,6]]
    les=[[4,2,1,0.5],[0.5,0.5,0.5,0.5],[2,1,0.5,4],[0.5,0.5,0.5,0.5],
         [0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[1,1,1,1],[0.5,0.5,0.5,0.5]]
    mims=[[160,160,160,160],[160,160,160,160],[160,160,160,160],[160,160,160,160],
         [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[160,160,160,160],[160,160,160,160]]
    
    caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
            [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
    var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    
    #bloques de memorias separadas por la variable que cambia en cada caso
    ws=[1,3,6,7]
    ls=[0,2]
    mim=[4,5]
    
    #Variable que cambia en cada caso
    #var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    #dts=[]
    #times=[]
    
    cT=[]
    scT=[]
    Vp=[]
    V=[]
    n=0
    #archivo_mim=0
    #Leemos todos los archivos de la carpeta para 
    #hacer una media de los valores de cada chip
    h=0
    for i in os.listdir(path):
        if 'csv' in i and 'filtro' not in i:
            if 'V' in i:
                Vp.append(int(i[-6:-4]))
                #archivo_mim=1
            else:
                Vp.append(0)
            if Vp[h]==3 or Vp[h]==15 or Vp[h]==24 or Vp[h]==0:
                #print(Vp)
                print(i)
                c=[]
                sc=[]
                #Leemos cada archivo y almacenamos los datos
                dft=pd.read_csv(path+i)
                arrt=dft.to_numpy()
                
                for data in arrt[:,variable*2]:
                    c.append(data*1000)
                for data in arrt[:,variable*2+1]:
                    sc.append(data*1000)    
                n=n+1
                V.append(Vp[h])
                cT.append(c)
                scT.append(sc)
            h=h+1
    #comparamos las caract de las memorias con los valores obtenidos del ajuste
    regres=r.regs2(caract,cT)    
    
    #Esta función nos da las rectas del ajuste anterior para representarlas
    hs=r.plotss2(caract,regres,var)
    
    fig = plt.figure(figsize=(20,10),constrained_layout=True)
    gs = fig.add_gridspec(2, 4, hspace=0.2,wspace=0.1)
    axs=gs.subplots()    
    #############################  SELN  ###############################
    
    colores = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    
    for i in ls:
        if i<=3:
            col=i
            row=0
        else:
            col=i-4
            row=1
        #print(col,row)
        for j in range(0,n):
            axs[row, col].errorbar(les[i],cT[j][i*4:i*4+4],scT[j][i*4:i*4+4],ls='',
                marker='o',color=colores[j], label='V='+str(V[j]),capsize=3) 
            axs[row, col].plot(hs[j][i][0],hs[j][i][1],color=colores[j], ls='--')
    
        axs[row, col].legend(loc="upper right")
        axs[row, col].set(xlabel='L ($\mu m$)')
        
    axs[0, 0].set_title('NMOS')
    axs[0, 1].set_title('NMOS_WIDTH')
    axs[0, 2].set_title('PMOS')
    axs[0, 3].set_title('TG')
    axs[1, 0].set_title('TG_VAR_MIM')
    axs[1, 1].set_title('NMOS_VAR_MIM')
    axs[1, 2].set_title('TG_L_1u')
    axs[1, 2].set_title('TG_L_1u')
    axs[1, 3].set_title('PMOS_WIDTH')
    
    for i in ws:
        '''
        #No representamos los datos que dan mal en el bloque MIM
        if i==1 and archivo_mim==1:
            print('No hay datos')
        else:
            '''
        if i<=3:
            col=i
            row=0
        else:
            col=i-4
            row=1
        #print(col,row)
        for j in range(0,n):
            axs[row, col].errorbar(wes[i],cT[j][i*4:i*4+4],scT[j][i*4:i*4+4],ls='',
                marker='o',color=colores[j], label='V='+str(V[j]),capsize=3) 
            axs[row, col].plot(hs[j][i][0],hs[j][i][1],color=colores[j], ls='--')
        axs[row, col].legend(loc="upper right")
        axs[row, col].set(xlabel='W ($\mu m$)')
    
    for i in mim:
        '''
        #No representamos los datos que dan mal en el bloque MIM
        if i==4 and archivo_mim==1:
            print('No hay datos')
        else:'''
    
        if i<=3:
            col=i
            row=0
        else:
            col=i-4
            row=1
        #print(col,row)
        for j in range(0,n):
            axs[row, col].errorbar(mims[i],cT[j][i*4:i*4+4],scT[j][i*4:i*4+4],ls='',
                marker='o',color=colores[j], label='V='+str(V[j]),capsize=3) 
            axs[row, col].plot(hs[j][i][0],hs[j][i][1],color=colores[j], ls='--')
        axs[row, col].legend(loc="upper right")    
        axs[row, col].set(xlabel='C (mF)')
    
        
    ejes=[axs[0,0],axs[1,0]]
    for ax in ejes:
        ax.set(ylabel='fotocorriente (V/ms)')
        
    
    if variable==0:
        var='Vin'
    if variable==1:
        var='a'    
    if variable==2:
        var='Vhold'
    if variable==3:
        var='c'
        
    fig.savefig(path+carpeta+'_'+var+'_voltajes_sinluzmedias.pdf',format='pdf')
    fig.savefig(path+carpeta+'_'+var+'_voltajes_sinluzmedias.png')

#graf=input('Nombre de la carpeta (variando el voltaje): ')
#ajstr=int(input("Variable: (0-Vin 1-a 2-Vhold 3-c) "))
#caracts(graf, ajstr)

#0 es Vin 1 es a 2 es Vhold y 3 es c
#Representar las medias de los datos obtenidos para una memoria en particular
def voltajes(carpeta,variable,bloque,memoria):
    
    carpeta='T_'+str(carpeta)
    folder="Datos/"
    ajst="ajust/"
    medias="MEDIAS/"

    #la carpeta basicamentes es elegir NCAP, MIM o PCAP
    path=folder+ajst+medias+carpeta+'/'
    
    ##### CARACTERISTICAS MEMORIAS ################
    
    caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
            [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
    var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']


    #Matrices para almacenar los datos de la variable a estudiar y los voltajes
    P=[]
    Pp=[]
    cT=[]
    scT=[]
    Vp=[]
    V=[]
    n=0
    #archivo_mim=0
    
    #Leemos todos los archivos de la carpeta y almacenamos los valores de
    #la variable y memoria indicada ya promediados, así como de los voltajes
    h=0
    for i in os.listdir(path):
        if 'csv' in i and 'filtro' not in i:
            if 'V' in i:
                Vp.append(int(i[-6:-4]))
                P.append(potencia(int(i[-6:-4])))
                #archivo_mim=1
            else:
                #Archivo sin luz
                Vp.append(0)
                P.append(0)
            #Podemos seleccionar si queremos estudiar algún voltaje en particular, o excluir alguno
            if Vp[h]!=24 and Vp[h]!=410 and Vp[h]!=418 and Vp[h]!=110 and Vp[h]!=113:
                #print(Vp)
                #print(i)
                c=[]
                sc=[]
                #Leemos cada archivo y almacenamos los datos
                dft=pd.read_csv(path+i)
                arrt=dft.to_numpy()
                if variable==3 or variable==1:
                    c.append(arrt[memoria+bloque*4,variable*2]*1000)
                    sc.append(arrt[memoria+bloque*4,variable*2+1]*1000)
                else:
                    c.append(arrt[memoria+bloque*4,variable*2])
                    sc.append(arrt[memoria+bloque*4,variable*2+1])                    
                n=n+1
                V.append(Vp[h])
                Pp.append(P[h])
                cT=cT+c
                scT=scT+sc
            h=h+1
            
    colores = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    
    bloques=['NMOS','NMOS_WIDTH','PMOS','TG','TG_VAR_MIM','NMOS_VAR_MIM','TG_L_1u','PMOS_WIDTH']
    
    plt.rcParams["figure.figsize"] = (9,7.3)
    plt.rcParams["figure.constrained_layout.use"] = True
    #plt.figure(figsize=(7.5,5),constrained_layout=True)
    color=(bloque+1)*memoria
    if (bloque+1)*memoria>19:
        color=bloque+memoria    
    #Reresentamos
    plt.errorbar(Pp,cT,scT,ls='-',marker='o',color=colores[color], label=var[bloque]+": "+str(caract[bloque][memoria]),capsize=3) 
    plt.title(bloques[bloque],fontsize=27)
    plt.legend(loc="upper right",fontsize=22)
    plt.xlabel('P ($W/m^2$)',fontsize=27)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=16)
    #plt.ylabel('I/c (V/s)')

    #Ejes y nombre en función de la variable
    if variable==0:
        vari='Vin'
        plt.ylabel('V (V)',fontsize=20)
    if variable==1:
        vari='a'
        plt.ylabel('Tiempo (s)',fontsize=20)
    if variable==2:
        vari='Vhold'
        plt.ylabel('V (V)',fontsize=20)
    if variable==3:
        vari='c'
        plt.ylabel('I/c (V/s)',fontsize=20)
        
    #plt.savefig(path+carpeta+'medias_'+vari+"_"+bloques[bloque]+"_"+str(caract[bloque][memoria])+'.png')
    #plt.savefig(path+carpeta+'medias_'+vari+"_"+bloques[bloque]+"_"+str(caract[bloque][memoria])+'.pdf',format='pdf')

#Representar las medias de los datos obtenidos para una memoria en particular restando el valor para voltaje cero
def voltajes_relativos(carpeta,variable,bloque,memoria):
    
    carpeta='T_'+str(carpeta)
    folder="Datos/"
    ajst="ajust/"
    medias="MEDIAS/"

    #la carpeta basicamentes es elegir NCAP, MIM o PCAP
    path=folder+ajst+medias+carpeta+'/'
    # CARACTERISTICAS MEMORIAS
    wes=[[0.5,0.5,0.5,0.5],[4,2,1,6],[0.5,0.5,0.5,0.5],[0.5,1,2,4],
         [1,1,1,1],[1,1,1,1],[0.5,1,2,4],[4,2,1,6]]
    les=[[4,2,1,0.5],[0.5,0.5,0.5,0.5],[2,1,0.5,4],[0.5,0.5,0.5,0.5],
         [0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[1,1,1,1],[0.5,0.5,0.5,0.5]]
    mims=[[160,160,160,160],[160,160,160,160],[160,160,160,160],[160,160,160,160],
         [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[160,160,160,160],[160,160,160,160]]
    
    caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
            [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
    var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    
    #bloques de memorias separadas por la variable que cambia en cada caso
    ws=[1,3,6,7]
    ls=[0,2]
    mim=[4,5]
    
    #Variable que cambia en cada caso
    #var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    #dts=[]
    #times=[]
    P=[]
    Pp=[]
    cT=[]
    scT=[]
    Vp=[]
    V=[]
    #archivo_mim=0
    #Leemos todos los archivos de la carpeta para 
    #hacer una media de los valores de cada chip
    for i in os.listdir(path):
        if 'csv' in i and 'filtro' not in i:
            if 'V' not in i:
                dft=pd.read_csv(path+i)
                arrt=dft.to_numpy()
                c0=1000*arrt[memoria+bloque*4,variable*2]
                sc0=arrt[memoria+bloque*4,variable*2+1]*1000
                #V.append(0)
                #print(sc0)
    h=0
    for i in os.listdir(path):
        if 'csv' in i and 'filtro' not in i:
            if 'V' in i:
                Vp.append(int(i[-6:-4]))
                P.append(potencia(int(i[-6:-4])))

                if Vp[h]!=24 and Vp[h]!=410 and Vp[h]!=413:
                    dft=pd.read_csv(path+i)
                    arrt=dft.to_numpy()
                    #archivo_mim=1
                    cT.append(1000*arrt[memoria+bloque*4,variable*2]-c0)
                    scT.append(((arrt[memoria+bloque*4,variable*2+1]*1000)**2+sc0**2)**0.5)
                    #print(Vp)
                    #print(cT)
                    #print(i)
                    Pp.append(P[h])
                    V.append(Vp[h])

                h=h+1

    
    colores = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    
    bloques=['NMOS','NMOS_WIDTH','PMOS','TG','TG_VAR_MIM','NMOS_VAR_MIM','TG_L_1u','PMOS_WIDTH']
    #fig=plt.figure(figsize=(9,5),constrained_layout=True)
    plt.rcParams["figure.figsize"] = (9,7.3)
    plt.rcParams["figure.constrained_layout.use"] = True  
    color=(bloque+1)*memoria
    if (bloque+1)*memoria>19:
        color=bloque+memoria
    plt.errorbar(Pp,cT,scT,ls='-',marker='o',color=colores[color], label=var[bloque]+": "+str(caract[bloque][memoria]),capsize=3) 
    plt.title(bloques[bloque],fontsize=27)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=16)
    plt.legend(loc="upper right",fontsize=22)
    plt.xlabel('P ($W/m^2$)',fontsize=27)

        
    
    if variable==0:
        vari='Vin'
        plt.ylabel('V (V)',fontsize=27)
    if variable==1:
        vari='a'
        plt.ylabel('Tiempo (ms)',fontsize=27)
    if variable==2:
        vari='Vhold'
        plt.ylabel('V (V)',fontsize=27)
    if variable==3:
        vari='c'
        plt.ylabel('I/c (V/s)',fontsize=27)

    #plt.savefig(path+carpeta+'rel_'+vari+"_"+bloques[bloque]+"_"+str(caract[bloque][memoria])+'.png')
    #plt.savefig(path+carpeta+'rel_'+vari+"_"+bloques[bloque]+"_"+str(caract[bloque][memoria])+'.pdf',format='pdf')

#Representar las medias de los datos obtenidos para una memoria en particular restando el valor para voltaje cero
def voltajes_chip(NMP,variable,bloque,memoria,chip):      
    
    #NMP es una variable para saber de que bloque hablamos
    if NMP=="N":
        NMP="NCAP"
    if NMP=='P':
        NMP="PCAP"
    if NMP=="M":
        NMP="MIM"
    
    chip=str(chip)
    folder="Datos/"
    ajst="ajust/"
    medias="MEDIAS/"

    #la carpeta basicamentes es elegir NCAP, MIM o PCAP
    path=folder+ajst
    
    # CARACTERISTICAS MEMORIAS

    caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
            [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
    var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    
    colores = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    
    bloques=['NMOS','NMOS_WIDTH','PMOS','TG','TG_VAR_MIM','NMOS_VAR_MIM','TG_L_1u','PMOS_WIDTH']
    
    #Variable que cambia en cada caso
    #var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    #dts=[]
    #times=[]
    P=[]
    Pp=[]
    cT=[]
    scT=[]
    Vp=[]
    V=[]
    n=0
    #archivo_mim=0
    #Leemos todos los archivos de la carpeta para 
    #hacer una media de los valores de cada chip
    h=0
    for carpeta in os.listdir(path):
         if NMP[0:3]==carpeta[0:3] and os.path.isdir(path+carpeta+"/") and 'filtro' not in carpeta:
             for i in os.listdir(path+carpeta+"/"):
                 if 'csv' in i and "8500" in i:
                    if len(chip)==2 and chip==i[14:16]:       
                        if 'V' in i:
                            if NMP[0]=='M':
                                Vp.append(int(i[34:36]))
                                P.append(potencia(int(i[34:36])))

                            else:
                                Vp.append(int(i[35:37]))
                                P.append(potencia(int(i[35:37])))
                            #archivo_mim=1
                        else:
                            Vp.append(0)
                            P.append(0)
                        
                        if Vp[h]!=24 and Vp[h]!=28 and Vp[h]!=26:
                            #print(i)
                            #Leemos cada archivo y almacenamos los datos
                            dft=pd.read_csv(path+carpeta+"/"+i)
                            arrt=dft.to_numpy()
                            
                            cT.append(1000*arrt[memoria+bloque*4,variable*2])
                            scT.append(arrt[memoria+bloque*4,variable*2+1]*1000)    
                            n=n+1
                            V.append(Vp[h])
                            Pp.append(P[h])

                            #print(Vp)
                        h=h+1              

                    elif chip==i[14] and i[15]=='_':       
                        if 'V' in i:
                            if NMP[0]=='M':
                                Vp.append(int(i[33:35]))
                                P.append(potencia(int(i[33:35])))
                            else:
                                Vp.append(int(i[34:36]))
                                P.append(potencia(int(i[34:36])))
                            #archivo_mim=1
                        else:
                            Vp.append(0)
                            P.append(0)
                        
                        if Vp[h]!=24 and Vp[h]!=28 and Vp[h]!=26:
                            #print(i)
                            #Leemos cada archivo y almacenamos los datos
                            dft=pd.read_csv(path+carpeta+"/"+i)
                            arrt=dft.to_numpy()
                            
                            cT.append(1000*arrt[memoria,variable*2])
                            scT.append(arrt[memoria,variable*2+1]*1000)    
                            n=n+1
                            Pp.append(P[h])
                            V.append(Vp[h])
                            #print(cT)
                        h=h+1
                

    #fig=plt.figure(figsize=(9,5),constrained_layout=True)
    plt.rcParams["figure.figsize"] = (9,7.3)
    plt.rcParams["figure.constrained_layout.use"] = True
        
    plt.errorbar(Pp,cT,scT,ls='-',marker='o',color=colores[int(chip)+memoria], label='chip: '+chip+" "+var[bloque]+": "+str(caract[bloque][memoria]),capsize=3) 
    plt.title(bloques[bloque]+" memoria con "+var[bloque]+": "+str(caract[bloque][memoria]),fontsize=27)
    plt.legend(loc="upper right",fontsize=22)
    plt.xlabel('P ($W/m^2$)',fontsize=27)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=16)
        
    
    if variable==0:
        vari='Vin'
        plt.ylabel('V (V)',fontsize=27)
    if variable==1:
        vari='a'
        plt.ylabel('Tiempo (ms)',fontsize=27)
    if variable==2:
        vari='Vhold'
        plt.ylabel('V (V)',fontsize=27)
    if variable==3:
        vari='c'
        plt.ylabel('I/c (V/s)',fontsize=27)
        
    #plt.savefig(path+"T_"+NMP+'/chip_'+chip+'_'+vari+"_"+bloques[bloque]+"_"+str(caract[bloque][memoria])+'.png')
    #plt.savefig(path+"T_"+NMP+'/chip_'+chip+'_'+vari+"_"+bloques[bloque]+'_'+str(caract[bloque][memoria])+'.pdf',format='pdf')

def voltajes_filtros(carpeta,variable,bloque,memoria):
    
    carpeta='T_'+str(carpeta)
    folder="Datos/"
    ajst="ajust/"
    medias="MEDIAS/"

    #la carpeta basicamentes es elegir NCAP, MIM o PCAP
    path=folder+ajst+medias+carpeta+'/'
    # CARACTERISTICAS MEMORIAS
    wes=[[0.5,0.5,0.5,0.5],[4,2,1,6],[0.5,0.5,0.5,0.5],[0.5,1,2,4],
         [1,1,1,1],[1,1,1,1],[0.5,1,2,4],[4,2,1,6]]
    les=[[4,2,1,0.5],[0.5,0.5,0.5,0.5],[2,1,0.5,4],[0.5,0.5,0.5,0.5],
         [0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[1,1,1,1],[0.5,0.5,0.5,0.5]]
    mims=[[160,160,160,160],[160,160,160,160],[160,160,160,160],[160,160,160,160],
         [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[160,160,160,160],[160,160,160,160]]
    
    caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
            [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
    var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    
    #bloques de memorias separadas por la variable que cambia en cada caso
    ws=[1,3,6,7]
    ls=[0,2]
    mim=[4,5]
    
    #Variable que cambia en cada caso
    #var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    #dts=[]
    #times=[]
    
    cT=[]
    scT=[]
    Vp=[]
    V=[]
    c0=[]
    sc0=[]
    colour=[]
    label=[]
    #archivo_mim=0
    #Leemos todos los archivos de la carpeta para 
    #hacer una media de los valores de cada chip
    for i in os.listdir(path):
        if 'csv' in i and 'filtro' not in i and 'V' not in i:
            if 'V' not in i:
                dft=pd.read_csv(path+i)
                arrt=dft.to_numpy()
                for data in arrt[:,variable*2]:
                    c0.append(data*1000)
                for data in arrt[:,variable*2+1]:
                    sc0.append(data*1000)    

    h=0
    for i in os.listdir(path):
        if 'csv' in i and 'filtro' in i:
            print(i)
            c=[]
            sc=[]
            if "525" in i:
                colour.append('#4aff00')
                label.append("525")                  
            elif "470" in i:
                colour.append('#00a9ff')
                label.append("470")
            elif "660" in i:
                colour.append('#ff0000')   
                label.append("660")
            
            dft=pd.read_csv(path+i)
            arrt=dft.to_numpy()
            #archivo_mim=1
            for data in arrt[:,variable*2]:
                c.append(data*1000)
            for data in arrt[:,variable*2+1]:
                sc.append(data*1000)   
            #print(Vp)
            #print(cT)
            #print(i)
            cT.append(c)
            scT.append(sc)
    
    bloques=['NMOS','NMOS_WIDTH','PMOS','TG','TG_VAR_MIM','NMOS_VAR_MIM','TG_L_1u','PMOS_WIDTH']
    #fig=plt.figure(figsize=(9,5),constrained_layout=True)
    plt.errorbar(caract[bloque],c0[bloque*4:bloque*4+4],sc0[bloque*4:bloque*4+4],ls='',marker='o',color='k', label="Sin filtro",capsize=3) 
    for i in range(0,3):
        plt.errorbar(caract[bloque],cT[i][bloque*4:bloque*4+4],scT[i][bloque*4:bloque*4+4],ls='',marker='o',color=colour[i], label="Filtro BP"+label[i],capsize=3) 
    plt.title(bloques[bloque])
    plt.legend(loc="upper right")
    if var[bloque]=="mim":
        plt.xlabel("C (mf)")
    else:
        plt.xlabel(var[bloque]+" $\mu m$")

        
    
    if variable==0:
        vari='Vin'
        plt.ylabel('V (V)')
    if variable==1:
        vari='a'
        plt.ylabel('Tiempo (ms)')
    if variable==2:
        vari='Vhold'
        plt.ylabel('V (V)')
    if variable==3:
        vari='c'
        plt.ylabel('I/c (V/s)')

    #plt.savefig(path+carpeta+'filtros_'+vari+"_"+bloques[bloque]+'.png')
    #plt.savefig(path+carpeta+'filtros_'+vari+"_"+bloques[bloque]+'.pdf',format='pdf')

'''

bloque=int(input("Número del bloque a estudiar: (0-7) "))
memoria=input("Memoria: (0-3 o t para todas) ") 

file=input("Nombre de carpeta (sin T_): ")

estudiar=input("Total/Relativos/Chip (T/R/nº chip/0 para todos) ")
'''

memoria="t"
file="MIM_8500masv"
#estudiar="R"
for withs in ("_sin1",""):
    if withs=="_sin1":
        sin=1
    else:
        sin=0
    for estudiar in ("R","T"):
        for bloque in range(0,8):
            plt.close("all")
                    
            if file[0]=="N":
                NMP="NCAP"
            if file[0]=='P':
                NMP="PCAP"
            if file[0]=="M":
                NMP="MIM"
            if estudiar=="T":
                if memoria=="t":
                    for i in range(sin,4):
                        voltajes(file,3,bloque,i)
                    plt.savefig(path+"T_"+file+"/"+NMP+"_"+bloques[bloque]+withs+'.png')
                    plt.savefig(path+"T_"+file+"/"+NMP+"_"+bloques[bloque]+withs+'.pdf',format='pdf')
                else:
                    voltajes(file,3,bloque,int(memoria))
            
            elif estudiar=="R":
                if memoria=="t":
                    for i in range(sin,4):
                        voltajes_relativos(file,3,bloque,i) 
                    plt.savefig(path+"T_"+file+"/"+NMP+"_"+bloques[bloque]+'_relativos'+withs+'.png')
                    plt.savefig(path+"T_"+file+"/"+NMP+"_"+bloques[bloque]+'_relativos'+withs+'.pdf',format='pdf')
                else:
                    voltajes_relativos(file,3,bloque,int(memoria))
                    
            elif estudiar=="0":
                if memoria=="t":
                    for chip in range(0,16):
                        for i in range(0,4):
                            voltajes_chip(file,3,bloque,i,chip) 
                else:
                    for chip in range(0,16):
                        voltajes_chip(file,3,bloque,int(memoria),chip)
                    
            else:
                if memoria=="t":
                    for i in range(0,4):
                        voltajes_chip(file,3,bloque,i,int(estudiar)) 
                else:
                    voltajes_chip(file,3,bloque,int(memoria),int(estudiar))


'''

#graf=input('Nombre de la carpeta (variando el voltaje): ')
#ajstr=int(input("Variable: (0-Vin 1-a 2-Vhold 3-c) "))
#caracts(graf, ajstr)
def comparar(memoria):
    carpeta='NCAP_sin2'
    folder="Datos/"
    ajst="ajust/"
    
    path=folder+ajst+carpeta+'/'
    # CARACTERISTICAS MEMORIAS
    wes=[[0.5,0.5,0.5,0.5],[4,2,1,6],[0.5,0.5,0.5,0.5],[0.5,1,2,4],
         [1,1,1,1],[1,1,1,1],[0.5,1,2,4],[4,2,1,6]]
    les=[[4,2,1,0.5],[0.5,0.5,0.5,0.5],[2,1,0.5,4],[0.5,0.5,0.5,0.5],
         [0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[1,1,1,1],[0.5,0.5,0.5,0.5]]
    mims=[[160,160,160,160],[160,160,160,160],[160,160,160,160],[160,160,160,160],
         [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[160,160,160,160],[160,160,160,160]]
    
    caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
            [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
    var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    
    #bloques de memorias separadas por la variable que cambia en cada caso
    ws=[1,3,6,7]
    ls=[0,2]
    mim=[4,5]
    
    #Variable que cambia en cada caso
    #var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    #dts=[]
    #times=[]
    V=[]
    val=[]
    sval=[]
    
    n=0
    archivo_mim=0
    #Leemos todos los archivos de la carpeta para 
    #hacer una media de los valores de cada chip
    for i in os.listdir(path):
        #Cojemos solo archivos de datos y que sean sin filtros o sin luz
        aux=[]
        saux=[]
        if 'csv' in i and 'f' not in i:
            if 'z' in i:
                ajstr=0
            else:
                ajstr=1
                
            if i[0]=='M':
                V.append(i[-6:-4])
                archivo_mim=1
            else:
                V.append(i[-6:-4])
    
            #Leemos cada archivo y almacenamos los datos
            dft=pd.read_csv(path+i)
            arrt=dft.to_numpy()
            for data in arrt[:]:
                if ajstr==1:
                    dts=[data[0],data[2],data[4],data[6]]
                    sdts=[data[1],data[3],data[5],data[7]]
                if ajstr==1:
                    dts=[data[0],data[2],data[4]]
                    sdts=[data[1],data[3],data[5]]
                aux.append(dts)
                saux.append(sdts)
            n=n+1   
        val.append(aux)
        sval.append(saux)
    
     
    time=np.linspace(0, 1600, 1000)
    
    for i in range(0,3):
        if len(val[i*3][memoria])==3:
            y=simple(time,*val[i*3][memoria])
        else:
            y=luz1(time,*val[i*3][memoria])
        plt.plot(time,y,label=os.listdir(path)[i*3])
        plt.legend(loc=0)
    
    
   '''  
 


########## PRUEBAS #################
'''  
#wps=[[0,0,0,0],[0,0,0,0],[0.5,0.5,0.5,0.5],[1,1,1,1],[1,1,1,1],[0,0,0,0],[1,1,1,1],[4,2,1,6]]
#wns=[[0.5,0.5,0.5,0.5],[4,2,1,6],[0,0,0,0],[0.5,1,2,4],[1,1,1,1],[1,1,1,1],[0.5,1,2,4],[0,0,0,0]]   
#lns=[[4,2,1,0.5],[0.5,0.5,0.5,0.5],[0,0,0,0],[0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[1,1,1,1],[0,0,0,0]]
#lps=[[0,0,0,0],[0,0,0,0],[2,1,0.5,4],[0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5],[0,0,0,0],[1,1,1,1],[0.5,0.5,0.5,0.5]]
#Reorganizamos los datos 
bux=[]
sbux=[]

for j in range(0,32):
    aux=[]
    saux=[]
    for i in range(0,n):
        aux.append(cT[i][j])
        saux.append(scT[i][j])
    bux.append(aux)
    sbux.append(saux)
    
  
fig = plt.figure()
gs = fig.add_gridspec(2, 1, hspace=0, wspace=0)
axs=gs.subplots(sharey='row')
ylabels=['V/s'] 

colores=['g','b','k','r','orange','gold']
h=0
labels=['NMOS','PMOS','TG','TG']
for i in ls:
    for j in range(0,n):
        axs[h].plot(les[i],cT[j][i*4:i*4+4],
    marker='o',color=colores[j], label=labels[h]+' L='+str(les[i][0])+' V='+str(V[j]))
    
    axs[h].legend(loc=0,ncol=2, fancybox=True, shadow=True,fontsize=8)
    h=h+1

axs[1].set(xlabel='W $(\mu m)$')
axs[1].set(ylabel='W $(\mu m)$')
'''
