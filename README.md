# htlc-erc20-demo
Hashed Timelock Contract (HTLC) demonstration on ERC20 tokens.

The HTLC used in this demonstration is from [here](https://github.com/chatch/hashed-timelock-contract-ethereum).

## Prerequisite
* ganache-cli
* python3
* python3 web3 library

## Demonstration steps

### Step 1: Preparation

Prepare a terminal and run 
```
ganache-cli -m abcdef
```
Note: Use this mnemonic as the account information is hardcoded.

Prepare another terminal to run the event listener
```
python3 e99_eventlistener.py
```

### Step 2: Deploy contracts and setup token balances for both Alice and Bob

Bring up another terminal
```
python3 e1_deploycontracts.py
python3 e2_setup.py
```

### Step 3: Alice locks her USD100
```
python3 e5_alice_lock_usd.py
```

Keep an eye on the event listener. A contract ID is recorded in HTLC, which is Alice's USD asset. Besides, a hashlock is returned and it will be used in Step 4 when Bob is locking his asset.

### Step 4: Bob locks his EUR90
```
python3 e6_bob_lock_eur_hash.py
```
Use the haslock value obtained in Step 3. Upon complete, another contract ID is recorded in HTLC, which is Bob's EUR asset.

### Step 5: Alice unlocks Bob's asset
```
python3 e7_alice_unlock_eur.py
```
Alice uses Bob's contract ID (from Step 4) and her secret in order to collect Bob's asset.

### Step 6: Bob unlocks Alice's asset
```
python3 e8_bob_unlock_usd.py
```
Bob first accesses his contract ID in order to obtain the secret provided by Alice. Then Bob provides Alice's contract ID (from Step 3) and the same secret to collect Alice's asset.

Atomic swap complets.

## Simulating atomic swap not happening

Instead of running Step 5 and Step 6, after timeout (hardcoded 2 minutes), use this to refund both
```
python3 e9_bothsiderefund.py
```
And we see the locked assets are returned to both sides respectively.
