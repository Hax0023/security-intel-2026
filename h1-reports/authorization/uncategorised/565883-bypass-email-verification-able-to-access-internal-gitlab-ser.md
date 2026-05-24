# Email Verification Bypass via SCIM Provisioning - Access to Internal GitLab Services

## Metadata
- **Source:** HackerOne
- **Report:** 565883 | https://hackerone.com/reports/565883
- **Submitted:** 2019-05-04
- **Reporter:** ngalog
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authentication Bypass, Email Verification Bypass, Privilege Escalation, Identity Spoofing, SCIM API Abuse
- **CVEs:** CVE-2019-5473
- **Category:** uncategorised

## Summary
A SCIM provisioning function in GitLab allowed group owners to create users with verified @gitlab.com email addresses without completing the email verification process. This enabled attackers to impersonate legitimate GitLab employees and gain unauthorized access to internal services that rely on email domain validation (@gitlab.com) for access control. The vulnerability affected GitLab.com's identity provider functionality for downstream services.

## Attack scenario
1. Attacker upgrades a GitLab group to Gold plan to access SAML/SCIM configuration
2. Attacker generates a SCIM token from the SAML SSO configuration page
3. Attacker crafts a SCIM API request to /api/scim/v2/groups/GROUP_NAME/Users with a spoofed @gitlab.com email address
4. SCIM API creates the user account with the email marked as verified without sending verification emails
5. Attacker uses the SAML SSO login endpoint with the externalId to authenticate as the newly created user
6. Attacker gains access to internal GitLab services that check for @gitlab.com email domain membership

## Root cause
The SCIM provisioning endpoint did not validate email ownership or require email verification before marking emails as verified. The system trusted the SCIM provisioning process without implementing secondary email verification checks, particularly for sensitive domains like @gitlab.com.

## Attacker mindset
An attacker with group owner privileges (potentially obtained through social engineering or legitimate group creation) could systematically create fake employee accounts with @gitlab.com emails to infiltrate internal GitLab infrastructure. The attacker recognized that GitLab itself uses its own platform for internal service authentication, making this a path to compromise internal systems.

## Defensive takeaways
- Implement email verification requirements in SCIM provisioning, even for enterprise workflows - do not skip verification for any provisioning method
- Maintain a separate verification state that differentiates between provisioning systems and user-initiated email verification
- Add rate limiting and anomaly detection on SCIM user creation endpoints, especially for sensitive email domains
- Require additional authentication/approval for creating users with @gitlab.com or other privileged domain emails via SCIM
- Audit all internal services using GitLab as IdP and implement additional verification layers beyond email domain checking
- Implement scope limitations on SCIM tokens - restrict which email domains can be provisioned
- Add logging and alerting for SCIM user creation with internal domain emails
- Consider implementing SCIM user pre-validation with existing employee directories before account creation

## Variant hunting
Check if other provisioning methods (Directory Sync, LDAP) have similar email verification bypasses
Audit SAML attribute mapping to see if email attributes can be manipulated during federation
Test other privileged email domains or organizational email patterns for the same bypass
Investigate if SCIM token permissions can be escalated beyond intended scope
Check if user email domains can be changed post-provisioning via SCIM PATCH requests without verification
Test if the bypass applies to subdomains or alternative domain variations
Verify if other identity attributes (username, displayName) can be spoofed to match internal naming conventions

## MITRE ATT&CK
- T1078.003 - Valid Accounts: Cloud Accounts
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1556.003 - Modify Authentication Process: Assertion/Token Forgery

## Notes
This vulnerability is particularly impactful because GitLab.com itself uses GitLab for internal service authentication, creating a direct path to infrastructure compromise. The reporter noted they previously documented a list of internal services affected but could not relocate it. The vulnerability required Gold plan access, limiting the attack surface but not eliminating risk from legitimate group owners or those who obtain stolen credentials. The SCIM API's trust in the provisioning system without independent email verification represents a common architectural flaw in enterprise identity systems.

## Full report
<details><summary>Expand</summary>

### Summary
Hi, I found the new SCIM provisioning function allows any group owner in gitlab to create any user with verified email address. i.e. I can create user with email address ngalog@gitlab.com, and gitlab.com will think ngalog@gitlab.com is verified already.

This will bring problem to the client app that uses Gitlab as Identity Provider, and check if the user's email domain matches `@gitlab.com`, then using this email verification bypass, we can access the service now.

I used to have a list of internal services/sites of gitlab uses gitlab.com to sign in and check if the signed in user has @gitlab.com as their email domain. But I can't find them any more, I am sure gitlab security team know what are those services. And exposure of those services would bring a high security impact to gitlab infrastructure.

### Steps to reproduce
- In gitlab.com, upgrade your Group plan to gold
- Visit `https://gitlab.com/groups/GROUP_PATH/-/saml` and setup the SAML SSO as documented
- Same page, create SCIM token
- Use the same SCIM token to issue the request below

```
POST /api/scim/v2/groups/YOUR_GROUP_NAME/Users HTTP/1.1
Host: gitlab.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/scim+json
Authorization: Bearer YOUR_SCIM_TOKEN
Content-Length: 291

{"externalId":"REPLACE_ME","active":null,"userName":"anyusernamewilldo","emails":[{"primary":true,"type":"work","value":"ANYGITLABEMAIL@gitlab.com"}],"name":{"formatted":"Test User","familyName":"User","givenName":"Test3"},"schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],"meta":{"resourceType":"User"}}
```

- And open a new private window and use https://gitlab.com/groups/GROUP_NAME/-/saml/sso?token=xqz82m-b to login using the externalId specified in the POST JSON body
- Now you are logged in as the newly created user and bypassed the email verification process



### Impact

I used to have a list of internal services/sites of gitlab uses gitlab.com to sign in and check if the signed in user has @gitlab.com as their email domain. But I can't find them any more, I am sure gitlab security team know what are those services. And exposure of those services would bring a high security impact to gitlab infrastructure.

### Examples

Check the user username4 on gitlab.com, you will see his email address is ngalog@gitlab.com and verified.

### What is the current *bug* behavior?

Email is verified without going through the verification process

### What is the expected *correct* behavior?

Email should not be verified using this method

### Relevant logs and/or screenshots

{F484033}

This bug happens on GitLab.com

#### Results of GitLab environment info

This bug happens on GitLab.com)

## Impact

see above

</details>

---
*Analysed by Claude on 2026-05-24*
