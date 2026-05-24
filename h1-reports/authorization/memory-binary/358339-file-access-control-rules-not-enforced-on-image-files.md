# File Access Control Rules Not Enforced on Image Files and Previews in Nextcloud

## Metadata
- **Source:** HackerOne
- **Report:** 358339 | https://hackerone.com/reports/358339
- **Submitted:** 2018-05-28
- **Reporter:** reinism
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Authorization Bypass, Information Disclosure, API Security Misconfiguration
- **CVEs:** CVE-2018-3762
- **Category:** memory-binary

## Summary
Nextcloud's Files Access Control app fails to enforce access restrictions on image thumbnail/preview generation and file listing APIs. Unprivileged users can bypass file access control rules to enumerate all files via WebDAV search and retrieve previews of restricted images at arbitrary resolutions, even if the admin has explicitly denied access.

## Attack scenario
1. Administrator creates access control rules restricting file access for unprivileged users and tags sensitive files with restrictive tags
2. Attacker gains unprivileged user credentials or is granted limited shared access to a folder containing restricted files
3. Attacker uses WebDAV search API to recursively list all files in the folder hierarchy, bypassing access control checks, obtaining file paths and MIME types
4. Attacker identifies image files from the enumerated list and constructs direct requests to the thumbnail/preview API at /apps/files/api/v1/thumbnail/{width}/{height}/{filepath}
5. Thumbnail API generates preview images on-demand without validating access control rules, returning full-resolution previews of restricted images
6. Attacker downloads previews of restricted files or text file screenshots containing sensitive information that should have been protected

## Root cause
The thumbnail/preview generation API (/apps/files/api/v1/thumbnail/) and WebDAV search functionality do not invoke the Files Access Control app's permission checks before generating or returning file previews and listings. The access control rules are enforced at the file browser level but bypass occurs at lower-level API endpoints that directly access file storage without proper authorization middleware.

## Attacker mindset
An attacker with legitimate but limited access (unprivileged user or restricted share recipient) seeks to escalate privileges by discovering an API endpoint that bypasses access controls. The attacker recognizes that preview/thumbnail generation is resource-intensive and likely handles permissions separately from the main file access layer, making it a weak point. By crafting direct API requests rather than using the web interface, the attacker avoids triggering logging and detection mechanisms.

## Defensive takeaways
- Implement centralized authorization checks in a reusable service/middleware that ALL file-related APIs must invoke, including preview, thumbnail, and WebDAV endpoints
- Ensure access control rules are enforced at the earliest point in the request handling pipeline, before any file processing or preview generation
- Audit all file access APIs (REST, WebDAV, preview, thumbnail, search) to verify they implement identical permission checks
- Disable or restrict the WebDAV SEARCH method if it is not essential, or implement granular permission filtering on search results
- Generate preview files only after successful authorization; cache previews with access control metadata and validate user permissions on cache hits
- Log all preview/thumbnail API requests and access attempts, especially for restricted files
- Implement rate limiting on preview/thumbnail endpoints to prevent enumeration and bulk download attacks
- Conduct security testing of all file-access APIs with users having varying permission levels to detect authorization bypass

## Variant hunting
Search for similar bypass patterns in: (1) other file preview/thumbnail endpoints in Nextcloud or competing platforms; (2) other lazy-loading or on-demand resource generation APIs that may skip authorization; (3) WebDAV implementations in other applications that enumerate files without permission filtering; (4) REST APIs that process user-supplied file paths without validating access; (5) Export or bulk-download features that generate temporary files or archives without re-checking permissions.

## MITRE ATT&CK
- T1190
- T1566
- T1552
- T1526
- T1087
- T1083

## Notes
This vulnerability affects Nextcloud 13.0.2snap1 with Files Access Control v1.3.0. The issue demonstrates a critical gap between high-level access control policies and low-level API implementations. The attacker does not need to generate previews themselves; previews are created on-demand by the vulnerable API, making the attack passive from the admin's perspective. The ability to enumerate files at arbitrary depth via WebDAV SEARCH is a separate but related vulnerability that aids reconnaissance.

## Full report
<details><summary>Expand</summary>

1. Installed Nextcloud from Snap package (version 13.0.2snap1, revision 6916) on fresh Ubuntu 18.04 LTS install.
2. Installed and enabled Files access control (v1.3.0) and Files automated tagging (v1.3.0) apps.
3. As an administrator created an invisible collaborative tag `Secret`.
4. Added Files automated tagging rule to add the `Secret` tag for all files with user membership of `admin` group.
5. Added Files access control rule restricting the access for all files with the `Secret` tag and user who is not a member of `admin` group.
6. Created unprivileged user `user`.
7. Accessed the `admin` account from WebDAV interface (in order to avoid generating automatic file previews) and created the following files/folders on the server:

    ```
    folder:    Secret_Folder
    folder:    Secret_Folder/Secret_Subfolder
    file:      Secret_Folder/Secret_Subfolder/Secret_Picture.jpeg
    file:      Secret_Folder/Secret_Subfolder/Secret_Text.txt
    ```
8. Shared the `Secret_Folder` from `admin` user to the unprivileged user `user` with no edit rights.
9. From client computer authorized as the unprivileged user `user` and used WebDAV search to recursively list all files with their MIME types with the following `curl` command: {F302611}. This command downloaded the list of all shared files as an xml file: {F302614}.
10. Identified an image file `Secret_Folder/Secret_Subfolder/Secret_Picture.jpeg` from the file list and accessed its contents through files preview API with the following `curl` command:

    ```
    curl -u user 'https://test.frp.lv/index.php/apps/files/api/v1/thumbnail/1212/750/Secret_Folder/Secret_Subfolder/Secret_Picture.jpeg' -H 'Content-Type: application/x-www-form-urlencoded' > Secret_Picture.jpeg
    ```

## Impact

1. The unauthorized attacker can list all files recursively for an unlimited depth, even if explicitly denied by `Files access control` rules.
2. The unauthorized attacker can view the contents of all denied image files up to their maximum resolution. It is up to the attacker to choose the required image resolution (1024 x 768 in the example) and construct corresponding `GET` query through image preview API. Note that it is not even required for the file owner to use web interface and preview the protected image files before the attack. The corresponding image preview files are generated on the server upon the request of the attacker.
3. If the file owner has logged in Nextcloud web interface and browsed the protected files, thus automatically rendering thumbnail previews, it also becomes possible for the attacker to access previews of protected text files with the following `curl` command referencing the text file from the example, choosing 4096x4096 resolution:

    ```
    curl -u user 'https://test.frp.lv/index.php/apps/files/api/v1/thumbnail/4096/4096/Secret_Folder/Secret_Subfolder/Secret_Text.txt' -H 'Content-Type: application/x-www-form-urlencoded' > Secret_Text.png
    ```
The obtained preview image can contain critical information that should have been protected - see example of downloaded preview below:
{F302628}

</details>

---
*Analysed by Claude on 2026-05-24*
