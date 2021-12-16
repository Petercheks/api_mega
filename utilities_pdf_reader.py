#Metodos para trabajar la data

def getUserName(stringData):
    index = stringData.index('Usuario:')
    user = stringData[index:].replace('Usuario: ', '')
    
    return user

def getTlfSolicitante(stringData):
    index = stringData.index('TELF:')
    tlf = stringData[index:index+15].replace('TELF:', '')
    
    return tlf.replace('\u00a0', '')

def getNroOperation(stringData):
    indexInit = stringData.index('Nro.Ope.:')
    indexEnd = stringData.index('Ref.:')
    nro = stringData[indexInit:indexEnd-1].replace('Nro.Ope.: ', '')
    
    return nro

def getCostosEnvio(stringData):
    dataPrices = []
    
    indexInit = stringData.index('Costo Envío:')
    indexTotalUsd = stringData.index('TOTAL USD:')
    indexTotalPesos = stringData.index('TOTAL PESOS:')
    
    price = stringData[indexInit:indexTotalUsd-1].replace('Costo Envío: ', '')
    dataPrices.append(price)
    
    usdTotal = stringData[indexTotalUsd:indexTotalPesos-1].replace('TOTAL USD: ', '')
    dataPrices.append(usdTotal)
    
    pesosTotal = stringData[indexTotalPesos:].replace('TOTAL PESOS: ', '')
    dataPrices.append(pesosTotal)
    
    return dataPrices

def getTc(stringData):
    indexInit = stringData.index('T.C.')
    indexEnd =stringData.index('VALOR APROX')
    tc = stringData[indexInit:indexEnd-1].replace('T.C. ', '').strip()
    
    return tc

def getArrayMontoAprox(stringData):
    dataDivise = []
    
    indexInit = stringData.index('VALOR APROX.')
    indexEnd = stringData.index(':')
    
    divisa = stringData[indexInit:indexEnd].replace('VALOR APROX.', '').strip()
    dataDivise.append(divisa.replace('\xa0', ''))
    montoPesos = stringData[indexEnd:].strip()
    dataDivise.append(montoPesos.replace('\xa0', ''))
    
    
    return dataDivise
    