# Google Authenticator - Cross Site Scripting

## Metadata
- **Source:** HackerOne
- **Report:** 172606 | https://hackerone.com/reports/172606
- **Submitted:** 2016-09-28
- **Reporter:** iamsha4yan
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello
#Vulnerable File: :
`/views/token-prompt.php`

#Vulnerable Link : 
`15`
`<input type="hidden" name="gapup_login_nonce" value="<?php echo esc_attr( $_REQUEST['gapup_login_nonce'] ) ?>" />`

# Vulnerable Code:
`<?php echo esc_attr( $_REQUEST['gapup_login_nonce'] ) ?>`

Good Luck/

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

Hello
#Vulnerable File: :
`/views/token-prompt.php`

#Vulnerable Link : 
`15`
`<input type="hidden" name="gapup_login_nonce" value="<?php echo esc_attr( $_REQUEST['gapup_login_nonce'] ) ?>" />`

# Vulnerable Code:
`<?php echo esc_attr( $_REQUEST['gapup_login_nonce'] ) ?>`

Good Luck/

</details>

---
*Analysed by Claude on 2026-05-24*
