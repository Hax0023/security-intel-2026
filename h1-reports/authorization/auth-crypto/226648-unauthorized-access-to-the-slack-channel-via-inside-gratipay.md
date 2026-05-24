# Unauthorized Slack Channel Invitations via Parameter Manipulation on inside.gratipay.com

## Metadata
- **Source:** HackerOne
- **Report:** 226648 | https://hackerone.com/reports/226648
- **Submitted:** 2017-05-06
- **Reporter:** 7h0r4pp4n
- **Program:** Gratipay
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Authentication Bypass, Authorization Bypass, Improper Input Validation, Spam/Abuse
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker could force send Slack workspace invitations to arbitrary email addresses by modifying the 'coc' parameter to 1 in POST requests to the Slack invitation endpoint. The vulnerability bypassed server-side validation checks and allowed unlimited invitation spam with no rate limiting. This enabled unauthorized access invitations to the Gratipay Slack workspace.

## Attack scenario
1. Attacker identifies the Slack invitation endpoint at gratipay-slackin.herokuapp.com/invite
2. Attacker crafts a POST request with JSON payload including coc=1 parameter and target email address
3. Server-side validation is bypassed due to the coc parameter modification
4. Despite returning 400 Bad Request response, the invitation email is still sent from Slack
5. Attacker repeats process with multiple email addresses without rate limiting
6. Target users receive unsolicited Slack workspace invitations, leading to potential unauthorized workspace access

## Root cause
The server-side validation logic for the Slack invitation endpoint did not properly handle the 'coc' parameter. When set to 1, it bypassed critical authorization checks while still processing and sending the invitation. The application likely relied on client-side validation or failed to properly validate all parameter combinations, allowing the constraint to be circumvented.

## Attacker mindset
An attacker would recognize that modifying API parameters (coc=1) could bypass validation logic. The 400 response would normally indicate failure, but the attacker discovered that invitations were still being sent. This suggests fuzzing or reverse-engineering the API to find parameter combinations that bypass controls. The absence of rate limiting made this a scalable attack for spam or coordinated account registration.

## Defensive takeaways
- Implement server-side validation for ALL input parameters, not relying on specific parameter presence
- Never trust HTTP status codes as the sole indicator of request processing outcome - verify both response code and action completion
- Apply rate limiting and CAPTCHA challenges to invitation/account creation endpoints
- Validate that authorization checks occur BEFORE any side effects (email sending) are executed
- Log and alert on invitation endpoints receiving unusual patterns of requests
- Implement proper CSRF protection on sensitive actions like invitations
- Use allowlist validation for parameters rather than blacklist/blocklist approaches
- Conduct security testing of all parameter combinations, not just happy path scenarios

## Variant hunting
Test other boolean/numeric parameters (coc=0, coc=true, coc=false) for bypass behavior
Attempt to manipulate other POST parameters with numeric values to trigger different code paths
Investigate if similar parameter manipulation works on other invitation endpoints
Check if 'coc' parameter exists in other parts of the application with bypass potential
Test modification of Content-Type headers in conjunction with coc parameter
Attempt JSON injection or type confusion attacks with coc parameter
Review similar Slackin implementations for comparable validation logic flaws

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1598
- T1078

## Notes
The vulnerability demonstrates a classic validation bypass through parameter manipulation. The interesting aspect is that the server returns an error code (400) but still performs the dangerous action (sending invitation). This is a common implementation flaw where developers check response codes without verifying that the privileged action was actually prevented. The lack of rate limiting and the ability to target arbitrary email addresses makes this a high-impact spam/abuse vulnerability. The 'coc' parameter likely refers to 'Code of Conduct' acceptance, suggesting the developer intended it as a flag to bypass CoC acknowledgment checks, but failed to ensure this didn't bypass authentication/authorization entirely.

## Full report
<details><summary>Expand</summary>

# Summary
It is possible to force send invites for gratipay slack channel to arbitary email ids with no bruteforce limit. This is done by modifying the `coc` parameter to `1` in the POST data sent from https://inside.gratipay.com/appendices/chat

# Description
Sending a post request with `coc` parameter set to `1` appears to be bypassing some validation that is being done in the server. Without the same, the server responds with `Woot. Check your email` to the requests. 

**Request**
```
POST /invite HTTP/1.1
Host: gratipay-slackin.herokuapp.com
Content-Type: application/json
Content-Length: 36

{"coc":1,"email":"dobum@alienware13.com"}
```

**Response**
```
HTTP/1.1 400 Bad Request
Server: Cowboy
Connection: keep-alive
X-Powered-By: Express
Content-Type: application/json; charset=utf-8
Content-Length: 93
Date: Sat, 06 May 2017 22:33:39 GMT
Via: 1.1 vegur

{"msg":"You have already been invited to Slack. Check for an email from feedback@slack.com."}
```

Even though the response is a `400 Bad Request`, an invite email is received from `"Slack" <feedback@slack.com>` with the subject `Paul Kuruvilla has invited you to join a Slack team`.
Whatever the validation may be, this allows invites to be forced sent to arbitary email ids with no brute force limit.

# Steps To Reproduce
 * Send the post data with an arbitary email id
 * An invite to the gratipay slack channel `gratipay.slack.com` will be received at that email account 

# Supporting References:
  * https://gratipay.slack.com/team/dobum

</details>

---
*Analysed by Claude on 2026-05-24*
