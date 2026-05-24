# twitter api access token leaked on github 

## Metadata
- **Source:** HackerOne
- **Report:** 361089 | https://hackerone.com/reports/361089
- **Submitted:** 2018-06-02
- **Reporter:** sonahri501
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cleartext Storage of Sensitive Information
- **CVEs:** None
- **Category:** uncategorised

## Summary
sensitive token were leaked on GitHub page of liberapay . also mixpanel token was leaked
TWITTER_CONSUMER_KEY=QBB9vEhxO4DFiieRF68zTA
 TWITTER_CONSUMER_SECRET=mUymh1hVMiQdMQbduQFYRi79EYYVeOZGrhj27H59H78
+TWITTER_ACCESS_KEY=34175404-G6W8Hh19GWuUhIMEXK0LyZsy7N9aCMcy1bYJ9rI
+TWITTER_ACCESS_SECRET=K6wxV1OCsihZAkEPkWtoLYDiRJnWajBBWn4UgliTRQ
 TWITTER_CALLBACK=http://127.0.0.1:8537/on/twitter/associate
 M

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

sensitive token were leaked on GitHub page of liberapay . also mixpanel token was leaked
TWITTER_CONSUMER_KEY=QBB9vEhxO4DFiieRF68zTA
 TWITTER_CONSUMER_SECRET=mUymh1hVMiQdMQbduQFYRi79EYYVeOZGrhj27H59H78
+TWITTER_ACCESS_KEY=34175404-G6W8Hh19GWuUhIMEXK0LyZsy7N9aCMcy1bYJ9rI
+TWITTER_ACCESS_SECRET=K6wxV1OCsihZAkEPkWtoLYDiRJnWajBBWn4UgliTRQ
 TWITTER_CALLBACK=http://127.0.0.1:8537/on/twitter/associate
 MIXPANEL_TOKEN=cb9dec68ac0ee57071f0be39f164a417

## Impact

a attacker with your credentials can have severe impact

</details>

---
*Analysed by Claude on 2026-05-24*
