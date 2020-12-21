from Data import Data
import ssl
import sys
import xmlrpclib
from datetime import date

class PaidList:
    def __init__(self):
        self.username = 'admin' #the user
        self.pwd = 'Valerza2020' #the user
        self.dbname = 'valersa'    #the database
        self.uid = 0
        self.url = 'http://54.211.171.131:8069' #url


    def getConnection(self):
        gcontext = ssl._create_unverified_context()
        sock_common = xmlrpclib.ServerProxy (self.url+'/xmlrpc/common',context=gcontext)
        self.uid = sock_common.login(self.dbname, self.username, self.pwd)
        return xmlrpclib.ServerProxy(self.url+'/xmlrpc/object',context=gcontext)




    def getAmountsAvailabe(self):
        sock = self.getConnection()
        investment_ids = sock.execute(self.dbname,self.uid,self.pwd,'crm.investment','search',[('state','=','confirmed'), ('re_egreso', '>', 0)])
        dataList = []
        count = 0
        for investment_id in investment_ids:
            investment_data = sock.execute(self.dbname,self.uid,self.pwd,'crm.investment','read',investment_id,['name','cuit','partner_id', 'currency_id', 'write_date', 're_egreso', 're_egreso_pago', 'cbu'])
            partner_data = sock.execute(self.dbname,self.uid,self.pwd,'res.partner','read',investment_data[0]['partner_id'][0],['name', 'cuit']) 
            index = [i for i in range(len(dataList)) if dataList[i].partnerId == investment_data[0]['partner_id'][0]] 
            if len(index) > 0:
                if investment_data[0]['re_egreso_pago'] == 'Transferencia':
                    if investment_data[0]['currency_id'][0] == 3: #USD
                        dataList[index[0]].availableUSDTransfer = dataList[index[0]].availableUSDTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            dataList[index[0]].cbuUSD = str(investment_data[0]['cbu'])
                    else:
                        dataList[index[0]].availableARSTransfer = dataList[index[0]].availableARSTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            dataList[index[0]].cbuARS = str(investment_data[0]['cbu'])
                else:
                    if investment_data[0]['currency_id'][1] == 'USD':
                        dataList[index[0]].availableUSDATM = dataList[index[0]].availableUSDATM + investment_data[0]['re_egreso']
                    else:
                        dataList[index[0]].availableARSATM = dataList[index[0]].availableARSATM + investment_data[0]['re_egreso']
            else:
                data = Data()
                data.cbuARS = '-'
                data.cbuUSD = '-'
                data.cuit = partner_data[0]['cuit']
                data.nombre = partner_data[0]['name']
                data.partnerId = investment_data[0]['partner_id'][0]

                if investment_data[0]['re_egreso_pago'] == 'Transferencia':
                    if investment_data[0]['currency_id'][0] == 3: #USD
                        data.availableUSDTransfer = data.availableUSDTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            data.cbuUSD = str(investment_data[0]['cbu'])
                    else:
                        data.availableARSTransfer = data.availableARSTransfer + investment_data[0]['re_egreso']
                        if str(investment_data[0]['cbu']).upper() != 'FALSE':
                            data.cbuARS = str(investment_data[0]['cbu'])
                else:
                    if investment_data[0]['currency_id'][0] == 3:
                        data.availableUSDATM = data.availableUSDATM + investment_data[0]['re_egreso']
                    else:
                        data.availableARSATM = data.availableARSATM + investment_data[0]['re_egreso']
                dataList.append(data)
        return dataList
    

    def exportARS(self, list):
        exportFile = []
        counter = 0
        totalAmount = 0
        header = 'RC,PAGO,30714470775,,,,,,,,'
        body = ''
        dateNow = date.today()
        exportFile.append(header)
        for element in list:
            if element.availableARSTransfer > 0:
                counter += 1
                totalAmount += element.availableARSTransfer
                body = 'RT,' + str(counter)
                body += ','+ str(element.partnerId)
                body += ',' + str(element.cuit)
                body += ',' + element.nombre
                body += ',' + str(element.cbuARS) 
                body += ',' + date.today().strftime('%d/%m/%Y')
                body += ',$'
                body += ',' + str(element.availableARSTransfer)
                body += ',,'
                exportFile.append(body)
                
        footer = 'RF, '+ str(counter)+', '+ str(totalAmount)+ ',,,,,,,,'
        exportFile.append(footer)
        return exportFile


    def exportUSD(self, list):
        exportFile = []
        counter = 0
        totalAmount = 0
        header = 'RC,PAGO,30714470775,,,,,,,,'
        body = ''
        dateNow = date.today()
        exportFile.append(header)
        for element in list:
            if element.availableUSDTransfer > 0:
                counter += 1
                totalAmount += element.availableUSDTransfer
                body = 'RT,' + str(counter)
                body += ','+ str(element.partnerId)
                body += ',' + str(element.cuit)
                body += ',' + element.nombre
                body += ',' + str(element.cbuUSD) 
                body += ',' + date.today().strftime('%d/%m/%Y')
                body += ',$'
                body += ',' + str(element.availableARSTransfer)
                body += ',,'
                exportFile.append(body)
                
        footer = 'RF, '+ str(counter)+', '+ str(totalAmount)+ ',,,,,,,,'
        exportFile.append(footer)
        return exportFile




# f = open('inversores.csv','w')
# writer = csv.DictWriter(f, fieldnames=fieldnames)
# writer.writeheader()

# investment_ids = sock.execute(dbname,uid,pwd,'crm.investment','search',[('state','=','confirmed'),('pv','>',1000000)])

    

#     def __init__(self):
#         self.availableARSTransfer = 0
#         self.availableUSDTransfer = 0
#         self.availableARSATM = 0
#         self.availableUSDATM = 0
#         self.cuit: '0'
#         self.nombre: '-'
#         self.cbu
        



# campos clientes -> mobile, dni, email
# moneda (res.currency)-> currency_id, name


# for investment_id in investment_ids:
# 	investment_data = sock.execute(dbname,uid,pwd,'crm.investment','read',investment_id,['name','pv','partner_id'])
#     partner_data = sock.execute(dbname,uid,pwd,'res.partner','read',investment_data[0]['partner_id'][0],['phone'])
# 	# writer.writerow({'Cliente': investment_data[0]['name'],'customer': investment_data[0]['partner_id'][1],'capital': investment_data[0]['pv']})
# 	# print( partner_data)


# f.close()