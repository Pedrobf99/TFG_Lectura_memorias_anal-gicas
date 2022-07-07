#!/usr/bin/python
#-*- coding: utf-8 -*-

import numpy as np
import scipy.optimize as so
from scipy.stats import chisquare
import matplotlib.pylab as plt
from math import log10,floor
import os
import pandas as pd
import warnings

def round_it(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def redondear(a):
    if a>=1:
        red=round(a,2)
    else:
        red=round_it(a,2)
    return red
    
def regresionSimple(x,y):
    n=len(x)
    sx=sum(x); sy=sum(y); xx=np.dot(x,x); yy=np.dot(y,y); xy=np.dot(x,y); st=0
    denom=(n*xx-sx**2)
    b=(n*xy-sx*sy)/denom
    a=(xx*sy-sx*xy)/denom
    for i in range(0,len(x)):
        	st=st+(y[i]-a-b*x[i])**2
    s=np.sqrt(st/(n-2))
    sa=s*np.sqrt(xx/(n*xx-sx**2))
    sb=s*np.sqrt(n/(n*xx-sx**2))
    r=(n*xy-sx*sy)/np.sqrt((n*xx-sx**2)*(n*yy-sy**2))
    return [a,b,sa,sb,r,s]

def rsq(varf,varm):
    return (1-varf/varm)
# Tipo de ajuste al que sometemos nuestros datos
def simple_og(t,Vin,a,Vhold):
    return Vin*np.exp(-t/a)+Vhold
def luz1(t,Vin,a,Vhold,c):
    return Vin*np.exp(-t/a)+Vhold+c*t
def simple(t,Vin,a,c):
    return Vin*(1-np.exp(-t/a))+c*t
'''
def luz2(t,Vin,a,Vhold,c,Vin2,a2):
    return Vin*np.exp(-t/a)+Vhold+c*t+Vin2*np.exp(-t/a2)
'''
#Realizamos el ajuste y nos permite graficar los valores y la función resultado
def ajuste(t_final,b,bounds,mem,ajust):
    
    if ajust==0:
        if bounds:
            coef,cov=so.curve_fit(simple,t_final,b,bounds=bounds)
        else:
            coef,cov=so.curve_fit(simple,t_final,b,bounds=[[0.1,0,0],[4,1.9,2]])
            
    if ajust==1:
        if bounds:
            coef,cov=so.curve_fit(luz1,t_final,b,bounds=bounds)
        else:
            coef,cov=so.curve_fit(luz1,t_final,b,bounds=[[0.1,0,0,-100],[1.2,200,2,0]])    
            
    perr = np.sqrt(np.diag(cov))
    
    '''
    cor=np.zeros([3,3])
    for j in range(0,3):
        for i in range(0,3):
            cor[i][j]=(cov[i][j]/np.sqrt(cov[i][i]*cov[j][j]))
    a=cor[0][1]**2+cor[0][2]**2+cor[1][2]**2
    print(a)
    if a<1:
        print("Memoria: "+str(mem))
    '''
    #print("La matriz de correlacion es: "+'\n'+str(cor))
    return coef,perr

def ajuste_graph(t_final,b,filename,boundes,ajust):
    hs=[]
    
    if filename[17]=='N' or filename[17]=='P' or filename[17]=='M':
        chip=filename[14:16]+'/'
        memor=filename[17]
    else:
        chip=filename[14]+'/'
        memor=filename[16]
        
    ajustes=filename[:8]
    file=filename[8:]
    
    for j in range(0,8):
        for i in range(0,4):
            t_final1=t_final[i+j*4][1:]
            b1=b[i+j*4][1:]
            t1 = np.linspace(0, t_final1[-1]*1.1, 100)
            if ajust==0:
                if boundes:
                    coef,cov=so.curve_fit(simple,t_final1,b1,bounds=boundes)
                else:
                    coef,cov=so.curve_fit(simple,t_final1,b1,bounds=[[0.1,0,0],[4,1.9,2]])
                f=simple(t1,*coef)
                fexp=simple(np.array(t_final1),*coef)
                chi,p0=chisquare(b1,fexp,ddof=3)

            if ajust==1:
                if boundes:
                    coef,cov=so.curve_fit(luz1,t_final1,b1,bounds=boundes)
                else:
                    coef,cov=so.curve_fit(luz1,t_final1,b1,bounds=[[0.1,0,0,-100],[1.2,200,2,0]])   
                f=luz1(t1,*coef)
                fexp=luz1(np.array(t_final1),*coef)
                #print(b1)
                #print(fexp)
                chi,p0=chisquare(b1,fexp,ddof=4)
            
            hs.append([t1,f,chi,p0])
            #print("Chis: "+str(redondear(chi))+" p-value: "+str(p0))
            #print(p0)
    colours=['r','b','g','k']
    
    #fig, axs = plt.subplots(2, 4,figsize=(20,10))
    fig = plt.figure(figsize=(14,7),constrained_layout=True)
    gs = fig.add_gridspec(2, 4, hspace=0.2,wspace=0.1)
    axs=gs.subplots(sharex='col')    
    #############################  SELN  ###############################
    
    sV=5/1024*1/np.sqrt(12)
    
    labels=['4','2','1','0.5']
    for i in range(0,4):
        axs[0, 0].plot(hs[i][0],hs[i][1],color=colours[i], label='Ln:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i][2])))
        #axs[0, 0].errorbar(t_final[i],b[i],sV,ls='',marker='o', markersize=1,color=colours[i])
        axs[0, 0].plot(t_final[i],b[i],ls='',marker='o', markersize=1,color=colours[i])

    axs[0, 0].legend(loc="upper right")
    axs[0, 0].set_title('NMOS', fontsize=15)
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[0, 1].plot(hs[i+4][0],hs[i+4][1],color=colours[i], label='Wn:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+4][2])))
        #axs[0, 1].errorbar(t_final[i+4],b[i+4],sV,ls='', markersize=1,marker='o',color=colours[i])
        axs[0, 1].plot(t_final[i+4],b[i+4],ls='', markersize=1,marker='o',color=colours[i])

    axs[0, 1].legend(loc="upper right")
    axs[0, 1].set_title('NMOS_WIDTH', fontsize=15)
    
    labels=['2','1','0.5','4']
    for i in range(0,4):
        axs[0, 2].plot(hs[i+8][0],hs[i+8][1],color=colours[i], label='Lp:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+8][2])))
        #axs[0, 2].errorbar(t_final[i+8],b[i+8],sV,ls='', markersize=1,marker='o',color=colours[i])
        axs[0, 2].plot(t_final[i+8],b[i+8],ls='', markersize=1,marker='o',color=colours[i])
    
    axs[0, 2].legend(loc="upper right")
    axs[0, 2].set_title('PMOS', fontsize=15)
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[0, 3].plot(hs[i+12][0],hs[i+12][1],color=colours[i], label='Wn:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+12][2])))
        #axs[0, 3].errorbar(t_final[i+12],b[i+12],sV, markersize=1,ls='',marker='o',color=colours[i])
        axs[0, 3].plot(t_final[i+12],b[i+12],ls='', markersize=1,marker='o',color=colours[i])

    axs[0, 3].legend(loc="upper right")
    axs[0, 3].set_title('TG', fontsize=15)
    
    #############################  SEL  ###############################
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 0].plot(hs[i+16][0],hs[i+16][1],color=colours[i], label='mim:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+16][2])))
        #axs[1, 0].errorbar(t_final[i+16],b[i+16],sV, markersize=1,ls='',marker='o',color=colours[i])
        axs[1, 0].plot(t_final[i+16],b[i+16],ls='', markersize=1,marker='o',color=colours[i])

    axs[1, 0].legend(loc="upper right")
    axs[1, 0].set_title('TG_VAR_MIM', fontsize=15)
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 1].plot(hs[i+20][0],hs[i+20][1],color=colours[i], label='mim:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+20][2])))
        #axs[1, 1].errorbar(t_final[i+20],b[i+20],sV,ls='', markersize=1,marker='o',color=colours[i])
        axs[1, 1].plot(t_final[i+20],b[i+20],ls='', markersize=1,marker='o',color=colours[i])

    axs[1, 1].legend(loc="upper right")
    axs[1, 1].set_title('NMOS_VAR_MIM', fontsize=15)
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[1, 2].plot(hs[i+24][0],hs[i+24][1],color=colours[i], label='Wn:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+24][2])))
        #axs[1, 2].errorbar(t_final[i+24],b[i+24],sV,ls='', markersize=1,marker='o',color=colours[i])
        axs[1, 2].plot(t_final[i+24],b[i+24],ls='', markersize=1,marker='o',color=colours[i])

    axs[1, 2].legend(loc="upper right")
    axs[1, 2].set_title('TG_L_1u', fontsize=15)
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[1, 3].plot(hs[i+28][0],hs[i+28][1],color=colours[i], label='Wp:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+28][2])))
        #axs[1, 3].errorbar(t_final[i+28],b[i+28],sV,ls='', markersize=1,marker='o',color=colours[i])
        axs[1, 3].plot(t_final[i+28],b[i+28],ls='', markersize=1,marker='o',color=colours[i])

    axs[1, 3].legend(loc="upper right")
    axs[1, 3].set_title('PMOS_WIDTH', fontsize=15)
    
    for ax in axs[1].flat:
        #ax.set(xlabel='Tiempo (ms)', labelsize=15)
        ax.set_xlabel('Tiempo (ms)', fontsize=15)
    

        
    ejes=[axs[0,0],axs[1,0]]
    for ax in ejes:
        ax.set_ylabel('Voltaje (V)', fontsize=15)
        #ax.set(ylabel='Voltaje (V)', labelsize=15)
        

    for i in range(0,4):
        for j in range(0,2):
            axs[j,i].tick_params(axis='y', labelsize=15)
            axs[j,i].tick_params(axis='x', labelsize=15)
            
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    '''
    for ax in axs.flat:
        ax.label_outer()
    '''
    if memor=="N":
        bloque='NCAP'
    elif memor=="M":
        bloque='MIM'
    elif memor=="P":
        bloque='PCAP'
    else:
        bloque=memor
    
    path=ajustes+chip+bloque+'/'
    if not os.path.exists(path):
        os.makedirs(path)
    
    fig.savefig(ajustes+chip+bloque+'/'+file+'_error.png')

    fig.savefig(ajustes+chip+bloque+'/'+file+'_error.pdf',format='pdf')
    
    return 'Nombre de la gráfica: '+file+'_error.png'



def regs(caract,valores,ajstr):
    vari=[]
    ajstra=ajstr+3
    for j in range(0,ajstra):
        ass=[]
        bs=[]
        sas=[]
        sbs=[]
        rs=[]
        ss=[]
        for i in range(0,8):
            a,b,sa,sb,r,s=regresionSimple(caract[i], valores[i][j*2]) #regresion lineal de cada 4 valores
            
            ass.append(a)
            bs.append(b)
            sas.append(sa)
            sbs.append(sb)
            rs.append(r**2)
            ss.append(s)
            
        vari.append([ass,bs,sas,sbs,rs,ss]) 
        #recogemos todos los valores de las 
        #regresiones de cada variable vin,rc,vhold
    if ajstr==0:
        return vari[0],vari[1],vari[2]
    if ajstr==1:
        return vari[0],vari[1],vari[2],vari[3]
    
def f(x,a,b):
    return x*b+a

def plotss(cars,regres,var,ajstr):
    hs=[]
    ajstra=ajstr+3
    for j in range(0,ajstra):
        for i in range(0,8):
            if var[i]=='mim':
                x = np.linspace(0, 200, 30)
            else:
                x = np.linspace(0, 6, 30)
            a=regres[j][0][i]
            b=regres[j][1][i]
            h=f(x,a,b)
            
            hs.append([x,h])
    
    return hs

def regs2(wles,varia):
    vari=[]
    #ajstra=ajstr+3

    ass=[]
    bs=[]
    sas=[]
    sbs=[]
    rs=[]
    ss=[]
    for j in range(0,len(varia)): #Numero de archivos (voltajes, distancias...)
        ass=[]
        bs=[]
        sas=[]
        sbs=[]
        rs=[]
        ss=[]
        for i in range(0,8): #Recorremos la matriz de cada tipo de memoria
        #Dondo hemos almacenado la variable que cambia en cada caso
           
            a,b,sa,sb,r,s=regresionSimple(wles[i], varia[j][i*4:i*4+4]) #regresion lineal de cada 4 valores
            
            ass.append(a)
            bs.append(b)
            sas.append(sa)
            sbs.append(sb)
            rs.append(r**2)
            ss.append(s)
            
        vari.append([ass,bs,sas,sbs,rs,ss])
        #recogemos todos los valores de las 
        #regresiones para un voltaje, distancia...
    
    
    return vari

def plotss2(cars,regres,var):
    hs=[]
    for j in range(0,len(regres)):
        file=[]
        for i in range(0,8):
            if var[i]=='mim':
                x = np.linspace(0, 200, 30)
            else:
                x = np.linspace(0, 6, 30)
            a=regres[j][0][i]
            b=regres[j][1][i]
            h=f(x,a,b)
            
            file.append([x,h])
        hs.append(file)
    return hs


def bounds(filename,memoria):
    folder="Datos/"
    ajst="ajust/"
    
    if filename[17]=='N' or filename[17]=='P' or filename[17]=='M':
        chip=filename[14:16]
        mem=filename[17]
        decena=1
    else:
        chip=filename[14]
        mem=filename[16]
        decena=0
        
    #ajustes=filename[:8]
    #file=filename[8:]
    #chip=file[14]
    #mem=file[16]
    #luz=file[-5]
    #ajstr=1
    if mem=="N":
        carpeta="NCAP_0"
    elif mem=="M":
        carpeta="MIM_0"
    elif mem=="P":
        carpeta="PCAP_0"
    path=folder+ajst+carpeta+'/'
    
 
    #V=[]
    val=[]
    sval=[]
    
    for i in os.listdir(path):
        if 'csv' in i:
            if decena==0 and i[14]==chip:
                #Leemos cada archivo y almacenamos los datos
                dft=pd.read_csv(path+i)
                arrt=dft.to_numpy()
                
                dts=[arrt[memoria][0],arrt[memoria][2],arrt[memoria][4]]
                sdts=[arrt[memoria][1]*2,arrt[memoria][3]*2,arrt[memoria][5]*2]
                
                val.append(dts)
                sval.append(sdts)
                boundes=[[dts[0]-sdts[0],dts[1]-sdts[1],dts[2]-sdts[2],-50],[dts[0]+sdts[0],dts[1]+sdts[1],dts[2]+sdts[2],50]]    
            elif decena==1 and i[14:16]==chip:
                #Leemos cada archivo y almacenamos los datos
                dft=pd.read_csv(path+i)
                arrt=dft.to_numpy()
                
                dts=[arrt[memoria][0],arrt[memoria][2],arrt[memoria][4]]
                sdts=[arrt[memoria][1]*2,arrt[memoria][3]*2,arrt[memoria][5]*2]
                
                val.append(dts)
                sval.append(sdts)
                boundes=[[dts[0]-sdts[0],dts[1]-sdts[1],dts[2]-sdts[2],-50],[dts[0]+sdts[0],dts[1]+sdts[1],dts[2]+sdts[2],50]]   
    return boundes

def ajuste_graph2(t_final,b,filename,boundes,ajust):
    hs=[]
    if filename[17]=='N' or filename[17]=='P' or filename[17]=='M':
        chip=filename[14:16]+'/'
        memor=filename[17]
    else:
        chip=filename[14]+'/'
        memor=filename[16]
        
    ajustes=filename[:8]
    file=filename[8:]
    #print(filename)
    
    for j in range(0,8):
        for i in range(0,4):
            t_final1=t_final[i+j*4][1:]
            b1=b[i+j*4][1:]
            t1 = np.linspace(0, t_final1[-1]*1.1, 100)
            if ajust==0:
                if boundes:
                    coef,cov=so.curve_fit(simple,t_final1,b1,bounds=boundes)
                else:
                    coef,cov=so.curve_fit(simple,t_final1,b1,bounds=[[0.1,0,0],[4,1.9,2]])
                f=simple(t1,*coef)
                fexp=simple(np.array(t_final1),*coef)
                chi,p0=chisquare(b1,fexp,ddof=3)

            if ajust==1:
                boundes=bounds(filename,j*4+i)
                coef,cov=so.curve_fit(luz1,t_final1,b1,bounds=boundes)   
                f=luz1(t1,*coef)
                fexp=luz1(np.array(t_final1),*coef)
                chi,p0=chisquare(b1,fexp,ddof=4)
            
            hs.append([t1,f,chi,p0])
            #print("Chis: "+str(redondear(chi))+" p-value: "+str(p0))
            #print(p0)
    colours=['r','b','g','k']
    
    #fig, axs = plt.subplots(2, 4,figsize=(20,10))
    fig = plt.figure(figsize=(19,9.5),constrained_layout=True)
    gs = fig.add_gridspec(2, 4, hspace=0.2,wspace=0.1)
    axs=gs.subplots(sharex='col')    
    #############################  SELN  ###############################
    
    labels=['4','2','1','0.5']
    for i in range(0,4):
        axs[0, 0].plot(hs[i][0],hs[i][1],color=colours[i], label='Ln:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i][2])))
        axs[0, 0].plot(t_final[i],b[i],ls='',marker='o', markersize=1,color=colours[i])

    axs[0, 0].legend(loc="upper right")
    axs[0, 0].set_title('NMOS')
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[0, 1].plot(hs[i+4][0],hs[i+4][1],color=colours[i], label='Wn:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+4][2])))
        axs[0, 1].plot(t_final[i+4],b[i+4],ls='', markersize=1,marker='o',color=colours[i])
    axs[0, 1].legend(loc="upper right")
    axs[0, 1].set_title('NMOS_WIDTH')
    
    labels=['2','1','0.5','4']
    for i in range(0,4):
        axs[0, 2].plot(hs[i+8][0],hs[i+8][1],color=colours[i], label='Lp:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+8][2])))
        axs[0, 2].plot(t_final[i+8],b[i+8],ls='', markersize=1,marker='o',color=colours[i])
    axs[0, 2].legend(loc="upper right")
    axs[0, 2].set_title('PMOS')
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[0, 3].plot(hs[i+12][0],hs[i+12][1],color=colours[i], label='Wn:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+12][2])))
        axs[0, 3].plot(t_final[i+12],b[i+12], markersize=1,ls='',marker='o',color=colours[i])
    axs[0, 3].legend(loc="upper right")
    axs[0, 3].set_title('TG')
    
    #############################  SEL  ###############################
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 0].plot(hs[i+16][0],hs[i+16][1],color=colours[i], label='mim:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+16][2])))
        axs[1, 0].plot(t_final[i+16],b[i+16], markersize=1,ls='',marker='o',color=colours[i])
    axs[1, 0].legend(loc="upper right")
    axs[1, 0].set_title('TG_VAR_MIM')
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 1].plot(hs[i+20][0],hs[i+20][1],color=colours[i], label='mim:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+20][2])))
        axs[1, 1].plot(t_final[i+20],b[i+20],ls='', markersize=1,marker='o',color=colours[i])
    axs[1, 1].legend(loc="upper right")
    axs[1, 1].set_title('NMOS_VAR_MIM')
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[1, 2].plot(hs[i+24][0],hs[i+24][1],color=colours[i], label='Wn:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+24][2])))
        axs[1, 2].plot(t_final[i+24],b[i+24],ls='', markersize=1,marker='o',color=colours[i])
    axs[1, 2].legend(loc="upper right")
    axs[1, 2].set_title('TG_L_1u')
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[1, 3].plot(hs[i+28][0],hs[i+28][1],color=colours[i], label='Wp:'+labels[i]+'; $\chi^2= $'+str(redondear(hs[i+28][2])))
        axs[1, 3].plot(t_final[i+28],b[i+28],ls='', markersize=1,marker='o',color=colours[i])
    axs[1, 3].legend(loc="upper right")
    axs[1, 3].set_title('PMOS_WIDTH')
    
    
    
    for ax in axs[1].flat:
        ax.set(xlabel='Tiempo (ms)')
    ejes=[axs[0,0],axs[1,0]]
    for ax in ejes:
        ax.set(ylabel='Voltaje (V)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    '''
    for ax in axs.flat:
        ax.label_outer()
    '''
    if memor=="N":
        bloque='NCAP'
    elif memor=="M":
        bloque='MIM'
    elif memor=="P":
        bloque='PCAP'
    else:
        bloque=memor
    
    path=ajustes+chip+bloque+'bound/'
    if not os.path.exists(path):
        os.makedirs(path)
    
    fig.savefig(ajustes+chip+bloque+'bound/'+file+'_ajustesboundes.png')

    fig.savefig(ajustes+chip+bloque+'bound/'+file+'_ajustesboundes.pdf',format='pdf')
    
    return 'Nombre de la gráfica: '+file+'_ajustes.png'
