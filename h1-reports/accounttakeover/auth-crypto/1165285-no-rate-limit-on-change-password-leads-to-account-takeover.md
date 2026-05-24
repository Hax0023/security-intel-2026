# No Rate limit on change password leads to account takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1165285 | https://hackerone.com/reports/1165285
- **Submitted:** 2021-04-14
- **Reporter:** dreamispossible
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Restriction of Authentication Attempts
- **CVEs:** None
- **Category:** auth-crypto

## Summary
## Summary:
I found when login and go to changing password, there is no rate limit on that function, which leads to takeover the account.

## Steps To Reproduce:

1-Create account on (https://old.reddit.com) & move to your setting,```In my case I chose !23Qweasdzxc as the password.```

2-Go to change password on (https://old.reddit.com/prefs/update/#) & enter the wrong password in old password   a

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

## Summary:
I found when login and go to changing password, there is no rate limit on that function, which leads to takeover the account.

## Steps To Reproduce:

1-Create account on (https://old.reddit.com) & move to your setting,```In my case I chose !23Qweasdzxc as the password.```

2-Go to change password on (https://old.reddit.com/prefs/update/#) & enter the wrong password in old password   and enter new password and confirm the password.


3-Intercept the request & send it to Burp Intruder .

4-Make word-list & and start Brute Forcing.```Make sure to add the correct password in the wordlist, I made  8890 words in the wordlist```

finally you can see the correct password in the response.like the following response .
███


And as you can see I made more than 8000 requests.
and there is no rate limit.
{F1265803}

## Impact

If the attacker gets the user's cookies  through XSS or in somehow,he is able to takeover the account.

</details>

---
*Analysed by Claude on 2026-05-24*
