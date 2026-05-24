# IDOR on ██████ via direct photo URL leads to unauthorized access to deleted and other users' photos

## Metadata
- **Source:** HackerOne
- **Report:** 3518758 | https://hackerone.com/reports/3518758
- **Submitted:** 2026-01-21
- **Reporter:** shiva2550
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
An Insecure Direct Object Reference (IDOR) vulnerability exists in the application that allows unauthorized access to photos belonging to other users. The application does not properly validate whether the logged-in user is authorized to access a photo when accessing it via direct URL. This allows any authenticated user to view photos from other users' albums, including photos that hav

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

## Summary:
An Insecure Direct Object Reference (IDOR) vulnerability exists in the application that allows unauthorized access to photos belonging to other users. The application does not properly validate whether the logged-in user is authorized to access a photo when accessing it via direct URL. This allows any authenticated user to view photos from other users' albums, including photos that have been deleted.

## Steps To Reproduce:

**Account A:**

1. Create an album
2. Upload a photo
3. Note the direct image URL: `https://████████/remote.php/dav/photos/███████/albums/srk./10700342-1.jpeg`
4. Delete that photo
5. Save the URL for future reference

**Account B:**

1. Copy the old image URL from Account A: `https://████/remote.php/dav/photos/████████/albums/srk./10700342-1.jpeg`
2. Paste it in the browser
3. The image loads successfully, even though Account B is a different user and the photo was deleted

## Supporting Material/References:

* Vulnerable URL pattern: `https://████████/remote.php/dav/photos/[user_email]/albums/[album_name]/[photo_id]`
* The photo was accessible despite being deleted and belonging to another account

</details>

---
*Analysed by Claude on 2026-05-24*
