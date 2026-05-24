# DOM XSS on http://talks.lystit.com

## Metadata
- **Source:** HackerOne
- **Report:** 1031644 | https://hackerone.com/reports/1031644
- **Submitted:** 2020-11-11
- **Reporter:** gamer7112
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - DOM
- **CVEs:** None
- **Category:** web-api

## Summary
#Description
DOM XSS can be achieved via a postMessage due to an insecure postMessage handler being registered.

#POC
1. Visit https://gamer7112.com/lyst_1.html
2. Click the link
3. View alert

#Vulnerable Code
Located at http://talks.lystit.com/data-saloon-presentation/plugin/notes/notes.html
```javascript
window.addEventListener('message', function(event) {
    var data = JSON.parse(event.data);

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

#Description
DOM XSS can be achieved via a postMessage due to an insecure postMessage handler being registered.

#POC
1. Visit https://gamer7112.com/lyst_1.html
2. Click the link
3. View alert

#Vulnerable Code
Located at http://talks.lystit.com/data-saloon-presentation/plugin/notes/notes.html
```javascript
window.addEventListener('message', function(event) {
    var data = JSON.parse(event.data);

    // No need for updating the notes in case of fragment changes
    if (data.notes !== undefined) {
        if (data.markdown) {
            notes.innerHTML = marked(data.notes);
        } else {
            notes.innerHTML = data.notes;
        }
    }

    silenced = true;

    // Update the note slides
    currentSlide.contentWindow.Reveal.slide(data.indexh, data.indexv, data.indexf);
    nextSlide.contentWindow.Reveal.slide(data.nextindexh, data.nextindexv);

    silenced = false;

}, false);
```

## Impact

XSS allows for an attacker to execute arbitrary javascript on another user.

</details>

---
*Analysed by Claude on 2026-05-24*
