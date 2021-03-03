# coding=utf-8
import sys
from cloudflare_dynamic_dns import verify

# Check authorize status
result = verify(fully_respon=False)
# Print the output
if type(result) is bool:
    if result is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif result is False:
        print("Error occurred, please check the error.log file.")
elif type(result) is dict:
    print("Result output as dictionary.")
elif type(result) is str:
    print(f"The authorize status is: {result}.")

sys.exit()