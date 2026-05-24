# Open Redirect in Rails ActionableExceptions Middleware (CVE-2020-8185 Incomplete Fix)

## Metadata
- **Source:** HackerOne
- **Report:** 904059 | https://hackerone.com/reports/904059
- **Submitted:** 2020-06-21
- **Reporter:** ooooooo_q
- **Program:** Rails
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** CVE-2020-8264, CVE-2020-8185
- **Category:** uncategorised

## Summary
Rails 6.0.0 through 6.0.3.1 contains an open redirect vulnerability in the actionable_exceptions middleware that directly redirects users based on unsanitized request parameters. The vulnerability allows attackers to redirect victims to arbitrary external URLs through a crafted POST request to the /rails/actions endpoint.

## Attack scenario
1. Attacker creates a malicious HTML form on attacker-controlled domain with POST action to vulnerable Rails application's /rails/actions endpoint
2. Form includes hidden parameter 'location' set to attacker's phishing or SSRF target URL
3. Victim visits attacker's page and submits the form (via button click or automatic submission)
4. Rails application processes POST request and validates it as an 'actionable request' in production mode
5. Middleware extracts unvalidated 'location' parameter and constructs HTTP 302 redirect response
6. Victim browser follows redirect to attacker-controlled destination, potentially for credential theft or internal network probing

## Root cause
The actionable_exceptions middleware in ActionPack directly uses user-supplied request.params[:location] in the Location HTTP header without validation or sanitization. The 'location' parameter is only HTML-escaped in the response body but the actual redirect header uses the raw untrusted value. This was an incomplete fix for CVE-2020-8185 which only addressed the HTML escaping aspect.

## Attacker mindset
An attacker would recognize that while the POST-to-GET conversion makes phishing less practical, the vulnerability remains valuable for bypassing referrer policies (redirecting from trusted domain to attacker domain), Server-Side Request Forgery attacks against internal services, and potentially CORS bypass scenarios where the redirect origin matters more than the method.

## Defensive takeaways
- Always validate and whitelist redirect destinations; never trust user input for Location headers
- Use a URL validator that checks against an allowlist of safe domains/paths rather than attempting to fix unvalidated input after-the-fact
- Apply the same validation rigor to Location headers as to other security-critical parameters
- Implement redirect security checks at framework level, not just at view/escaping level
- Consider whether exception-handling middleware should ever redirect to user-supplied locations
- Test security fixes comprehensively across all code paths that use the vulnerable parameter

## Variant hunting
Search for similar patterns: (1) other middleware or controllers that accept 'location' parameters, (2) any exception handling code that constructs redirects, (3) uses of request.params in Location headers anywhere in ActionPack or Rails ecosystem, (4) incomplete input sanitization where HTML escaping is applied but URL validation is missing

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1190 - Exploit Public-Facing Application
- T1201 - Password Policy Discovery
- T1557.002 - Man-in-the-Browser

## Notes
This CVE represents an important lesson in security fix validation - the initial CVE-2020-8185 fix addressed HTML escaping but missed the core validation issue. The fix in 6.0.3.2 changed the actionable_request conditions, making exploitation harder but not eliminating the root cause. The POST-method requirement actually provides some natural mitigation against casual phishing but doesn't prevent sophisticated attacks or SSRF abuse. The researcher correctly identified that this deserves separate security announcement despite being related to CVE-2020-8185.

## Full report
<details><summary>Expand</summary>

Hello,
I was looking at the change log (https://github.com/rails/rails/commit/2121b9d20b60ed503aa041ef7b926d331ed79fc2) for CVE-2020-8185 and found another problem existed.

https://github.com/rails/rails/blob/v6.0.3.1/actionpack/lib/action_dispatch/middleware/actionable_exceptions.rb#L21

```ruby
  redirect_to request.params[:location]
end

private
  def actionable_request?(request)
    request.show_exceptions? && request.post? && request.path == endpoint
  end

  def redirect_to(location)
    body = "<html><body>You are being <a href=\"#{ERB::Util.unwrapped_html_escape(location)}\">redirected</a>.</body></html>"

    [302, {
      "Content-Type" => "text/html; charset=#{Response.default_charset}",
      "Content-Length" => body.bytesize.to_s,
      "Location" => location,
    }, [body]]
  end
```

There was an open redirect issue because the request parameter `location` was not validated.
In 6.0.3.2, since the condition of `actionable_request?` has changed, this problem is less likely to occur.


### PoC


#### 1. Prepare server

Prepare an attackable 6.0.3.1 version of Rails server

```
❯ rails -v
Rails 6.0.3.1

❯ RAILS_ENV=production rails s
...
* Environment: production
* Listening on tcp://0.0.0.0:3000
```

#### 2. Attack server 

Prepare the server for attack on another port.

```html
<form method="post" action="http://localhost:3000/rails/actions?error=ActiveRecord::PendingMigrationError&action=Run%20pending%20migrations&location=https://www.hackerone.com/">
	<button type="submit">click!</button>
</form>
````

```
python3 -m http.server 8000
```

#### 3. Open browser

Open the `http://localhost:8000/attack.html` url in your browser and click the button.
Redirect to `https://www.hackerone.com/` url.

{F876518}

## Impact

It will be fixed with 6.0.3.2 as with CVE-2020-8185(https://groups.google.com/g/rubyonrails-security/c/pAe9EV8gbM0), but I think it is necessary to announce it again because the range of influence is different.

This open redirect changes from POST method to Get Method, so it may be difficult to use for phishing.On the other hand, it may affect bypass of referrer check or SSRF.

</details>

---
*Analysed by Claude on 2026-05-24*
