# Apple SecTrust Legacy Path Certificate Validation Bypass in libcurl

## Metadata
- **Source:** HackerOne
- **Report:** 3374554 | https://hackerone.com/reports/3374554
- **Submitted:** 2025-10-07
- **Reporter:** giant_anteater
- **Program:** libcurl
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Type Confusion, Logic Error, Certificate Validation Bypass, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
libcurl built with USE_APPLE_SECTRUST on pre-10.14 macOS/iOS contains a type confusion bug where OSStatus is incorrectly compared to SecTrustResultType enum values, causing the certificate validation result to never be checked. This allows untrusted certificates to be accepted when the native Apple CA store is used.

## Attack scenario
1. Attacker sets up malicious TLS server with self-signed or otherwise untrusted certificate
2. Victim uses curl built with USE_APPLE_SECTRUST on macOS <10.14 or iOS <12 to connect to attacker-controlled URL
3. LibCurl invokes OpenSSL or GnuTLS backend which fails local certificate validation
4. Backend delegates to Apple SecTrust verification via legacy path (pre-10.14 code)
5. Legacy code confuses OSStatus with SecTrustResultType, failing to check actual sec_result variable
6. Connection succeeds despite untrusted certificate, enabling Man-in-the-Middle attack

## Root cause
Variable type confusion in lib/vtls/apple.c lines 270-271: the code compares 'status' (OSStatus type) against 'kSecTrustResultUnspecified' and 'kSecTrustResultProceed' (SecTrustResultType enum values) instead of comparing the actual 'sec_result' variable. OSStatus value 0 (noErr) will never equal kSecTrustResultType values, causing the validation result check to always fail silently and leave result as CURLE_OK.

## Attacker mindset
An attacker conducting MITM attacks targets curl users on legacy Apple systems. By exploiting this logic error, they can intercept HTTPS traffic without detection by simply presenting an untrusted certificate. The bug is particularly valuable because it's in the certificate validation layer—the last security checkpoint.

## Defensive takeaways
- Use static analysis tools to catch type mismatches in security-critical code paths, especially enum comparisons
- Maintain separate test coverage for platform-specific code paths and legacy OS versions
- Implement mandatory code review processes for certificate validation logic with domain expertise
- Use type-safe APIs that prevent OSStatus/SecTrustResultType confusion (e.g., SecTrustEvaluateWithError)
- Add compile-time assertions or runtime sanity checks to verify trust evaluation results before accepting connections
- Deprecate and remove legacy API paths on older OS versions with clear migration guidance
- Test with untrusted certificate matrices as part of security regression testing

## Variant hunting
Search for other enum/status code type confusions in vtls/ backends (GnuTLS, OpenSSL, Schannel, Secure Transport wrappers)
Audit all SecTrust API calls for correct variable references in conditional branches
Review other Apple API legacy code paths for similar result-checking bugs (SecCertificateCreate, SecKeyCreate)
Examine other TLS backends for inverted or missing validation checks in fallback paths
Look for similar pattern: declaring one variable (sec_result) but checking another (status) in security decisions
Check for unreachable code or dead variable assignments in certificate validation paths

## MITRE ATT&CK
- T1557.002 - Man-in-the-Middle: HTTPS Interception
- T1190 - Exploit Public-Facing Application
- T1200 - Traffic Signaling
- T1556 - Modify Authentication Process
- T1021.001 - Remote Services: Remote Access Software (via MITM)

## Notes
Report demonstrates sophisticated understanding of multi-layered code flow (OpenSSL/GnuTLS -> Apple SecTrust -> legacy vs modern code paths). Bug is strictly logical (comparing wrong variable) rather than requiring runtime side effects. Reproducibility on modern hardware is limited due to __builtin_available runtime checks, but static analysis clearly demonstrates the defect. The vulnerability has low default exposure due to compile-time gating (USE_APPLE_SECTRUST off by default) but represents critical security bypass for affected configurations. Proper fix requires changing lines 270-271 to compare 'sec_result' instead of 'status'.

## Full report
<details><summary>Expand</summary>

## Summary:
When libcurl is built with USE_APPLE_SECTRUST and runs on Apple OS versions that lack SecTrustEvaluateWithError (macOS <10.14 / iOS <12), the legacy verification path miscompares OSStatus to SecTrustResultType and never checks the SecTrust result. This can cause untrusted certificates to be accepted.

[Statement clarifying if an AI was used to find the issue or generate the report]
This report was prepared with assistance from an AI code analysis tool; the core diagnosis and scope were validated by a combination of classical software, manual inspection of the code, and AI.

## Affected version
Reproduced on current master (as of 2025‑10‑07). Affects builds that enable `USE_APPLE_SECTRUST` and run on macOS <10.14 / iOS <12. The defect is in `lib/vtls/apple.c` and is independent of the TLS backend choice (it is reached via OpenSSL or GnuTLS when the native CA store is used).

## Steps To Reproduce:

### Code Verification (Any modern macOS):

1. Inspect the vulnerable code in `lib/vtls/apple.c` lines 263-275
2. Observe the type confusion: `status` (OSStatus) is compared to `kSecTrustResultType` enum values
3. Create test program demonstrating the logic bug (see verification artifacts)
4. Create untrusted certificate and verify system curl rejects it

### Runtime Exploitation (Requires macOS <10.14 or iOS <12):

**Note:** This requires an actual legacy system. Building with 
`-DCMAKE_OSX_DEPLOYMENT_TARGET=10.13` on modern macOS will NOT trigger 
the bug at runtime due to `__builtin_available` checks.

1. On a system running macOS 10.13.6 (High Sierra) or earlier, build curl:
   ```
   cmake -DUSE_APPLE_SECTRUST=ON -DCURL_USE_OPENSSL=ON \
         -DCMAKE_BUILD_TYPE=Release ..
   ```

2. Create untrusted certificates (as described)

3. Start test server: `openssl s_server -accept 8443 -www -key leaf.key -cert leaf.pem`

4. Test: `./src/curl -v https://localhost:8443/`
   - **Expected secure behavior:** Connection rejected
   - **Actual buggy behavior:** Connection succeeds

### Alternative Verification Without Legacy Hardware:

Since the bug is a clear logic error (comparing wrong variable), it can be 
confirmed through:
- Static code analysis (lines 270-271 compare `status` instead of `sec_result`)
- Logic demonstration (status=0 never equals kSecTrustResultUnspecified=4)
- The fact that `result` remains `CURLE_OK` when the conditions fail

## Supporting Material/References:

Problematic code (legacy fallback uses SecTrustEvaluate; compares `status` to SecTrustResultType instead of checking `sec_result`):

```263:275:lib/vtls/apple.c
#ifndef REQUIRES_SecTrustEvaluateWithError
SecTrustResultType sec_result;
status = SecTrustEvaluate(trust, &sec_result);

if(status != noErr) {
  failf(data, "Apple SecTrust verification failed: error %i", (int)status);
}
else if((status == kSecTrustResultUnspecified) ||
        (status == kSecTrustResultProceed)) {
  /* "unspecified" means system-trusted with no explicit user setting */
  result = CURLE_OK;
}
#endif /* REQUIRES_SecTrustEvaluateWithError */
```

Correct modern code path (only available on 10.14+/iOS 12+):
```238:240:lib/vtls/apple.c
result = SecTrustEvaluateWithError(trust, &error) ?
         CURLE_OK : CURLE_PEER_FAILED_VERIFICATION;
```

Behavioral gates where Apple SecTrust verification is invoked:
- OpenSSL:
```5165:5177:lib/vtls/openssl.c
if(!verified &&
   conn_config->verifypeer && ssl_config->native_ca_store &&
   (ossl_verify == X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY)) {
  result = ossl_apple_verify(..., &verified);
  ...
}
```
- GnuTLS:
```1666:1676:lib/vtls/gtls.c
if(!verified && ssl_config->native_ca_store &&
   (verify_status & GNUTLS_CERT_SIGNER_NOT_FOUND)) {
  result = glts_apple_verify(..., &verified);
  ...
}
```
```

## Impact

## Summary:
On affected configurations (USE_APPLE_SECTRUST builds running on pre‑10.14 Apple OS with native CA verification engaged), an attacker can bypass TLS certificate validation. This enables Man‑in‑the‑Middle interception, compromising confidentiality and integrity of HTTPS and other TLS‑protected transfers.

Scope caveats:
- Feature is compile‑time gated (`USE_APPLE_SECTRUST`) and off by default in CMake.
- Runtime reachability depends on backend conditions (OpenSSL “unable to get local issuer certificate” or GnuTLS “signer not found”).
- The bug only affects older Apple OS versions that lack `SecTrustEvaluateWithError`; modern Apple OS uses the correct code path.

</details>

---
*Analysed by Claude on 2026-05-24*
