# Android App Bypasses File Download Restrictions

## Metadata
- **Source:** HackerOne
- **Report:** 2380133 | https://hackerone.com/reports/2380133
- **Submitted:** 2024-02-19
- **Reporter:** hakuna
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Authorization Bypass, Access Control Weakness, Client-Side Security Enforcement
- **CVEs:** None
- **Category:** uncategorised

## Summary
An Android app fails to enforce server-side download restrictions set by file owners. Users can download PDFs, documents, images, and presentations despite the owner disabling download permissions. This allows unauthorized access to sensitive documents that were intentionally restricted.

## Attack scenario
1. Owner shares a folder containing sensitive files (PDFs, documents, images) with a user
2. Owner explicitly disables 'Allow download' permission for the shared folder
3. Recipient opens the shared files using the Android mobile app
4. Recipient accesses the file viewer and taps the menu to reveal export/save options
5. Recipient selects 'Download as' (for documents) or 'Use as' (for images) to save the file locally
6. File is successfully downloaded and saved to device storage, bypassing the access control

## Root cause
The Android app implements download restrictions at the UI level only, without validating permissions against the server before allowing downloads. The app trusts the file viewer and export functionality without checking the 'Allow download' permission flag from the server.

## Attacker mindset
A malicious user granted read-only access to sensitive files can exploit the mobile app's weaker permission enforcement to exfiltrate documents that were explicitly restricted from download by the owner.

## Defensive takeaways
- Always enforce access control on the server-side, never rely on client-side validation
- Validate user permissions before serving file content or download streams
- Implement consistent permission checks across all client platforms (web, mobile, desktop)
- Block export/save functionality at the viewer level if download permissions are denied
- Log and audit file access attempts, especially when restrictions are involved
- Ensure mobile app permission checks match server-side authorization logic
- Return HTTP 403 Forbidden when users without download permission request files

## Variant hunting
Check if 'Allow upload' restrictions can be bypassed in the Android app
Test whether other file types (.docx, .xlsx, .pptx) bypass restrictions
Verify if share link recipients face the same bypass when accessing shared files
Check if preview-only permissions can be bypassed via screenshot or caching
Test if iOS app has similar authorization bypass vulnerabilities
Examine whether 'view only' mode can be circumvented through app features
Check if cached files can be accessed after permissions are revoked

## MITRE ATT&CK
- T1190
- T1566
- T1530

## Notes
The bug report notes that some file types (.mp3, .mp4, .txt) cannot be opened, suggesting selective implementation of viewer functionality. The fact that 'unchecking doesn't apply the first time' indicates potential UI/sync issues that may compound the security problem. The infinite loading on 'Save as' function suggests incomplete feature implementation that could mask other vulnerabilities.

## Full report
<details><summary>Expand</summary>

## Summary:
If the owner of a file - of type PDF, document, image or presentation - shares it with a user and disable download, the user can still download it using the Android app.

## Steps To Reproduce:
 
  1. As user1, in the "Files" app, create a folder containing files of different formats (PDF, .odt, .png, .odp...)
  2. Share the folder to user2 and uncheck "Allow download" (repeat this step twice as unchecking the box doesn't apply the first time)
  3. As user2, in the Android app, open:
           - a PDF: in the viewer click the top right menu, choose "Download as" and select "PDF document" or "PDF document as...". You receive a "Download completed" notification and can open and save the file on your phone.
           - a .odp:  same as above
           - a .odt:  same as above and you can also choose ".epub"
           - an image (.png, .jpg): choose "Use the image as" and "Wallpaper". The file will be saved in internal memory - not easily accessible but still. You can also choose the image as Whatsapp profile picture or contact photo

**Screenshots: **
{F3060341}

**Additional notes on the tests: **
- What I could open but couldn't download: .mp3, .mp4, .txt
- What I couldn't open because it won't load (there's an infinite loader and a "Loading takes longer than expected" error ): .md, .csv
- Trying to export the document by clicking "File">"Save as"  from the viewer (pdf /odt) will open a pop up to choose a filename, and after clicking "Save" there's an infinite loading icon which is blocking the UI.

## Impact

Sensitive documents leak.

</details>

---
*Analysed by Claude on 2026-05-24*
