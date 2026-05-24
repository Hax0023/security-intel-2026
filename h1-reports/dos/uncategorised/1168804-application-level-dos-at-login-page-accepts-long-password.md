# Application-level Denial of Service via Excessive Password Length

## Metadata
- **Source:** HackerOne
- **Report:** 1168804 | https://hackerone.com/reports/1168804
- **Submitted:** 2021-04-19
- **Reporter:** e100_speaks
- **Program:** AJAX Shop (ajaxshop.nl)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Input Validation Flaw
- **CVEs:** None
- **Category:** uncategorised

## Summary
The login/signup page accepts arbitrarily long passwords without validation, allowing an attacker to submit extremely long input strings that consume server resources and cause application slowdown or unavailability. By submitting a password with thousands of characters during signup, the application processes this excessive input, leading to potential resource exhaustion and denial of service conditions.

## Attack scenario
1. Attacker navigates to the application signup page at https://www.ajaxshop.nl/nl/account
2. Attacker enters valid credentials but crafts a password consisting of thousands of characters (e.g., 5000+ character string)
3. Attacker submits the signup form with the oversized password
4. Application processes the excessively long password without validation or truncation, consuming memory and CPU resources
5. Multiple repeat submissions with large passwords further exhaust server resources
6. Legitimate users experience slow response times or application unavailability due to resource exhaustion

## Root cause
The application lacks input validation and length restrictions on the password field. There are no server-side checks to enforce maximum password length, and the application processes the entire input string without constraint, leading to inefficient memory allocation and processing overhead.

## Attacker mindset
An attacker identifies an input field that accepts unbounded user input without validation. Rather than exploit for data theft, they recognize the opportunity to abuse application resources by overwhelming the password processing mechanism, discovering that the signup endpoint becomes a vector for application-level DoS without rate limiting.

## Defensive takeaways
- Implement strict input validation with maximum length constraints on all password fields (typically 128-256 characters)
- Apply length validation both on client-side (UX) and server-side (security)
- Implement rate limiting on authentication endpoints to prevent abuse from repeated submissions
- Add resource quotas and timeouts for password hashing operations
- Monitor for suspicious patterns such as repeated submissions with extremely large inputs
- Consider implementing CAPTCHA or account lockout mechanisms after multiple failed attempts
- Use secure password hashing algorithms with reasonable iteration counts to prevent compute exhaustion

## Variant hunting
Test other text input fields (username, email, profile fields) for unbounded length acceptance
Submit large payloads to API endpoints that accept JSON or form data
Test file upload endpoints for oversized file submissions causing DoS
Check for resource exhaustion in search functionality with extremely long queries
Test comment/feedback fields with massive input strings
Examine database query operations that may exponentially increase with input size
Look for similar flaws in password reset, two-factor authentication, or account recovery flows

## MITRE ATT&CK
- T1499
- T1499.004

## Notes
This is a classic application-level DoS vulnerability exploiting missing input validation. Unlike network-level DoS attacks, this requires minimal resources from the attacker and directly targets application architecture flaws. The vulnerability is easily reproducible and doesn't require authentication. The impact can be amplified through automation or distributed submission patterns. This type of vulnerability is often underestimated but can cause significant availability issues in production environments.

## Full report
<details><summary>Expand</summary>

Application-level Denial of Service (DOS)

It is an emerging class of security attacks on sites. They aim to overwhelm the site by flooding the server with requests that are disguised as legitimate users. The sudden increase in traffic shuts down machines and networks to make them unavailable to other users.
A DOS most often happens when an application contains either functional or architectural flaws that allow for remote interactions to consume large quantities of the host system’s resources, which can lead to the system locking-up or otherwise failing to deliver content.
DOS and DDoS (distributed denial of service) attacks are difficult to distinguish from regular surges of traffic. DoS testing is recommended to make sure your site is protected.
Step to reproduce. 

1.	Go to the link https://www.ajaxshop.nl/nl/account
2.	Signup using the email id. 
3.	On password field try to input many digits, any large password whatever is convenient for you.
4.	The password I tried is:
T123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789hellohellohellohello

## Impact

Impact :
it is possible to cause a denial a service attack on the server. This may lead to the unavailability of the websites for the legitimate users.

Remediation :
The server might not be able to handle such lengthy passwords coming from different machines simultaneously. The attacker can perform a DDOS attack by using this vulnerability.
 
The password hashing implementation must be fixed to limit the maximum length of accepted passwords.
There are two reasons for limiting the password size. 
I.	Hashing a large amount of data can cause significant resource consumption on behalf of the server and would be an easy target for Denial-of-Service attack.
II.	Normally all sites have a password minimum to maximum length like 72 characters limit or 48 limits to prevent Denial of Service attack. 

References :
https://hackerone.com/reports/840598
https://hackerone.com/reports/783356

</details>

---
*Analysed by Claude on 2026-05-24*
