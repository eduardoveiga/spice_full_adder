#encoding: utf-8
from decimal import *
import os
import shutil
import re

# ---------------------------------------------------------------------------  #    Funçôes
import random
def Rand():
    return 0.8

def Troca(copia,seed,wire):
    r=random.Random()
    qcrit = r.randint(1,500)
    startime = r.randint(1,400)
    amplitudeini = r.randint(1,1000)
    startime1 = startime + 0.01
    amplitudeend = r.randint(1,1000)
    
    copia[19] = 'iexp 0 aux exp(0 '+str(qcrit)+'u '+str(startime)+'p '+str(amplitudeini)+'p '+str(startime1)+'p '+str(amplitudeend)+'p)\n'
    copia[21] = 'vobs aux '+wire+' 0\n'
    


def Salva_Resultados (arquivo,i,transistor, passou,signals, ciclo):
    count = 0
    etapa = 0
    
    resultados=os.popen('ngspice '+arquivo).readlines()
    #print(resultados)
    for r,resultado in enumerate(resultados):
        regex=re.split("targ= |trig= ",resultado)
        if len(regex) != 3:
            continue
        targ=float(regex[1].strip())
        trig=float(regex[2].strip(' \n'))

        print("count",count)
        print ("diference")
        print(targ - signals[count][0])
        print(abs(targ - signals[count][0]) > abs(ciclo))
        print(trig - signals[count][1])
        print(abs(trig - signals[count][1]) > abs(ciclo))

        if abs(targ - signals[count][0]) > abs(ciclo):
            continue
        if abs(trig - signals[count][1]) > abs(ciclo):
            continue
        count = count + 1
        if count != 5:
            continue
        etapa  = 1
        
    passou[i] = passou[i] + etapa
    return passou
	


def Volume_de_arquivos(copia, transistor, numero,seed,wire):
        nome_arquivo =  str(transistor)+'_'+ str(numero) + '.cir'
        arquivo_copia = open(nome_arquivo, 'w')
        Troca(copia,seed,wire)
        arquivo_copia.writelines(copia)
        return nome_arquivo
def main():
    

    nome_arquivo = 'spice_h.cir'
    signals = [[6.128101e-10,2.053672e-10],[1.012790e-09,8.221390e-10],[1.605582e-09,1.405441e-09],[8.228000e-10,6.171893e-10],[1.618237e-09,1.023539e-09]]
    ciclo = 2e-10
    arquivo = open(nome_arquivo, 'r')
    leitura = []
    copia = []
    leitura = arquivo.readlines()
    copia = leitura
    numero = 100
    seed = 42
    transistores = ['T1','T2','T3','T4','T5', 'T6', 'T7', 'T8', 'T9', 'T10','T11','T12','T13','T14','T15', 'T16', 'T17', 'T18', 'T19', 'T20','T21','T22','T23','T24','T25', 'T26', 'T27', 'T28', 'T29', 'T30',]
    #transistores = ['T30']
    wires  = ['w12','w12','w34','w34','w34','w34','w78','w78','w910','w910','w1112','w1112','sum','sum','w1516','w1516','sum','sum','w1920','w1920','w910','w910','w2324','w2324','w2526','w2526','w2627','w2627','carry','carry']
    #wires = ['carry']
    print('TRANSISTORES',len(transistores))
    print('WIRES',len(wires))
              
    passou = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    arquivo.close()

    for i,transistor in enumerate(transistores):
        for j in range(0,numero):
            wire = wires[i]
            nome_arquivo2 = Volume_de_arquivos(copia,i,j,seed,wire)
            passou=Salva_Resultados(nome_arquivo2,i,transistor,passou, signals, ciclo)
    print(passou)
print ("------------------------Inicio-------------------------------")

main()



print ('------------------------Fim-------------------------------------')










