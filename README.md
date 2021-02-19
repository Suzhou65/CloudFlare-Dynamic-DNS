# CloudFlare-Dynamic-DNS
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/CloudFlare-Dynamic-DNS)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/CloudFlare-Dynamic-DNS.svg)](https://github.com/axetroy/github-size-badge)

A small python module for request / update DNS Record at CloudFlare DNS server.

For more information on the CloudFlare API please take a look at [Cloudflare API Documentation](https://api.cloudflare.com/).

## Contents
- [CloudFlare Dynamic DNS](#cloudflare-dynamic-dns)
  * [Usage](#usage)
    + [Data request](#data-request)
    + [Request or update DNS record](#request-or-update-dns-record)
    + [Update CNAME record](#update-cname-record)
  * [Python module](#python-module)
  * [Function](#function)
    + [Verify API Token](#verify-cloudflare-api-token)
    + [Print All DNS records](#print-all-dns-records)
    + [Asking IPv4 address](#asking-ipv4-address)
    + [Request DNS A record](#request-dns-a-record)
    + [Update DNS A record](#update-dns-a-record)
    + [Asking IPv6 address](#asking-ipv6-address)
    + [Request DNS AAAA record](#request-dns-aaaa-record)
    + [Update DNS AAAA record](#update-dns-aaaa-record)
    + [Refresh CNAME record](#refresh-cname-record)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module-1)
  * [License](#license)
  * [Resources](#resources)
    + [My Gist](#my-gist)
    + [CloudFlare API](#cloudflare-api)
    + [IP address request API](#ip-address-request-api)

## Usage
For using this module, you need to have a domain name, and choice CloudFlare as the DNS hosting services.

Logged in the Cloudflare Dashboard, and go to User Profile, choice [API Tokens](https://dash.cloudflare.com/profile/api-tokens), generated API Token. **Once successfully generated, the token secret is only shown once**, make sure to copy the secret to a secure place. 

### Data request
This function needs some configuration which is necessary.
```python
auth_key = "Bearer ••••••••••••••••••••••••••••••••••••••••"
auth_mail = "example@gmail.com"
zone_id = "••••••••••••••••••••••••••••••••••••"
```
- **auth_key** is the API Token you get
- **auth_mail** is the email address associated with your account
- **zone_id** is the 36 characters ID associated the domain name you want to control, it can be found in [Cloudflare Dashboard](https://dash.cloudflare.com/).

### Request or update DNS record
This function needs some configuration which is necessary.
```python
id_ipv4 = "••••••••••••••••••••••••••••••••"
id_ipv6 = "••••••••••••••••••••••••••••••••"

proxy_able = True
proxy_mode = False
```
- **id_ipv4** is the 32 characters ID which associated with domain(or subdomain) DNS record.
- **id_ipv6** is the 32 characters ID which associated with domain(or subdomain) DNS record.
- **proxy_able** is the capability of CloudFlare proxy, depend on CloudFlare default.
- **proxy_mode** is the setting of CloudFlare proxy Enable / Disable.

TTL, Time to live for DNS record, default Value is **automatic (1)**

### Update CNAME record
```python
cname_id = "••••••••••••••••••••••••••••••••"
zone_name = "_••••••••••••••••••••••••••••••••.ipv4.example.com"
zone_content = "••••••••••••••••••••••••••••••••.••••••••••••••••••••••••••••••••.•••••••••••••••.example.com"
```
- **cname_id** is the 32 characters ID which associated with CNAME record.
- **zone_name** is the CNAME name.
- **zone_content** si the CNAME Target.

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
```python
import json
from cloudflare_dynamic_dns import verify

ststus = verify(auth_key, auth_mail)

if ststus is None:
    print("Error Occurred")
elif type(ststus) is int:
    print("Error Occurred")
elif type(ststus) is str:
    print(ststus)
```
If the API Token activated successfully, the result will print as ```string```.
```text
active
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Print All DNS records
```python
import json
from cloudflare_dynamic_dns import all_data

dns_data = all_data(auth_key, auth_mail, zone_id)

if dns_data is None:
    print("Error Occurred")
elif type(dns_data) is int:
    print("Error Occurred")
elif type(dns_data) is dict:
    with open("cloudflare_dns_data.json", "w", encoding='utf-8') as f:
        json.dump(dns_data, f, ensure_ascii=False, indent=4)
```
If the request send successfully, the result will print as ```dictionary```. it can storage as a JSON data file, which named ```cloudflare_dns_data.json```.

You can find the 32 characters ID which associated the individual DNS record, which above zone_id. For example:
```text
{'result': [{'id': '••••••••••••••••••••••••••••••••••••',
   'zone_id': '••••••••••••••••••••••••••••••••••••',
   'zone_name': 'example.com',
   'name': 'example.com',
   'type': 'A',
   'content': '127.0.0.1',
   'proxiable': True,
   'proxied': True,
   'ttl': 1,
   'locked': False,
   'meta': {'auto_added': False,
    'managed_by_apps': False,
    'managed_by_argo_tunnel': False,
    'source': 'primary'},
   'created_on': '2020-08-24T03:30:28.114514Z',
   'modified_on': '2020-08-24T03:30:28.114514Z'}],
 'success': True,
 'errors': [],
 'messages': [],
 'result_info': {'page': 1,
  'per_page': 20,
  'count': 1,
  'total_count': 1,
  'total_pages': 1}}
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Asking IPv4 address
```python
from cloudflare_dynamic_dns import ipv4_check()

local_ipv4 = ipv4_check()

if local_ipv4 is None:
  print("Error Occurred")
elif type(local_ipv4) is int:
  print("Error Occurred")
elif type(local_ipv4) is str:
  print(local_ipv4)
```
If the request send successfully, the result will print as ```string```.
```text
192.168.0.1
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Request DNS A record
```python
from cloudflare_dynamic_dns import ask_record_4
id_ipv4 = "••••••••••••••••••••••••••••••••"

record_a_ststus = ask_record_4(auth_key, auth_mail, zone_id, id_ipv4)

if record_a_ststus is None:
  print("Error Occurred")
elif type(record_a_ststus) is int:
  print("Error Occurred")
elif type(record_a_ststus) is str:
  print(record_a_ststus)
```
If the request send successfully, the result will print as ```string```.
```text
192.168.0.1
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Update DNS A record
```python
from cloudflare_dynamic_dns import update_record_4
id_ipv4 = "••••••••••••••••••••••••••••••••"
domain_4 = "ipv4.example.com"
address_4 = "192.168.0.1"

update_a = update_record_4(auth_key, auth_mail, zone_id, id_ipv4, domain_4, address_4, proxy_able, proxy_mode)

if update_a is None:
  print("Error Occurred")
elif type(update_a) is int:
  print("Error Occurred")
elif type(update_a) is dict:
  print(update_a)
```
- **domain_4** is the domain(or subdomain) you want to update.
- **address_4** is the IP address you want to update.

If the request send successfully, the result will print as ```dictionary```, which can storage as a JSON Format file.
```text
{'result': {'id': '••••••••••••••••••••••••••••••••',
  'zone_id': '••••••••••••••••••••••••••••••••',
  'zone_name': 'example.com',
  'name': 'ipv4.example.com',
  'type': 'A',
  'content': '192.168.0.1',
  'proxiable': True,
  'proxied': False,
  'ttl': 1,
  'locked': False,
  'meta': {'auto_added': False,
   'managed_by_apps': False,
   'managed_by_argo_tunnel': False,
   'source': 'primary'},
  'created_on': '2021-01-18T14:35:03.341602Z',
  'modified_on': '2021-01-18T14:35:03.341602Z'},
 'success': True,
 'errors': [],
 'messages': []}
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Asking IPv6 address
```python
from cloudflare_dynamic_dns import ipv6_check()

local_ipv6 = ipv6_check()

if local_ipv6 is None:
  print("Error Occurred")
elif type(local_ipv6) is int:
  print("Error Occurred")
elif type(local_ipv6) is str:
  print(local_ipv6)
```
If the request send successfully, the result will print as ```string```.
```text
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Request DNS AAAA record
```python
from cloudflare_dynamic_dns import ask_record_6
id_ipv6 = "••••••••••••••••••••••••••••••••"

record_aaaa_ststus = ask_record_6(auth_key, auth_mail, zone_id, id_ipv6)

if record_aaaa_ststus is None:
  print("Error Occurred")
elif type(record_aaaa_ststus) is int:
  print("Error Occurred")
elif type(record_aaaa_ststus) is str:
  print(record_aaaa_ststus)
```
If the request send successfully, the result will print as ```string```.
```text
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Update DNS AAAA record
```python
from cloudflare_dynamic_dns import update_record_6
id_ipv6 = "••••••••••••••••••••••••••••••••"
domain_6 = "ipv6.example.com"
address_6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"

update_aaaa = update_record_6(auth_key, auth_mail, zone_id, id_ipv6, domain_6, address_6, proxy_able, proxy_mode)

if update_aaaa is None:
  print("Error Occurred")
elif type(update_aaaa) is int:
  print("Error Occurred")
elif type(update_aaaa) is dict:
  print(update_aaaa)
```
- **domain_6** is the domain(or subdomain) you want to update.
- **address_6** is the IP address you want to update.

If the request send successfully, the result will print as ```dictionary```, which can storage as a JSON Format file.
```text
{'result': {'id': '••••••••••••••••••••••••••••••••',
  'zone_id': '••••••••••••••••••••••••••••••••',
  'zone_name': 'example.com',
  'name': 'ipv6.example.com',
  'type': 'AAAA',
  'content': '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
  'proxiable': True,
  'proxied': False,
  'ttl': 1,
  'locked': False,
  'meta': {'auto_added': False,
   'managed_by_apps': False,
   'managed_by_argo_tunnel': False,
   'source': 'primary'},
  'created_on': '2021-01-18T14:35:04.627124Z',
  'modified_on': '2021-01-18T14:35:04.627124Z'},
 'success': True,
 'errors': [],
 'messages': []}
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

### Refresh CNAME record
```python
from cloudflare_dynamic_dns import canme_refresh
cname_id = "••••••••••••••••••••••••••••••••"
zone_name = "_••••••••••••••••••••••••••••••••.example.com"
zone_content = "••••••••••••••••••••••••••••••••.••••••••••••••••••••••••••••••••.•••••••••••••••.example.com"

cname_status = canme_refresh(auth_key, auth_mail, zone_id, cname_id, zone_name, zone_content)

if cname_status is None:
  print("Error Occurred")
elif type(cname_status) is int:
  print("Error Occurred")
elif type(cname_status) is dict:
  print(cname_status)
```
If the request send successfully, the result will print as ```dictionary```, which can storage as a JSON Format file.
```text
{'result': {'id': '••••••••••••••••••••••••••••••••',
  'zone_id': '••••••••••••••••••••••••••••••••',
  'zone_name': 'example.com',
  'name': '_••••••••••••••••••••••••••••••••.example.com',
  'type': 'CNAME',
  'content': '••••••••••••••••••••••••••••••••.••••••••••••••••••••••••••••••••.•••••••••••••••.example.com',
  'proxiable': False,
  'proxied': False,
  'ttl': 1,
  'locked': False,
  'meta': {'auto_added': False,
   'managed_by_apps': False,
   'managed_by_argo_tunnel': False,
   'managed_cname': True,
   'source': 'primary'},
  'created_on': '2021-01-21T09:40:46.13279Z',
  'modified_on': '2021-01-21T09:40:46.13279Z'},
 'success': True,
 'errors': [],
 'messages': []}
```
If error occurred, it will return ```None``` and saving logs to a file, or return HTTP status code as ```integer```.

## Dependencies
### Python version
- Python 3.6 or above

### Python module
- json
- logging
- requests

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
