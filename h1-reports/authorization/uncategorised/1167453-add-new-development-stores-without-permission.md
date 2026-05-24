# Unauthorized Development Store Creation via Insufficient Permission Validation

## Metadata
- **Source:** HackerOne
- **Report:** 1167453 | https://hackerone.com/reports/1167453
- **Submitted:** 2021-04-17
- **Reporter:** jmp_35p
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Authorization Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff member with permission to manage only managed stores could create and access development stores due to missing authorization checks on the /organizationID/stores/signup_object/dev_store endpoint. The endpoint returns a valid token for development store creation if the user has any store access, bypassing role-based access controls that should restrict this capability.

## Attack scenario
1. Organization owner grants staff member Doe permissions for both development and managed store creation
2. Doe initiates development store creation flow and obtains a valid signup token from /organizationID/stores/signup_object/dev_store
3. Owner revokes Doe's development store permission, leaving only managed store access
4. Doe continues with the stored token and completes development store creation via POST /services/signup/create
5. Doe automatically logs into the newly created development store, gaining unauthorized access
6. Alternative: Doe directly queries the endpoint after permission revocation to obtain a fresh token and proceeds with store creation

## Root cause
The /organizationID/stores/signup_object/dev_store endpoint performs insufficient authorization validation. It checks only that a user has 'store access' but fails to verify they specifically have 'development store creation' permission before issuing a signup token. The permission check likely occurs at the UI layer rather than enforcing authorization at the API level before token generation.

## Attacker mindset
A disgruntled or opportunistic staff member with partial access discovers that permission boundaries are enforced client-side rather than server-side. By obtaining a token before permissions are revoked, or by exploiting the weak API-level validation, they can exceed their assigned privileges to create development stores. This enables unauthorized resource creation and potential account takeover.

## Defensive takeaways
- Implement server-side authorization checks on all API endpoints, particularly those issuing tokens or creating resources
- Validate user permissions at the point of token issuance, not just at UI/request submission
- Enforce authorization checks before returning sensitive tokens that grant access to restricted operations
- Implement permission revocation that invalidates existing tokens or ongoing operations initiated under previous permission grants
- Use fine-grained role-based access control (RBAC) that explicitly restricts capability access (development store creation vs managed store management)
- Add audit logging for permission changes and resource creation attempts by staff members
- Consider time-bound tokens with short expiration for sensitive operations like store creation
- Perform authorization re-validation at the final resource creation step, not just at token request

## Variant hunting
Check other store-related endpoints (/organizationID/stores/signup_object/managed_store, etc.) for similar permission bypass
Test if other resource creation endpoints (apps, themes, channels) have the same vulnerability pattern
Examine if permission changes invalidate in-flight requests or only affect new requests
Investigate whether the vulnerability exists for other staff roles (developer, merchant, collaborator)
Test if the token can be reused multiple times or across different organization contexts
Check if similar authorization bypasses exist in partner API endpoints vs dashboard endpoints

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
This is a classic broken access control vulnerability where authorization is enforced at the wrong layer. The fact that the user could proceed with a token obtained before permission revocation suggests tokens lack proper expiration or permission binding. The report demonstrates both programmatic API exploitation and UI-based proof-of-concept, strengthening the report quality.

## Full report
<details><summary>Expand</summary>

Details
A staff member who only has permission to add and remove managed stores can also create development stores. It appears proper permission checks are not performed when /organizationID/stores/signup_object/dev_store endpoint is queried, as long as a staff member has store access, a token is returned. I decided to do this from the partner dashboard to proof that not only can development stores be created, they can also be logged into. Further information on setup and steps to reproduce are provided below.

Setup
Organization owner - Owner 
Staff member - Doe
1. Owner gives Doe both development store and managed store permission. See dev_store_B.png for details.
2. Doe logs in and visits https://partners.shopify.com/organizationID/stores/new and selects development store.
3. Owner edits Doe's permission so he can only add and remove managed stores. See dev_store.png for details.

Steps to reproduce
1. Doe proceeds to create the development store and gets logged in automatically. See dev_store_A.png, dev_store_C.png and dev_store_D.png for details.
2. Alternatively, send a GET request to /organizationID/stores/signup_object/dev_store to obtain the required token. See dev_store_G.png for details.
3. The token obtained above should be used in the following POST request.See dev_store_E.png and dev_store_F.png.

```
POST /services/signup/create HTTP/1.1
Host: app.shopify.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/86.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 1224
Origin: https://app.shopify.com
DNT: 1
Connection: close
Cookie: ...

_y=&ref=&ssid=&source=&source_url=&source_url_referer=&signup_code=&signup_source=development+shop&signup_source_details=test_app_or_theme&signup_page=&signup_page_referer=&signup_locale=&domain_to_connect=&signup%5Bshop_name%5D=newiez2&signup%5Bsubdomain%5D=&signup%5Bfirst_name%5D=&signup%5Blast_name%5D=&signup%5Bemail%5D=example%40gmail.com&signup%5Bpassword%5D=5syyyypT&signup%5Bconfirm_password%5D=5syyyypT&signup%5Baddress1%5D=Suite+10&signup%5Bcity%5D=London&signup%5Bprovince%5D=&signup%5Bzip%5D=Swe10928&signup%5Bcountry%5D=GB&signup%5Bphone%5D=&signup%5Bpos%5D=&signup%5Bextra%5D%5Baffiliate_shop%5D=eyJfcmFpbHMiOnsibWVzc2F&signup%5Bextra%5D%5Borganization_id%5D=1022333&signup%5Bextra%5D%5Bpartner_test_shop%5D=&signup%5Bsignup_types%5D%5B%5D=affiliate_shop&identity_account_experiment=

```

## Impact

Staff member can perform actions that require permission

</details>

---
*Analysed by Claude on 2026-05-24*
