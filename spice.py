#encoding: utf-8
from decimal import *
import os
import shutil
import re

# ---------------------------------------------------------------------------  #    Funçôes
import random
def Rand():
    return 0.8

def Troca(copia,wire,sinal_logico,qcrit):
    if sinal_logico == 0:
        copia[19] = 'iexp 0 aux exp(0 '+str(qcrit)+'u  200p 10p 200.01p 320p)\n'
    else:
        copia[19] = 'iexp aux 0 exp(0 '+str(qcrit)+'u  200p 10p 200.01p 320p)\n'


    copia[21] = 'vobs aux '+wire+' 0\n'
    
def Troca_input(copia,a,b,c):
    copia[10] = 'Va wa GND ' + str(a)+'\n'
    copia[11] = 'Vb wb GND ' + str(b)+'\n'
    copia[12] = 'Vc wc GND ' + str(c)+'\n'
def Salva_Resultados (arquivo,i,node, passou):
    etapa = 1
    falhou = False
    
    resultados=os.popen('ngspice '+arquivo).readlines()
    #print(resultados)
    for r,resultado in enumerate(resultados):
        regex=re.split("targ= |trig= ",resultado)
        if len(regex) >1:
            falhou = True
            etapa = 0
    passou[node] = passou[node] + etapa
    print(etapa,falhou)
    return passou,falhou
	


def Volume_de_arquivos(copia, inputs,node,sinal_logico,qcrit):
        nome_arquivo =  inputs+'_'+node+'_'+ str(qcrit) + '.cir'
        arquivo_copia = open(nome_arquivo, 'w')
        Troca(copia,node, sinal_logico,qcrit)
        arquivo_copia.writelines(copia)
        return nome_arquivo
def Volume_de_arquivos_input(copia, a,b,c):
        nome_arquivo =  str(a)+str(b)+str(c) + '.cir'
        arquivo_copia = open(nome_arquivo, 'w')
        Troca_input(copia,a,b,c)
        arquivo_copia.writelines(copia)
        return nome_arquivo
def main():
    
    nome_arquivo = 'spice_h3.cir'
    #signals = [[6.128101e-10,2.053672e-10],[1.012790e-09,8.221390e-10],[1.605582e-09,1.405441e-09],[8.228000e-10,6.171893e-10],[1.618237e-09,1.023539e-09]]
    #ciclo = 2e-10
    arquivo = open(nome_arquivo, 'r')
    leitura = []
    copia = []
    leitura = arquivo.readlines()
    copia = leitura
    amplitude_inicial = 0
    amplitude_final = 1000
    iteracoes = 100
    passo = int((amplitude_final - amplitude_inicial)/iteracoes)
    amplitudes  = [*range(amplitude_inicial,amplitude_final, passo)]
    passou_global = {}
    amplitudes_de_falha_global = {}
    
    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                nome_arquivo2 = Volume_de_arquivos_input(copia,a,b,c)
                print (nome_arquivo2)
                saida=os.popen('ngspice '+nome_arquivo2).readlines()
                nodes_values =  {}
                transistores = ['T1','T2','T3','T4','T5', 'T6', 'T7', 'T8', 'T9', 'T10','T11','T12','T13','T14','T15', 'T16', 'T17', 'T18', 'T19', 'T20','T21','T22','T23','T24','T25', 'T26', 'T27', 'T28', 'T29', 'T30']
   
                wires  = ['w12','w12','w34','w34','w34','w34','w78','w78','w910','w910','w1112','w1112','sum','sum','w1516','w1516','sum','sum','w1920','w1920','w2122','w2122','w2324','w2324','w2526','w2526','w2627','w2627','carry','carry']
                nodes = list(dict.fromkeys(wires))
                print (nodes)

                for linha in  saida:
                    linha = linha.split()
                    if len(linha)>1 and linha[0] in wires:
                       if float(linha[1])>= 0.5:
                           nodes_values[linha[0]] = 1
                       else:
                           nodes_values[linha[0]] = 0

              
                passou = dict.fromkeys(wires,0)
                amplitudes_de_falha = dict.fromkeys(wires)
    
                arquivo.close()

#   for i,transistor in enumerate(transistores):
#       for j, amplitude in enumerate(amplitudes):
#           wire = wires[i]    
#           nome_arquivo2 = Volume_de_arquivos(copia,i,j,wire,nodes_values[wire],amplitude)
#           passou,falhou=Salva_Resultados(nome_arquivo2,i,transistor,passou)
#           if falhou == True:
#               amplitudes_de_falha[transistor] = amplitude
#               break

                for i,node in enumerate(nodes):
                    for j, amplitude in enumerate(amplitudes):
           # wire = wires[i]    
                        nome_arquivo2 = Volume_de_arquivos(copia,str(a)+str(b)+str(c),node,nodes_values[node],amplitude)
                        passou,falhou=Salva_Resultados(nome_arquivo2,i,node,passou)

                        if falhou == True:
                           amplitudes_de_falha[node] = amplitude
                           break

            
                passou_global[str(a)+str(b)+str(c)]  = passou
                amplitudes_de_falha_global[str(a)+str(b)+str(c)] = amplitudes_de_falha
    print(passou_global)
    print(" ")
    print(amplitudes_de_falha_global)
print ("------------------------Inicio-------------------------------")

main()



print ('------------------------Fim-------------------------------------')










