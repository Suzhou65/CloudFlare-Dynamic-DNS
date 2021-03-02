#coding=utf-8
import sys
import cloudflare_dynamic_dns

#Asking payload
canme_name = input("Please enter the NAME: ")
canme_content = input("Please enter the VALUE: ")

#Update
refresh_canme = cloudflare_dynamic_dns.update_cname(canme_name, canme_content)

#Check result
if type(refresh_canme) is bool:
    if refresh_canme is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif refresh_canme is False:
        print("Error occurred, please check the error.log file.")
elif type(refresh_canme) is dict:
    cname_update_status = refresh_canme["success"]
    print(f"The respon is: {cname_update_status}")

sys.exit()