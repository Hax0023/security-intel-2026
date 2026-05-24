# XSS by MathML at Active Storage

## Metadata
- **Source:** HackerOne
- **Report:** 429873 | https://hackerone.com/reports/429873
- **Submitted:** 2018-10-28
- **Reporter:** ooooooo_q
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** CVE-2018-16477
- **Category:** web-api

## Summary
In Active Storage, formats treated as binary have been confirmed, It does not contain `application/mathml+xml`.

https://github.com/rails/rails/commit/d40284b1a44773b03d78ca67a888b94fd330d1b1


In `Marcel::MimeType.for`, if content-type can not be determined with magic byte, since it is determined using the extension, uploading the file with `.mml` will be judged as `application/mathml+xml`.

```r

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

In Active Storage, formats treated as binary have been confirmed, It does not contain `application/mathml+xml`.

https://github.com/rails/rails/commit/d40284b1a44773b03d78ca67a888b94fd330d1b1


In `Marcel::MimeType.for`, if content-type can not be determined with magic byte, since it is determined using the extension, uploading the file with `.mml` will be judged as `application/mathml+xml`.

```ruby
#https://github.com/minad/mimemagic/blob/master/lib/mimemagic/tables.rb#L387
    'mml' => 'application/mathml+xml',
```

I confirmed that MathML XSS is executable in Mac Firefox 63. (https://html5sec.org/#130)


```xml
<math xmlns="http://www.w3.org/1998/Math/MathML" href="javascript:alert(location)">click page
</math>
```

Upload the above contents as `math.mml`, open the URL directly in Firefox and click in the screen to open an alert.

## Impact

It will allow attacks against Firefox users.

</details>

---
*Analysed by Claude on 2026-05-24*
