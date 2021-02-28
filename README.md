# CloudFlare-Dynamic-DNS
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/CloudFlare-Dynamic-DNS)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/CloudFlare-Dynamic-DNS.svg)](https://github.com/axetroy/github-size-badge)

A small python module for request / update DNS Record at CloudFlare DNS server.

## Contents
- [CloudFlare-Dynamic-DNS](#cloudflare-dynamic-dns)
  * [Contents](#contents)
  * [Usage](#usage)
    + [Scheduling](#scheduling)
    + [CloudFlare API](#cloudflare-api)
    + [Request or update DNS record](#request-or-update-dns-record)
    + [Update DNS record](#update-dns-record)
    + [Update CNAME record](#update-cname-record)
  * [Configuration file](#configuration-file)
  * [Python module](#python-module)
  * [Function](#function)
    + [Verify CloudFlare API Token](#verify-cloudflare-api-token)
    + [Print All DNS records](#print-all-dns-records)
    + [Asking IPv4 address](#asking-ipv4-address)
    + [Request DNS A record](#request-dns-a-record)
    + [Update DNS A record](#update-dns-a-record)
    + [Asking IPv6 address](#asking-ipv6-address)
    + [Request DNS AAAA record](#request-dns-aaaa-record)
    + [Update DNS AAAA record](#update-dns-aaaa-record)
    + [Refresh CNAME record](#refresh-cname-record)
    + [Error handling](#error-handling)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module-1)
  * [License](#license)
  * [Resources](#resources)
    + [My Gist](#my-gist)
    + [CloudFlare API](#cloudflare-api-1)
    + [IP address request API](#ip-address-request-api)

## Usage
### Scheduling
- Schedule  
You can using schedule module for job scheduling, you can found the scheduling setting at scripts examples.  
If you want to using schedule module for job scheduling, [install this module](https://pypi.org/project/schedule/) are needed.
```python
import schedule

#Execute setting
schedule.every(30).minutes.do( #Something Package as function)
#Loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
#Crtl+C to exit
except KeyboardInterrupt:
  print("GoodBye ...")
```

- Crontab  
Alternatively, automatically execute via cron.
```shell
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
0 9-22/1 * * *  pi python /home/pi/python_script/ddns_ipv4.py
0 */1   * * *   pi python /home/pi/python_script/ddns_ipv6.py
#
```
### CloudFlare API
For using this module, you need to have a domain name, and choice CloudFlare as the DNS hosting services.

Logged in the Cloudflare Dashboard, and go to User Profile, choice [API Tokens](https://dash.cloudflare.com/profile/api-tokens), generated API Token. ```Once successfully generated, the token secret is only shown once```, make sure to copy the secret to a secure place.

First time running this module, it will asking the basic authorization data.
```text
Configuration not found, please enter basic authorization data.

Please enter the auth_key: Bearer ••••••••••••••••••••••••••••••••••••••••
Please enter the auth_mail: example@gmail.com
Please enter the zone ID: ••••••••••••••••••••••••••••••••••••
Authorization data saved successfully.
```
- ```auth_key``` is the 40 characters API Token has ```Bearer``` header.
- ```auth_mail``` is the email address associated with your account
- ```zone ID``` is the 36 characters ID associated the domain you want to control.

If you fill in with correct configure store at ```config.json```, it will skip initialization step when first time running.
### Request or update DNS record
DNS record ID is necessary, Configure store at ```config.json```.
```json
"id": {
  "dns_a_record_id": "••••••••••••••••••••••••••••••••",
  "dns_a_domain": "ipv4.example.com",
  "dns_aaaa_record_id": "••••••••••••••••••••••••••••••••",
  "dns_aaaa_domain": "ipv6.example.com",
  "proxy_able": true,
  "proxy_mode": true
  }
```
- ```dns_a_record_id``` is the 32 characters ID which associated with domain DNS A record.
- ```dns_a_domain``` is the domain name associated with domain DNS A record.
- ```dns_aaaa_record_id``` is the 32 characters ID which associated with domain DNS AAAA record.
- ```dns_aaaa_domain``` is the domain name associated with domain DNS AAAA record.
- ```proxy_able``` is the capability of CloudFlare proxy, depend on CloudFlare default.
- ```proxy_mode``` is the setting of CloudFlare proxy Enable / Disable.
### Update DNS record
IP address is necessary, input as ```update_address_ipv4``` or ```update_address_ipv6```.
```python
import cloudflare_dynamic_dns

#Update IPv4
cloudflare_dynamic_dns.update_record_ipv4(update_address_ipv4)
#Update IPv6
cloudflare_dynamic_dns.update_record_ipv6(update_address_ipv6)
```
Updated IP address will store at ```config.json```.
```json
"ip_address": {
  "dns_a_address": "1.1.1.1",
  "dns_aaaa_address": "2606:4700:4700::1111"
  }
```
- ```TTL```, Time to live for DNS record, default Value is ```automatic (1)```

### Update CNAME record
CNAME record ID is necessary, Configure store at ```config.json```.
```python
import cloudflare_dynamic_dns

#Asking payload
canme_name = input("Please enter the NAME: ")
canme_content = input("Please enter the VALUE: ")
#Update
refresh_canme = cloudflare_dynamic_dns.update_cname(canme_name, canme_content)
```
- ```canme_name``` is the CNAME name.
- ```canme_content``` si the CNAME Target.

Updated CNAME record will store at ```config.json```.
```json
"cname": {
  "dns_cname_record_id": "••••••••••••••••••••••••••••••••",
  "zone_name": "subdomain.example.com",
  "zone_target": "target.example.com"
  }
```
- ```dns_cname_record_id``` is the 32 characters ID which associated with CNAME record.

## Configuration file
This module store configuration as JSON format file, named ```config.json```.

You can editing the clean copy, which looks like this:
```json
{
   "api_auth": {
      "auth_key": "",
      "auth_mail": "",
      "initialize_time": ""
   },
  "zone": {
      "zone_id": ""
   },
  "id": {
      "dns_a_record_id": "",
      "dns_a_domain": "",
      "dns_aaaa_record_id": "",
      "dns_aaaa_domain": "",
      "proxy_able": true,
      "proxy_mode": true
   },
   "ip_address": {
      "dns_a_address": "",
      "dns_aaaa_address": ""
  },
  "cname": {
      "dns_cname_record_id": "",
      "zone_name": "",
      "zone_target": ""
   },
  "last_update_time": {
      "ddns_4_update_time": "",
      "ddns_6_update_time": "",
      "canme_update_time": ""
   }
}
```
If you fill in with correct configure, it will skip initialization step.

## Python module
- Import the module
```python
import cloudflare_dynamic_dns
```
```python
import cloudflare_dynamic_dns as cloudflare
```
- Alternatively, you can import the function independent
```python
from cloudflare_dynamic_dns import verify
```

## Function
### Verify CloudFlare API Token
Refer to ```verify.py```.  
It will print the verify result as string:
```text
The authorize status is: active
```
Otherwise it will print:
```text
CloudFlare API connect timeout occurred, or request not success.
```
```text
Error occurred, please check the error.log file.
```
### Print All DNS records
Refer to ```dns_record_asking.py```.  
It will save the result as JSON file and print the messages:
```text
Successfully get data form CloudFlare, saving to JSON file ....
Data storage at 'cloudflare_dns_data.json'.
```
Otherwise it will print:
```text
CloudFlare API connect timeout occurred, or request not success.
```
```text
Error occurred, please check the error.log file.
```
### Asking IPv4 address
```python
import cloudflare_dynamic_dns

#Asking newest IP address
ipv4_newest = cloudflare_dynamic_dns.get_ipv4()
#Check asking result
if type(ipv4_newest) is bool:
    if ipv4_newest is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif ipv4_newest is False:
        print("Error occurred, please check the error.log file.")
elif type(ipv4_newest) is str:
  print(ipv4_newest)
```
If successfully get IP address, it will print
```text
1.1.1.1
```
If error occurred, it will return ```Boolean``` as the result.
### Request DNS A record
```python
import cloudflare_dynamic_dns

#Get IP address recording in CloudFlare
ipv4_origin = cloudflare_dynamic_dns.database_record_ipv4()
#Check asking result
if type(ipv4_origin) is bool:
    if ipv4_origin is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif ipv4_origin is False:
        print("Error occurred, please check the error.log file.")
elif type(ipv4_origin) is str:
  print(ipv4_origin)
```
If successfully get DNS A record, it will print
```text
1.1.1.1
```
If error occurred, it will return ```Boolean``` as the result.
### Update DNS A record
Refer to ```ddns_ipv4.py```.  
It will print the messages if no need a refresh:
```text
IP address is same as DNS record, update is not necessary.
```
Otherwise it will sending update request and print result:
```text
The respon is: True
```
If error occurred, it will print:
```text
CloudFlare API connect timeout occurred, or request not success.
```
```text
Error occurred, please check the error.log file.
```
### Asking IPv6 address
```python
import cloudflare_dynamic_dns

#Asking newest IP address
ipv6_newest = cloudflare_dynamic_dns.get_ipv6()
#Check asking result
if type(ipv6_newest) is bool:
    if ipv6_newest is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif ipv6_newest is False:
        print("Error occurred, please check the error.log file.")
elif type(ipv6_newest) is str:
  print(ipv6_newest)
```
If successfully get IP address, it will print
```text
2606:4700:4700::1111
```
If error occurred, it will return ```Boolean``` as the result.
### Request DNS AAAA record
```python
import cloudflare_dynamic_dns

#Get IP address recording in CloudFlare
ipv6_origin = cloudflare_dynamic_dns.database_record_ipv6()
#Check asking result
if type(ipv6_origin) is bool:
    if ipv6_origin is True:
        print("CloudFlare API connect timeout occurred, or request not success.")
    elif ipv6_origin is False:
        print("Error occurred, please check the error.log file.")
elif type(ipv6_origin) is str:
  print(ipv6_origin)
```
If successfully get DNS AAAA record, it will print
```text
2606:4700:4700::1111
```
If error occurred, it will return ```Boolean``` as the result.
### Update DNS AAAA record
Refer to ```ddns_ipv6.py```.  
It will print the messages if no need a refresh:
```text
IP address is same as DNS record, update is not necessary.
```
Otherwise it will sending update request and print result:
```text
The respon is: True
```
If error occurred, it will print:
```text
CloudFlare API connect timeout occurred, or request not success.
```
```text
Error occurred, please check the error.log file.
```
### Refresh CNAME record
Refer to ```cname_update.py```.  
```python
import cloudflare_dynamic_dns

#Asking payload
canme_name = input("Please enter the NAME: ")
canme_content = input("Please enter the VALUE: ")
#Update
refresh_canme = cloudflare_dynamic_dns.update_cname(canme_name, canme_content)
```
It will print the messages if update request successfully sending:
```text
The respon is: True
```
If error occurred, it will print:
```text
CloudFlare API connect timeout occurred, or request not success.
```
```text
Error occurred, please check the error.log file.
```
### Error handling 
Error message store at ```error.log```

## Dependencies
### Python version
- Python 3.6 or above
### Python module
- json
- getpass
- logging
- requests
- datetime

## License
General Public License -3.0

## Resources
### My Gist
- [Verify API Token for CloudFlare API](https://gist.github.com/Suzhou65/cf63b430bfc44c03a3b1fbe2af10d6a9)
- [Get DNS record from CloudFlare API](https://gist.github.com/Suzhou65/8b9e5e5360f9c0a363e82038bb0d29b8)
- [Get IPv4, IPv6 DNS record from CloudFlare API](https://gist.github.com/Suzhou65/3488991186cbf6749b20dfc2ff5dea79)
### CloudFlare API
- [Cloudflare API v4 Documentation](https://api.cloudflare.com/)
### IP address request API
- [ipv6-test.com](https://ipv6-test.com/api/)
- [ipify](https://www.ipify.org/)
