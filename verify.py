#coding=utf-8
import sys
import cloudflare_dynamic_dns

#Check authorize status
result = cloudflare_dynamic_dns.verify()
#Print the output
if type(result) is bool:
    if result is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif result is False:
        print("Error occurred, please check the error.log file.")
elif type(result) is str:
    print(f"The authorize status is: {result}.")

sys.exit()