import re
import json
import requests as client
from tabulate import tabulate
from configparser import RawConfigParser

API_URL = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=%s&address=%s&apikey=%s"

if __name__ == '__main__':
    config = RawConfigParser()
    config.read('config.ini')

    ACCESS_TOKEN = config['ACCESS']['BSC_API_TOKEN']

    with open('accounts.json') as accounts:
        accountsData = json.load(accounts)

    headers = ['', 'ACCOUNT', 'CURRENCY', 'AMOUNT']

    for account in accountsData:
        dataToPrint = []
        rowCount = 0

        accountName = account["name"]
        accountAddress = account['address']

        for coin in account['coins']:
            rowCount += 1

            coinName = coin['name']
            coinContract = coin['contract']

            url = API_URL % (coinContract, accountAddress, ACCESS_TOKEN)
            response = client.get(url)
            result = response.json()['result']

            if result != '0':
                integer = result[:len(result)-18]
                fraction = result[len(integer):]
                fraction = re.sub("0+$", '0', fraction)
                result = f"{integer}.{fraction}"

            dataToPrint.append([rowCount, accountName.upper(), coinName.upper(), result])
        print(tabulate(dataToPrint, headers=headers, tablefmt='double_grid'))
