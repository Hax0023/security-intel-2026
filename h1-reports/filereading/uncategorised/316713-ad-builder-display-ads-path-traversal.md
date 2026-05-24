# Ad Builder Display Ads Path Traversal via Zip Extraction and CSV Processing

## Metadata
- **Source:** HackerOne
- **Report:** 316713 | https://hackerone.com/reports/316713
- **Submitted:** 2018-02-16
- **Reporter:** ajxchapman
- **Program:** Semrush
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Path Traversal, Arbitrary File Read, Zip Slip, Directory Traversal
- **CVEs:** None
- **Category:** uncategorised

## Summary
Semrush Ad Builder Display Ads feature is vulnerable to path traversal attacks through two vectors: malicious zip file entries with traversal sequences (e.g., `../`) that extract outside intended directories, and CSV file fields that reference arbitrary files on the filesystem via path traversal. An attacker can upload a crafted zip file to read arbitrary files from the system or extract files to unintended locations.

## Attack scenario
1. Attacker creates a zip file containing a CSV with image path field containing traversal sequences like `../../../usr/share/pixmaps/debian-logo.png`
2. Attacker uploads the malicious zip to Ad Builder via 'New Ad' > 'From File' workflow
3. Backend extracts zip file, but fails to sanitize filenames containing `../` sequences
4. CSV processor reads image paths without validation and resolves them relative to filesystem root
5. Attacker successfully references or extracts arbitrary files from the system, potentially leaking sensitive information or writing files outside intended directories
6. Attacker observes referenced image is rendered in produced advert, confirming file access success

## Root cause
Insufficient input validation and path sanitization in two locations: (1) zip file extraction logic fails to neutralize path traversal sequences in entry filenames before extraction, and (2) CSV field processor does not validate or canonicalize image path references before file operations, allowing relative path traversal sequences to escape the intended directory.

## Attacker mindset
An authenticated attacker seeks to exfiltrate sensitive files from the server (e.g., configuration files, credentials, system information via Debian logo discovery) or achieve arbitrary file write to compromise system integrity. The attacker leverages the file import feature as an attack surface, exploiting trust in user-supplied archives.

## Defensive takeaways
- Implement strict zip file extraction with path traversal prevention: validate all extracted file paths are within intended directory using canonical path comparison
- Sanitize all file path inputs from CSV fields by rejecting entries containing `..`, `./`, absolute paths, or null bytes; use whitelisting of expected relative paths
- Store uploaded files with randomized names in isolated directories and restrict filesystem access permissions
- Implement and enforce file type validation based on content (magic bytes), not just extensions
- Use dedicated secure zip extraction libraries with built-in protections against Zip Slip vulnerabilities
- Apply principle of least privilege to file system operations; run extraction and processing in sandboxed environment with minimal permissions
- Add logging and monitoring for file access patterns that attempt traversal sequences
- Implement content security policy to prevent rendering of unexpectedly sourced images in advertisements

## Variant hunting
Search for similar vulnerabilities in other Semrush file import features (creative uploads, document imports). Test other ad platforms with zip-based asset imports. Look for path traversal in CSV processors across any web application accepting user-supplied CSV files with file references. Examine other archive extraction operations (tar, gz) in Semrush infrastructure.

## MITRE ATT&CK
- T1190
- T1083
- T1566.001
- T1021.001
- T1552.001

## Notes
Reporter indicates test files created outside intended directory during testing and should be removed by Semrush team. The error message disclosure revealing full file paths (`/███████/█████/ab_███_1246354_displayAds.tmp.unpack/`) aids attacker understanding of filesystem structure. Report references sensitive path information that has been redacted in this analysis. The vulnerability requires authentication but allows significant system reconnaissance (OS identification via default image detection) and potential lateral movement through arbitrary file write.

## Full report
<details><summary>Expand</summary>

**Summary:** 
The Semrush Ad Builder for Display Ads is vulnerable to path traversal when extracting zip files and referencing images from the embedded `data.csv` file.

**Description:** 
The Semrush Ad Builder for Display Ads allows users to import Display Ads from an uploaded zip file. The backend functionality that extracts the uploaded zip file and processes the files contained within is vulnerable to path traversal in multiple places.

Firstly, the zip extractor is vulnerable to path traversal from zip file names, allowing files to be extracted outside of the intended destination directory. Uploaded zip files are extracted to the `/█████████/██████████/ab_<api key>_<project id>_displayAds.tmp.unpack` destination directory (where ``<api key>`` and ``<project id>`` are the user's api key and the current project id respectively). If a zip file is extracted which includes a filename with a path traversal specifier (e.g. `/../`), it will be extracted outside of the intended destination directory.

Example zip file contents and extraction locations:
```
Zip file path    Extracted file path
data.csv      => /██████/█████/ab_███████_1246354_displayAds.tmp.unpack/data.csv
words.csv     => /████████/████/ab_███_1246354_displayAds.tmp.unpack/words.csv
../1.png      => /█████████/███/1.png
```

The full file path of the zip file destination was identified from error messages observed during testing, e.g.:
```json
{"jsonrpc":"2.0","id":"1c46d1ff-7327-4be2-8b8f-69c1906fb71c","error":{"code":-32603,"message":"mkdir /███████/█████/ab_███_1246354_displayAds.tmp.unpack/link: not a directory"}}
```

Secondly, the Display Ads file processor is vulnerable to path traversal when processing `data.csv` files. The `Image`, `Square image`, `Logo` and `Landscape logo` fields of the `data.csv` file are all vulnerable to path traversal. Including an `Image` path with path traversal specifiers allows us to reference images which already exist on the Ad Builder system. For example the path `../../../usr/share/pixmaps/debian-logo.png` will reference the `/usr/share/pixmaps/debian-logo.png` image which exists by default on most Debian based systems. This image will be used in the produced advert.

Please note that during testing I have created two files outside of the `/████████/█████/ab_█████_1246354_displayAds.tmp.unpack/` folder, `/██████/████████/1.png` and `/█████/███/link`. These files should be removed when this issue is confirmed.

## Browsers Verified In:

  * Firefox version 58.0.2 (64-bit)

## Steps To Reproduce:

  1. Create a new Semrush project
  2. Select "Ad Builder" then "Display Ads"
  3. Then select "New Ad" -> "From File" and upload one of the zips attached to this issue
  4. Click through the rest of the wizard
  5. Observe the outcome in the produced advert

See the attached screen capture for a demonstration of this issue.

## Supporting Material/References:

**Zip file referencing pre existing image outside the zip file (`/usr/share/pixmaps/debian-logo.png`)**

`display-ads-deb.zip` (Attachment ████████)
```bash
$ zipinfo display-ads-deb.zip
Archive:  display-ads-deb.zip
Zip file size: 581 bytes, number of entries: 2
-rw-r--r--  3.0 unx      432 tx defN 18-Feb-16 07:35 data.csv
-rw-r--r--  3.0 unx       48 tx stor 18-Feb-15 18:28 words.csv
2 files, 480 bytes uncompressed, 269 bytes compressed:  44.0%
```

`data.csv`
```csv
Status,Campaign,Campaign Type,Ad Group,Short headline,Long headline,Description,Business name,Image,Square image,Logo,Landscape logo,Final URL,Final mobile URL,Tracking URL
Enabled,Default campaign,Display Network only,Default Group,Something,Something,Something,Something,../../../usr/share/pixmaps/debian-logo.png,../../../usr/share/pixmaps/debian-logo.png,../../../usr/share/pixmaps/debian-logo.png,,http://semrush.webhooks.pw,,
```

Uploading this zip file, which contains no images, to the Display Ads Ad Builder will create an advert which references an image that already exists on the system outside the intended destination directory. The referenced image is `/usr/share/pixmaps/debian-logo.png` which exists by default on most Debian based systems. From this we can infer that the Ad Builder is running some Debian derivative Linux.

**Zip file extracting file outside of the intended destination directory (`/███/███████/1.png`)**

`display-ads-trav.zip` (Attachment ██████)
```bash
$ zipinfo display-ads-trav.zip
Archive:  display-ads-trav.zip
Zip file size: 18357 bytes, number of entries: 4
drwxr-xr-x  3.0 unx        0 bx stor 18-Feb-16 07:37 aa/
-rw-r--r--  3.0 unx    25650 bx defN 18-Feb-16 07:37 ../1.png
-rw-r--r--  3.0 unx      306 tx defN 18-Feb-16 07:42 data.csv
-rw-r--r--  3.0 unx       48 tx stor 18-Feb-15 18:28 words.csv
4 files, 26004 bytes uncompressed, 17767 bytes compressed:  31.7%
```

`data.csv`
```csv
Status,Campaign,Campaign Type,Ad Group,Short headline,Long headline,Description,Business name,Image,Square image,Logo,Landscape logo,Final URL,Final mobile URL,Tracking URL
Enabled,Default Campaign,Display Network only,Default Group,Something,Something,Something,Something,,,,,http://semrush.webhooks.pw,,
```

Uploading this zip file to the Display Ads Ad Builder will place the `1.png` image in the `/███████/███` directory, which is outside the intended destination directory (`/████████/██████████/ab_███_1246354_displayAds.tmp.unpack/`). No images are referenced in the created advert.

**Zip file referencing created image outside the zip file (`/███████/██████/1.png`)**

`display-ads-new.zip` (Attachment ███████)
```bash
$ zipinfo display-ads-new.zip
Archive:  display-ads-new.zip
Zip file size: 574 bytes, number of entries: 2
-rw-r--r--  3.0 unx      390 tx defN 18-Feb-16 07:48 data.csv
-rw-r--r--  3.0 unx       48 tx stor 18-Feb-15 18:28 words.csv
2 files, 438 bytes uncompressed, 262 bytes compressed:  40.2%
```

`data.csv`
```csv
Status,Campaign,Campaign Type,Ad Group,Short headline,Long headline,Description,Business name,Image,Square image,Logo,Landscape logo,Final URL,Final mobile URL,Tracking URL
Enabled,Default Campaign,Display Network only,Default Group,Something,Something,Something,Something,../../../██████/█████/1.png,../../../███████/█████/1.png,../../../████/█████/1.png,,http://semrush.webhooks.pw,,
```

Uploading this zip file, which contains no images, to the Display Ads Ad Builder will create an advert which references the image `/████████/████/1.png` created by `display-ads-trav.zip` above.

## Impact

These issues can be abused to place arbitrary files in writable directories on the Ad Buider system and infer the existence of █████ious system properties and installed packages (such as Linux flavour, python version, golang version, etc.). 

In the worst case this issue could lead to complete compromise of the Ad Builder system through writing scripts or executables to directories where they will be automatically executed. During testing however, I have been unable to identify any writable directories outside of `/███/████████` and it's subdirectories. For this reason I have not included the full system compromise in consideration of the CVSSv3 calculation. However, other writable directories may exist on the system which could increase the impact of this issue significantly.

</details>

---
*Analysed by Claude on 2026-05-24*
