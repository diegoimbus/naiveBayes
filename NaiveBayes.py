# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 18:53:31 2018

"""
import pandas as pd
import math  
#importamos  las constentes que nos sirven para det prob 
dfApriori = pd.read_csv('apriori.csv')
dfCondicional = pd.read_csv('condicional.csv')
dfContinuas = pd.read_csv('continuas.csv')

def distNormal(x,mean,stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1/(math.sqrt(2*math.pi)*stdev)) * exponent

def ProbTotal(ProbApriori, ProbCondS, ProbCondBP, ProbCondCh, ProbNormalEdad,ProbNormalNa,ProbNormalK):
        return 10**(math.log10(ProbApriori)+math.log10(ProbCondS)+math.log10(ProbCondBP)+math.log10(ProbCondCh)+math.log10(ProbNormalEdad)+math.log10(ProbNormalNa)+math.log10(ProbNormalK))

#List Recovery
DrugACond = dfCondicional.iloc[0].tolist()
DrugBCond = dfCondicional.iloc[1].tolist()
DrugCCond = dfCondicional.iloc[2].tolist()
DrugXCond = dfCondicional.iloc[3].tolist()
DrugYCond = dfCondicional.iloc[4].tolist()


ContDrugA = dfContinuas.iloc[0].tolist()
ContDrugB = dfContinuas.iloc[1].tolist()
ContDrugC = dfContinuas.iloc[2].tolist()
ContDrugX = dfContinuas.iloc[3].tolist()
ContDrugY = dfContinuas.iloc[4].tolist()

#Abrimos valores incresados por usuario desde pag web
VEdad = float(input("Ingrese edad: "))
VSexo = raw_input("Ingrese sexo (F/M): ")
VBP = raw_input("Ingrese BP {HIGH, NORMAL, LOW}: ")
VCh = raw_input("Ingrese Cholesterol {HIGH, NORMAL, LOW}: ")
VNa = float(input("Ingrese Na: "))
VK = float(input("Ingrese K: "))
#SEXO
probSA=0
probSB=0
probSC=0
probSX=0
probSY=0

#BP
probBPA=0
probBPB=0
probBPC=0
probBPX=0
probBPY=0

#CH ALTO
probCHA=0
probCHB=0
probCHC=0
probCHX=0
probCHY=0

if (VSexo) == 'F':
    #SEXO CONDICIONAL FEMENINO
    probSA=DrugACond[1]
    probSB=DrugBCond[1]
    probSC=DrugCCond[1]
    probSX=DrugXCond[1]
    probSY=DrugYCond[1]

elif (VSexo)=='M':
    #SEXO CONDICIONAL MASCULINO
    probSA=DrugACond[2]
    probSB=DrugBCond[2]
    probSC=DrugCCond[2]
    probSX=DrugXCond[2]
    probSY=DrugYCond[2]

if (VBP) == 'HIGH':
    #BP CONDICIONAL ALTA
    probBPA=DrugACond[3]
    probBPB=DrugBCond[3]
    probBPC=DrugCCond[3]
    probBPX=DrugXCond[3]
    probBPY=DrugYCond[3]
                
elif (VBP) == 'NORMAL':
    #VP COND NORMAL
    probBPA=DrugACond[4]
    probBPB=DrugBCond[4]
    probBPC=DrugCCond[4]
    probBPX=DrugXCond[4]
    probBPY=DrugYCond[4]
                
elif(VBP) == 'LOW':
    #VP COND BAJA
    probBPA=DrugACond[5]
    probBPB=DrugBCond[5]
    probBPC=DrugCCond[5]
    probBPX=DrugXCond[5]
    probBPY=DrugYCond[5]

if (VCh) == 'HIGH':
    #CH COND ALTA
    probCHA=DrugACond[6]
    probCHB=DrugBCond[6]
    probCHC=DrugCCond[6]
    probCHX=DrugXCond[6]
    probCHY=DrugYCond[6]
elif (VCh) == 'NORMAL':
    #CH COND NORMAL
    probCHA=DrugACond[7]
    probCHB=DrugBCond[7]
    probCHC=DrugCCond[7]
    probCHX=DrugXCond[7]
    probCHY=DrugYCond[7]
elif (VCh) == 'LOW':
    #CH COND BAJA
    probCHA=DrugACond[8]
    probCHB=DrugBCond[8]
    probCHC=DrugCCond[8]
    probCHX=DrugXCond[8]
    probCHY=DrugYCond[8]
 # Valores TABLA 3
MediaEdadDA = ContDrugA[1]
MediaNaDA  = ContDrugA[3]
MediaKDA = ContDrugA[5]
VarEdadDA = ContDrugA[2]
VarNaDA = ContDrugA[4]
VarKDA = ContDrugA[6]

MediaEdadDB = ContDrugB[1]
MediaNaDB  = ContDrugB[3]
MediaKDB = ContDrugB[5]
VarEdadDB = ContDrugB[2]
VarNaDB = ContDrugB[4]
VarKDB = ContDrugB[6]

MediaEdadDC = ContDrugC[1]
MediaNaDC  = ContDrugC[3]
MediaKDC = ContDrugC[5]
VarEdadDC = ContDrugC[2]
VarNaDC = ContDrugC[4]
VarKDC = ContDrugC[6]

MediaEdadDX = ContDrugX[1]
MediaNaDX  = ContDrugX[3]
MediaKDX = ContDrugX[5]
VarEdadDX = ContDrugX[2]
VarNaDX = ContDrugX[4]
VarKDX = ContDrugX[6]
            
MediaEdadDY = ContDrugY[1]
MediaNaDY  = ContDrugY[3]
MediaKDY = ContDrugY[5]
VarEdadDY = ContDrugY[2]
VarNaDY = ContDrugY[4]
VarKDY = ContDrugY[6]    

            #DistNormal
ProbDistNormalDAEdad = distNormal(VEdad, MediaEdadDA, VarEdadDA )
ProbDistNormalDANa = distNormal(VNa, MediaNaDA, VarNaDA )
ProbDistNormalDAK = distNormal(VK, MediaKDA, VarKDA )   

ProbDistNormalDBEdad = distNormal(VEdad, MediaEdadDB, VarEdadDB )
ProbDistNormalDBNa = distNormal(VNa, MediaNaDB, VarNaDB )
ProbDistNormalDBK = distNormal(VK, MediaKDB, VarKDB )

ProbDistNormalDCEdad = distNormal(VEdad, MediaEdadDC, VarEdadDC )
ProbDistNormalDCNa = distNormal(VNa, MediaNaDC, VarNaDC )
ProbDistNormalDCK = distNormal(VK, MediaKDC, VarKDC )

ProbDistNormalDXEdad = distNormal(VEdad, MediaEdadDX, VarEdadDX )
ProbDistNormalDXNa = distNormal(VNa, MediaNaDX, VarNaDX )
ProbDistNormalDXK = distNormal(VK, MediaKDX, VarKDX )

ProbDistNormalDYEdad = distNormal(VEdad, MediaEdadDY, VarEdadDY )
ProbDistNormalDYNa = distNormal(VNa, MediaNaDY, VarNaDY )
ProbDistNormalDYK = distNormal(VK, MediaKDY, VarKDY )

#Valores a priori
p1 = dfApriori.iloc[0].tolist()
p2 = dfApriori.iloc[1].tolist()
p3 = dfApriori.iloc[2].tolist()
p4 = dfApriori.iloc[3].tolist()
p5 = dfApriori.iloc[4].tolist()

#Recuperamos ProbApriori, quitamos columnas de drogas
probAprioriA = p1[1]
probAprioriB = p2[1]
probAprioriC = p3[1]
probAprioriX = p4[1]
probAprioriY = p5[1]

#Calculamos la probabilidad total:
ProbTotal1 = ProbTotal(probAprioriA,probSA,probBPA,probCHA,ProbDistNormalDAEdad,ProbDistNormalDANa, ProbDistNormalDAK)
ProbTotal2 = ProbTotal(probAprioriB,probSB,probBPB,probCHB,ProbDistNormalDBEdad,ProbDistNormalDBNa, ProbDistNormalDBK)
ProbTotal3 = ProbTotal(probAprioriC,probSC,probBPC,probCHC,ProbDistNormalDCEdad,ProbDistNormalDCNa, ProbDistNormalDCK)
ProbTotal4 = ProbTotal(probAprioriX,probSX,probBPX,probCHX,ProbDistNormalDXEdad,ProbDistNormalDXNa, ProbDistNormalDXK)
ProbTotal5 = ProbTotal(probAprioriY,probSY,probBPY,probCHY,ProbDistNormalDYEdad,ProbDistNormalDYNa, ProbDistNormalDYK)

#Normalizacion de la prob total
SumTotal = ProbTotal1 + ProbTotal2 +ProbTotal3 +ProbTotal4 +ProbTotal5 
TOTALProbTotal1N = ProbTotal1 *100/ SumTotal
TOTALProbTotal2N = ProbTotal2 *100/ SumTotal
TOTALProbTotal3N = ProbTotal3 *100/ SumTotal
TOTALProbTotal4N = ProbTotal4 *100/ SumTotal
TOTALProbTotal5N = ProbTotal5 *100/ SumTotal

print("TOTALProbTotal1N: ",TOTALProbTotal1N)
print("TOTALProbTotal2N: ",TOTALProbTotal2N)
print("TOTALProbTotal3N: ",TOTALProbTotal3N)
print("TOTALProbTotal4N: ",TOTALProbTotal4N)
print("TOTALProbTotalN: ",TOTALProbTotal5N)
            
#Determinamos la prob mas alta
print("TODO FUNCIONA")
ClassResul = 0
if TOTALProbTotal1N>TOTALProbTotal2N and TOTALProbTotal1N>TOTALProbTotal3N and TOTALProbTotal1N>TOTALProbTotal4N and TOTALProbTotal1N>TOTALProbTotal5N:
    ClassResul = TOTALProbTotal1N
    print("Probabilidad mas alta pertenece a la Droga A y es: ", ClassResul)
if TOTALProbTotal2N>TOTALProbTotal3N and TOTALProbTotal2N>TOTALProbTotal4N and TOTALProbTotal2N>TOTALProbTotal5N and TOTALProbTotal2N>TOTALProbTotal1N:
    ClassResul = TOTALProbTotal2N
    print("Probabilidad mas alta pertenece a la Droga B y es: ", ClassResul)
if TOTALProbTotal3N>TOTALProbTotal4N and TOTALProbTotal3N>TOTALProbTotal5N and TOTALProbTotal3N>TOTALProbTotal2N and TOTALProbTotal3N>TOTALProbTotal1N:
    ClassResul = TOTALProbTotal3N
    print("Probabilidad mas alta pertenece a la Droga C y es: ", ClassResul)
if TOTALProbTotal4N>TOTALProbTotal5N and TOTALProbTotal4N>TOTALProbTotal3N and TOTALProbTotal4N>TOTALProbTotal2N and TOTALProbTotal4N>TOTALProbTotal1N:
    ClassResul = TOTALProbTotal4N
    print("Probabilidad mas alta pertenece a la Droga X y es: ", ClassResul)
if TOTALProbTotal5N>TOTALProbTotal4N and TOTALProbTotal5N>TOTALProbTotal3N and TOTALProbTotal5N>TOTALProbTotal2N and TOTALProbTotal5N>TOTALProbTotal1N:
    ClassResul = TOTALProbTotal5N
    print("Probabilidad mas alta pertenece a la Droga Y y es: ", ClassResul)
                
