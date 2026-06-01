# Schannel Custom-CA Path Skips Extended Key Usage (EKU) Enforcement

## Metadata
- **Source:** HackerOne
- **Report:** 3734992 | https://hackerone.com/reports/3734992
- **Submitted:** 2026-05-14
- **Reporter:** giant_anteater
- **Program:** curl
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Improper Certificate Validation, Missing EKU Constraint Enforcement, Man-in-the-Middle (MitM) Vulnerability
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Schannel certificate verification path in curl fails to enforce Extended Key Usage (EKU) constraints when using custom CA bundles (CURLOPT_CAINFO or CURLOPT_CAINFO_BLOB on Windows). A certificate chain containing only id-kp-clientAuth instead of id-kp-serverAuth may incorrectly pass peer verification. This creates a MitM vulnerability in private PKI environments where non-server certificates are issued from trusted CAs.

## Attack scenario
1. Attacker obtains a certificate for target hostname (e.g., server.example.com) from a CA present in victim's custom CA bundle
2. Attacker generates certificate with only clientAuth EKU constraint, not serverAuth
3. Victim uses curl with --cacert pointing to custom CA bundle containing attacker's CA
4. curl processes connection using Schannel custom-CA verification path instead of native Windows validation
5. CertGetCertificateChain is called without RequestedUsage parameter, skipping EKU enforcement
6. Windows does not set CERT_TRUST_IS_NOT_VALID_FOR_USAGE flag; certificate validation passes
7. Attacker intercepts TLS connection and presents invalid-EKU certificate that curl accepts

## Root cause
The Curl_verify_certificate() function in lib/vtls/schannel_verify.c initializes CERT_CHAIN_PARA with only cbSize set, leaving RequestedUsage member zeroed. This omission prevents Windows CertGetCertificateChain from evaluating server-auth EKU constraints. Additionally, no subsequent CertVerifyCertificateChainPolicy call with CERT_CHAIN_POLICY_SSL is made to enforce authorization usage. The native Schannel path correctly enforces EKU, but the custom-CA manual validation detour does not.

## Attacker mindset
Exploit misconfiguration in curl's custom CA verification to bypass EKU enforcement. Target private PKI environments (enterprise, IoT, embedded systems) where certificate issuance may be broader and a clientAuth-only certificate is achievable. Avoid self-signed certificates which remain unaffected. Perform MitM attack by intercepting traffic to services using curl with custom CA bundles on Windows.

## Defensive takeaways
- Populate CERT_CHAIN_PARA.RequestedUsage with server-auth EKU requirements before calling CertGetCertificateChain
- Call CertVerifyCertificateChainPolicy with CERT_CHAIN_POLICY_SSL policy to enforce server-authorization constraints
- Do not leave CERT_CHAIN_PARA zero-initialized; explicitly configure all required validation parameters
- Test custom-CA validation paths alongside default system validation paths to ensure feature parity
- Add integration tests for non-standard EKU combinations to catch validation bypasses
- Review Windows API documentation for proper certificate chain validation patterns
- Consider using CERT_TRUST_IS_NOT_VALID_FOR_USAGE in rejection logic when applicable

## Variant hunting
Check OpenSSL/GnuTLS custom-CA paths for similar EKU enforcement gaps
Audit other curl TLS backends (Secure Transport on macOS, etc.) for EKU validation completeness
Search for other CERT_CHAIN_PARA initializations in curl codebase; verify all set RequestedUsage appropriately
Test with certificates containing only id-kp-clientAuth, id-kp-OCSPSigning, or other non-serverAuth EKUs
Review enterprise PKI environments for over-issuance of multi-purpose or clientAuth-only certificates
Test curl with revocation checking disabled to isolate EKU validation from revocation logic

## MITRE ATT&CK
- T1190
- T1556
- T1557.001
- T1021.001

## Notes
Reporter notes lack of Windows testing due to environment limitations; vulnerability is based on source code review and Win32 API documentation analysis. The bug is specific to Windows 7+ when CURLOPT_CAINFO or CURLOPT_CAINFO_BLOB is supplied. Impact is limited to private PKI scenarios; public certificate authorities rarely issue non-serverAuth certificates for server hostnames. The existing trust-mask logic cannot detect this issue because Windows never sets CERT_TRUST_IS_NOT_VALID_FOR_USAGE when EKU validation is not requested. Reproducer provided includes certificate generation steps and predicted unpatched behavior.

## Full report
<details><summary>Expand</summary>

Hi all,

We believe the Schannel custom-CA verification path in `lib/vtls/schannel_verify.c` may skip Extended Key Usage enforcement. In particular, a certificate that chains to the trusted custom CA but contains only `id-kp-clientAuth`, rather than `id-kp-serverAuth`, may pass peer verification on Windows when curl is used with `CURLOPT_CAINFO` or `CURLOPT_CAINFO_BLOB` set.

Note: We have not actually tested this on a Windows machine (due to lack of ability), so this report is currently based on source review and Win32 API documentation.

The relevant code is in `Curl_verify_certificate()`. It allocates a `CERT_CHAIN_PARA`, zeroes it, sets only `cbSize`, and passes it to `CertGetCertificateChain`:

```c
CERT_CHAIN_PARA ChainPara;

memset(&ChainPara, 0, sizeof(ChainPara));
ChainPara.cbSize = sizeof(ChainPara);

if(!CertGetCertificateChain(cert_chain_engine,
                            pCertContextServer,
                            NULL,
                            pCertContextServer->hCertStore,
                            &ChainPara,
                            (ssl_config->no_revoke ? 0 :
                             CERT_CHAIN_REVOCATION_CHECK_CHAIN),
                            NULL,
                            &pChainContext)) {
```

Because `RequestedUsage` is left unset, chain building appears to run without an EKU constraint. Microsoft documents that server/client authorization distinctions should be expressed through the `RequestedUsage` member passed to `CertGetCertificateChain`, and then enforced with `CertVerifyCertificateChainPolicy` as appropriate. In the current Schannel verification path, we do not see either `RequestedUsage` populated for `serverAuth` or a subsequent `CertVerifyCertificateChainPolicy(CERT_CHAIN_POLICY_SSL, ...)` call. As a result, Windows may have no reason to set `CERT_TRUST_IS_NOT_VALID_FOR_USAGE` for a leaf that lacks `id-kp-serverAuth`.

This also explains why the existing trust-mask logic does not help. The mask does not suppress `CERT_TRUST_IS_NOT_VALID_FOR_USAGE` (`0x10`), so if Windows set that bit, curl would already fail correctly. The issue seems to be that this path never asks Windows to evaluate server-auth EKU in the first place.

The affected path is entered when `CURLOPT_CAINFO` or `CURLOPT_CAINFO_BLOB` is supplied on Windows 7 or later, which sets `backend->use_manual_cred_validation = TRUE` in `schannel.c`. If `CURLOPT_SSL_VERIFYPEER` is enabled, curl then dispatches to `Curl_verify_certificate()`. When no custom CA is provided, curl stays on Schannel's native validation path instead. That distinction matters because the issue appears specific to the manual custom-CA detour.

The practical consequence is a possible MitM in environments where an attacker can obtain a certificate for the target hostname from a CA that is present in the victim's custom CA bundle, but where that certificate is not valid for server authentication. This does not appear to be exploitable with a self-signed certificate. The main risk seems to be private PKI environments, such as enterprise, IoT, or embedded deployments, where non-server certificates may be issued more broadly.

Below is a reproducer. The certificate-generation steps are cross-platform with OpenSSL. The curl step is Windows-only, and the expected result is still a prediction based on source analysis and Microsoft API behavior.

Step 1: generate a CA and issue a certificate for `server.example.com` with only `id-kp-clientAuth` and no `id-kp-serverAuth`:

```sh
# CA key and self-signed certificate
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 3650 -key ca.key -out ca.pem \
    -subj "/CN=Test CA"

# Server key and CSR
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr \
    -subj "/CN=server.example.com"

# Extension file: SAN + clientAuth EKU only
cat > server_exts.cnf << 'EOF'
subjectAltName   = DNS:server.example.com
extendedKeyUsage = clientAuth
EOF

# Sign the server cert with the CA
openssl x509 -req -days 365 -in server.csr \
    -CA ca.pem -CAkey ca.key -CAcreateserial \
    -extfile server_exts.cnf \
    -out server.pem

# Confirm: should show clientAuth and not serverAuth
openssl x509 -in server.pem -noout -text | grep -A3 "Extended Key"
```

Step 2: on Windows, serve `server.pem` and `server.key` from any TLS server, add a hosts-file entry for `server.example.com`, then run:

```bat
curl --cacert ca.pem https://server.example.com/
```

Expected behavior: curl should reject the connection with an error such as `(60) SSL certificate problem: certificate is not valid for the requested usage`.

Predicted actual behavior on the unpatched Schannel `--cacert` path: the connection succeeds, because `CertGetCertificateChain` is called with no requested EKU and therefore may not set `CERT_TRUST_IS_NOT_VALID_FOR_USAGE`, allowing the existing trust-mask check to pass.

As a control, importing `ca.pem` into the Windows root store and running without `--cacert` should exercise Schannel's native path instead. If that path rejects the certificate, it would further indicate that the EKU gap is specific to the manual custom-CA path.

Two possible fixes stand out.

Option A, minimal: populate `RequestedUsage` before calling `CertGetCertificateChain`:

```diff
-  CERT_CHAIN_PARA ChainPara;
-
-  memset(&ChainPara, 0, sizeof(ChainPara));
-  ChainPara.cbSize = sizeof(ChainPara);
+  CERT_CHAIN_PARA ChainPara;
+  LPSTR serverAuthOID = (LPSTR)szOID_PKIX_KP_SERVER_AUTH;
+
+  memset(&ChainPara, 0, sizeof(ChainPara));
+  ChainPara.cbSize = sizeof(ChainPara);
+  ChainPara.RequestedUsage.dwType = USAGE_MATCH_TYPE_AND;
+  ChainPara.RequestedUsage.Usage.cUsageIdentifier = 1;
+  ChainPara.RequestedUsage.Usage.rgpszUsageIdentifier = &serverAuthOID;
```

Option B, more complete: call `CertVerifyCertificateChainPolicy(CERT_CHAIN_POLICY_SSL, ...)` after chain building. That would align this path more closely with normal Schannel TLS policy evaluation and should cover EKU and related SSL policy checks in a more standard way.

Either approach may be sufficient. Option B seems more robust, while Option A is the smallest targeted change.

Thank you,
AISLE Research Team

## Impact

An attacker who can obtain a hostname-valid certificate from a CA in the victim's custom CURLOPT_CAINFO or CURLOPT_CAINFO_BLOB bundle may be able to bypass server-auth EKU checks on Windows and intercept libcurl connections on the Schannel manual-validation path. This appears limited to custom-CA configurations and is most relevant in private PKI environments where non-server certificates may be issued more broadly; it does not appear to be exploitable with a self-signed certificate.

</details>

---
*Analysed by Claude on 2026-05-31*
