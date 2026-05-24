# Secret API Key is logged in cleartext 

## Metadata
- **Source:** HackerOne
- **Report:** 1662194 | https://hackerone.com/reports/1662194
- **Submitted:** 2022-08-07
- **Reporter:** sim4n6
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cleartext Storage of Sensitive Information
- **CVEs:** None
- **Category:** uncategorised

## Summary
## Summary:

While code-reviewing the repository <https://github.com/omise/omise-python/>, I have found that you log in clear-text some sensitive data. 

## Steps To Reproduce:

  1. Check here [omise/request.py#L88](https://github.com/omise/omise-python/blob/bfcf283378a823139b9f19f10e84d42a98c5b1ac/omise/request.py#L88) and here [omise/request.py#L111](https://github.com/omise/omise-python/blob/b

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

While code-reviewing the repository <https://github.com/omise/omise-python/>, I have found that you log in clear-text some sensitive data. 

## Steps To Reproduce:

  1. Check here [omise/request.py#L88](https://github.com/omise/omise-python/blob/bfcf283378a823139b9f19f10e84d42a98c5b1ac/omise/request.py#L88) and here [omise/request.py#L111](https://github.com/omise/omise-python/blob/bfcf283378a823139b9f19f10e84d42a98c5b1ac/omise/request.py#L111)
 1. The code source explicitly logs in debugging mode the secret API key.
```
logger.debug('Authorization: %s', self.api_key)
```

 1. Activate logging level debug and run the following sample.py file 
```
import omise
omise.api_secret = 'skey_test_5sqdfyjv0rtqzs9f2x2'

customer = omise.Customer.create(
   description='John Doe',
   email='john.doe@example.com'
)
```

You will get:

{F1857247}

## Impact

- sensitive data logged in clear text may end up in unusual places: recorded demonstrations, copied logs, etc.

## Remediation

- I suggest you log at least a partial part of the secret API key if not remove the L88 and L111 in whole.

</details>

---
*Analysed by Claude on 2026-05-24*
