# Information Disclosure: Real-time Report Submission Monitoring via Response Differential Analysis

## Metadata
- **Source:** HackerOne
- **Report:** 159890 | https://hackerone.com/reports/159890
- **Submitted:** 2016-08-17
- **Reporter:** saeedhashem
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Timing Attack, Response Differential Analysis, Lack of Rate Limiting, Insufficient Access Controls
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The `/reports/[report_id].json` endpoint exhibits differential response behavior that allows unauthenticated users to determine whether a report has been submitted. Submitted but inaccessible reports return a blank JSON response (zero length), while non-existent reports return a 404 error with JSON content, enabling an attacker to enumerate and monitor report submission activity in real-time.

## Attack scenario
1. Attacker identifies that the endpoint `/reports/[report_id].json` responds differently based on report submission status
2. Attacker develops a script that queries sequential report IDs and measures response length (36 bytes vs other lengths)
3. Attacker determines the last submitted report number by binary searching or sequential scanning
4. Attacker enters a monitoring loop, continuously polling for new report IDs at regular intervals
5. When a new report is submitted, the response pattern changes, allowing attacker to detect and timestamp the submission
6. Attacker aggregates this data to infer platform activity patterns, peak submission times, and user engagement metrics

## Root cause
The application implements different response payloads for different authorization/existence states without normalizing response structure. The distinction between 'report exists but user lacks access' (blank JSON) and 'report does not exist' (JSON error object) creates an observable side-channel that leaks information about submission status.

## Attacker mindset
Reconnaissance and competitive intelligence gathering. An attacker or competitor could use this to: monitor when specific researchers are active, track vulnerability disclosure trends, estimate platform growth metrics, or identify timing patterns for targeted social engineering.

## Defensive takeaways
- Normalize all error responses to return identical structure and length regardless of reason (existence vs authorization vs rate limiting)
- Implement rate limiting on report enumeration endpoints to prevent automated scanning
- Consider removing or restricting JSON API access to unauthenticated users
- Use constant-time comparisons and padding to prevent response size analysis attacks
- Return identical HTTP status codes for 'not found' and 'unauthorized' scenarios
- Monitor for suspicious enumeration patterns indicative of this attack
- Implement CAPTCHA or other friction for users querying non-existent report IDs at scale

## Variant hunting
Check other endpoints with resource IDs for similar differential responses (e.g., `/users/[id].json`, `/vulnerabilities/[id].json`)
Test timing differences in response generation for authorized vs unauthorized access
Examine webhook or notification endpoints that might leak timing information
Review any publicly accessible logs or activity feeds that could be enumerated
Test other content types (XML, CSV) for similar differential behavior
Investigate if other HTTP headers (Content-Length, Vary, etc.) leak distinguishing information

## MITRE ATT&CK
- T1592.002 - Gather Victim Host Information: Software
- T1589.001 - Gather Victim Identity Information: Credentials
- T1040 - Network Sniffing
- T1598 - Phishing for Information
- T1538 - Cloud Service Discovery

## Notes
This is a relatively low-impact but clever information disclosure vulnerability exploiting response differential analysis rather than traditional authentication bypass. The reporter demonstrated good understanding by developing a working PoC and explaining the business logic impact. The vulnerability relies on the attacker's ability to make many requests without rate limiting. Timeline indicates this was reported in 2016, making it a historical reference for defensive practices that should prevent similar issues. The attack could be enhanced with statistical analysis to infer business metrics like market timing of vulnerability reports.

## Full report
<details><summary>Expand</summary>

Hey ,

I would like to report an issue with the server responses that allow anyone users to monitor and track the reports' submission and the platform activity .

##Description :

The issue occurs on the endpoint '/reports/[report_id].json' due to the difference between server responses for submitted reports and  the yet not submitted ones .

If the report is already submitted and the logged in user has no access to it the html response will return a message saying `Oops! You can't access this report because it isn't public yet.` and the JSON response will return a blank page , zero length .

And if the report id passed to the endpoint hasn't been submitted yet , the HTML response will return a not found page , and the JSON response will return `{"status":"404","error":"Not Found"}` .

##PoC :

I wrote a simple python script can exploit this behaviour , it's my first pentesting python script by the way , sorry for the poor coding , I just learned how to do this today but you'll get the idea  :

```
import requests
import time
from datetime import datetime

start = raw_input("\nEnter the last report you know about [Ignore if before #159875]: ")
if start == '' :
    start = 159874
else :
    start = int(start)

if start < 159874 :
    start = 159874

def getReport(report):
    url = 'https://hackerone.com/reports/%s.json' % str(report)
    res = requests.get(url)
    l = len(res.text)
    if l == 36 :
        return 0 
    else:
        return 1 

def lastReport(start):
    for report in range( start ,1000000):
        if getReport(report):
            continue
        else :
            report = report - 1
            return report

last = lastReport(start)
print "\n[+]Last submitted report is : #%s\n" % str(last)

def getNext(last):
    report = last + 1
    if getReport(report):
        now = datetime.now()
        print "Report number #%s has been submited at %s/%s/%s %s:%s\n" % (report , now.month, now.day, now.year, now.hour, now.minute)
        last = report
        getNext(last)
    else :
        time.sleep(30)
        last = report - 1
        getNext(last)

getNext(last)
```
As the markdown missed up the code a bit I'm attaching it in two files 
F112672 => works well on Windows
F112671 => works well on Linux

The output of the script would be like :

{F112668}
{F112670}

Basically it records the date and time of every newly submitted report , of course that can be improved to generate hourly or daily reports about the platform activities , when hackers are mostly active , how frequent reports are submitted on H1 and so on , all is normally undisclosed information , only platform operator should know about .

##Impact :

I think it's too permissive for a highly secure platform to leave a way open for third parties to track its activity and its user interactions with the platform , which considered as privilege information only platform operators should be allowed to get their hands onto .

Thank you guys , glad that I've learned something new today specifically for this report , hope it qualifies and worth addressing . 

Best regards ,
Thanks ,

</details>

---
*Analysed by Claude on 2026-05-24*
