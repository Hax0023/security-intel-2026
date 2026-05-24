# Not clearing hex-decoded variable after usage in Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 168293 | https://hackerone.com/reports/168293
- **Submitted:** 2016-09-14
- **Reporter:** sstok
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
All the sensitive information variables are zeroed from memory, expect the hex2bin value of "validator".

https://github.com/paragonie/airship/blob/8f04f071c414c3893cf66311839d20a343af1237/src/Engine/Security/Authentication.php#L223-L236

```
        $stored = \Sodium\hex2bin($record[$f['validator']]);
        \Sodium\memzero($record[$f['validator']]);
        if (!\hash_equals($stored, $val)) {
 

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

All the sensitive information variables are zeroed from memory, expect the hex2bin value of "validator".

https://github.com/paragonie/airship/blob/8f04f071c414c3893cf66311839d20a343af1237/src/Engine/Security/Authentication.php#L223-L236

```
        $stored = \Sodium\hex2bin($record[$f['validator']]);
        \Sodium\memzero($record[$f['validator']]);
        if (!\hash_equals($stored, $val)) {
            throw new LongTermAuthAlert(
                \trk('errors.security.invalid_persistent_token')
            );
        }
        $userID = (int) $record[$f['userid']];
        $_SESSION['session_canary'] = $this->db->cell(
            'SELECT session_canary FROM airship_users WHERE userid = ?',
            $userID
        );
        return $userID;
```

The encoded value of "validator" is zeroed from memory, but the **decoded** version is not.
The value of $stored is not returned anywhere, so it should be zeroed from memory.

Note. As the exception throw stops the flow, it should *also* be cleared when the hash doesn't equal 👍

</details>

---
*Analysed by Claude on 2026-05-24*
