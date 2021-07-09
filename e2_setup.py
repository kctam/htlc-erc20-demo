from web3 import Web3

# use ganache-cli -m abcdef to bring up a local ethereum network
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
master = "0x747e967c24abEC02b7243e3287CC5Ec0F4534A89"
master_privkey = "0x9ab344e3121e72311debb966aaa0cbee5943b99c95914a0e7992227bc5822e29"
token_abi = [{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"uint256","name":"_totalsupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
# Read token ID for USD and EUR

token_file = open("token-usd-contractid", "r")
token_usd_id = token_file.read()
token_usd_contract = w3.eth.contract(
    address=token_usd_id,
    abi=token_abi
)

token_file = open("token-eur-contractid", "r")
token_eur_id = token_file.read()
token_eur_contract = w3.eth.contract(
    address=token_eur_id,
    abi=token_abi
)

# master transfer 100 USD to Alice, 90 EUR to Bob
alice = "0x2b55CD0D2a47044c4C1C2295eA5317c4eB7C8ED2"
bob = "0xDb2eD3D31565183CC4e644d04aCdAcd3d1430523"

nonce = w3.eth.getTransactionCount(master)
tx = token_usd_contract.functions.transfer(
    alice,
    100
).buildTransaction({
    'gas': 70000,
    'from': master,
    'nonce': nonce
})

signed_tx = w3.eth.account.signTransaction(tx, private_key=master_privkey)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
w3.eth.waitForTransactionReceipt(tx_hash)
print("100 USD transferred to Alice")

nonce = w3.eth.getTransactionCount(master)
tx = token_eur_contract.functions.transfer(
    bob,
    90
).buildTransaction({
    'gas': 70000,
    'from': master,
    'nonce': nonce
})

signed_tx = w3.eth.account.signTransaction(tx, private_key=master_privkey)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
w3.eth.waitForTransactionReceipt(tx_hash)
print("90 USD transferred to Bob")

# check both balance
usd_balance = token_usd_contract.functions.balanceOf(alice).call()
eur_balance = token_eur_contract.functions.balanceOf(alice).call()
print("Alice's balance: %d USD and %d EUR." % (usd_balance, eur_balance))

usd_balance = token_usd_contract.functions.balanceOf(bob).call()
eur_balance = token_eur_contract.functions.balanceOf(bob).call()
print("Bob's balance: %d USD and %d EUR." % (usd_balance, eur_balance))