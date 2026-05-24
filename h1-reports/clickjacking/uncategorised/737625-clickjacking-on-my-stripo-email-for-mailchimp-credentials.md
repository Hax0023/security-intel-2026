# Clickjacking on my.stripo.email MailChimp OAuth Integration

## Metadata
- **Source:** HackerOne
- **Report:** 737625 | https://hackerone.com/reports/737625
- **Submitted:** 2019-11-14
- **Reporter:** jasongardner
- **Program:** Stripo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Clickjacking/UI Redressing, Missing X-Frame-Options Header, OAuth Credential Theft, Insufficient Frame-busting Protection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The MailChimp OAuth authorization page at my.stripo.email lacks clickjacking protections, allowing attackers to overlay the login iframe transparently and capture user credentials. An attacker can host a malicious page embedding the OAuth flow iframe and use social engineering to trick users into authenticating, granting unauthorized access to MailChimp accounts.

## Attack scenario
1. Attacker identifies that my.stripo.email's MailChimp export/auth page is missing X-Frame-Options headers
2. Attacker creates a malicious webpage embedding the MailChimp OAuth iframe with CSS opacity/positioning tricks to make it invisible or partially overlaid
3. Attacker crafts a phishing email claiming the user needs to 'verify account' or 'update MailChimp settings'
4. Victim clicks the link and is presented with seemingly legitimate content while unknowingly interacting with the hidden OAuth iframe
5. User enters MailChimp credentials into the transparent iframe layer, believing they're authenticating legitimately
6. Attacker receives OAuth authorization code and gains full access to victim's MailChimp account and customer lists

## Root cause
The OAuth authorization page at my.stripo.email lacks proper framebuster protection mechanisms. The absence of X-Frame-Options HTTP header (should be set to DENY or SAMEORIGIN) and Content-Security-Policy frame-ancestors directive allows the page to be embedded in cross-origin iframes. The attacker's proof-of-concept demonstrates successful iframe embedding without restriction.

## Attacker mindset
An opportunistic threat actor targeting email marketing platforms recognizes that OAuth authorization pages handling sensitive credentials are high-value targets. By combining clickjacking with social engineering, they can scale credential theft across many users without deploying complex malware, directly accessing customer data and account control with minimal detection risk.

## Defensive takeaways
- Implement X-Frame-Options: DENY header on all authentication and authorization endpoints
- Deploy Content-Security-Policy with frame-ancestors 'none' or 'self' directive
- Add frame-busting JavaScript that actively breaks out of iframe contexts (e.g., if (self !== top) { top.location = self.location; })
- Use SameSite cookie attributes to prevent credential transmission in cross-site iframe contexts
- Implement visual frame-busting UI indicators to alert users if page is being framed unexpectedly
- Apply strict CSP policies limiting script sources and disabling unsafe inline scripts
- Conduct clickjacking-specific penetration testing for all user-facing authentication flows

## Variant hunting
Search for other Stripo endpoints handling sensitive integrations (Salesforce, HubSpot, ConvertKit OAuth flows) that may have identical frameable vulnerabilities. Check third-party OAuth redirect URIs belonging to Stripo partners for missing frame protections. Review any user-facing settings pages or export functionality that could be clickjacked to perform account actions.

## MITRE ATT&CK
- T1187 - Forced Authentication
- T1056 - Input Capture (credential interception via overlaid UI)
- T1566 - Phishing (email delivering clickjack payload)
- T1539 - Steal Web Session Cookie (OAuth token theft)
- T1550 - Use Alternate Authentication Material (stolen OAuth credentials)

## Notes
The researcher provided working proof-of-concept code demonstrating iframe embedding with anti-framing bypass techniques. The vulnerability chain—missing frame-busting headers + OAuth-protected credential page + social engineering vector—creates a complete attack scenario with high impact (full MailChimp account compromise). The report shows practical exploitation knowledge but lacks evidence of actual bounty resolution or vendor response timeline.

## Full report
<details><summary>Expand</summary>

Clickjacking is a malicious hacking technique where attackers can acquire sensitive data.

Through simple social engineering techniques these links can be sent out to unsuspecting customers to steal their credentials or perform actions on their accounts.

For this example I saw that where I goto export to MailChimp that page is vulnerable to clickjacking and it is a page where the user enters a username and password which would grant me whatever access that user has if I just feed the data from a keylogger on the HTML into another page with tables to store the info.

Here is the HTML code I have embedded on my sites.google.com link:

<html>
<head>
<title>Clickjack test page</title>
</head>
<body>
<p>When you enter your e-mail and login here it will be captured and the attacker can now gain access to your customer e-mail lists</p>
	
<iframe src= "https://login.mailchimp.com/oauth2/authorize?response_type=code&client_id=350877244304&redirect_uri=https%3A%2F%2Fmy.stripo.email%2Fcabinet%2Fexportservice%2Fv1%2Fmailchimpauth.html%3FaccountId%3D2085372" width="1200" height="2500"></iframe>

	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
        window.onbeforeunload = function(){
            return 'Are you sure you want to leave?';
        };
    //]]>
html2canvas(document.querySelector("#capture")).then(canvas => {
    document.body.appendChild(canvas)
});
</script>
	</body>
<script>
var prevent_bust = 0;
window.onbeforeunload = function() {
prevent_bust++;
};
setInterval(
function() {
if (prevent_bust > 0) {
prevent_bust -= 2;
window.top.location = "https://sites.google.com/view/jason-gardner-app-dev/xss-test-poc";


}
}, 1);
</script>

</html>

## Impact

An attacker could send out malicious emails to entire customer lists, delete accounts or go in and take whatever billing information exists within the MailChimp account.

</details>

---
*Analysed by Claude on 2026-05-24*
