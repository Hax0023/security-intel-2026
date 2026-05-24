# 2FA Settings Changed Without Fund Freeze/Delay Protection

## Metadata
- **Source:** HackerOne
- **Report:** 16696 | https://hackerone.com/reports/16696
- **Submitted:** 2014-06-16
- **Reporter:** bbohn
- **Program:** Coinbase
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Insufficient Access Controls, Missing Security Delay Mechanism, Account Takeover, Weak 2FA Change Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Coinbase allowed 2FA settings to be changed without implementing a mandatory freeze or delay on fund withdrawals, enabling attackers who compromised email accounts to immediately withdraw funds. The lack of this security control permitted unauthorized Bitcoin purchases totaling $1,000 despite the 2FA method being changed from Authy to SMS.

## Attack scenario
1. Attacker compromises victim's email account through phishing or malware
2. Attacker uses password reset features to gain access to secondary accounts dependent on compromised email
3. Attacker exploits SMS interception vulnerability (Text to Web feature on AT&T) to capture SMS codes
4. Attacker changes Coinbase 2FA method from Authy (app-based) to SMS (interceptable)
5. Attacker immediately executes unauthorized Bitcoin withdrawals/purchases without triggering fund freeze
6. Legitimate account owner receives SMS notifications too late and discovers fraudulent transactions already processed

## Root cause
Coinbase failed to implement a security best practice standard in the cryptocurrency industry: mandatory delays or account freezes triggered when authentication mechanisms are modified. This absence allowed immediate exploitation of compromised accounts without giving legitimate users time to detect and respond to unauthorized 2FA changes.

## Attacker mindset
The attacker demonstrated sophisticated social engineering and account targeting strategy, conducting reconnaissance on victim's email inboxes for days before executing coordinated multi-platform attacks. The targeting of cryptocurrency accounts specifically shows intent to exploit known gaps in security controls for maximum financial gain within withdrawal limits.

## Defensive takeaways
- Implement mandatory 24-48 hour delays on all withdrawals following 2FA method changes
- Require email verification link confirmation before 2FA changes take effect
- Add notification and confirmation steps when switching from app-based 2FA (Authy) to SMS-based 2FA
- Implement account lockdown or freeze upon 2FA modification until user confirms via existing authentication method
- Add rate limiting and anomaly detection for authentication changes from unusual locations/devices
- Require step-up authentication (security questions, identity verification) before allowing 2FA downgrades
- Educate users about email account compromise risks and offer alternative recovery methods beyond email

## Variant hunting
Search for similar issues across cryptocurrency exchanges and financial platforms lacking fund freeze mechanisms on: password changes, email changes, withdrawal address whitelisting removals, 2FA downgrades, and payment method additions.

## MITRE ATT&CK
- T1190
- T1566
- T1098
- T1556
- T1021
- T1021.001

## Notes
This report predates modern cryptocurrency security standards but identifies a critical gap. The vulnerability chain demonstrates how email compromise cascades into account takeover. The attacker's use of AT&T's Text to Web feature shows supply chain attack elements. Industry consensus now requires security delays on 2FA changes, making this a validation of security best practices rather than novel vulnerability.

## Full report
<details><summary>Expand</summary>

With the nature of bitcoin's instant transactions and the increase level of phishing/malware attempts on users, many bitcoin related businesses have freeze/delays on funds once a user changes their 2FA settings.

That design keeps the 2FA from being defeated instantly if the user's email account has been breached.  It gives the true owner of an account time to respond to breaches and work with companies to prove identity if they lost access to their email account.  If there isn't a breach, and the user needs to change the 2FA legitimately, it is a simple delay on movement of funds in the name of security.

Recently I was attacked by a team of hackers that first gained access to my father's email account that had top level access to my email accounts.  The hackers read and researched my inboxes for days and staged a full attack on my online accounts Sunday 6/8.

They changed my email account passwords and used 'lost password' feature to gain access to my other accounts.  My ATT account was a first target where they added many features that even the online chat rep I spoke with did not know existed. Text to Web was activated and also call forwarding of incoming calls was also enabled.  Text to Web allows the hacker to view all text messages onto a web page.  I asked the rep if they had that type of service and he said that it didn't exist. It was enabled for over 24 hours since I was told it didn't exist but I stumbled upon the link and then saw all my SMS messages on a web page.  This feature removes any security with SMS and also allows hackers to reset/reinstall 2FA applications like Authy since SMS is used to sync.

I believe the hackers switched my Coinbase account from using Authy to just simple SMS codes.  I saw two authentication code text messages on my phone for the two fraudulent bitcoin purchases of $666.28 and $333.17 to max out the $1,000 daily limit.  I did not use that method before and am shocked that the account did not have any delay/freeze on funds after such a change.  

Other bitcoin businesses range from freezing the account as soon as the 2FA is altered to having a day delay on all withdrawals as standard policy.

I am out $1,000 and would like to know why Coinbase does not give their users the ability to protect themselves more when 1FA is breached and 2FA is being altered.

-Bill  

</details>

---
*Analysed by Claude on 2026-05-24*
