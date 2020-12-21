from PaidList import PaidList



caller = PaidList()
dataList = caller.getAmountsAvailabe()
# for element in dataList:
#         print('Cliente: '+element.nombre)
#         print('Monto en ARS a transferir: '+ str(element.availableARSTransfer))
#         print('Monto en ARS a pagar por caja: '+str(element.availableARSATM))
#         print('Monto en USD a transferir: ' + str(element.availableUSDTransfer))
#         print('Monto en USD a pagar por caja: '+str(element.availableUSDATM))
#         print('CBU USD: ' + element.cbuUSD)
#         print('CBU ARS: ' + element.cbuARS)

exportListARS = caller.exportARS(dataList)
exportListUSD = caller.exportUSD(dataList)

print('Archivo de exportacion de pagos en ARS')
print('======================================')
for element in exportListARS:
        print(element)


print('')
print('Archivo de exportacion de pagos en USD')
print('======================================')
for element in exportListUSD:
        print(element)