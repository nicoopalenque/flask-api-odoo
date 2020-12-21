from flask import Flask
from PaidList import PaidList
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
#app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/list-ars', methods=['GET'])
def ExportARS():
    caller = PaidList()
    dataList = caller.getAmountsAvailabe()
    exportListARS = caller.exportARS(dataList)

    return json.dumps(exportListARS, ensure_ascii=False)

@app.route('/list-usd', methods=['GET'])
def ExportUSD():
    caller = PaidList()
    dataList = caller.getAmountsAvailabe()
    exportListUSD = caller.exportUSD(dataList)

    return json.dumps(exportListUSD,ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=True, port=4000)