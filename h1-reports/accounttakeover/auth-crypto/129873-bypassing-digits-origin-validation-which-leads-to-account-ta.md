# Bypassing Digits Origin Validation via Regex Wildcard Exploitation Leading to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 129873 | https://hackerone.com/reports/129873
- **Submitted:** 2016-04-11
- **Reporter:** filedescriptor
- **Program:** Twitter/Digits
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Improper Input Validation, Insecure PostMessage Origin Verification, Regular Expression Injection, Authentication Bypass, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Digits SDK uses String.prototype.search() to validate postMessage origin, which implicitly converts the origin string to a regular expression where dots act as wildcards. An attacker can craft a domain like 'www.d.gits.co' that matches the regex pattern of 'www.digits.com', bypassing origin validation and receiving sensitive authentication data intended for legitimate sites.

## Attack scenario
1. Attacker registers or controls a domain matching Digits' origin pattern via regex wildcard abuse (e.g., www.d.gits.co where each dot is a wildcard)
2. Attacker hosts a malicious HTML page on this domain with JavaScript that mimics Digits authentication flow
3. Victim visits attacker's domain and clicks a button triggering postMessage communication with Digits iframe
4. Digits SDK receives postMessage from attacker's origin and performs flawed validation using search() method
5. Origin validation passes because regex wildcard matching succeeds (www.d.gits.co matches www.digits.com pattern)
6. Digits sends authentication token/phone number data to attacker's domain, attacker associates it with victim's account and performs silent account takeover

## Root cause
The origin validation logic uses String.prototype.search(t.origin) which implicitly converts the origin string parameter to a regular expression. In regex syntax, dots (.) are metacharacters matching any single character, allowing 'www.d.gits.co' to match 'www.digits.com'. The developers mistakenly treated search() as a string matching function when it performs regex pattern matching.

## Attacker mindset
An attacker identifies that postMessage communication is commonly vulnerable to origin spoofing and recognizes the specific implementation flaw where string-to-regex conversion enables wildcard matching. They exploit this to establish an authentication channel with Digits' backend, capture session tokens silently, and perform account takeover on integrated services like Fabric without user awareness or interaction.

## Defensive takeaways
- Always use strict string comparison (=== or exact match) for origin validation, never pass user-controlled strings to regex constructors or methods without explicit intent
- Replace String.search() with String.includes() or direct equality checks for origin validation in postMessage handlers
- Implement allowlist-based origin validation that explicitly compares against known trusted origins rather than pattern matching
- Escape or sanitize any string converted to regex to prevent metacharacter interpretation
- Use static analysis tools to detect implicit string-to-regex conversions in security-critical code paths
- Add origin validation at multiple layers: both on SDK side and backend message verification
- Implement additional message signing/HMAC validation beyond origin checks to prevent replay and spoofing attacks
- Regularly audit all postMessage implementations for similar origin validation bypasses

## Variant hunting
Search for other postMessage handlers using String.search(), String.match(), or RegExp constructors with unsanitized origin values. Look for similar patterns in third-party authentication SDKs, OAuth implementations, and cross-origin communication frameworks. Check for implicit regex conversions in other JavaScript authentication libraries and browser extension communication channels.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1185 - Man in the Middle
- T1078 - Valid Accounts
- T1550 - Use Alternate Authentication Material

## Notes
This vulnerability demonstrates how subtle JavaScript API misunderstandings can lead to critical security flaws. The attacker doesn't need user interaction for account takeover as Digits silently processes authenticated postMessages. The vulnerability affected Twitter's official Fabric SDK, a widely-used mobile development platform. The PoC domain 'www.d.gits.co' is a clever exploitation of regex wildcards where each dot can match any character, making 'www.d.gits.co' a valid regex match for 'www.digits.com'. This is a classic example of using the wrong tool for the job - search() is designed for pattern matching, not strict origin validation.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report an important issue that affects websites that has integrated "Signin with Digits" , leading to potential account takeover.

#Detail
In Digits architecture, the data communication channel between Digits and customer's site relies on *postMessage()*. In order to prevent malicious websites prevent themselves to be the legit Digits website and send arbitrary commands to the customer's websites, an origin validation is in place in the SDK. Specifically, the code that's responsible to perform the validation is as follow:

**File: https://cdn.digits.com/1/sdk.js**
```javascript
e.exports = {
    sdk_host: "https://www.digits.com",
[..]
onReceiveMessage: function(t) {
    this.config && -1 !== this.config.get("sdk_host").search(t.origin) && this.resolve(t.data)
},
```
In short, the event origin is checked against Digits' origin in this line:`-1 !== this.config.get("sdk_host").search(t.origin)`, which is the same as `-1 !== "https://www.digits.com".search(t.origin)`. In essence, it looks for the occurrence of Digit's origin from sender's origin.

The way the validation is done is however flawed. According to the [docs of String.prototype.search()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/search), the method takes a regular repression object instead of a string. If anything other than regexp is passed, it will get implicitly converted into a regexp. In this case, `t.origin` which is a string is converted into a regexp.

In regular expression, a dot (.) is treated as a wildcard. In other words, any character of Digits' origin can be replaced with a dot. An attacker can take advantage of it and use a special domain instead of the official one to bypass the validation, such as `www.d.gits.co`

An example of comparing such a special domain looks like this: 
`www.d.gits.co`
`www.digits.com`
Notice that `www.d.gits.co` is now a subset of `www.digits.com`, thus it effective bypasses the validation.

#Impact
It affects websites that have integrated Digits signin feature, leading to potential account takeover issue on those websites. Twitter official applications like Fabric is also affected.

#PoC
To provide a concrete example of how this vulnerability can lead to account takeover, a Proof of Concept against Fabric is presented.

1. Make sure you have logged in Fabric.io
2. Go to https://www.d.gits.co/fabric.html
3. Click the button
4. You will see a phone number is automatically associated with your account
5. Now, attacker can use the reset password with Digits feature to takeover the account

Notice the attack can be done silently without user interaction and awareness.

A video demo: https://vimeo.com/162397716 (password: origin)

#Fix
In my opinion, a simple string comparison is enough for validation. Therefore I recommend changing it to use either `indexOf` or `===`.

</details>

---
*Analysed by Claude on 2026-05-11*
