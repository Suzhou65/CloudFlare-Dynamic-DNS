#coding=utf-8
import sys
import cloudflare_dynamic_dns

#Asking newest IP address
ipv4_newest = cloudflare_dynamic_dns.get_ipv4()
#Get IP address recording in CloudFlare
ipv4_origin = cloudflare_dynamic_dns.database_record_ipv4()

#Check asking result
if type(ipv4_newest) is bool:
    if ipv4_newest is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif ipv4_newest is False:
        print("Error occurred, please check the error.log file.")
#Compare
elif type(ipv4_newest) is str:
    if ipv4_newest == ipv4_origin:
        print ("IP address is same as DNS record, update is not necessary.")
    #If needed to update
    else:
        update_address_ipv4 = ipv4_newest
        refresh = cloudflare_dynamic_dns.update_record_ipv4(update_address_ipv4)
        if type(refresh) is bool:
            if refresh is True:
                print("CloudFlare API connect timeout occurred, or request not success.")
            elif refresh is False:
                print("Error occurred, please check the error.log file.")
        elif type(refresh) is dict:
            update_status = refresh["success"]
            print(f"The respon is: {update_status}")

sys.exit()