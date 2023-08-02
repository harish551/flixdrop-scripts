# flixdrop-scripts
this repository contains scripts related to claiming flixdrop

# Requirements
python3

# Instructions

```bash
git clone https://github.com/harish551/flixdrop-scripts.git
cd flixdrop-scripts
python3 claim_flixdrop.py
```
Check generated tx carefully & make sure you've balance in your account before broadcasting tx on to chain

## Sign & Broadcast
1. Sign generated transaction
```bash
omniflixhubd tx sign flixdrop_claim_tx.json --chain-id omniflixhub-1 --from {your_key_name} --rpc https://rpc.omniflix.network:443 > signed_flixdrop_claim_tx.json
``` 
Check signed tx & make sure everything is good

2. Broadcast signed transaction
```bash
omniflixhubd tx broadcast signed_flixdrop_claim_tx.json --node https://rpc.omniflix.network:443 -b sync
```
3. Check tx
```bash
omniflixhubd q tx {tx_hash} --node https://rpc.omniflix.network:443
```
---

## Example Output
```
$ python3 claim_flix.py                                                  
Enter your omniflix address (omniflix1..): omniflix1fmvc9d
fetching claimable flix & campaigns..

-----------------------------------------------
claimable amount: 750.0 FLIX
-----------------------------------------------


-----------------------------------------------
Campaign Name: OmniFlix OG Collectors
Eligible NFTs:  1
-----------------------------------------------


-----------------------------------------------
Campaign Name: Token Gated Telegram OGs
Eligible NFTs:  1
-----------------------------------------------


-----------------------------------------------
Campaign Name: OmniFlix Delegator Snapshot - 2
Eligible NFTs:  1
-----------------------------------------------


-----------------------------------------------
Campaign Name: FlixNet-4 Campaign Participants
Eligible NFTs:  2
-----------------------------------------------

Total Eligible NFTs:  5
Generate tx file for claiming (Y/n):y

-----------------------------------------------
Required Gas: 11742500
Required Fee: 0.011752 FLIX
-----------------------------------------------

Writing tx into flixdrop_claim_tx.json ..
Done ..
```
 

