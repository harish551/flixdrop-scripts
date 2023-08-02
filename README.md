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

 

