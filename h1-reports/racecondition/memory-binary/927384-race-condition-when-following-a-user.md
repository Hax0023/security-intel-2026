# Race Condition when following a user

## Metadata
- **Source:** HackerOne
- **Report:** 927384 | https://hackerone.com/reports/927384
- **Submitted:** 2020-07-19
- **Reporter:** bugra
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
- **CVEs:** None
- **Category:** memory-binary

## Summary
## Summary:
Hi team,
There is a race condition vulnerability when following a user. If you send the `Follow` requests asynchronously, you can follow a user multiple times instead getting an error message.
I've been using Turbo Intruder extension at Burp Suite for trying Race Condition attacks. I can recommend it for reproduce this vulnerability.

## Steps To Reproduce:

  1. Go to any user's profi

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

## Summary:
Hi team,
There is a race condition vulnerability when following a user. If you send the `Follow` requests asynchronously, you can follow a user multiple times instead getting an error message.
I've been using Turbo Intruder extension at Burp Suite for trying Race Condition attacks. I can recommend it for reproduce this vulnerability.

## Steps To Reproduce:

  1. Go to any user's profile
  1. Turn on Intercept at Burp Suite and click `Follow` button
  1. Right click to follow request, click `Send to turbo intruder` and drop the request
  1. Add a fake header that contains `%s` value. Like `Test: %s `
  1. Paste this Python code to Turbo Intruder :
       ```python
def queueRequests(target, wordlists):
        engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           pipeline=False
                           )

        for i in range(30):
            engine.queue(target.req, str(i), gate='race1')

        engine.openGate('race1')
        engine.complete(timeout=60)
def handleResponse(req, interesting):
        table.add(req)
       ```
 5. Click `Attack` button. Turbo Intruder will send 30 requests, check the status codes. If you see multiple responses with `201 Created` status, that means you followed the user multiple times.

## PoC Video :
{F913171}

## Impact

Race Condition vulnerability allows to following a user multiple times with one account

Thanks,
Bugra

</details>

---
*Analysed by Claude on 2026-05-24*
