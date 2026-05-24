# Denial of Service via Mutation Aliasing in GraphQL Account Recovery Phone Number Verification API

## Metadata
- **Source:** HackerOne
- **Report:** 3287208 | https://hackerone.com/reports/3287208
- **Submitted:** 2025-08-05
- **Reporter:** hellokbit
- **Program:** Unknown (HackerOne Report #3287208)
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Insufficient Rate Limiting, Lack of Query Complexity Analysis
- **CVEs:** None
- **Category:** web-api

## Summary
A GraphQL API endpoint for account recovery phone number verification lacks protection against mutation aliasing, allowing attackers to execute the same expensive mutation multiple times within a single request. Each aliased mutation adds approximately 8 seconds of processing time, enabling resource exhaustion and service degradation with minimal network traffic.

## Attack scenario
1. Attacker discovers the verifyAccountRecoveryPhoneNumber mutation endpoint and identifies it performs expensive backend operations (8 seconds per execution)
2. Attacker crafts a single GraphQL request containing 10-20 aliases of the same mutation with identical or dummy input parameters
3. Attacker sends the request to the GraphQL endpoint, triggering sequential execution of all aliased mutations on the server
4. Server processes each mutation independently, consuming CPU, memory, and backend resources for 80-160+ seconds total
5. Legitimate users attempting to access the service experience severe latency or connection timeouts
6. Attacker repeats requests from multiple sources to sustain DoS condition and further degrade availability

## Root cause
The GraphQL server implementation does not enforce limits on: (1) the number of aliases per mutation in a single request, (2) the total query complexity/cost before execution, or (3) the number of times expensive operations can be repeated. The server executes each alias sequentially without resource throttling or deduplication checks.

## Attacker mindset
An attacker recognizes that GraphQL's aliasing feature, designed for legitimate batch operations, can be abused to force repeated expensive computations. The attacker understands that a single request with multiple aliases bypasses traditional rate limiting (per-request counting) and can exhaust server resources more efficiently than traditional DoS attacks requiring high volume traffic.

## Defensive takeaways
- Implement query complexity analysis frameworks (e.g., GraphQL Shield, graphql-depth-limit) to calculate and enforce maximum query cost before execution
- Enforce strict limits on the number of aliases allowed per mutation in a single request (recommend max 2-3)
- Add rate limiting at the operation level, not just the request level, to track expensive mutation executions
- Implement caching and deduplication logic to detect and reject identical operations within a single request
- Set aggressive timeouts on individual mutation execution and request processing
- Monitor and alert on unexpectedly long request processing times or resource consumption patterns
- Validate that expensive mutations (those with long processing times) include additional rate limiting or CAPTCHA verification
- Implement mutation execution quotas per user/IP address over time windows

## Variant hunting
Identify other mutations or queries with expensive backend operations and test for aliasing abuse
Test nested mutations within mutations to see if they bypass alias counting logic
Attempt combinations of different mutations in a single request to exceed complexity limits
Test subscription endpoints for similar aliasing vulnerabilities
Check if variable reuse can be exploited to amplify complexity without increasing payload size
Investigate whether fragments can be used to hide aliasing from detection mechanisms
Test if query batching mechanisms bypass complexity analysis entirely

## MITRE ATT&CK
- T1499.4
- T1190

## Notes
This vulnerability demonstrates how GraphQL features designed for optimization (aliasing, batching) become attack vectors when not properly constrained. The 8-second operation time suggests expensive database queries, external API calls, or cryptographic operations. The simplicity of exploitation (single request, no authentication bypass required) combined with high impact makes this a critical severity issue. No bounty amount was disclosed in the provided content.

## Full report
<details><summary>Expand</summary>

**Summary:**
The GraphQL API’s `verifyAccountRecoveryPhoneNumber` mutation can be aliased multiple times in a single request, causing the server to process each mutation sequentially. Each additional alias adds approximately 8 seconds to the server’s response time, enabling (DoS) attack by exhausting server resources and increasing latency.

**Description:**
The `verifyAccountRecoveryPhoneNumber` mutation is designed to verify user phone numbers during account recovery phone change. However, the API does not limit the number of mutation aliases in a single GraphQL request. When the same mutation is repeated with different aliases, the server executes each one separately, performing expensive backend operations multiple times. This leads to a linear increase in response time based on the number of aliases included. The result is a resource exhaustion vulnerability that can degrade or deny service availability to legitimate users.

### Steps To Reproduce

1. Prepare a GraphQL mutation request with multiple aliases for `verifyAccountRecoveryPhoneNumber`, 
In this case, the response time will exceed 20 seconds because each alias (verify1, verify2, verify3) adds approximately 8 seconds of processing time.
```graphql
mutation VerifyAccountRecoveryPhoneNumberMutations($verification_code: String!, $otp_code: String) {
    verify1: verifyAccountRecoveryPhoneNumber(input: { verification_code: $verification_code, otp_code: $otp_code }) {
        __typename
        me {
            
        }
    }
    verify2: verifyAccountRecoveryPhoneNumber(input: { verification_code: $verification_code, otp_code: $otp_code }) {
        __typename
    }
    verify3: verifyAccountRecoveryPhoneNumber(input: { verification_code: $verification_code, otp_code: $otp_code }) {
        __typename
    }
}
}
```

2. Send the request to the GraphQL endpoint with valid or dummy `verification_code` and `otp_code` variables.

3. Observe the response time increases by 8 seconds for each additional mutation alias included.

## Impact

An attacker can exploit this vulnerability to cause a Denial of Service (DoS) by sending a single GraphQL request with multiple aliases of the expensive mutation. This forces the server to perform repeated, resource-intensive operations sequentially, significantly increasing response times and consuming server resources. As a result, legitimate users may experience severe delays or be completely unable to access the affected service, leading to degraded availability and potential service disruption. This  DoS attack can be triggered without high network traffic, making it easier to exploit stealthily.

</details>

---
*Analysed by Claude on 2026-05-24*
