import sys,os
import datetime
import pandas as pd


DOMAIN = 'https://api.algohouse.ai'
trades_aggregated_fields = [
    {'name':'ts', 'type': 'Date'}, 
    {'name':'open', 'type': 'Float'}, 
    {'name':'high', 'type': 'Float'}, 
    {'name':'low', 'type': 'Float'}, 
    {'name':'close', 'type': 'Float'}, 
    {'name':'volume', 'type': 'Int'}, 
    {'name':'rec_count', 'type': 'Int'}, 
    {'name':'avg_price', 'type': 'Float'}, 
    ]

def trades_aggregated_to_df(api_res):
  lines = api_res.split('\n')
  res_list = []
  for line in lines:
    if line == '# END':
      break
    rec_str = line.split('\t')
    # print(len(rec_str))
    rec = {}
    for i, cell in enumerate(rec_str):
        field_name = trades_aggregated_fields[i]['name']
        field_type = trades_aggregated_fields[i]['type']
        if field_type == 'Date':
          cell_value = datetime.datetime.utcfromtimestamp(int(cell)/1000)
        if field_type == 'Float':
          cell_value = float(cell)
        if field_type == 'Int':
          cell_value = int(cell)
        if field_type == 'String':
          cell_value = cell
        rec[field_name] = cell_value
      # print(cell)
    res_list.append(rec)

  df = pd.DataFrame.from_records(res_list)
  return df


def get_trades_aggregated(USER_EMAIL, SIGNKEY,
          exchange='', instrument='',
          from_time='', to_time='',
          aggregation='1m'):
  query = f"/trades_aggregated?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}&aggregation={aggregation}"
  rts = (os.popen('date +%s').read() + '000').replace('\n', '')
  q = f"{query}&signerEmail={USER_EMAIL}&requestTimestamp={rts}"
  # print(q)
  cl = "echo -n '"+q+"' | openssl dgst -sha256 -hmac "+SIGNKEY+"| awk '{print $2}'"
  sig = os.popen(cl).read().replace('\n', '')
  url = f"{DOMAIN}{q}&signature={sig}"
  api_res = os.popen(f"curl {url}".replace('&', '\&')).read()
  
  result = trades_aggregated_to_df(api_res)
  
  return result
