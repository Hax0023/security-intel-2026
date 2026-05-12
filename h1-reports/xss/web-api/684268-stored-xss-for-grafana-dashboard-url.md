# Stored XSS in Grafana Dashboard URL Configuration via Unvalidated Protocol

## Metadata
- **Source:** HackerOne
- **Report:** 684268 | https://hackerone.com/reports/684268
- **Submitted:** 2019-08-29
- **Reporter:** xanbanx
- **Program:** GitLab
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, URL Protocol Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's admin metrics and profiling settings where the Grafana dashboard URL field fails to validate the protocol, allowing administrators to inject javascript: protocol payloads. When other administrators access the metrics dashboard, the malicious JavaScript executes in their session context, enabling CSRF token theft and account compromise.

## Attack scenario
1. Malicious administrator navigates to /admin/application_settings/metrics_and_profiling#js-grafana-settings
2. Administrator enters a javascript: protocol payload (e.g., javascript:alert(window.opener.document.location)) in the Grafana domain field
3. Payload is stored without protocol validation in the application database
4. Victim administrator visits Monitoring > Metrics Dashboard page containing the malicious link
5. Victim clicks the Grafana dashboard link which opens in new tab (target=_blank)
6. JavaScript payload executes in victim's session context with access to window.opener, allowing CSRF token theft and privilege escalation

## Root cause
The Grafana dashboard URL input field performs insufficient validation, accepting any protocol (including javascript:) without restricting to http or https schemes. The URL is stored and rendered as a clickable link without sanitization or protocol enforcement.

## Attacker mindset
A malicious administrator seeking to escalate privileges or compromise other administrator accounts. By injecting JavaScript that exploits window.opener, they bypass the protection of target=_blank, gaining access to the victim's session context to steal CSRF tokens and perform unauthorized actions like SSH key injection.

## Defensive takeaways
- Implement strict URL validation that only permits http:// and https:// protocols
- Use URL parsing libraries to validate protocol before storage
- Apply Content Security Policy (CSP) headers to prevent javascript: protocol execution
- Sanitize or escape URL output when rendering in HTML contexts
- Implement CSRF token rotation and SameSite cookie attributes
- Add additional validation layers for sensitive configuration fields
- Consider using rel=noopener noreferrer on all external links
- Audit all URL input fields application-wide for similar bypasses
- Implement security testing for protocol validation in input validation logic

## Variant hunting
Search for other URL input fields in admin settings (monitoring, integrations, webhooks, etc.)
Check for similar protocol validation issues in project/group settings
Look for data: protocol injection in URL fields
Test vbscript: and other browser-executable protocols
Review all <a> tag rendering without protocol validation
Search for URL fields that use regex instead of proper URL parsing
Check settings that accept URLs but don't enforce HTTPS
Look for stored URLs rendered in SVG or other contexts where javascript: executes

## MITRE ATT&CK
- T1190
- T1539
- T1566
- T1655

## Notes
This vulnerability is particularly dangerous because it targets administrators with high-privilege accounts. The use of window.opener to bypass target=_blank protection is a sophisticated exploitation technique. The proof-of-concept demonstrates actual credential theft capability through CSRF token extraction and SSH key injection, making this a critical privilege escalation vector. The vulnerability exists in GitLab 12.3.0-pre and likely affects multiple versions.

## Full report
<details><summary>Expand</summary>

Hi GitLab Security Team 

### Summary

I found a stored XSS vulnerability in the admins page. The administrator can set up a Grafana dashboard. Here, the administrator can either enter a relative URL or an absolute address. However, when adding an absolute URL, the protocol is not checked allowing to add a Javascript payload. However, when clicking on the URL, the corresponding `<a>` contains the `target="_blank"` attribute, which means a new tab is opened. However, by exploiting the `window.opener` attribute, I still can access the original tab allowing me to steal for example the CSRF token.

### Steps to reproduce

Tested locally on GitLab Enterprise 12.3.0-pre 7e45734123b

1. As an administrator go to `http://example.gitlab.com/admin/application_settings/metrics_and_profiling#js-grafana-settings`
2. Enter the following payload `javascript:alert(window.opener.document.location)`
3. Within the admin sidebar open `Monitoring ->  Metrics Dashboard`

See the the Javascript being executed

### Impact

Stored Javascript code is being executed on behalf of another user's session. Although this is only visible within the admins page, it's severity is the same. A malicious administrator can attack other administrator users with that. For example, the CSRF token can be stolen allowing, i.e., to add the attacker's SSH key to the victims user account. This can be done for example using the following payload:

```
javascript:var csrf = window.opener.$('meta[name=csrf-token]').attr('content'); window.opener.$.post('/profile/keys', { 'authenticity_token': csrf, 'key[key]': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDUXhvMZ/BFqgVY4iWWv2lrs2alZHA6CoNcnZWH7gxObXGeFK89/itFbI8NrEDE291LRScBL1nuHs0xlf7uidf97uFGVMyIW8TKeaG/j5q6olr9ejiOZhiiGGkQZf1iSTV4VYN77EtG7iV62VB1ZbwnCau1xT5mlXbd8E4WzaHIxuOY8Ao8EozouaQzWt+I1xJx5rufVwItmTaX5QKV5Cuv8GhMRUb1UqujNKr22/rbWnut0pSzB1+uE4S4E1AaCNX9Byy0z65nzupk5kdj8y/qJ3pk8UBOgQtJCFEOwc42EHS3JwTeMRNRXs9bwqRJfXUomXL1LZ5Eua7UX7aQq7pf admin@foo.com', 'key[title]': 'admin@foo.com' });
```

### What is the current *bug* behavior?

The URL entered in the Grafana domain is not validated allowing arbitrary javascript being entered.

### What is the expected *correct* behavior?

The URL input field should only allow valid URLs for http(s).

### Relevant logs and/or screenshots

(Paste any relevant logs - please use code blocks (```) to format console output,
logs, and code as it's very hard to read otherwise.)

### Output of checks

#### Results of GitLab environment info

```
System information
System:         Ubuntu 18.04
Proxy:          no
Current User:   xanbanx
Using RVM:      no
Ruby Version:   2.6.3p62
Gem Version:    3.0.3
Bundler Version:1.17.2
Rake Version:   12.3.2
Redis Version:  4.0.9
Git Version:    2.23.0
Sidekiq Version:5.2.7
Go Version:     go1.12.6 linux/amd64

GitLab information
Version:        12.3.0-pre
Revision:       7e45734123b
Directory:      /home/xanbanx/gdk/gdk-ee/gitlab
DB Adapter:     PostgreSQL
DB Version:     10.10
URL:            http://localhost:3001
HTTP Clone URL: http://localhost:3001/some-group/some-project.git
SSH Clone URL:  ssh://xanbanx@localhost:2222/some-group/some-project.git
Elasticsearch:  no
Geo:            no
Using LDAP:     no
Using Omniauth: yes
Omniauth Providers: 

GitLab Shell
Version:        9.4.1
Repository storage paths:
- default:      /home/xanbanx/gdk/gdk-ee/repositories
GitLab Shell path:              /home/xanbanx/gdk/gdk-ee/gitlab-shell
Git:            /usr/bin/git

```

Best,
Xanbanx

## Impact

See above

</details>

---
*Analysed by Claude on 2026-05-12*
