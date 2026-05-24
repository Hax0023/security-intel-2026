# Exposed Spring Boot Actuator APIs Leaking Sensitive Data Including Credentials, JWT Secrets, and Customer Information

## Metadata
- **Source:** HackerOne
- **Report:** 783360 | https://hackerone.com/reports/783360
- **Submitted:** 2020-01-25
- **Reporter:** secyour-org
- **Program:** Stripo
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Insecure Direct Object References, Information Disclosure, Misconfiguration, Insufficient Access Control, Credential Exposure
- **CVEs:** None
- **Category:** memory-binary

## Summary
Stripo misconfigured its Spring Boot actuator endpoints to be publicly accessible without authentication, exposing a heap dump download feature that reveals sensitive data including database credentials, JWT secret keys, admin accounts, customer PII, and source code. An unauthenticated attacker can download and analyze memory dumps to extract secrets used for account takeover, payment fraud, and system compromise.

## Attack scenario
1. Attacker discovers the public actuator endpoint by scanning common Spring Boot paths on Stripo domains
2. Attacker accesses the heapdump endpoint (https://my.stripo.email/cabinet/stripeapi/actuator/heapdump) without authentication
3. Attacker downloads the server memory dump file containing all in-memory secrets and credentials
4. Attacker uses memory analysis tools (Eclipse MAT, VisualVM) to parse and search the heap dump for sensitive strings
5. Attacker extracts JWT secret keys, admin credentials, database passwords, and API tokens from the memory dump
6. Attacker leverages extracted secrets to forge JWT tokens, impersonate admins, access databases, or manipulate payments

## Root cause
Spring Boot actuator endpoints were not properly secured with authentication or disabled in production. The application exposed sensitive management endpoints including heapdump functionality to the public internet without access controls, allowing unauthenticated information disclosure.

## Attacker mindset
An attacker would recognize this as a quick win to obtain maximum leverage - a single unauthenticated request exposes all critical secrets needed for complete system compromise. The attacker would prioritize extracting JWT secrets for account takeover and admin credentials for privilege escalation.

## Defensive takeaways
- Disable all non-essential Spring Boot actuator endpoints in production or restrict to localhost only
- Require strong authentication and authorization for all actuator endpoints that must remain enabled
- Implement network-level access controls to restrict actuator endpoints to internal networks only
- Regularly audit Spring Boot configuration to ensure management endpoints are properly secured
- Implement secrets management solutions to avoid storing sensitive data in application properties or environment variables
- Enable application monitoring to detect unauthorized actuator access attempts
- Conduct memory analysis testing to identify what sensitive data is retained in heap dumps
- Use Spring Security to explicitly configure actuator security requirements

## Variant hunting
Search for other publicly exposed actuator endpoints across different microservices and domains; test for accessible endpoints like /actuator/configprops, /actuator/env, /actuator/threaddump, /actuator/metrics, and /actuator/loggers which may leak additional configuration and environment details; check for similar misconfigurations in other services using Spring Boot or comparable frameworks with management APIs

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1083
- T1087
- T1110
- T1078
- T1555

## Notes
The vulnerability affected multiple domains simultaneously (my.stripo.email, plugins.stripo.email, plugin.stripo.email), suggesting systemic misconfiguration across the infrastructure. The researcher noted uncertainty about reporting scope but correctly identified this as a single root cause affecting multiple instances. The exposed heapdump is particularly dangerous as it captures runtime memory including cryptographic keys needed for JWT forgery. The severity is amplified by the ability to access billing and payment systems through leaked credentials.

## Full report
<details><summary>Expand</summary>

## Summary:
Stripo uses Spring boot for the backend API development , and misconfigured the application to open actuator APIs to the public.

This issue is found in 3 domains , don't know if I need to publish 3 reports for that, or just one report , but the domains are :
https://my.stripo.email/cabinet/stripeapi/actuator
https://plugins.stripo.email/actuator
https://plugin.stripo.email/actuator

it might be available in other micro services as well



## Steps To Reproduce:

  1. Go to the following URL : https://my.stripo.email/cabinet/stripeapi/actuator/heapdump
  1. This url will download the heap dump of the server 
  1. using a memory analyzer such as Eclipse memory analyzer or VisualVM open the downloaded file
  1. By searching inside the file you can find all the secrets , credentials , urls , JWT tokens & JWT secret keys, which can be used and generate any JWT token and takeover any account on the system.
  1. Attached some examples of what can be found and used by this vulnerability, and you can imagine any bad scenario, and this issue can be used to take over/down Stripo

## Supporting Material/References:
Please find more information about actuator on the following URL:
https://docs.spring.io/spring-boot/docs/current-SNAPSHOT/actuator-api/html/#heapdump


Example of open functionalities:
████

Admin Credentials:
███

Other User's information:
█████████

Billing Service Credentials:
████

Config Server Credentials:
███████

## Impact

This vulnerability allows any attacker to perform many severe attacks such as :

- Upgrade accounts without payments.
- Get logged in customer information and get access to the session & JWT tokes to take over accounts
- PII Data leaking 
- Accessing all credentials from the application properties such as , admin credentials, swagger credentials , billing credentials .
- Get database credentials
- Server Environment variable
- Server config Properties.
- Payments manipulations and money stealing
- and more

</details>

---
*Analysed by Claude on 2026-05-24*
