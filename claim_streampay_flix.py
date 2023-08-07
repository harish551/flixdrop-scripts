# coding: utf-8
import json
import requests
import datetime

STREAMPAY_URL = 'https://data-api.omniflix.studio/streams?address={}&status=ongoing&limit={}'
DEFAULT_LIMIT = 10
DEFAULT_GAS = 200000

sample_tx = {'body': {'messages': [],
  'memo': '',
  'timeout_height': '0',
  'extension_options': [],
  'non_critical_extension_options': []},
 'auth_info': {'signer_infos': [],
  'fee': {'amount': [{'denom': 'uflix', 'amount': '200'}],
   'gas_limit': '200000',
   'payer': '',
   'granter': ''}},
 'signatures': []}
 

def get_active_streams(address):
	limit = DEFAULT_LIMIT
	url = STREAMPAY_URL.format(address, limit)
	res = requests.get(url)
	if res.status_code != 200:
	    print(res.json())
	    return []
	result = res.json()['result']
	if result['count'] > limit:
	    limit = result['count']
	    url = STREAMPAY_URL.format(address, limit)
	    res = requests.get(url)
	    if res.status_code != 200:
	        print(res.json())
	        return []
	    result = res.json()['result']
	streams = result['list']
	receiving_streams = []
	for stream in streams:
	    if stream['recipient'] == address:
	        receiving_streams.append(stream)
	return receiving_streams
                   
def calculate_claimable_flix(address):
    streams = get_active_streams(address)
    print('\n----------------------------------')
    print('No of streams in: ', len(streams))
    print('----------------------------------\n')
    
def calculate_streamed_flix(amount, start, end):
	s = datetime.datetime.strptime(start[:-5], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)
	e = datetime.datetime.strptime(end[:-5], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)
	total_secs = (e-s).total_seconds()
	now_time = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

	streamed_secs = (now_time-s).total_seconds()
	streamed_percentage = int(streamed_secs)/total_secs

	return int(amount*streamed_percentage)


def calculate_claimable_flix(address):
    streams = get_active_streams(address)
    print('\n----------------------------------')
    print('No of streams in: ', len(streams))
    print('----------------------------------\n')
    total_flix = 0
    total_streamed_flix = 0
    total_claimed_flix = 0
    total_claimable_flix = 0
    claim_messages = []
    print('----------------------------------\n')
    for stream in streams:
        if stream['amount']['denom'] == 'uflix':
            amount = stream['amount']['amount']
            claimed_flix = stream['claimed_amount']['amount']
            streamed_flix = calculate_streamed_flix(amount, stream['start_time'], stream['end_time'])
            total_streamed_flix += streamed_flix
            claimable_flix = streamed_flix - claimed_flix
            print('Streamed ID: ', stream['id'])
            print(f'Streamed FLIX: {streamed_flix/(10**6)}/{amount/(10**6)}\n')
            total_flix += amount
            total_claimed_flix += claimed_flix
            total_claimable_flix += claimable_flix
            claim_messages.append({'@type': '/OmniFlix.streampay.v1.MsgClaimStreamedAmount', 'stream_id': stream['id'], 'claimer': address})
            
    print('-----------------------------------\n')
    print('----------------------------------------------')        
    print(f'Total FLIX: {total_flix//10**6}')
    print(f'Total Streamed FLIX: {total_streamed_flix/10**6}')
    print(f'Total Claimed FLIX: {total_claimed_flix/10**6}')
    print(f'Total Claimable FLIX: {total_claimable_flix/10**6}')
    print('----------------------------------------------\n')
    
    text_in = str(input('Generate claim transaction (Y/n): '))
    gen_tx = False
    if text_in.lower() == 'y' or text_in.lower() == 'yes':
        gen_tx = True
    if not gen_tx:
        return 
       
    sample_tx['body']['messages']=claim_messages
    gas_limit = int(DEFAULT_GAS + (DEFAULT_GAS/1.1)*len(claim_messages)-1)
    sample_tx['auth_info']['fee']['gas_limit'] = str(gas_limit)
    fee_amount = int(gas_limit * 0.001) + 1
    sample_tx['auth_info']['fee']['amount'][0]['amount'] = str(fee_amount)
    print('------------------------------------------------')
    print('Required Gas: ', gas_limit)
    print(f'Rquired TX Fee: {fee_amount}')
    print('------------------------------------------------\n')
    
    out_tx_file = 'streampay-flix-claim-tx.json'
    with open(out_tx_file, 'w') as sctf:
        json.dump(sample_tx, sctf, indent=2)
    print(f'successfully generated streampay claim transaction and saved at {out_tx_file}')
                 
addr = str(input('Enter your omniflix account address (omniflix1...): '))
calculate_claimable_flix(addr)
