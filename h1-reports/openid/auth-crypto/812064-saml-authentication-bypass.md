# SAML Authentication Bypass via Unsigned Response Element Injection

## Metadata
- **Source:** HackerOne
- **Report:** 812064 | https://hackerone.com/reports/812064
- **Submitted:** 2020-03-06
- **Reporter:** tomp1
- **Program:** Meteor
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** XML Signature Wrapping, Authentication Bypass, XML External Entity (XXE) variant, Signature Validation Logic Error
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The SAML authentication implementation in meteor-accounts-saml fails to verify that the validated signature corresponds to the Response element being processed. An attacker can prepend an unsigned malicious Response element to a valid SAML response, causing the code to validate the original signature but process the attacker-controlled Response element instead, enabling complete authentication bypass.

## Attack scenario
1. Attacker intercepts a legitimate SAML login flow and captures a valid SAML response containing a proper signature
2. Attacker crafts a malicious SAML response with forged assertions (e.g., NameID=admin, elevated privileges)
3. Attacker inserts the malicious Response element at the beginning of the XML document, placing the valid signature later
4. Attacker sends the modified SAMLResponse parameter in the POST request to the login endpoint
5. The vulnerable code validates the first discovered Signature element (the original valid one)
6. The vulnerable code then processes the first Response element (the malicious one), bypassing authentication checks and logging in as the impersonated user

## Root cause
The signature validation and response processing use independent element selection mechanisms without cross-referencing. The code selects the first Signature element globally via XPath, then independently selects the first Response element via getElementsByTagNameNS. No verification ensures these elements are related or that the selected Response was actually signed. Additionally, status validation occurs before signature validation, further weakening the security posture.

## Attacker mindset
An attacker with network visibility (MITM, proxy access, or captured SAML responses) can repurpose legitimate signatures from valid SAML exchanges to validate forged authentication claims. By exploiting XML's hierarchical structure and the code's loose element selection logic, the attacker achieves privilege escalation and complete account compromise with minimal cryptographic breaking required.

## Defensive takeaways
- Always use cryptographic reference URIs (#id) or explicit parent-child relationships to verify signatures apply to the exact element being processed
- Validate signatures before parsing and trusting any element data from the response
- Implement explicit binding between the signature and the signed element; reject responses where this relationship is ambiguous
- Use established SAML libraries with proper signature wrapping attack defenses rather than custom parsing
- Avoid relying on element ordering or index-based selection; use explicit references and IDs
- Perform comprehensive XML schema validation before cryptographic operations
- Consider using XML canonicalization to prevent structural manipulation attacks
- Implement defense-in-depth with additional claim validation (e.g., issuer verification, assertion time validation)

## Variant hunting
Check for similar XPath-based signature selection patterns in other SAML/XML processing code
Search for cases where signature validation and data extraction are separated without explicit binding
Look for applications using xml-crypto or similar libraries with custom wrapper code
Investigate SAML implementations using getElementsByTagName instead of properly-scoped reference URIs
Test other XML-based authentication protocols (WS-Security, XACML) for similar wrapping vulnerabilities
Examine order-dependent parsing logic in other XML security libraries

## MITRE ATT&CK
- T1190
- T1528
- T1556
- T1110
- T1187

## Notes
This is a classic XML Signature Wrapping (XSW) attack. The vulnerability demonstrates why OWASP recommends using well-tested SAML libraries (like OneLogin, python3-saml) rather than custom implementations. The fact that status validation precedes signature validation is an additional red flag. The POC script requirement indicates successful exploitation was demonstrated. This affects all versions of the library based on code history analysis.

## Full report
<details><summary>Expand</summary>

## Summary

When using SAML authentication, responses are not checked properly. This allows attacker to inject/modify any assertions in the SAML response and thus, for example, authenticate as administrator.

## Description

Following code snippets are from *app/meteor-accounts-saml/server/saml_utils.js*
When checking the signature, the first Signature element which is found in the whole response XML is used:

`316 const signature = xmlCrypto.xpath(doc, '//*[local-name(.)=\'Signature\' and namespace-uri(.)=\'http://www.w3.org/2000/09/xmldsig#\']')[0];`

 After the XML signature has been verified, the code proceeds to use the first Response element found in the whole XML to get assertions and attributes. 

`516 const response = doc.getElementsByTagNameNS('urn:oasis:names:tc:SAML:2.0:protocol', 'Response')[0];`

**However there is no check that the signature that was checked relates to the response element that is being used.** Thus attacker can take a valid SAML response, with some valid signature, and add Response element, that has no signatures, in the beginning of the XML. The code finds the original signature and validates that, but proceeds to use the malicious Response element, which is found first in the document.

Also the validating the status from the response happens before signature validation

`501 const statusValidateObj = self.validateStatus(doc);`

## Releases Affected:

Tested on 3.0.3 but appears to affect all versions based on the history of saml_utils.js file.

## Steps To Reproduce (from initial installation to vulnerability):

  1. Configure the application to use SAML authentication
  1. When logging in, intercept the POST request with a proxy tool
  1. Use the attached `samlbypasspoc.py` file to create a new value for the parameter `SAMLResponse`. Run the script in python3 with the URL encoded SAMLResponse as argument.
  1. Replace the parameter value with the one given by the POC script and forward the request

This requires altering the POC to suite the configuration. Beginning from the line 25, you can alter the response elements as needed to desired values. 

In the sample POC file, attributes `OrganizationName` and `Email` and the element `NameID` are changed. In the setup I tested this resulted in login as a newly created admin.

## Supporting Material/References:

  * samlbypasspoc.py

## Suggested mitigation

  * Refactor the code so that the same elements (references) are used when checking the signature and when reading the attributes
  * Do not use hard coded indexes when selecting the elements

## Impact

SAML authentication can be bypassed and attacker can log in as any user (e.g. admin user)

</details>

---
*Analysed by Claude on 2026-05-24*
