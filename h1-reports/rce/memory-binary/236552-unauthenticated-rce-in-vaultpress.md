# Unauthenticated Remote Code Execution in Vaultpress via Unsafe openssl_verify Usage

## Metadata
- **Source:** HackerOne
- **Report:** 236552 | https://hackerone.com/reports/236552
- **Submitted:** 2017-06-05
- **Reporter:** b258ea62bf297b02afa9854
- **Program:** Automattic/Vaultpress
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Improper Input Validation, Type Juggling, Authentication Bypass, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
Vaultpress fails to properly validate API signatures due to unsafe usage of PHP's openssl_verify() function, which returns -1 on error instead of 0 on failure. An attacker can bypass signature validation by providing a valid signature from a different key type, causing openssl_verify to return -1, which evaluates to true in PHP's loose comparison, leading to unauthenticated RCE.

## Attack scenario
1. Attacker crafts a malicious request to the Vaultpress endpoint with vaultpress=true parameter
2. Attacker generates a signature using a different key type than expected (e.g., different algorithm or key format)
3. This causes openssl_verify() to return -1 (error condition) instead of 0 (verification failure)
4. The code uses loose comparison (if statement) treating -1 as truthy, bypassing signature validation
5. Attacker's malicious post data passes validation despite invalid signature
6. Attacker achieves unauthenticated RCE by executing arbitrary code through Vaultpress API

## Root cause
The validate_api_signature() method uses PHP's loose comparison (if condition) on openssl_verify() return value without explicitly checking for the success value of 1. The function returns three distinct values (1=success, 0=failure, -1=error), but -1 is truthy in PHP, allowing error conditions to bypass signature validation.

## Attacker mindset
The attacker recognized that common security functions often have multiple return states that developers mishandle. By understanding openssl_verify's three-state return value and PHP's type juggling rules, they identified that triggering an error condition (return -1) bypasses the authentication check entirely, turning a validation feature into a vulnerability.

## Defensive takeaways
- Always use strict comparison (===) when checking return values from security functions
- Document and handle all possible return states of cryptographic functions explicitly
- Return values from validation functions should be boolean only, not multi-state integers
- Implement defense-in-depth with firewall rules as primary control, not fallback
- Test error conditions and edge cases in signature validation code paths
- Use static analysis tools to detect loose comparison usage with security-critical functions
- Validate key type compatibility before performing cryptographic operations

## Variant hunting
Search for other instances of openssl_verify, hash_hmac_algos, or similar cryptographic validation functions using loose comparison (if, ||, &&) instead of strict comparison (===, !==). Check for other API signature validation mechanisms that may have similar type-juggling vulnerabilities. Look for patterns where return values are used in boolean contexts without explicit type checking.

## MITRE ATT&CK
- T1190
- T1589
- T1592
- T1566

## Notes
This vulnerability chain required two conditions: (1) firewall bypass or disabled firewall, and (2) openssl being used for verification. The PoC demonstrates generating incompatible key types to force openssl_verify to return -1. The fix is minimal but critical - changing loose to strict comparison prevents the type juggling attack. This highlights how security-critical PHP code must be written defensively given the language's permissive type system.

## Full report
<details><summary>Expand</summary>

Hitting wordpress instalattion with vaultpress on it with get parameter vaultpress=true attacker is one method away from RCE and that method is **validate_api_signature**.

In this method we have the following constraints:
1. Firewall
2. Usage (recomended) of openssl to validate API call

In case of disabled firewall or its bypass ( easy on many configurations, specially the ones behind proxy/balancer servers ) then in case of usage of openssl to verify the signature we have easy bypass because unsafe usage of **openssl_verify** PHP function.

```
if ( $this->can_use_openssl() ) {
			
			$sslsig = '';
			if ( isset( $post['sslsig'] ) ) {
				$sslsig = $post['sslsig'];
				unset( $post['sslsig'] );
			}
			if ( openssl_verify( serialize( array( 'uri' => $uri, 'post' => $post ) ), base64_decode( $sslsig ), $this->get_option( 'public_key' ) ) ) {
				return true;
			} else {
				$__vp_validate_error = array( 'error' => 'invalid_signed_data' );
				return false;
			}
		}
```
This function **openssl_verify** have 3 possible values as result value: 
- int(1) success 
- int(0) failure to verify
- int(-1) error 

but we all know that 
```
if (-1) {echo "Hi RCE";}
```
will print **Hi RCE**

Proposed fix:
```
if ( openssl_verify( serialize( array( 'uri' => $uri, 'post' => $post ) ), base64_decode( $sslsig ), $this->get_option( 'public_key' ) ) ===1 ) {
				return true;
			} else {
				$__vp_validate_error = array( 'error' => 'invalid_signed_data' );
				return false;
			}
```
In order to get the idea how to cause **openssl_verify** to return -1all you need is to provide valid signature towards public key from different type. Check the uploaded files and execute them in the CMD in the following order:
```
php genkey1.php
php genkey2.php
php PoC.php
```


</details>

---
*Analysed by Claude on 2026-05-12*
