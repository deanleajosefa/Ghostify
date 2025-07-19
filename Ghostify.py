import json
import requests
import time
from typing import List

ETHERSCAN_API_KEY = 'YourAPIKeyHere'
ETHERSCAN_URL = 'https://api.etherscan.io/api'

def get_tx_count(address: str) -> int:
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    data = response.json()
    if data['status'] != '1':
        return 0
    txs = data['result']
    outgoing = [tx for tx in txs if tx['from'].lower() == address.lower()]
    return len(outgoing)

def get_balance(address: str) -> float:
    params = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    data = response.json()
    if data['status'] != '1':
        return 0.0
    balance_wei = int(data['result'])
    return balance_wei / 1e18

def detect_ghost_wallets(addresses: List[str]) -> List[dict]:
    ghost_wallets = []
    for i, address in enumerate(addresses):
        print(f"[{i+1}/{len(addresses)}] Проверка {address}...")
        tx_count = get_tx_count(address)
        balance = get_balance(address)
        if tx_count == 0 and balance > 0:
            ghost_wallets.append({'address': address, 'balance': balance})
        time.sleep(0.2)
    return ghost_wallets

if __name__ == "__main__":
    input_file = 'wallets.txt'
    try:
        with open(input_file, 'r') as f:
            addresses = [line.strip() for line in f if line.strip()]
        result = detect_ghost_wallets(addresses)
        print("\n👻 Найденные 'призрачные' кошельки:")
        print(json.dumps(result, indent=2))
    except FileNotFoundError:
        print(f"Файл {input_file} не найден. Создайте файл с адресами по одному на строку.")
