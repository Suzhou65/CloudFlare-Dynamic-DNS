#coding=utf-8
import json
import logging
import datetime
import requests
from getpass import getpass

#Error handling
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a", format=FORMAT)

#Time
def current_time():
    today = datetime.datetime.now()
    return today.strftime('%Y-%m-%d %H:%M:%S')

#Configuration
def configuration( update_config=() ):
    if bool(update_config) is False:
        #Reading configuration file
        try:
            with open("config.json", "r") as configuration_file:
                #Return dictionary
                return json.load(configuration_file)
        #If file not found
        except FileNotFoundError:
            #Stamp
            time_initialize = current_time()
            #Initialization
            print("Configuration not found, please enter basic authorization data.\r\n")
            api_auth_key = getpass("Please enter the auth_key: ")
            api_auth_mail = input("Please enter the auth_mail: ")
            api_zone_id = getpass("Please enter the zone ID: ")
            #Dictionary
            initialize_config = {
                "api_auth": {
                    "auth_key": api_auth_key,
                    "auth_mail": api_auth_mail,
                    "initialize_time": time_initialize},
                "zone": {
                    "zone_id": api_zone_id},
                "id": {
                    "dns_a_record_id": "",
                    "dns_a_domain": "",
                    "dns_aaaa_record_id": "",
                    "dns_aaaa_domain": "",
                    "proxy_able": True,
                    "proxy_mode": True},
                "ip_address": {
                    "dns_a_address": "",
                    "dns_aaaa_address": ""},
                "cname": {
                    "dns_cname_record_id": "",
                    "zone_name": "",
                    "zone_target": ""},
                "last_update_time": {
                    "ddns_4_update_time": "",
                    "ddns_6_update_time": "",
                    "canme_update_time": ""}
                    }
            #Save configuration file
            with open("config.json", "w") as configuration_file:
                json.dump(initialize_config, configuration_file, indent=3)
                print("Authorization data saved successfully.")
                #Return dictionary after initialize
                return initialize_config
    #Update configuration file
    elif bool(update_config) is True:
        with open("config.json", "w") as configuration_file:
            json.dump(update_config, configuration_file, indent=3)
            #Return dictionary after update
            return update_config

#Global CloudFlare API
global cloudflare_api
cloudflare_api = "https://api.cloudflare.com/client/v4/"

#Requests authorization header
def headers():
    #Read configuration
    load_headers = configuration(update_config=False)
    #Get value
    auth_key = load_headers["api_auth"]["auth_key"]
    auth_mail = load_headers["api_auth"]["auth_mail"]
    #Header Payload
    return {'Authorization':auth_key, 'X-Auth-Email':auth_mail, 'Content-Type':'application/json'}

#Verify CloudFlare API
def verify():
    #URL
    verify_request = cloudflare_api + "user/tokens/verify"
    #Asking CloudFlare
    try:
        verify_respon = requests.get(verify_request, headers=headers(), timeout=3)
        #Success
        if verify_respon.status_code == 200:
            verify_result_dict = json.loads(verify_respon.text)
            verify_respon.close()
            return verify_result_dict["result"]["status"]
        #Not success
        else:
            verify_respon.close()
            logging.warning(verify_respon.status_code)
            return True
    #Timeout
    except requests.exceptions.Timeout as error_timeout:
        logging.warning(error_timeout)
        return True
    #Error
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Get All DNS records
def database_record():
    #Read configuration
    load_zone = configuration(update_config=False)
    #Get value
    zone_id = load_zone["zone"]["zone_id"]
    #URL
    data_request = cloudflare_api + "zones/" + zone_id + "/dns_records"
    try:
        database_respon = requests.get(data_request, headers=headers(), timeout=3)
        if database_respon.status_code == 200:
            database_dict = json.loads(database_respon.text)
            database_respon.close()
            return database_dict
        else:
            database_respon.close()
            logging.warning(database_respon.status_code)
            return True
    except requests.exceptions.Timeout as error_timeout:
        logging.warning(error_timeout)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Request DNS A records
def database_record_ipv4():
    #Read configuration
    record_config = configuration(update_config=False)
    #Get value
    zone_id = record_config["zone"]["zone_id"]
    record_id = record_config["id"]["dns_a_record_id"]
    #URL
    data_request = cloudflare_api + "zones/" + zone_id + "/dns_records/" + record_id
    try:
        record_4_respon = requests.get(data_request, headers=headers(), timeout=3)
        if record_4_respon.status_code == 200:
            record_4_dict = json.loads(record_4_respon.text)
            record_4_respon.close()
            #Get IP address from dictionary
            return record_4_dict["result"]["content"]
        else:
            record_4_respon.close()
            logging.warning(record_4_respon.status_code)
            return True
    except requests.exceptions.Timeout as error_timeout:
        logging.warning(error_timeout)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Update DNS A records
def update_record_ipv4( update_address_ipv4=() ):
    #Read configuration
    record_config = configuration(update_config=False)
    #Get value
    zone_id = record_config["zone"]["zone_id"]
    record_id = record_config["id"]["dns_a_record_id"]
    update_domain = record_config["id"]["dns_a_domain"]
    proxy_ability = record_config["id"]["proxy_able"]
    proxy_select = record_config["id"]["proxy_mode"]
    #Payload
    update_4_dict = {
        "type": "A",
        "name": update_domain,
        "content": update_address_ipv4,
        "proxiable": proxy_ability,
        "proxied": proxy_select,
        "ttl" : 1,}
    #JSON payload
    update_4_json = json.dumps(update_4_dict)
    #URL
    data_update = cloudflare_api + "zones/" + zone_id + "/dns_records/" + record_id
    try:
        update_record_v4 = requests.put(data_update, headers=headers(), data=update_4_json, timeout=3)
        if update_record_v4.status_code == 200:
            update_4_respon = json.loads(update_record_v4.text)
            update_record_v4.close()
            #Update configuration
            time_update = current_time()
            update_config = record_config
            update_config["ip_address"]["dns_a_address"] = update_address_ipv4
            update_config["last_update_time"]["ddns_4_update_time"] = time_update
            configuration(update_config)
            #Return dictionary
            return update_4_respon
        else:
            update_record_v4.close()
            logging.warning(update_record_v4.status_code)
            return True
    except requests.exceptions.Timeout as error_timeout:
        logging.warning(error_timeout)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Get IPv4
def get_ipv4():
    ipify_params = {"format": "json"}
    iptest_params = "json"
    try:
        ipify4 = requests.get("https://api.ipify.org/", params=ipify_params, timeout=2)
        if ipify4.status_code == 200:
            ipv4_json = json.loads(ipify4.text)
            ipify4.close()
            #Get string from dictionary
            return ipv4_json["ip"]
        else:
            pass
    except requests.exceptions.Timeout:
        try:
            iptest4 = requests.get("https://v4.ipv6-test.com/api/myip.php", params=iptest_params, timeout=3)
            if iptest4.status_code == 200:
                ipv4_json = json.loads(iptest4.text)
                iptest4.close()
                return ipv4_json["address"]
            else:
                logging.warning(iptest4.status_code)
                return True
        except requests.exceptions.Timeout as error_timeout:
            logging.warning(error_timeout)
            return True
        except Exception as error_status:
            logging.exception(error_status)
            return False    
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Request DNS AAAA records
def database_record_ipv6():
    #Read configuration
    record_config = configuration(update_config=False)
    #Get value
    zone_id = record_config["zone"]["zone_id"]
    record_id = record_config["id"]["dns_aaaa_record_id"]
    #URL
    data_request = cloudflare_api + "zones/" + zone_id + "/dns_records/" + record_id
    try:
        record_6_respon = requests.get(data_request, headers=headers(), timeout=3)
        if record_6_respon.status_code == 200:
            record_6_dict = json.loads(record_6_respon.text)
            record_6_respon.close()
            return record_6_dict["result"]["content"]
        else:
            record_6_respon.close()
            logging.warning(record_6_respon.status_code)
            return True
    except requests.exceptions.Timeout as error_timeout:
        logging.warning(error_timeout)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Update DNS AAAA records
def update_record_ipv6( update_address_ipv6=() ):
    #Read configuration
    record_config = configuration(update_config=False)
    #Get value
    zone_id = record_config["zone"]["zone_id"]
    record_id = record_config["id"]["dns_aaaa_record_id"]
    update_domain = record_config["id"]["dns_aaaa_domain"]
    proxy_ability = record_config["id"]["proxy_able"]
    proxy_select = record_config["id"]["proxy_mode"]
    #Payload
    update_6_dict = {
        "type": "AAAA",
        "name": update_domain,
        "content": update_address_ipv6,
        "proxiable": proxy_ability,
        "proxied": proxy_select,
        "ttl" : 1,}
    #JSON payload
    update_6_json = json.dumps(update_6_dict)
    #URL
    data_update = cloudflare_api + "zones/" + zone_id + "/dns_records/" + record_id
    try:
        update_record_v6 = requests.put(data_update, headers=headers(), data=update_6_json, timeout=3)
        if update_record_v6.status_code == 200:
            update_6_respon = json.loads(update_record_v6.text)
            update_record_v6.close()
            #Update configuration
            time_update = current_time()
            update_config = record_config
            update_config["ip_address"]["dns_aaaa_address"] = update_address_ipv6
            update_config["last_update_time"]["ddns_6_update_time"] = time_update
            configuration(update_config)
            #Return dictionary
            return update_6_respon
        else:
            update_record_v6.close()
            logging.warning(update_record_v6.status_code)
            return True
    except requests.exceptions.Timeout as error_timeout:
        logging.warning(error_timeout)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Get IPv6
def get_ipv6():
    ipify_params = {"format": "json"}
    iptest_params = "json"
    try:
        ipify6 = requests.get("https://api64.ipify.org/", params=ipify_params, verify=False, timeout=2)
        if ipify6.status_code == 200:
            ipv6_json = json.loads(ipify6.text)
            ipify6.close()
            #Get string from dictionary
            return ipv6_json["ip"]
        else:
            pass
    except requests.exceptions.Timeout:
        try:
            iptest6 = requests.get("https://v6.ipv6-test.com/api/myip.php", params=iptest_params, timeout=3)
            if iptest6.status_code == 200:
                ipv6_json = json.loads(iptest6.text)
                iptest6.close()
                return ipv6_json.get["address"]
            else:
                logging.warning(iptest6.status_code)
                return True
        except requests.exceptions.Timeout as error_timeout:
            logging.warning(error_timeout)
            return True
        except Exception as error_status:
            logging.exception(error_status)
            return False
    except Exception as error_status:
        logging.exception(error_status)
        return False

#Update DNS AAAA records
def update_cname( canme_name=(), canme_content=() ):
    #Read configuration
    record_config = configuration(update_config=False)
    #Get value
    zone_id = record_config["zone"]["zone_id"]
    canme_id = record_config["cname"]["dns_cname_record_id"]
    #Payload
    update_canme_dict = {
        "type": "CNAME",
        "name": canme_name,
        "content": canme_content,
        "proxiable": False,
        "proxied": False,
        "ttl" : 1,}
    update_cname_json = json.dumps(update_canme_dict)
    #URL
    cname_update = cloudflare_api + "zones/" + zone_id + "/dns_records/" + canme_id
    try:
        cname_respon = requests.put(cname_update, headers=headers(), data=update_cname_json, timeout=3)
        if cname_respon.status_code == 200:
            update_cname_respon = json.loads(cname_respon.text)
            cname_respon.close()
            #Update configuration
            time_update = current_time()
            update_config = record_config
            update_config["cname"]["zone_name"] = canme_name
            update_config["cname"]["zone_target"] = canme_content
            update_config["last_update_time"]["canme_update_time"] = time_update
            configuration(update_config)
            #Return dictionary
            return update_cname_respon
        else:
            cname_respon.close()
            logging.warning(cname_respon.status_code)
            return True
    except requests.exceptions.Timeout as error_timeout:
        logging.warning(error_timeout)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#20210227