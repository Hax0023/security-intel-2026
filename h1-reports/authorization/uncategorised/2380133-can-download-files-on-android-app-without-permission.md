# Unauthorized File Download on Android App Despite Permission Restrictions

## Metadata
- **Source:** HackerOne
- **Report:** 2380133 | https://hackerone.com/reports/2380133
- **Submitted:** 2024-02-19
- **Reporter:** hakuna
- **Program:** Unknown (File Sharing/Collaboration App)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Authorization Bypass, Improper Permission Enforcement
- **CVEs:** None
- **Category:** uncategorised

## Summary
An Android app fails to enforce download restrictions set by file owners, allowing users with view-only access to download shared files (PDFs, documents, images, presentations) through alternative export/save mechanisms. This directly contradicts the owner's explicit permission settings and enables unauthorized access to sensitive documents.

## Attack scenario
1. User1 (file owner) creates files in various formats (PDF, ODT, PNG, ODP) and shares them with User2
2. User1 explicitly disables the 'Allow download' permission for User2 to prevent file extraction
3. User2 opens a restricted file on the Android app using the built-in viewer
4. User2 accesses the top-right menu and selects 'Download as' or 'Use the image as' options
5. User2 successfully downloads or exports the file to local device storage despite restrictions
6. User2 gains persistent offline access to sensitive documents they were only supposed to view

## Root cause
The Android app implements download restrictions only at the network/API level but fails to enforce the same restrictions on client-side export, save-as, and image utility functions. The viewer components bypass permission checks when exporting content to alternate formats or local storage destinations.

## Attacker mindset
A malicious insider or disgruntled colleague with view-only access seeks to exfiltrate confidential documents that have been explicitly restricted from download. The attacker recognizes that the app's UI provides alternative export pathways (save-as, use-as-wallpaper) that are not guarded by the same permission logic.

## Defensive takeaways
- Enforce download/export restrictions at all exit points: enforce permission checks for 'Download as', 'Save as', 'Export', and 'Use as' functions, not just primary download buttons
- Implement server-side validation: require backend confirmation of download permissions before serving file content for any export operation
- Disable file viewer export options when download permission is revoked: grey out or remove 'Download', 'Export', 'Save as', and image utility options from the UI
- Conduct permission model review: audit all code paths that handle file retrieval to ensure consistent authorization enforcement
- Use intent filters cautiously: restrict files from being shared to external apps or system functions (wallpaper, contact photo) when download is disabled
- Implement DLP controls: prevent files from being saved to accessible device directories unless explicitly permitted
- Perform cross-platform testing: verify that restrictions are enforced consistently across web, iOS, Android, and desktop clients

## Variant hunting
Check if print-to-PDF or screenshot capture bypasses restrictions
Test whether sharing to third-party apps (messaging, cloud storage) is restricted
Verify if caching behavior stores downloaded files in accessible locations
Test other file formats (.docx, .xlsx, .pptx) not mentioned in the original report
Check if offline mode persists files that should be restricted
Test whether the 'Allow download' setting applies retroactively to previously shared files
Examine if permission changes take effect immediately or require re-sharing
Check for race conditions between permission updates and active download sessions

## MITRE ATT&CK
- T1190
- T1199
- T1005
- T1020
- T1537
- T1078

## Notes
The reporter identified multiple export pathways (Download as, Use as image) that circumvent restrictions. The issue affects multiple file formats inconsistently—some files (.mp3, .mp4, .txt) could not be opened, suggesting format-specific viewer implementations. The 'Allow download' toggle required clicking twice to apply, indicating potential UI/state management issues. The infinite loading on 'Save as' suggests backend issues but doesn't prevent the core bypass via alternate export methods.

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
