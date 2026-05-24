# Exposure of Admin Credentials in Client-Side JavaScript

## Metadata
- **Source:** HackerOne
- **Report:** 1703733 | https://hackerone.com/reports/1703733
- **Submitted:** 2022-09-18
- **Reporter:** coyemerald
- **Program:** Not specified in report
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Credentials in Source Code, Sensitive Data Exposure, Hardcoded Secrets, Weak Cryptography (MD5), Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Admin credentials (username and MD5-hashed password) were hardcoded in client-side JavaScript code visible in page source. The MD5 hash was easily decryptable, allowing attackers to obtain plaintext credentials. This exposure enables unauthorized access to admin functionality and potential client data compromise.

## Attack scenario
1. Attacker visits the vulnerable subdomain URL
2. Attacker views page source code using CTRL+U or browser developer tools
3. Attacker locates the mobucksApi.placeAd() function call containing uid 'mtnng' and passwd hash
4. Attacker uses online MD5 hash decryption tools to reverse the hash to plaintext password
5. Attacker authenticates as admin user 'mtnng' using recovered credentials
6. Attacker accesses admin panel and exfiltrates sensitive client information or modifies application data

## Root cause
Developers embedded sensitive credentials (username and password hash) directly in client-side JavaScript code intended for public consumption, combining multiple security failures: storing credentials in frontend code, using weak MD5 hashing instead of proper authentication mechanisms, and failing to implement secrets management or environment-based configuration

## Attacker mindset
Low effort, high reward reconnaissance. Attackers expect to find exposed credentials through basic source code inspection - a common practice during reconnaissance. The use of MD5 indicates developers underestimated discoverability; attackers routinely check page sources for hardcoded secrets and maintain rainbow tables for common weak hashes.

## Defensive takeaways
- Never store credentials, API keys, or authentication tokens in client-side code
- Use backend authentication services with secure session management instead of embedded credentials
- Implement proper secrets management (environment variables, vault systems) for any necessary credentials
- Replace MD5 hashing with modern, salted algorithms (bcrypt, scrypt, argon2) if password hashing is necessary
- Conduct regular source code audits and implement pre-commit hooks to detect hardcoded secrets
- Use Content Security Policy (CSP) and code obfuscation as defense-in-depth measures
- Implement security scanning in CI/CD pipeline to detect exposed credentials
- Enforce principle of least privilege - credentials shown should have minimal necessary permissions

## Variant hunting
Search for similar patterns: (1) Other pages on same domain using mobucksApi or similar advertising SDKs containing credentials, (2) Credentials in minified JavaScript files, (3) Credentials in API endpoint calls visible in browser network requests, (4) Other subdomains with exposed authentication to different services, (5) Git repositories or backup files containing credential patterns, (6) Other weak hash formats (SHA1, unsalted SHA256) used in frontend code

## MITRE ATT&CK
- T1526 - Exposure of Sensitive Information
- T1078 - Valid Accounts
- T1589 - Gather Victim Identity Information
- T1557 - Adversary-in-the-Middle
- T1040 - Traffic Sniffing

## Notes
Report lacks key details (program name, bounty amount, actual credentials redacted). The 'mtnng' user appears related to MTN (likely telecom partner) advertising API integration. The fact credentials were in an advertising library integration suggests this may be partner account credentials rather than primary admin accounts, but impact remains high. MD5 decryption confirms weak password storage practices. Reporter properly redacted actual credentials in disclosure but included enough technical detail for reproduction. Indicates lack of code review process for third-party integration code.

## Full report
<details><summary>Expand</summary>

Hello Team, 
Ther an exposure of your username and password on this    subdomain █████

    uid: "mtnng",
        passwd: "██████████",



Steps To Reproduce:

Visit ███ 

Now, press CTRL+U to view the source code of this page,


Look for this code




       console.log(message);
    }
}

    (function (){
    const plid = 73;

    const mtnContainer = document.getElementById("mtn20238");
    const mtnUri = mtnContainer.childNodes[0].getAttribute("href");
    mtnContainer.addEventListener("click", ()=>fetch(mtnUri).catch(()=>{}));

    window.mobucksApi.placeAd({
        containerElementId: "mtn20238",
        uid: "mtnng",
        passwd: "███████",
        plid:plid,
        }, () => { 
            typeof mtnNoBanner == "function" && mtnNoBanner(plid,mtnContainer);

## Impact

The exposed password is in md5 which I was able to decrypt easily

uid: mtnng
hash = bd31568138edbfc0552a1ecc6886ea
plain password: ███

And as an attacker, this can be abused in lots of ways such as exposing some client's info

████

</details>

---
*Analysed by Claude on 2026-05-24*
