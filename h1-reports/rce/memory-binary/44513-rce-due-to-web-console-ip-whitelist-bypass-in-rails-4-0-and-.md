# RCE due to Web Console IP Whitelist bypass in Rails 4.0 and 4.1

## Metadata
- **Source:** HackerOne
- **Report:** 44513 | https://hackerone.com/reports/44513
- **Submitted:** 2015-01-21
- **Reporter:** joernchen
- **Program:** Rails Security
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** IP Whitelist Bypass, Parser Differential, Remote Code Execution, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Rails Web Console in versions 4.0 and 4.1 contains an IP whitelist bypass vulnerability due to a parser differential between the TRUSTED_PROXIES regex and IPAddr class. An attacker can supply crafted X-Forwarded-For headers with alternative IPv6 notations (e.g., 0000::1) to bypass the whitelist and gain remote code execution capabilities. While intended for development environments, this could compromise developer machines if Web Console is accessible.

## Attack scenario
1. Attacker identifies a target running Rails 4.0 or 4.1 with Web Console enabled in development mode
2. Attacker crafts an HTTP request with X-Forwarded-For header containing alternative IPv6 notation (0000::1) that bypasses TRUSTED_PROXIES regex
3. Rails remote_ip middleware fails to recognize the crafted header as a trusted proxy due to regex mismatch
4. Web Console receives the request and uses IPAddr to validate the IP, which normalizes 0000::1 to ::1 and passes validation
5. Attacker gains access to Web Console interface with arbitrary code execution capability
6. Attacker executes malicious Ruby statements to compromise the developer's machine or application

## Root cause
Parser differential vulnerability: Rails 4.0/4.1 use regex patterns (^::1$) to strip trusted proxies from X-Forwarded-For headers, but Web Console validates against IPAddr class which normalizes IPv6 addresses. Alternative IPv6 notations like 0000::1 bypass the regex but normalize to ::1 in IPAddr, creating an inconsistency in IP validation logic.

## Attacker mindset
An attacker recognizes that development environments are often less protected than production and targets developer machines directly. By understanding the difference in how IP validation is performed at different layers of the Rails stack, the attacker exploits this inconsistency to bypass security controls designed to restrict sensitive debugging tools. The attacker exploits the fact that developers may run vulnerable versions without realizing the exposure.

## Defensive takeaways
- Use consistent IP validation mechanisms across all layers of the application stack
- Normalize and validate all IP address inputs before comparison using a single, well-tested library
- Implement defense-in-depth: don't rely solely on IP whitelisting for sensitive debugging tools
- Disable Web Console by default in all environments and require explicit opt-in
- Upgrade to Rails 4.2+ where this vulnerability was fixed
- Implement network-level controls to restrict access to development environment endpoints
- Use authentication mechanisms in addition to IP whitelisting for Web Console access
- Regularly audit and test IP validation logic for parser differentials

## Variant hunting
Check for similar parser differentials in other IP validation implementations across Rails versions
Investigate X-Forwarded-For parsing in other middleware layers for inconsistent IP normalization
Test other alternative IPv6 notation formats against Rails IP validation (e.g., compressed forms, leading zeros)
Examine Client-IP header handling for similar bypass techniques
Review other web frameworks' handling of alternative IP address notations
Audit custom IP whitelist implementations that may use regex instead of IPAddr normalization
Test for similar issues with IPv4 edge cases (e.g., octal notation, hexadecimal notation)

## MITRE ATT&CK
- T1190
- T1021
- T1133
- T1078

## Notes
This vulnerability was reported to Rails Security Team prior to public disclosure. The vulnerability primarily affects development environments but could compromise developer machines if Web Console is accessible remotely. The fix involved standardizing IP validation in Rails 4.2. This is a classic example of a parser differential vulnerability where different components interpret the same input differently, leading to security boundary bypass.

## Full report
<details><summary>Expand</summary>

With the release of Ruby on Rails 4.2 the so called [Web Console](https://github.com/rails/web-console) was introduced. 

As the Web Console documentation states:
*Web Console is built explicitly for Rails 4.*

By default the Web Console is available in the Rails Development Environment and allows only the IPs `127.0.0.1` and `::1` to access the console in order to evaluate arbitrary Ruby statements for the purpose of debugging.

However with Rails Versions 4.1 and 4.0 the Web Console built in IP whitelist is bypassable.
This is due to the fact that Web Console parses the `request.remote_ip` to check if the IP is whitelisted with the Ruby class `IPAddr`. The Rails stack prior to 4.2 when calculating `request.remote_ip` uses [these regular expressions](https://github.com/rails/rails/blob/4-1-stable/actionpack/lib/action_dispatch/middleware/remote_ip.rb#L31-38) to strip out trusted Proxies from the HTTP Headers `X-Forwarded-For` and `Client-IP`.

Due to this parser differential an attacker might bypass the Web Console IP whitelist by supplying a HTTP header value of:

`X-Forwarded-For: 0000::1` 

This IPv6 address in the given notation would bypass the `TRUSTED_PROXIES` entry `^::1$` but match the `IPAddr` value of `::1` within Web Console.

As the Web Console is *intended* for debugging in the Development Environment this will most likely not affect Production setups, unless Web Console is explicitly enabled. But gaining RCE on Developer laptops might be fun as well ;).

I've already sent a description of this to the Rails Security Team via mail, but I've been asked to submit here again. 

The easiest mitigation of this issue would be to disallow execution of Web Console within Rails < 4.2.

</details>

---
*Analysed by Claude on 2026-05-12*
