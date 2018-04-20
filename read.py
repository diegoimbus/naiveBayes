from scipy.io import arff
import pandas as pd
import math

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

#leer el dataset
data = arff.loadarff('clasificacion-drug.arff')
df = pd.DataFrame(data[0])

#seleccionar la columna de clases y convertirla en una lista
listaDrogas = df['Drug'].tolist()
listaNa = df['Na'].tolist()
listaK = df['K'].tolist()

totalValores = len(listaDrogas)

#Agregar una nueva columna para Na/K
#NaK=[]
#for i in range(0, totalValores):
#    NaK.append(float(listaNa[i])/float(listaK[i]))
#
dftest = df.copy()   
df_na = df.copy()
df_K = df.copy()
#
#df_nak["Na/K"] = NaK
#
#listaNaK = df_nak['Na/K'].tolist()

listaEdades = df['Age'].tolist()

#Calculo de precision
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
    listaEdades[j] = round(listaEdades[j]/precision)  * precision


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
    listaNa[j] = round(listaNa[j]/precisionNa)  * precisionNa
    

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
    listaK[j] = round(listaK[j]/precisionK)  * precisionK 
    

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

df_apriori.to_csv('apriori.csv')


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
probsfda=(float(osfa)+1)/(contA+2)
probsmda=(float(osma)+1)/(contA+2)
probsfdb=(float(osfb)+1)/(contB+2)
probsmdb=(float(osmb)+1)/(contB+2)
probsfdc=(float(osfc)+1)/(contC+2)
probsmdc=(float(osmc)+1)/(contC+2)
probsfdx=(float(osfx)+1)/(contX+2)
probsmdx=(float(osmx)+1)/(contX+2)
probsfdy=(float(osfy)+1)/(contY+2)
probsmdy=(float(osmy)+1)/(contY+2)
probbhda=(float(obha)+1)/(contA+3)
probbnda=(float(obna)+1)/(contA+3)
probblda=(float(obla)+1)/(contA+3)
probbhdb=(float(obhb)+1)/(contB+3)
probbndb=(float(obnb)+1)/(contB+3)
probbldb=(float(oblb)+1)/(contB+3)
probbhdc=(float(obhc)+1)/(contC+3)
probbndc=(float(obnc)+1)/(contC+3)
probbldc=(float(oblc)+1)/(contC+3)
probbhdx=(float(obhx)+1)/(contX+3)
probbndx=(float(obnx)+1)/(contX+3)
probbldx=(float(oblx)+1)/(contX+3)
probbhdy=(float(obhy)+1)/(contY+3)
probbndy=(float(obny)+1)/(contY+3)
probbldy=(float(obly)+1)/(contY+3)
probchda=(float(ocha)+1)/(contA+3)
probcnda=(float(ocna)+1)/(contA+3)
probclda=(float(ocla)+1)/(contA+3)
probchdb=(float(ochb)+1)/(contB+3)
probcndb=(float(ocnb)+1)/(contB+3)
probcldb=(float(oclb)+1)/(contB+3)
probchdc=(float(ochc)+1)/(contC+3)
probcndc=(float(ocnc)+1)/(contC+3)
probcldc=(float(oclc)+1)/(contC+3)
probchdx=(float(ochx)+1)/(contX+3)
probcndx=(float(ocnx)+1)/(contX+3)
probcldx=(float(oclx)+1)/(contX+3)
probchdy=(float(ochy)+1)/(contY+3)
probcndy=(float(ocny)+1)/(contY+3)
probcldy=(float(ocly)+1)/(contY+3)

#CREAMOS VECTORES PARA EVITAR GRANDES FILAS DE DATOS
vectorcondicionalA=[probsfda, probsmda, probbhda, probbnda, probblda, probchda, probcnda, probclda]
vectorcondicionalB=[probsfdb, probsmdb, probbhdb, probbndb, probbldb, probchdb, probcndb, probcldb]
vectorcondicionalC=[probsfdc, probsmdc, probbhdc, probbndc, probbldc, probchdc, probcndc, probcldc]
vectorcondicionalX=[probsfdx, probsmdx, probbhdx, probbndx, probbldx, probchdx, probcndx, probcldx]
vectorcondicionalY=[probsfdy, probsmdy, probbhdy, probbndy, probbldy, probchdy, probcndy, probcldy]    

#EXPORTAR
df_condicional = pd.DataFrame([vectorcondicionalA, vectorcondicionalB, vectorcondicionalC, vectorcondicionalX, vectorcondicionalY], index = ['drugA', 'drugB', 'drugC', 'drugX', 'drugY'])

df_condicional.to_csv('condicional.csv')

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
df_continuas.to_csv('continuas.csv')
