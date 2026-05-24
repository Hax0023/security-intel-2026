# Signature Validation Error Handling in php-saml LogoutRequest/LogoutResponse

## Metadata
- **Source:** HackerOne
- **Report:** 213789 | https://hackerone.com/reports/213789
- **Submitted:** 2017-03-15
- **Reporter:** lukasreschke
- **Program:** Not specified (php-saml library vulnerability report)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper Input Validation, Cryptographic Failure, Type Confusion
- **CVEs:** None
- **Category:** uncategorised

## Summary
The php-saml library improperly handled signature verification errors in LogoutRequest/LogoutResponse processing by performing implicit boolean conversion on openssl_verify() return values. This caused cryptographic verification failures (return value -1) to be treated as successful verifications (boolean true), allowing potential SAML logout message tampering.

## Attack scenario
1. Attacker intercepts a legitimate LogoutRequest or LogoutResponse in transit
2. Attacker modifies the SAML message content (e.g., logout target, user identifiers)
3. Attacker re-signs the message with an invalid key or deliberately corrupts the signature
4. During verification, openssl_verify() encounters an error and returns -1
5. The php-saml library converts -1 to boolean true via implicit type casting
6. The modified logout message is accepted as valid, allowing the attacker to manipulate logout behavior

## Root cause
The LogoutRequest/LogoutResponse signature validator performed implicit boolean conversion on the return value of the verify() method without explicit checking for the three distinct return states (1=success, 0=failure, -1=error). The implicit PHP type conversion treats both 1 and -1 as truthy values, making errors indistinguishable from valid signatures.

## Attacker mindset
An attacker would exploit this to manipulate SAML logout flows by sending specially crafted logout messages that trigger signature verification errors. This could enable session fixation, account takeover via logout manipulation, or replay attacks in SSO implementations.

## Defensive takeaways
- Always explicitly check cryptographic function return values instead of relying on implicit type conversion
- Distinguish between success (1), failure (0), and error (-1) states in OpenSSL verification functions
- Implement strict return value validation: if (openssl_verify(...) !== 1) { reject }
- Apply security updates to cryptographic libraries and SAML implementations promptly
- Use static analysis tools to detect implicit boolean conversions on security-critical functions
- Test error handling paths in signature validation code with malformed/corrupted signatures
- Consider using safer language features that prevent implicit type coercion in security contexts

## Variant hunting
Check other SAML message types (AuthnRequest, Response, Assertion) for similar implicit conversion bugs
Audit other uses of XMLSecurityKey::verifySignature() in php-saml and dependent libraries
Search for other implicit boolean conversions on openssl_verify(), openssl_sign(), hash_hmac_algos() outputs
Review XML signature verification in other SAML libraries (java-saml, python3-saml) for equivalent issues
Examine other cryptographic function wrappers that might suffer from similar type confusion patterns
Investigate if SAMLAssertion verification (noted as unaffected) has different explicit validation that could be replicated

## MITRE ATT&CK
- T1190
- T1556
- T1485

## Notes
This vulnerability had lower impact because SAMLResponse signature validation was not affected (presumably using explicit return value checking). The fix required updating to php-saml 2.10.5 or later. This is a classic example of how implicit type casting in dynamically-typed languages can create security vulnerabilities in cryptographic implementations. The vulnerability primarily affected logout flows, which are often less monitored than authentication flows in SSO systems.

## Full report
<details><summary>Expand</summary>

The php-saml library as used by our SSO implementation had a minor security patch in 2.10.4 as per https://github.com/onelogin/php-saml/commit/949359f5cad5e1d085c4e5447d9aa8f49a6e82a1.  So we should update this in our next minor releases.

> Security update for signature validation on LogoutRequest/LogoutResponse.
>
> In order to verify Signatures on Logoutrequests and LogoutResponses we use
> the verifySignature of the class XMLSecurityKey from the xmlseclibs library.
> That method end up calling openssl_verify() depending on the signature algorithm used.
> 
> The openssl_verify() function returns 1 when the signature was successfully verified,
> 0 if it failed to verify with the given key, and -1 in case an error occurs.
> PHP allows translating numerical values to boolean implicitly, with the following correspondences:
> - 0 equals false.
> - Non-zero equals true.
> 
> This means that an implicit conversion to boolean of the values returned by openssl_verify()
> will convert an error state, signaled by the value -1, to a successful verification of the
> signature (represented by the boolean true).
> 
> The LogoutRequest/LogoutResponse signature validator was performing an implicit conversion > to boolean
> of the values returned by the verify() method, which subsequently will return the same output
> as openssl_verify() under most circumstances.
> This means an error during signature verification is treated as a successful verification by the  method.
>
> Since the signature validation of SAMLResponses were not affected, the impact of this security
vulnerability is lower, but an update of the php-saml toolkit is recommended.

</details>

---
*Analysed by Claude on 2026-05-24*
