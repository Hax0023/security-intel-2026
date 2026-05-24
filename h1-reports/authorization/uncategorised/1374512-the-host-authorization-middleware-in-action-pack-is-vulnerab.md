# Host Authorization Middleware Vulnerable to Crafted X-Forwarded-Host Values (Case Sensitivity Bypass)

## Metadata
- **Source:** HackerOne
- **Report:** 1374512 | https://hackerone.com/reports/1374512
- **Submitted:** 2021-10-19
- **Reporter:** mshtawythug
- **Program:** Rails (github.com/rails/rails)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, Host Header Validation Bypass, Case Sensitivity Logic Error
- **CVEs:** CVE-2021-22942
- **Category:** uncategorised

## Summary
The Host Authorization middleware in Action Pack fails to properly validate X-Forwarded-Host headers when they contain mixed or uppercase characters due to a missing `.downcase()` call. This allows attackers to bypass host authorization checks and redirect users to arbitrary domains. The vulnerability is a regression from the CVE-2021-22881 fix that incompletely addressed host validation logic.

## Attack scenario
1. Attacker identifies a Rails application using Host Authorization middleware with configured allowed hosts
2. Attacker crafts a request with X-Forwarded-Host header containing mixed case (e.g., 'Evil.com') or uppercase (e.g., 'EVIL.COM') domain
3. The middleware attempts to match the forwarded_host against valid_host pattern but fails because forwarded_host is not lowercased
4. The failed regex match returns nil for forwarded_host variable
5. The authorization check evaluates the condition: origin_host && permissions.allows?(origin_host) && (forwarded_host.nil? || permissions.allows?(forwarded_host))
6. Since forwarded_host is nil, the second part of the OR expression returns true, bypassing the host validation and allowing the redirect to attacker's domain

## Root cause
Missing `.downcase()` method call on the X-Forwarded-Host header value during regex matching. The origin_host uses `.downcase()` on HTTP_HOST but forwarded_host processing omits this normalization, causing case-sensitive regex match failures that result in nil values. The authorization logic incorrectly interprets nil as a passing condition due to the `forwarded_host.nil?` check in the OR clause.

## Attacker mindset
Attacker recognizes that recent security patches often have incomplete implementations and searches for edge cases. They understand HTTP header case-sensitivity handling and exploit the inconsistency between uppercase/mixed-case header matching in authorization logic. This is a bypass of a previous CVE fix, suggesting they actively hunt for regression vulnerabilities.

## Defensive takeaways
- Normalize all host/domain values consistently using the same case conversion (e.g., .downcase()) before any comparison or regex matching operations
- Avoid null/nil checks in authorization logic that inadvertently grant access when validation fails; use explicit deny-by-default approach
- Apply consistent validation rules across all sources of the same data (HTTP_HOST and X-Forwarded-Host should use identical logic)
- Include test cases for case-sensitivity edge cases when validating host headers
- Use canonical forms of hostnames before any authorization decision
- Review boolean logic in authorization checks to ensure nil/false states don't bypass security controls
- When patching security issues, verify the fix applies to all code paths handling the same data

## Variant hunting
Check for similar case-sensitivity issues in other middleware validation logic (e.g., X-Forwarded-Proto, X-Forwarded-For)
Hunt for other nil-checks in authorization boolean expressions that might unexpectedly grant access
Look for inconsistent .downcase() usage across different header validation routines in web frameworks
Search for regex matching operations on headers that don't normalize case beforehand
Test authorization bypasses using URL encoding variations and mixed-case HTTP headers in other Rails middleware
Examine host validation in reverse proxy configurations (nginx, Apache) for similar case-sensitivity issues
Check for incomplete patches to previous CVE-2021-22881 in older Rails versions

## MITRE ATT&CK
- T1190
- T1557
- T1598

## Notes
This is a follow-up vulnerability to CVE-2021-22881. The initial patch in commit 83a6ac3 was incomplete, failing to account for case-sensitivity in all code paths. Affects Rails <= 6.1.3.1. The vulnerability demonstrates how security patches must be comprehensive across all related code paths. The logic error shows how defensive programming practices like 'fail secure' are critical in authorization middleware.

## Full report
<details><summary>Expand</summary>

Title:         The Host Authorization middleware in Action Pack is vulnerable to crafted X-Forwarded-Host values
Scope:         https://github.com/rails/rails
Weakness:      Open Redirect
Severity:      Medium
Link:          https://hackerone.com/reports/1189310
Date:          2021-05-09 06:29:19 +0000
By:            @mshtawy
CVE IDs:       CVE-2021-22942, CVE-2021-22881

Details:
### Steps to reproduce
This is a follow up to  [CVE-2021-22881](https://github.com/advisories/GHSA-8877-prq4-9xfw) and  https://github.com/rails/rails/commit/83a6ac3fee8fd538ce7e0088913ff54f0f9bcb6f

with a controller like the following
```ruby
class TestsController < ApplicationController
  extend ActiveSupport::Concern

  def index
    redirect_to('/')
  end
end
```
when sending a request like the following where the URL has a mixed case characters 
``` bash
curl 'http://localhost:3000/tests' -H 'X-Forwarded-Host: Evil.com'
```
Or all capital case 
``` bash
curl 'http://localhost:3000/tests' -H 'X-Forwarded-Host: EVIL.COM'
```

### Expected behavior
```html
<div id="container">
  <h2>To allow requests to evil.com, add the following to your environment configuration:</h2>
  <pre>config.hosts &lt;&lt; "Evil.com"</pre>
</div>
```

### Actual behavior
```html
<html><body>You are being <a href="http://Evil.com/">redirected</a>.</body></html>% 
```

### System configuration
**Rails version**: 
Tested on Rails 6.1.3.1 and Rails 6.1.3.2
**Ruby version**:
N/A

### Notes

This was fixed in `main` in this PR https://github.com/rails/rails/pull/41435 but still affects <= 6.1.3.1 

The problem is in this code https://github.com/rails/rails/blob/6-1-stable/actionpack/lib/action_dispatch/middleware/host_authorization.rb#L115

``` ruby
origin_host = valid_host.match(
  request.get_header("HTTP_HOST").to_s.downcase)
forwarded_host = valid_host.match(
  request.x_forwarded_host.to_s.split(/,\s?/).last)
```

`forwarded_host` is missing a `downcase` after the `.to_s`, which results in `nil` assigned to `forwarded_host`, which then results in `true` in the following  code
```ruby
origin_host && @permissions.allows?(origin_host[:host]) && (forwarded_host.nil? || @permissions.allows?(forwarded_host[:host]))
```
because of the `nil?` check on the `forwarded_host`
```ruby
forwarded_host.nil? || @permissions.allows?(forwarded_host[:host])
```

The examples I gave are using `localhost`, but I also confirmed this using a production environment with a configuration like the following

```ruby
    Rails.application.config.hosts = %w(.EXAMPLE.com)
```

## Impact

Hackers can redirect victims to a malicious website.

Timeline:
2021-08-03 20:27:55 +0000: @tenderlove (bug triaged)


---

2021-09-07 20:30:35 +0000: @tenderlove (cve id added)


---

2021-10-05 20:37:19 +0000: @tenderlove (bug resolved)

## Impact

Hackers can redirect victims to a malicious website.

</details>

---
*Analysed by Claude on 2026-05-24*
