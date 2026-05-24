# File Transformation Creates Public Copies of Private Files Without Access Control

## Metadata
- **Source:** HackerOne
- **Report:** 1984060 | https://hackerone.com/reports/1984060
- **Submitted:** 2023-05-11
- **Reporter:** limusec
- **Program:** Mozilla (Phabricator)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insecure Direct Object References (IDOR), Information Disclosure, Authorization Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
When users upload private files to Phabricator and apply transformations (cropping, resizing), the system generates transformed copies that are publicly accessible regardless of the original file's privacy settings. Users cannot modify or delete these public copies, potentially exposing sensitive PII and personal data.

## Attack scenario
1. Attacker uploads a private image containing sensitive information (e.g., passport, financial documents, ID)
2. Attacker restricts visibility to 'only me' or 'no one' to ensure privacy
3. Attacker uses the 'View Transformations' feature to crop or resize the image to remove sensitive data
4. Attacker clicks 'regenerate' to create the transformed version
5. System generates a new public file link accessible to anyone without authentication
6. Attacker discovers they cannot modify or delete the transformed file, and it remains publicly accessible with original sensitive data intact

## Root cause
The transformation feature does not inherit or respect the parent file's privacy/visibility settings when creating transformed copies. The new transformed files are created with default public permissions, and the original file's access controls are not propagated or enforced on derived assets.

## Attacker mindset
An attacker could exploit this to expose PII of other users by uploading files on their behalf (if account compromise occurs) or by understanding that transformation creates public copies they can discover and access. More likely, legitimate users accidentally leak sensitive data thinking transformations maintain privacy.

## Defensive takeaways
- Always inherit parent file visibility/access control settings to all derived assets and transformations
- Implement permission checks at transformation generation time, not just at original upload
- Provide users with visibility into what permissions transformed files inherit
- Allow users to modify or delete transformed files with the same controls as original files
- Audit transformation feature to ensure it respects privacy boundaries
- Consider restricting transformations to only be available for public or specific user-owned files
- Log transformation creation and access for compliance and auditing purposes

## Variant hunting
Check if other file processing features (compression, format conversion, thumbnails) have the same visibility inheritance issue
Test whether transformation of group/org-shared private files exposes them differently
Verify if transformed files can be discovered through file listings or searches when original is private
Check if API endpoints for transformation bypass the same access controls
Test cascading transformations - if a transformed file is transformed again, does it maintain privacy?
Review if preview generation, caching, or CDN distribution of images has similar issues

## MITRE ATT&CK
- T1190
- T1020
- T1041
- T1526

## Notes
This is a classic access control inheritance issue where derived objects don't maintain parent security properties. The bug is particularly severe because: (1) it affects sensitive file types (documents, photos), (2) users are unaware transformations create public copies, (3) the transformed files cannot be controlled after creation, and (4) the feature appears to serve a legitimate use case (privacy-preserving editing) but does the opposite. This suggests the security model was not considered during feature design.

## Full report
<details><summary>Expand</summary>

## Summary:
When an user uploads a private file, ex (Screenshot 1), where only he has access to. Using the "View transformations" function can generate different kinds of image transformations (Screenshot 2). But after the generation of that transformation for example clicking on  the regenerate button next to profile. The function will create a cropped public image, where the user is unable to edit or modify his own generated image (Screenshot 3). 

Issue: You have a picture with you smiling and your passport holding in your hand (An example would be a "know you customer purpose" selfie). You like that picture on how you look, so you upload it on phabricator, privately, assuming nobody can view it. You click on view transformations, to modify and crop that picture, to get rid of the sensitive data passport you are holding in your hand, so only the face remains. After you clicked on the regenerate next to profile, you realize the crop doesn't work as intended and your passport data is still in there. So you want to modify/delete that picture but you cant. And what's worse that picture visible to anyone and you don't have access to remove it nor to modify it.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

 1.Upload a private picture here: https://phabricator.allizom.org/file/upload/
 2.Change the visibility to no one or just you.
 3. After the upload, click on "View Transformations" on the right.
 4. There you can create different transformations when you click on regenerate.
 5. After that you, you get a new preview to your generated picture. 
 6. Now go back, to the transforms page, and you get a new link on phabricator, that is public, and can't be changed.

I've added a video that showcases this behavior. 


## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]
I've added screenshots and a video to showcase this issue.
  * [attachment / reference]

## Impact

The user is assuming that he can upload private data securely. Not knowing that the transform feature will make his uploaded files public with no way to delete it, could in worst case leak PII information.

</details>

---
*Analysed by Claude on 2026-05-24*
