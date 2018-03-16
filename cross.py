#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 18:04:36 2018

@author: diego
"""

from scipy.io import arff
import pandas as pd
import math

def contarDrogas(df):
    listaDrogas = df['Drug'].tolist()
    contA=contB=contC=contX=contY=0
    totalValores = len(listaDrogas)
    for i in range(0,totalValores):
        if listaDrogas[i]=="drugA":
            contA += 1
        elif listaDrogas[i]=="drugB":
            contB += 1
        elif listaDrogas[i]=="drugC":
            contC += 1
        elif listaDrogas[i]=="drugX":
            contX += 1
        else:
            contY += 1
    drogas = [contA, contB, contC, contX, contY]
    return drogas

def hacerModelo(df):
    def probabilidad(x,mean,stdev):
        exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
        return (1/(math.sqrt(2*math.pi)*stdev)) * exponent

    def condDiscreta(se, bl, ch, index):
        contsef=contsem=contblh=contbln=contbll=contchh=contchn=contchl=0
        if se[index]=="F":
            contsef += 1
        elif se[index]=="M":
            contsem += 1
        if bl[index]=="HIGH":
            contblh += 1
        elif bl[index]=="NORMAL":
            contbln += 1
        elif bl[index]=="LOW":
            contbll += 1
        if ch[index]=="HIGH":
            contchh += 1
        elif ch[index]=="NORMAL":
            contchn += 1
        elif ch[index]=="LOW":
            contchl += 1
    
        vcd=[contsef,contsem, contblh, contbln, contbll, contchh, contchn, contchl]
        return vcd
    
    def desviacionEstandar(media, totalValor, acumulado):
        
        a = float((acumulado/(totalValor)))
        c = media*media
        b = abs(a-c)
        desviacion = math.sqrt(b)
        return desviacion
    
    #seleccionar la columna de clases y convertirla en una lista
    listaDrogas = df['Drug'].tolist()
    listaNa = df['Na'].tolist()
    listaK = df['K'].tolist()
    
    totalValores = len(listaDrogas)       

    df_na = df.copy()
    df_K = df.copy()
    
    listaEdades = df['Age'].tolist()

    df1 = df.sort_values('Age')
    listaEd = df1['Age'].tolist()
    ContAge1 = 0
    sumalistDelta = 0
    listaDelta = []
    #Calcular delta:
    for i in range(0, totalValores-1):
        ContAge1 = listaEd[i+1] - listaEd[i]  
        listaDelta.append(ContAge1)
        sumalistDelta = listaDelta[i] + sumalistDelta 
    #Calcular distic:
    ContDistic=0
    for i in range(0, totalValores-1):
        if listaDelta[i] != 0:
            ContDistic = 1 + ContDistic
    #Precision
    precision = sumalistDelta / ContDistic
    #Calculo Edad con Precision
    for j in range(0, totalValores-1):
        listaEdades[j] = math.ceil(listaEdades[j]/precision)  * precision
    
    #Calculo de precision para Na
    
    dfNa1 = df_na.sort_values('Na')
    listaNa1 = dfNa1['Na'].tolist()
    ContNa1 = 0
    sumalistDeltaNa1 = 0
    listaDeltaNa1 = []
    
    ##Calcular delta:
    for i in range(0, totalValores-1):
        ContNa1 = listaNa1[i+1] - listaNa1[i]  
        listaDeltaNa1.append(ContNa1)
        sumalistDeltaNa1 = listaDeltaNa1[i] + sumalistDeltaNa1 
    ##Calcular distic:
    ContDisticNa=0
    for i in range(0, totalValores-1):
        if listaDeltaNa1[i] != 0:
            ContDisticNa = 1 + ContDisticNa
    ##Precision
    precisionNa = sumalistDeltaNa1 / ContDisticNa
    #Calculo Na con Precision
    for j in range(0, totalValores-1):
        listaNa[j] = math.ceil(listaNa[j]/precisionNa)  * precisionNa
        
    #Calculo de precision para K
    
    dfK = df_K.sort_values('K')
    listaK1 = dfK['K'].tolist()
    Contk1 = 0
    sumalistDeltaK1 = 0
    listaDeltaK1 = []
    
    ##Calcular delta:
    for i in range(0, totalValores-1):
        ContK1 = listaK1[i+1] - listaK1[i]  
        listaDeltaK1.append(ContK1)
        sumalistDeltaK1 = listaDeltaK1[i] + sumalistDeltaK1 
    ##Calcular distic:
    ContDisticK=0
    for i in range(0, totalValores-1):
        if listaDeltaK1[i] != 0:
            ContDisticK = 1 + ContDisticK
    ##Precision
    precisionK = sumalistDeltaK1 / ContDisticK
    #Calculo Na con Precision
    for j in range(0, totalValores-1):
        listaK[j] = math.ceil(listaK[j]/precisionK)  * precisionK 
    
    listaSexos = df['Sex'].tolist()
    listaBP = df['BP'].tolist()
    listaCh = df['Cholesterol'].tolist()
    
    del df["Age"]
    
    df["Age"] = listaEdades
    
    del df['Na']
    
    df['Na'] = listaNa
    
    del df['K']
    
    df['K'] = listaK
    
    columns = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na', 'K','Drug']
    df = df[columns]
    
    #contar las veces q se repite cada clase
    contA=contB=contC=contX=contY=0
    
    for i in range(0,totalValores):
        if listaDrogas[i]=="drugA":
            contA += 1
        elif listaDrogas[i]=="drugB":
            contB += 1
        elif listaDrogas[i]=="drugC":
            contC += 1
        elif listaDrogas[i]=="drugX":
            contX += 1
        else:
            contY += 1
    
    #CALCULO TABLA 1: Probabilidad  de cada clase
    pA = float(contA)/totalValores
    pB = float(contB)/totalValores
    pC = float(contC)/totalValores
    pX = float(contX)/totalValores
    pY = float(contY)/totalValores
    #PROBABILIDADES A PRIORI
    
    df_apriori = pd.DataFrame([pA,pB,pC,pX,pY], index = ['drugA', 'drugB', 'drugC', 'drugX', 'drugY'])
    
    osfa=osma=obha=obna=obla=ocha=ocna=ocla=0
    osfb=osmb=obhb=obnb=oblb=ochb=ocnb=oclb=0
    osfc=osmc=obhc=obnc=oblc=ochc=ocnc=oclc=0
    osfx=osmx=obhx=obnx=oblx=ochx=ocnx=oclx=0
    osfy=osmy=obhy=obny=obly=ochy=ocny=ocly=0
    
    contEdadA=0
    contNaA=0
    contKA=0
    contDesvEdadA=0
    contDesvNaA=0
    contDesvKA=0
    
    contEdadB=0
    contNaB=0
    contKB=0
    contDesvEdadB=0
    contDesvNaB=0
    contDesvKB=0
    
    contEdadC=0
    contNaC=0
    contKC=0
    contDesvEdadC=0
    contDesvNaC=0
    contDesvKC=0
    
    contEdadX=0
    contNaX=0
    contKX=0
    contDesvEdadX=0
    contDesvNaX=0
    contDesvKX=0
    
    contEdadY=0
    contNaY=0
    contKY=0
    contDesvEdadY=0
    contDesvNaY=0
    contDesvKY=0
    
    for i in range(0, totalValores):
        if listaDrogas[i]=="drugA":
             
            contEdadA = contEdadA + listaEdades[i]
            contNaA = contNaA + listaNa[i]
            contKA = contKA +listaK[i]
    
            contDesvEdadA = contDesvEdadA + (listaEdades[i]** 2)
            contDesvNaA = contDesvNaA + (listaNa[i]** 2)
            contDesvKA = contDesvKA + (listaK[i] ** 2)
    
            #Contador de los valores de todos los atributos
            ppa = condDiscreta(listaSexos, listaBP, listaCh, i)
            osfa=osfa+ppa[0] #Contador Sexo femenino droga A
            osma=osma+ppa[1]
            obha=obha+ppa[2]
            obna=obna+ppa[3]
            obla=obla+ppa[4]
            ocha=ocha+ppa[5]
            ocna=ocna+ppa[6]
            ocla=ocla+ppa[7]#Contador Cholesterol bajo droga A
            
        elif listaDrogas[i]=="drugB":
            
            contEdadB = contEdadB + listaEdades[i]
            contNaB = contNaB + listaNa[i]
            contKB = contKB +listaK[i]
            
            contDesvEdadB = contDesvEdadB + (listaEdades[i] ** 2)
            contDesvNaB = contDesvNaB + (listaNa[i]** 2)
            contDesvKB = contDesvKB + (listaK[i] ** 2)
            
            
            ppb=condDiscreta(listaSexos,listaBP,listaCh,i)
            osfb=osfb+ppb[0]
            osmb=osmb+ppb[1]
            obhb=obhb+ppb[2]
            obnb=obnb+ppb[3]
            oblb=oblb+ppb[4]
            ochb=ochb+ppb[5]
            ocnb=ocnb+ppb[6]
            oclb=oclb+ppb[7]
            
        elif listaDrogas[i]=="drugC":
            
            contEdadC = contEdadC + listaEdades[i]
            contNaC = contNaC + listaNa[i]
            contKC = contKC +listaK[i]
    
            contDesvEdadC = contDesvEdadC + (listaEdades[i] ** 2)
            contDesvNaC = contDesvNaC + (listaNa[i]** 2)
            contDesvKC = contDesvKC + (listaK[i] ** 2)
            
            
            ppc=condDiscreta(listaSexos,listaBP,listaCh,i)
            osfc=osfc+ppc[0]
            osmc=osmc+ppc[1]
            obhc=obhc+ppc[2]
            obnc=obnc+ppc[3]
            oblc=oblc+ppc[4]
            ochc=ochc+ppc[5]
            ocnc=ocnc+ppc[6]
            oclc=oclc+ppc[7]
            
        elif listaDrogas[i]=="drugX":
            
            contEdadX = contEdadX + listaEdades[i]
            contNaX = contNaX + listaNa[i]
            contKX = contKX +listaK[i]
            
            contDesvEdadX = contDesvEdadX + (listaEdades[i] ** 2)
            contDesvNaX = contDesvNaX + (listaNa[i]** 2)
            contDesvKX = contDesvKX + (listaK[i] ** 2)
            
            
            ppx=condDiscreta(listaSexos,listaBP,listaCh,i)
            osfx=osfx+ppx[0]
            osmx=osmx+ppx[1]
            obhx=obhx+ppx[2]
            obnx=obnx+ppx[3]
            oblx=oblx+ppx[4]
            ochx=ochx+ppx[5]
            ocnx=ocnx+ppx[6]
            oclx=oclx+ppx[7]
            
        elif listaDrogas[i]=="drugY":
            
            contEdadY = contEdadY + listaEdades[i]
            contNaY = contNaY + listaNa[i]
            contKY = contKY +listaK[i]
            
            contDesvEdadY = contDesvEdadY + (listaEdades[i] ** 2)
            contDesvNaY = contDesvNaY + (listaNa[i]** 2)
            contDesvKY = contDesvKY + (listaK[i] ** 2)
            
            
            ppy=condDiscreta(listaSexos,listaBP,listaCh,i)
            osfy=osfy+ppy[0]
            osmy=osmy+ppy[1]
            obhy=obhy+ppy[2]
            obny=obny+ppy[3]
            obly=obly+ppy[4]
            ochy=ochy+ppy[5]
            ocny=ocny+ppy[6]
            ocly=ocly+ppy[7]
            
    #CALCULAMOS LA PROBABILIDAD PARA CADA SITUACION CONDICIONAL
    probsfda=(float(osfa)+1)/(contA+5)
    probsmda=(float(osma)+1)/(contA+5)
    probsfdb=(float(osfb)+1)/(contB+5)
    probsmdb=(float(osmb)+1)/(contB+5)
    probsfdc=(float(osfc)+1)/(contC+5)
    probsmdc=(float(osmc)+1)/(contC+5)
    probsfdx=(float(osfx)+1)/(contX+5)
    probsmdx=(float(osmx)+1)/(contX+5)
    probsfdy=(float(osfy)+1)/(contY+5)
    probsmdy=(float(osmy)+1)/(contY+5)
    probbhda=(float(obha)+1)/(contA+5)
    probbnda=(float(obna)+1)/(contA+5)
    probblda=(float(obla)+1)/(contA+5)
    probbhdb=(float(obhb)+1)/(contB+5)
    probbndb=(float(obnb)+1)/(contB+5)
    probbldb=(float(oblb)+1)/(contB+5)
    probbhdc=(float(obhc)+1)/(contC+5)
    probbndc=(float(obnc)+1)/(contC+5)
    probbldc=(float(oblc)+1)/(contC+5)
    probbhdx=(float(obhx)+1)/(contX+5)
    probbndx=(float(obnx)+1)/(contX+5)
    probbldx=(float(oblx)+1)/(contX+5)
    probbhdy=(float(obhy)+1)/(contY+5)
    probbndy=(float(obny)+1)/(contY+5)
    probbldy=(float(obly)+1)/(contY+5)
    probchda=(float(ocha)+1)/(contA+5)
    probcnda=(float(ocna)+1)/(contA+5)
    probclda=(float(ocla)+1)/(contA+5)
    probchdb=(float(ochb)+1)/(contB+5)
    probcndb=(float(ocnb)+1)/(contB+5)
    probcldb=(float(oclb)+1)/(contB+5)
    probchdc=(float(ochc)+1)/(contC+5)
    probcndc=(float(ocnc)+1)/(contC+5)
    probcldc=(float(oclc)+1)/(contC+5)
    probchdx=(float(ochx)+1)/(contX+5)
    probcndx=(float(ocnx)+1)/(contX+5)
    probcldx=(float(oclx)+1)/(contX+5)
    probchdy=(float(ochy)+1)/(contY+5)
    probcndy=(float(ocny)+1)/(contY+5)
    probcldy=(float(ocly)+1)/(contY+5)
    
    #CREAMOS VECTORES PARA EVITAR GRANDES FILAS DE DATOS
    vectorcondicionalA=[probsfda, probsmda, probbhda, probbnda, probblda, probchda, probcnda, probclda]
    vectorcondicionalB=[probsfdb, probsmdb, probbhdb, probbndb, probbldb, probchdb, probcndb, probcldb]
    vectorcondicionalC=[probsfdc, probsmdc, probbhdc, probbndc, probbldc, probchdc, probcndc, probcldc]
    vectorcondicionalX=[probsfdx, probsmdx, probbhdx, probbndx, probbldx, probchdx, probcndx, probcldx]
    vectorcondicionalY=[probsfdy, probsmdy, probbhdy, probbndy, probbldy, probchdy, probcndy, probcldy]    
    
    #EXPORTAR
    df_condicional = pd.DataFrame([vectorcondicionalA, vectorcondicionalB, vectorcondicionalC, vectorcondicionalX, vectorcondicionalY], index = ['drugA', 'drugB', 'drugC', 'drugX', 'drugY'])
        
    #MEDIA
    mediaEdadA = contEdadA/contA
    mediaNaA = contNaA/contA
    mediaKA = contKA/contA
    
    
    mediaEdadB = contEdadB/contB
    mediaNaB = contNaB/contB
    mediaKB = contKB/contB
    
    
    mediaEdadC = contEdadC/contC
    mediaNaC = contNaC/contC
    mediaKC = contKC/contC
    
    
    mediaEdadX = contEdadX/contX
    mediaNaX = contNaX/contX
    mediaKX = contKX/contX
    
    
    mediaEdadY = contEdadY/contY
    mediaNaY = contNaY/contY
    mediaKY = contKY/contY
    
    
    desvEstEdadA = desviacionEstandar(mediaEdadA, contA, contDesvEdadA)
    desvEstNaA = desviacionEstandar(mediaNaA, contA, contDesvNaA)
    desvEstKA = desviacionEstandar(mediaKA, contA, contDesvKA)
    
    
    desvEstEdadB = desviacionEstandar(mediaEdadB, contB, contDesvEdadB)
    desvEstNaB = desviacionEstandar(mediaNaB, contB, contDesvNaB)
    desvEstKB = desviacionEstandar(mediaKB, contB, contDesvKB)
    
    desvEstEdadC = desviacionEstandar(mediaEdadC, contC, contDesvEdadC)
    desvEstNaC = desviacionEstandar(mediaNaC, contC, contDesvNaC)
    desvEstKC = desviacionEstandar(mediaKC, contC, contDesvKC)
    
    
    desvEstEdadX = desviacionEstandar(mediaEdadX, contX, contDesvEdadX)
    desvEstNaX = desviacionEstandar(mediaNaX, contX, contDesvNaX)
    desvEstKX = desviacionEstandar(mediaKX, contX, contDesvKX)
    
    
    desvEstEdadY = desviacionEstandar(mediaEdadY, contY, contDesvEdadY)
    desvEstNaY = desviacionEstandar(mediaNaY, contY, contDesvNaY)
    desvEstKY = desviacionEstandar(mediaKY, contY, contDesvKY)
    
    
    continuasA =[mediaEdadA, desvEstEdadA, mediaNaA, desvEstNaA, mediaKA, desvEstKA]
    continuasB =[mediaEdadB, desvEstEdadB, mediaNaB, desvEstNaB, mediaKB, desvEstKB]
    continuasC =[mediaEdadC, desvEstEdadC, mediaNaC, desvEstNaC, mediaKC, desvEstKC]
    continuasX =[mediaEdadX, desvEstEdadX, mediaNaX, desvEstNaX, mediaKX, desvEstKX]
    continuasY =[mediaEdadY, desvEstEdadY, mediaNaY, desvEstNaY, mediaKY, desvEstKY]
    
    df_continuas = pd.DataFrame([continuasA, continuasB, continuasC, continuasX, continuasY], index = ['drugA', 'drugB', 'drugC', 'drugX', 'drugY'])
    totalidad = [df_apriori,df_condicional,df_continuas]
    return totalidad

def correrModelo(totalidad, ValorRes):
    dfApriori = totalidad[0]
    dfCondicional = totalidad[1]
    dfContinuas = totalidad[2]

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

    VEdad = ValorRes[0]
    VSexo = ValorRes[1]
    VBP = ValorRes[2]
    VCh = ValorRes[3]
    VNa = ValorRes[4]
    VK = ValorRes[5]

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
    
    #Determinamos la prob mas alta
    ClassResul = 0
    Clase =''

    if TOTALProbTotal1N>TOTALProbTotal2N and TOTALProbTotal1N>TOTALProbTotal3N and TOTALProbTotal1N>TOTALProbTotal4N and TOTALProbTotal1N>TOTALProbTotal5N:
        ClassResul = TOTALProbTotal1N
        Clase = 'DrugA'
    if TOTALProbTotal2N>TOTALProbTotal3N and TOTALProbTotal2N>TOTALProbTotal4N and TOTALProbTotal2N>TOTALProbTotal5N and TOTALProbTotal2N>TOTALProbTotal1N :
        ClassResul = TOTALProbTotal2N
        Clase = 'DrugB'
    if TOTALProbTotal3N>TOTALProbTotal4N and TOTALProbTotal3N>TOTALProbTotal5N and TOTALProbTotal3N>TOTALProbTotal2N and TOTALProbTotal3N>TOTALProbTotal1N:
        ClassResul = TOTALProbTotal3N
        Clase = 'DrugC'
    if TOTALProbTotal4N>TOTALProbTotal5N and TOTALProbTotal4N>TOTALProbTotal3N and TOTALProbTotal4N>TOTALProbTotal2N and TOTALProbTotal4N>TOTALProbTotal1N:
        ClassResul = TOTALProbTotal4N
        Clase = 'DrugX'
    if TOTALProbTotal5N>TOTALProbTotal4N and TOTALProbTotal5N>TOTALProbTotal3N and TOTALProbTotal5N>TOTALProbTotal2N and TOTALProbTotal5N>TOTALProbTotal1N:
        ClassResul = TOTALProbTotal5N
        Clase = 'DrugY'               
    return Clase

data = arff.loadarff('clasificacion-drug.arff')

df = pd.DataFrame(data[0])

x = range(0,199)

df = df.sort_values('Drug') 

dft = df.copy()

dft1 = df.copy()
dft2 = df.copy()
dft3 = df.copy()
dft4 = df.copy()
dft5 = df.copy()
dft6 = df.copy()
dft7 = df.copy()
dft8 = df.copy()
dft9 = df.copy()
dft10 = df.copy()

df_1 = pd.DataFrame()
df_2 = pd.DataFrame()
df_3 = pd.DataFrame()
df_4 = pd.DataFrame()
df_5 = pd.DataFrame()
df_6 = pd.DataFrame()
df_7 = pd.DataFrame()
df_8 = pd.DataFrame()
df_9 = pd.DataFrame()
df_10 = pd.DataFrame()

n = 0
n = float(input("Ingrese n: "))

for i in range (0,199,3):
    if n==3:
        df_1 = df_1.append(dft.iloc[i])
        df_2 = df_2.append(dft.iloc[i+1])
        df_3 = df_3.append(dft.iloc[i+2])
        dft=dft.drop(dft.index[[i]])
        dft=dft.drop(dft.index[[i+1]])
        dft=dft.drop(dft.index[[i+2]])
    elif n==5:
        df_1 = df_1.append(dft.iloc[i])
        df_2 = df_2.append(dft.iloc[i+1])
        df_3 = df_3.append(dft.iloc[i+2])
        df_4 = df_4.append(dft.iloc[i+3])
        df_5 = df_5.append(dft.iloc[i+4])
        dft=dft.drop(dft.index[[i]])
        dft=dft.drop(dft.index[[i+1]])
        dft=dft.drop(dft.index[[i+2]])
        dft=dft.drop(dft.index[[i+3]])
        dft=dft.drop(dft.index[[i+4]])
    elif n==7:
        df_1 = df_1.append(dft.iloc[i])
        df_2 = df_2.append(dft.iloc[i+1])
        df_3 = df_3.append(dft.iloc[i+2])
        df_4 = df_4.append(dft.iloc[i+3])
        df_5 = df_5.append(dft.iloc[i+4])
        df_6 = df_6.append(dft.iloc[i+5])
        df_7 = df_7.append(dft.iloc[i+6])
        dft=dft.drop(dft.index[[i]])
        dft=dft.drop(dft.index[[i+1]])
        dft=dft.drop(dft.index[[i+2]])
        dft=dft.drop(dft.index[[i+3]])
        dft=dft.drop(dft.index[[i+4]])
        dft=dft.drop(dft.index[[i+5]])
        dft=dft.drop(dft.index[[i+6]])
    elif n==10:
        df_1 = df_1.append(dft.iloc[i])
        df_2 = df_2.append(dft.iloc[i+1])
        df_3 = df_3.append(dft.iloc[i+2])
        df_4 = df_4.append(dft.iloc[i+3])
        df_5 = df_5.append(dft.iloc[i+4])
        df_6 = df_6.append(dft.iloc[i+5])
        df_7 = df_7.append(dft.iloc[i+6])
        df_8 = df_8.append(dft.iloc[i+7])
        df_9 = df_9.append(dft.iloc[i+8])
        df_10 = df_10.append(dft.iloc[i+9])
        dft=dft.drop(dft.index[[i]])
        dft=dft.drop(dft.index[[i+1]])
        dft=dft.drop(dft.index[[i+2]])
        dft=dft.drop(dft.index[[i+3]])
        dft=dft.drop(dft.index[[i+4]])
        dft=dft.drop(dft.index[[i+5]])
        dft=dft.drop(dft.index[[i+6]])
        dft=dft.drop(dft.index[[i+7]])
        dft=dft.drop(dft.index[[i+8]])
        dft=dft.drop(dft.index[[i+9]])
        