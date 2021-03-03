# coding=utf-8
import sys
import json
from cloudflare_dynamic_dns import database_record

# Get All DNS records
database = database_record()

# Check result
if type(database) is bool:
    if database is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif database is False:
        print("Error occurred, please check the error.log file.")
elif type(database) is dict:
    print("Successfully get data form CloudFlare, saving to JSON file ....")
    with open("cloudflare_dns_data.json", "w", encoding='utf-8') as record_json:
        json.dump(database, record_json, ensure_ascii=False, indent=5)
        record_json.close()
        print("Data storage at 'cloudflare_dns_data.json'.")

sys.exit()