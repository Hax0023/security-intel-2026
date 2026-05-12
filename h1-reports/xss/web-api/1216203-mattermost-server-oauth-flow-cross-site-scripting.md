# Mattermost Server OAuth Flow Reflected Cross-Site Scripting (XSS)

## Metadata
- **Source:** HackerOne
- **Report:** 1216203 | https://hackerone.com/reports/1216203
- **Submitted:** 2021-06-03
- **Reporter:** shielder
- **Program:** Mattermost
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Input Validation Failure, Improper Output Encoding
- **CVEs:** CVE-2021-37859
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Mattermost OAuth flow where the 'redirect_to' query parameter is not sanitized before being reflected in HTML responses. An attacker can craft a malicious link that executes arbitrary JavaScript in the victim's browser, potentially allowing unauthorized access to chat contents or administrative privileges depending on the victim's role.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload in the 'redirect_to' parameter targeting the OAuth mobile login endpoint
2. Attacker distributes the malicious link via phishing email, social media, or other social engineering channels
3. Victim clicks the link while authenticated to Mattermost or in a state where authentication can be obtained
4. The OAuth flow processes the request and calls RenderMobileError, which concatenates the unsanitized redirect_to parameter into HTML
5. JavaScript payload executes in victim's browser with their authentication context
6. Attacker gains ability to read messages (regular user) or modify server settings/create admin accounts (administrative user)

## Root cause
The 'redirect_to' query parameter from the HTTP GET request is extracted at line 284 in oauth.go and directly concatenated into an HTML href attribute at line 111 in utils/api.go without any sanitization or HTML encoding. The parameter flows through completeOAuth -> RenderMobileError -> RenderMobileMessage -> fmt.Fprintln without validation, allowing arbitrary HTML/JavaScript injection.

## Attacker mindset
An attacker recognizes that OAuth flows often handle redirects and may not properly validate redirect parameters. By targeting the mobile OAuth endpoint specifically, they exploit a code path that generates HTML dynamically. The attacker understands that users trust OAuth flows and will click links, making social engineering feasible. They recognize that administrative users would provide maximum impact.

## Defensive takeaways
- Always sanitize and HTML-encode user-supplied input before reflecting it in HTML responses, especially redirect URLs
- Use allowlists for redirect URLs rather than arbitrary user input - validate that redirect_to points to expected domains
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Use templating engines with automatic escaping rather than string concatenation for HTML generation
- Apply security headers like X-XSS-Protection and X-Content-Type-Options
- Validate OAuth parameters against strict whitelist patterns before any HTML generation
- Conduct security code review for all OAuth and authentication-related endpoints

## Variant hunting
Search for other instances where query parameters are concatenated into HTML responses without encoding (grep for 'fmt.Fprintln' with concatenated user input)
Check other OAuth providers integrated with Mattermost for similar redirect_to parameter handling
Review WebSocket and API endpoints that handle redirect parameters
Look for similar patterns in error handling functions that may reflect user input
Examine other mobile-specific endpoints that may have similar mobile error rendering logic
Search for unsafe string concatenation patterns in template rendering across the codebase

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1566.002 - Phishing: Spearphishing Link
- T1203 - Exploitation for Client Execution
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token

## Notes
The vulnerability specifically affects the mobile OAuth login endpoint (/oauth/shielder/mobile_login) and demonstrates a classic reflected XSS through inadequate output encoding. The attack is particularly dangerous because OAuth flows are inherently trusted by users, making phishing more effective. The impact scales with user privileges - regular users lose confidentiality of messages while administrators could have their accounts completely compromised. The PoC uses URL encoding (%22 for quotes, %3E for >) to bypass basic filters. Mattermost should implement URL validation for the redirect_to parameter using a strict allowlist approach or URL parsing library to ensure only valid internal redirects are permitted.

## Full report
<details><summary>Expand</summary>

## Summary:
The vulnerability is a reflected Cross-Site Scripting (XSS) via the OAuth flow. A victim clicking a malicious link pointing to the target Mattermost host will trigger the XSS. If the victim is a regular user, it is possible to obtain all of their Mattermost chat contents; if it’s an administrator, it is possible to create a new administrator.

## Root Cause Analysis:
The application fails to sanitize an HTTP query parameter before reflecting it within the HTML response during the OAuth flow.

```go=280
        if props != nil {
                action = props["action"]
                isMobile = action == model.OAUTH_ACTION_MOBILE
                if val, ok := props["redirect_to"]; ok {
[1]                     redirectURL = val
                        hasRedirectURL = redirectURL != ""
                }
        }
        renderError := func(err *model.AppError) {
                if isMobile && hasRedirectURL {
[2]                     utils.RenderMobileError(c.App.Config(), w, err, redirectURL)
                } else {
                        utils.RenderWebAppError(c.App.Config(), w, r, err, c.App.AsymmetricSigningKey())
                }
        }
```

The file "/web/oauth.go" (https://github.com/mattermost/mattermost-server/blob/master/web/oauth.go) contains the function "completeOAuth" which on line 284 values the variable "redirectURL" with the parameter "redirect_to" [1] of the query string of the HTTP GET request. Subsequently always inside of the same function to the line 291 comes called the function "utils.RenderMobileError" to which it comes passed like argument the variable "redirectURL" [2].

```go=103
func RenderMobileError(config *model.Config, w http.ResponseWriter, err *model.AppError, redirectURL string) {
        RenderMobileMessage(w, `
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" style="width: 64px; height: 64px; fill: #ccc">
                        <!-- Font Awesome Free 5.15.3 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) -->
                        <path d="M569.517 440.013C587.975 472.007 564.806 512 527.94 512H48.054c-36.937 0-59.999-40.055-41.577-71.987L246.423 23.985c18.467-32.009 64.72-31.951 83.154 0l239.94 416.028zM288 354c-25.405 0-46 20.595-46 46s20.595 46 46 46 46-20.595 46-46-20.595-46-46-46zm-43.673-165.346l7.418 136c.347 6.364 5.609 11.346 11.982 11.346h48.546c6.373 0 11.635-4.982 11.982-11.346l7.418-136c.375-6.874-5.098-12.654-11.982-12.654h-63.383c-6.884 0-12.356 5.78-11.981 12.654z"/>
                </svg>
                <h2> `+i18n.T("error")+` </h2>
                <p> `+err.Message+` </p>
[1]                <a href="`+redirectURL+`">
                        `+i18n.T("api.back_to_app", map[string]interface{}{"SiteName": config.TeamSettings.SiteName})+`
                </a>
        `)
}
```

The function "RenderMobileError" is contained within the file "utils/api.go" (https://github.com/mattermost/mattermost-server/blob/master/utils/api.go) at line 103, and the fourth argument of this function is "redirectURL". At line 104 the "RenderMobileMessage" function is called and at line 111 the variable "redirectURL" is concatenated (without being sanitised) with another string argument of the "RenderMobileMessage" function [1].

```go=157
[...]
                        </head>
                        <body>
                                <!-- mobile app message -->
                                <div class="message-container">
[1]                                     `+message+`
                                </div>
                        </body>
                </html>
        `)
```

Inside the "RenderMobileMessage" function (declared at line 117 of utils/api.go) "fmt.Fprintln" is called to print the HTTP response and the HTML page is dynamically built concatenating the "message" variable [1] (second argument of the function).

Call graph:
completeOAuth -(redirectURL=redirect_to)-> util.RenderMobileError(*,redirectURL) -(message=string+redirectURL)-> RenderMobileMessage(*,message) -> fmt.Fprintln(string+message)

Since the HTTP GET request parameter "redirect_to" is never sanitized and is appended to the HTML page, it is possible to trigger a reflected XSS.

## Steps To Reproduce:
1. Visit the following URL after replacing <mattermost_url> with the domain/ip of the mattermost server instance:
https://<mattermost_url>/oauth/shielder/mobile_login?redirect_to=%22%3E%3Cimg%20src=%22%22%20onerror=%22alert(%27zi0Black%20@%20Shielder%27)%22%3E

2. Notice the JavaScript's generated pop-up

## Supporting Material/References:
  * [attachment / F1324661]

## Impact

The following attack scenarios have been identified:
- If the victim is a regular user, the attacker could read the messages sent and received by the user.
- If the victim is an administrative user, the attacker could change the server settings (e.g. add a new administrative user).

</details>

---
*Analysed by Claude on 2026-05-12*
