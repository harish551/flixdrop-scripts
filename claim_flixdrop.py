# coding: utf-8
import json
import requests

CLAIMABLE_FLIX_URL = 'https://data-api.omniflix.studio/itc-campaigns/claims/{}/claimable-flix?verified=true&flixdrop=true'
NFTS_URL = 'https://data-api.omniflix.studio/itc-campaigns/{}/claims/{}/eligible-nfts?all=true'

DEFAULT_GAS = 200000
MIN_GAS_PRICE = 0.001


def get_nft_ids(campaign_id, address):
    url = NFTS_URL.format(campaign_id, address)
    #print('fetching eligible nfts ...')
    #print(url)
    res = requests.get(url)
    if res.status_code != 200:
        print('failed')
        print(res.json())
        
    result = res.json()['result']
    nfts = []
    for nft in result['list']:
    	nfts.append(nft['id'])
    print('Eligible NFTs: ', len(nfts)) 	
    return nfts
    
def get_claimable_flix(address):
	url = CLAIMABLE_FLIX_URL.format(address)
	print('fetching claimable flix & campaigns..')
	#print(url)
	res = requests.get(CLAIMABLE_FLIX_URL.format(address))
	if res.status_code != 200:
	    print('failed')
	    print(res.json())
	    return 0, []
	result = res.json()['result']
	claimable_flix = result['claimable_flix']
	print('\n-----------------------------------------------')
	print(f'claimable amount: {claimable_flix/1000000} FLIX')
	print('-----------------------------------------------\n')
	
	if claimable_flix == 0:
		return 0, []
	
	campaigns = []
	nft_count = 0
	for campaign in result['claimable_campaigns']:
		print('\n-----------------------------------------------')
		print('Campaign Name:', campaign['name'])
		nfts = get_nft_ids(campaign['id'], address)
		campaigns.append({
		'id': campaign['id'],
		'claims_count': campaign['claims_count'],
		'interaction': campaign['interaction'],
		'nfts': nfts,
		})
		nft_count += len(nfts)
		print('-----------------------------------------------\n')
	print('Total Eligible NFTs: ', nft_count)	
	return claimable_flix, campaigns
   
   
address = str(input('Enter your omniflix address (omniflix1..): '))   
claimable_flix, campaigns = get_claimable_flix(address)
if claimable_flix == 0:
	exit(0)
	
text_in = str(input('Generate tx file for claiming (Y/n):'))
generate_tx = False
if text_in.lower() == 'y' or text_in.lower() == 'yes':
	generate_tx = True
else:
	exit(0)	

claim_tx = {
    'body': {
        'messages': [],
        'memo': '',
        'timeout_height': '0',
        'extension_options': [],
        'non_critical_extension_options': []},
    'auth_info': {
        'signer_infos': [],
        'fee': {
            'amount': [{'denom': 'uflix', 'amount': '1000'}],
            'gas_limit': '500000',
            'payer': '',
            'granter': '',
        },
    },
    'signatures': [],
}

claim_messages = []
gas_required = 0
for campaign in campaigns:
	gas_required += (campaign['claims_count']*500)*len(campaign['nfts'])
	for nft in campaign['nfts']:
		claim_messages.append({
		    '@type': '/OmniFlix.itc.v1.MsgClaim',
		    'campaign_id': str(campaign['id']),
		    'nft_id': str(nft),
		    'interaction': campaign['interaction'],
		    'claimer': address,
		})
		
claim_tx['body']['messages'] = claim_messages
final_gas = DEFAULT_GAS + gas_required
claim_tx['auth_info']['fee']['gas_limit'] = str(final_gas)
fee = int(final_gas * MIN_GAS_PRICE)+10
claim_tx['auth_info']['fee']['amount'][0]['amount'] = str(fee)

print('\n-----------------------------------------------')
print(f'Required Gas: {final_gas}')
print(f'Required Fee: {fee/1000000} FLIX') 
print('-----------------------------------------------\n')

tx_file = 'flixdrop_claim_tx.json'
print(f'Writing tx into {tx_file} ..')

with open(tx_file, 'w') as fct:
	json.dump(claim_tx, fct, indent=2)

print('Done ..')	
