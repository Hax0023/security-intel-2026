# CBC Cut-and-Paste Attack Enabling Open Redirect and Potential XSS via URL Encryption/Decryption

## Metadata
- **Source:** HackerOne
- **Report:** 126203 | https://hackerone.com/reports/126203
- **Submitted:** 2016-03-26
- **Reporter:** orange
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cryptographic Weakness, CBC Mode Malleability, Open Redirect, Cross-Site Scripting (XSS), Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The Redirect.aspx endpoint on pages.et.uber.com implements CBC-mode encryption with block size 8 for URL redirects, but fails to verify the integrity of encrypted payloads, allowing attackers to perform CBC cut-and-paste attacks. An attacker can encrypt arbitrary URLs via the hangzhou1year endpoint and use ciphertext block manipulation to construct valid encrypted redirects to malicious domains or potentially inject XSS payloads.

## Attack scenario
1. Attacker identifies the hangzhou1year endpoint accepts user input and returns encrypted URLs via the EQ parameter
2. Attacker uses the parameter-based encryption oracle to encrypt attacker-controlled content (e.g., '@orange.tw/?')
3. Attacker extracts ciphertext blocks from encrypted legitimate domains and encrypted attacker payloads
4. Attacker performs CBC cut-and-paste manipulation: mixing ciphertext blocks from different encryptions to forge new valid ciphertexts
5. Attacker crafts malicious EQ parameter value using manipulated ciphertext blocks pointing to attacker's domain
6. Victim clicks link with crafted EQ parameter, Redirect.aspx decrypts and redirects to attacker's domain or executes injected script

## Root cause
The application uses CBC-mode encryption without authentication (no HMAC/AEAD), lacks integrity verification, and exposes an encryption oracle through the hangzhou1year endpoint. CBC mode is inherently malleable—attackers can manipulate ciphertext blocks to alter plaintext without knowing the encryption key. The absence of authenticated encryption allows these modifications to pass validation.

## Attacker mindset
Exploit cryptographic weakness in production redirect mechanism to redirect users to phishing sites or execute JavaScript. The attacker recognized that encryption without authentication is cryptographically broken, leveraged the encryption oracle to understand block boundaries and structure, then applied known CBC manipulation techniques to craft valid-looking encrypted payloads.

## Defensive takeaways
- Use authenticated encryption (AEAD ciphers like AES-GCM or ChaCha20-Poly1305) instead of raw CBC mode to prevent tampering
- Never use encryption alone; always pair with authentication (HMAC-SHA256 or built-in AEAD tag)
- Remove or restrict encryption oracles—do not expose endpoints that encrypt user-controlled input
- Implement strict URL validation and whitelist allowed redirect domains; reject data: and javascript: schemes
- Use cryptographic libraries and frameworks that default to authenticated encryption
- Apply defense-in-depth: validate decrypted output format and destination before redirecting
- Conduct cryptographic security reviews of all custom encryption implementations

## Variant hunting
Identify other endpoints accepting similar EQ parameters or encrypted tokens across Uber subdomains
Test for oracle patterns in any parameter-based encryption (token generation, state parameters, CSRF tokens)
Search for similar CBC implementations without authentication in legacy payment/authentication flows
Check for other redirect endpoints that decrypt without integrity verification
Probe for timing-based padding oracle attacks if decryption error messages leak timing information
Test other block cipher modes (ECB) used in redirect/encryption contexts for similar weaknesses

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1539

## Notes
This is a textbook example of why authenticated encryption is mandatory in practice. The researcher demonstrated sound cryptographic attack knowledge by identifying CBC malleability and constructing a working exploit. The report is particularly notable for showing that even without breaking the encryption, the lack of authentication makes the system vulnerable. The potential XSS variant via data: URIs elevates severity further. This vulnerability likely affected many Uber marketing/tracking URLs and deserved critical priority remediation.

## Full report
<details><summary>Expand</summary>

Hello, Uber Security Team

I found an vulnerability in Uber URL redirect page.

# Vulnerability
In page
```
http://pages.et.uber.com/Redirect.aspx?EQ=5c591a8916642e73ef70dd2c27bd4bad7d810b960a984f390e396861d8a70dfd8d4ad287476f76f106d578f9ace7becffd6e3b312bb4c389315d140317a39050ed569698560fe77404eb8e2f6b2299542477613ae27b43d6d75e133918f7531a2cbea134db7c614a0182342d7079019621af699d14cb1a7cfaa5d14b2982a1a7082d1ff2507b504e68763a7c621e409ef8dd7fe980c48e0664bcb71d4d96523bec4638573e1cff2ba6cc032c5986fe5497c86cfaefb22406bd798a7f8312fde3acd3757bd120dfa0e40f3acb1e99e66c
```

parameter "EQ" is an encrypted URL and "Redirect.aspx" will redirect page to url which is decrypted.
After some trying, it looks like encryted by **CBC mode** and block size is **8**.

And I found an URL 
```
https://pages.et.uber.com/hangzhou1year/?uuid=1234
```

This URL can encrypted itself. For example
Access
`https://pages.et.uber.com/hangzhou1year/?uuid=1234`
and view the source you will see
```
https://pages.et.uber.com/Redirect.aspx?EQ=5c591a8916642e73ef70dd2c27bd4bad7d810b960a984f390e396861d8a70dfd8d4ad287476f76f106d578f9ace7becffd6e3b312bb4c389315d140317a39050ed569698560fe77404eb8e2f6b2299542477613ae27b43d6d75e133918f7531a2cbea134db7c614a0182342d7079019621af699d14cb1a7cfaa5d14b2982a1a7082d1ff2507b504e68763a7c621e409ef8dd7fe980c48e0664bcb71d4d96523bec4638573e1cff2ba6cc032c5986fe5497c86cfaefb22406bd798a7f8312fde3acd3757bd120dfa025d290b1cf9a6e85
```
Above is the encrypted result of string `https://pages.et.uber.com/hangzhou1year/?uuid=1234`


# Exploiting
ok, now I can encrypt something by `?uuid=whatever` and decrypt something by `?EQ=whatever`

so I can decrypt all the cipher by `?EQ=whatever` (remember the padding...)

And I can create any cipher by **CBC cut and paste attack**
For Example, I encrypt `@orange.tw/?` and paste and cipher to bellow URL, when you access URL, you will redirect to orange.tw(my website)
```
http://pages.et.uber.com/Redirect.aspx?EQ=5c591a8916642e73ef70dd2c27bd4bad7d810b960a984f390e396861d8a70dfd8d4ad287476f76f106d578f9ace7becffd6e3b312bb4c389315d140317a39050ed569698560fe77404eb8e2f6b2299542477613ae27b43d6d75e133918f7531a2cbea134db7c614a0182342d7079019621af699d14cb1a7cfaa5d14b2982a1a7082d1ff2507b504e68763a7c621e409ef8dd7fe980c48e0664bcb71d4d96523bc9a3bb1c67bf3b0edc8be7c80b4a998d2ce17fd5dd704e741309ec46b0627b0c1924321b894eebbc0128fce2b552959e
```

I think this vulnerability also can lead to XSS by creating an URL like
```
data:text/html base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K
```
if I have more time doing research ( it's evening in my country now :O )


# Attachments

`fake.py` is my Python poc
`2016-03-26_172607.jpg` decrypt the last block of cipher (%08%08%08%08%08%08%08%08 represented it use PKCS #5 padding)


</details>

---
*Analysed by Claude on 2026-05-24*
