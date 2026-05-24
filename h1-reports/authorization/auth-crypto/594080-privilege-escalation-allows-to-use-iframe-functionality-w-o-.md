# Privilege Escalation: Bypass Upgrade Requirement for iframe Functionality

## Metadata
- **Source:** HackerOne
- **Report:** 594080 | https://hackerone.com/reports/594080
- **Submitted:** 2019-06-02
- **Reporter:** muon4
- **Program:** HackerOne (specific program not disclosed in report)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Client-Side Authorization Bypass, Frontend Security Control Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A client-side privilege escalation vulnerability allows users to bypass the upgrade requirement for iframe functionality by simply removing a `data-upgrade='true'` HTML attribute via developer tools. This enables unauthorized access to premium features without payment, representing a business logic bypass rather than a technical vulnerability.

## Attack scenario
1. Attacker logs into their account and navigates to a project's integrations page
2. Attacker observes the 'upgrade now' notification blocking access to iframe functionality
3. Attacker opens browser developer tools (F12) and inspects the HTML element for the iframe option
4. Attacker locates and deletes the `data-upgrade='true'` attribute from the element
5. Attacker clicks the iframe button and successfully accesses the feature without upgrading
6. Attacker can now add iframes to their project without paying for the premium feature

## Root cause
Security control implemented exclusively on the client-side (HTML attribute) without server-side validation. The application relies on a frontend attribute to gate access to premium features rather than enforcing authorization checks on the backend when the iframe functionality is actually used.

## Attacker mindset
Low-skill attacker with basic HTML/DOM knowledge seeking to obtain premium features without payment. This is opportunistic abuse requiring minimal technical sophistication.

## Defensive takeaways
- Never rely on client-side attributes (HTML, CSS, JavaScript) as the sole enforcement mechanism for access control
- Implement server-side authorization checks for all feature access and functionality, verifying user subscription/license status before processing requests
- Validate user permissions on every backend API call that provides premium functionality
- Use feature flags and entitlements managed server-side to control feature access
- Implement rate limiting and monitoring for suspicious feature access patterns
- Conduct security review of all paywall and licensing mechanisms to ensure backend enforcement

## Variant hunting
Search for other data-* attributes used for feature gating and attempt removal
Check other premium integrations (Slack, Zapier, webhooks, etc.) for similar client-side gate implementations
Look for disabled HTML attributes (disabled='true') that might gate other features
Inspect localStorage/sessionStorage for feature flags that could be manipulated
Test API endpoints directly without UI to bypass frontend controls
Check for other HTML classes or attributes that control feature visibility (visibility:hidden, display:none)

## MITRE ATT&CK
- T1190
- T1548
- T1199

## Notes
This is a classic example of security-through-obscurity rather than true security. The fix requires backend enforcement. The attacker likely discovered this through casual inspection of HTML while investigating why features were blocked, indicating poor security design. Recommend comprehensive audit of all freemium/paywall features.

## Full report
<details><summary>Expand</summary>

Hello team!

I've found a privilege escalation issue which allows to set iframes to the projects w/o upgrading.

### Steps to reproduce
- Login
- Navigate to the project
- Choose `integrations` and click the `IFrame`
- See that you'll get `upgrade now` notification
{F501019}
- Inspect the page with developer tool and choose the `upgrade` from `IFrame` icon
- Delete the `data-upgrade="true"` part
{F501023}
- Click the `IFrame` and see that you are able to add iframe to the page w/o upgrade
{F501024}


If you need any information please let me know.

Cheers!

## Impact

Users can use functionalities without paying

</details>

---
*Analysed by Claude on 2026-05-24*
