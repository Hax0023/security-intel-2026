# Open Redirect in scout24.greenhouse.io

## Metadata
- **Source:** HackerOne
- **Report:** 203726 | https://hackerone.com/reports/203726
- **Submitted:** 2017-02-06
- **Reporter:** cyneox
- **Program:** Greenhouse
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Insufficient Input Validation, Server-Side Request Manipulation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Scout24 Greenhouse job application portal fails to validate redirect URLs in the job_application[resume_url] and job_application[cover_letter_url] parameters. An attacker can intercept and modify the POST request to inject arbitrary URLs pointing to phishing sites or malware, which would be stored and presented to recruiters.

## Attack scenario
1. Attacker applies for a job at scout24.greenhouse.io and uploads legitimate PDF files
2. Attacker intercepts the multipart form POST request using a proxy tool like Burp Suite
3. Attacker modifies the job_application[resume_url] or job_application[cover_letter_url] parameters to point to a malicious domain (e.g., https://phishing-site.com)
4. Attacker forwards the tampered request to the server
5. The application accepts and stores the malicious URL without validation
6. Recruiters viewing the application are redirected to the attacker's phishing or malware site when clicking the document links

## Root cause
The application fails to validate that document URLs point to the legitimate AWS S3 bucket. It accepts arbitrary URLs in the resume_url and cover_letter_url parameters without verifying the domain or enforcing URL allowlist policies, allowing arbitrary redirect URLs to be stored.

## Attacker mindset
An attacker seeks to leverage the hiring process as an attack vector by compromising recruiter systems through credential theft (phishing) or malware distribution. By manipulating document URLs, attackers can create a convincing social engineering scenario where trusted recruiting staff click malicious links.

## Defensive takeaways
- Implement strict URL validation for all URL parameters - verify URLs point to expected S3 bucket or CDN domain using allowlisting
- Generate secure, unpredictable S3 URLs on the server-side only; never accept user-supplied URLs for document references
- Implement server-side URL whitelist validation that rejects any URLs not matching expected patterns (e.g., specific S3 bucket domains)
- Use indirect references or database IDs instead of storing user-controllable URLs
- Validate URL format and domain before storing in database
- Implement Content Security Policy headers to restrict redirect destinations
- Log and alert on URL parameter modifications that deviate from expected S3 URLs

## Variant hunting
Check other file upload parameters (cover_letter_url_filename, resume_url_filename) for similar injection points
Test other Greenhouse customer instances for the same vulnerability pattern
Examine all form parameters accepting URLs across the application
Look for similar patterns in other job application platforms using Greenhouse
Test document preview/download endpoints for open redirect vulnerabilities
Check if other document types (portfolio, references) have the same validation gap

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1598.002

## Notes
The vulnerability is exploitable by any job applicant without elevated privileges. The CSRF token is present in the request but does not prevent the attack since the attacker controls the request origin. The writeup is from Scout24's security team conducting authorized penetration testing, demonstrating responsible disclosure. The vulnerability has clear business impact as it compromises recruiter security and company reputation.

## Full report
<details><summary>Expand</summary>

## Open Redirect in scout24.greenhouse.io

The **Scout24 Security Team** did a penetration test against `scout24.greenhouse.io` in order to verify how Scout24 relevant data is protected against common attack vectors. Basically we have tested the (web) application against [OWASP Top 10](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project) using industry common metholodogies. 

## Reproduction steps

* Visit https://boards.greenhouse.io/scout24 and click on some job offer (I chosed [this one](https://boards.greenhouse.io/scout24/jobs/503488))
* After completing your personal information, you can *upload* some documents
	* Click `Attach` both under *Resume/CV* and *Cover Letter*
	* Upload some PDF files from your local host (in my case the file uwas called `neu.pdf`)
* In the end you send your application by clicking on `Submit Application`

Using a HTTP proxy (in my case that was [Burp](https://portswigger.net/burp/)) I was able to intercept the `POST` request made by the browser before being sent to the `greenhouse.io` API. This is some sample request:

### Proof-of-Concept (PoC)

```.http
POST /scout24/jobs/503488 HTTP/1.1
Host: boards.greenhouse.io
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-NewRelic-ID: VQ4PWFNbGwIFU1dbAgcB
X-CSRF-Token: zF19Ky8GR0J/ZP7aLfFiN+p8Udc+X8ikPyk0cX7LlzgS0i4wWFIchmqcmsR3aXA0T1XSNrXSWdrVb47bGjGrEg==
X-Requested-With: XMLHttpRequest
Referer: https://boards.greenhouse.io/scout24/jobs/503488
Content-Length: 4086
Content-Type: multipart/form-data; boundary=---------------------------844282227400113298508475861
Cookie: __utma=44269810.1998188318.1484665255.1484837763.1484901247.18; __utmz=44269810.1484837763.17.11.utmcsr=scout24.eu.auth0.com|utmccn=(referral)|utmcmd=referral|utmcct=/login/callback; __zlcmid=edg9prI9rr6P3K; __utmc=44269810; __utmb=44269810.15.9.1484902626060; __atuvc=4%7C3; __atuvs=5881cd5b6c1ca704003; _jbs=7897bb31a3e984da1f15ec3b3f0e8129; __utmt=1
Connection: close

[...]
-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[resume_url]"

https://grnhse-prod-jben-us-east-1.s3.amazonaws.com/applications%2Fresumes%2F1484902660983-1663bnwl7dt-b044057e6364840cde6c41d55de3a1e1%2Fneu.pdf
-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[resume_url_filename]"

neu.pdf
-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[cover_letter_url]"

https://grnhse-prod-jben-us-east-1.s3.amazonaws.com/applications%2Fresumes%2F1484902672335-lpk5xur1na-67346266367805828242f31b3887e539%2Fneu.pdf
-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[cover_letter_url_filename]"

neu.pdf
-----------------------------844282227400113298508475861--
```

As you can notice the files have been already uploaded to `AWS` and therfore a S3 bucket links are 
used within the requests. 

## Exploitability

Using a browser and a HTTP proxy the request can be easily intercepted. In the **original** request the `Content-Disposition` parameter `job_application[cover_letter_url]` in the `POST` request contains a S3 bucket link. However, after tampering the request, the parameters values can be changed. In our specific case the value (basically an URL) could be changed to:

* a phishing site
* a site containing some malware

After intercepting the request, the parameter was modified like this:

```.http
POST /scout24/jobs/503488 HTTP/1.1
Host: boards.greenhouse.io
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-NewRelic-ID: VQ4PWFNbGwIFU1dbAgcB
X-CSRF-Token: zF19Ky8GR0J/ZP7aLfFiN+p8Udc+X8ikPyk0cX7LlzgS0i4wWFIchmqcmsR3aXA0T1XSNrXSWdrVb47bGjGrEg==
X-Requested-With: XMLHttpRequest
Referer: https://boards.greenhouse.io/scout24/jobs/503488
Content-Length: 4086
Content-Type: multipart/form-data; boundary=---------------------------844282227400113298508475861
Cookie: __utma=44269810.1998188318.1484665255.1484837763.1484901247.18; __utmz=44269810.1484837763.17.11.utmcsr=scout24.eu.auth0.com|utmccn=(referral)|utmcmd=referral|utmcct=/login/callback; __zlcmid=edg9prI9rr6P3K; __utmc=44269810; __utmb=44269810.15.9.1484902626060; __atuvc=4%7C3; __atuvs=5881cd5b6c1ca704003; _jbs=7897bb31a3e984da1f15ec3b3f0e8129; __utmt=1
Connection: close
[...]

-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[resume_url]"

https://google.com
-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[resume_url_filename]"

neu.pdf
-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[cover_letter_url]"

http://google.com
-----------------------------844282227400113298508475861
Content-Disposition: form-data; name="job_application[cover_letter_url_filename]"
```

Whenever the hiring manager will try to view the uploaded content, the application will not be able to render the content. Instead the person will then try to **download** the file by clicking on `Download` (left upper corner). Although the browser shows that the URL points to some specific `AWS` domain, the content is actually loaded from somewhere else (in this case from [https://google.com](https://google.com)). 

Again, an attacker could then submit some URL containing malicious content or some phishing site. Only for the purpose of this report, something unspectacular like [https://google.com](https://google.com) has been chosen. 

## Impact

The attack can be conducted in multiple scenarios:

* anonymous person applies for some jobs and manipulates the parameters (like described above)
* internal employee adds referal for some person and also manipulates the parameters

In both cases the hiring manager would then unknowingly access the manipulated links which could then lead to:

* installation of trojan horses / ransomeware (in general malicious content)
* a phishing site where e.g. AD credentials are claimed to be required
* CSRF (Cross-Site Request Forgery) [attacks](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF))

## Remediation

The affected parameter should be first validated against some regular expression (e.g. allow only links that point to `grnhse-prod-jben-*.s3.amazonaws.com`). 







</details>

---
*Analysed by Claude on 2026-05-24*
