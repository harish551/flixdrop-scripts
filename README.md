# flixdrop-scripts
this repository contains scripts related to claiming flixdrop

# Requirements
python3

# Instructions

```bash
git clone https://github.com/harish551/flixdrop-scripts.git
cd flixdrop-scripts
```

## Claim FlixDrop
```bash
python3 claim_flixdrop.py
```
Enter your eligible account address and know details
Optionally you can generate tx for claiming

Check generated tx carefully & make sure you've balance in your account before broadcasting tx on to chain

### Sign & Broadcast
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

You can execute above transaction using an authz account too
Grant permission to authz account
```bash
omniflixhubd tx authz grant <grant recipient address> generic --msg-type=/OmniFlix.itc.v1.MsgClaim --chain-id omniflixhub-1 --from {your_key_name} --fees 500uflix --node https://rpc.omniflix.network:443
```
Execute claim from authz account
```bash
omniflixhubd tx authz exec flixdrop_claim_tx.json --chain-id omniflixhub-1 --from {authz-account} --gas auto --gas-adjustment 1.5 --gas-prices 0.001uflix --node https://rpc.omniflix.network:443
```

## Claim FLIX from streampay

```bash
python3 claim_streampay_flix.py
```
Enter your address and know streamed & claimable flix details

### Sign & Broadcast
1. Sign generated transaction
```bash
omniflixhubd tx sign streampay_flix_claim_tx.json --chain-id omniflixhub-1 --from {your_key_name} --rpc https://rpc.omniflix.network:443 > signed_streampay_flix_claim_tx.json
``` 
Check signed tx & make sure everything is good

2. Broadcast signed transaction
```bash
omniflixhubd tx broadcast signed_streampay_flix_claim_tx.json --node https://rpc.omniflix.network:443 -b sync
```
3. Check tx
```bash
omniflixhubd q tx {tx_hash} --node https://rpc.omniflix.network:443
```

You can execute above transaction using an authz account too
Grant permission to authz account
```bash
omniflixhubd tx authz grant <grant recipient address> generic --msg-type=/OmniFlix.streampay.v1.MsgClaimStreamedAmount --chain-id omniflixhub-1 --from {your_key_name} --fees 500uflix --node https://rpc.omniflix.network:443
```
Execute streampay claim from authz account
```bash
omniflixhubd tx authz exec streampay_flix_claim_tx.json --chain-id omniflixhub-1 --from {authz-account} --gas auto --gas-adjustment 1.5 --gas-prices 0.001uflix --node https://rpc.omniflix.network:443
```

