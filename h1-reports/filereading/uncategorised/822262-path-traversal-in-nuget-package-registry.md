# Path Traversal in GitLab NuGet Package Registry Leading to Arbitrary File Read

## Metadata
- **Source:** HackerOne
- **Report:** 822262 | https://hackerone.com/reports/822262
- **Submitted:** 2020-03-17
- **Reporter:** saltyyolk
- **Program:** GitLab
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Arbitrary File Read, Race Condition (combined)
- **CVEs:** CVE-2020-12448
- **Category:** uncategorised

## Summary
A path traversal vulnerability exists in the NuGet package registry metadata extraction service that allows attackers to create arbitrary files with .nupkg extension by injecting path traversal sequences in the version field of a nuspec XML manifest. When combined with a race condition in Gitaly, this enables reading of sensitive files from the GitLab instance such as .gitlab_shell_secret.

## Attack scenario
1. Attacker crafts a malicious nuspec XML file with path traversal payload in the version field (e.g., ../../../../../nyangawa)
2. Attacker zips the nuspec file into a .nupkg package and uploads it via the NuGet package registry API endpoint PUT /api/v4/projects/{id}/packages/nuget/
3. The metadata extraction service extracts package name and version from the XML without proper validation
4. The version string containing path traversal characters is concatenated with package name to create a new filename
5. The file system operation creates files in unintended directories due to the traversal characters
6. Attacker combines this with a known Gitaly race condition to read sensitive files like .gitlab_shell_secret

## Root cause
The metadata extraction service in ee/app/services/packages/nuget/metadata_extraction_service.rb extracts the version field from user-controlled XML without sanitization. The extracted version is directly used in filename construction in update_package_from_metadata_service.rb without path validation, allowing directory traversal sequences to escape the intended package directory.

## Attacker mindset
Opportunistic attacker leveraging package upload functionality combined with known infrastructure vulnerabilities to escalate from file write to sensitive file read capabilities. Demonstrates chaining of multiple weaknesses to achieve impact beyond single vulnerability scope.

## Defensive takeaways
- Implement strict validation on extracted metadata fields to reject or sanitize path traversal sequences (../, ..\ etc.)
- Use path normalization and verification to ensure constructed filenames remain within intended directories
- Apply basename() or similar functions to extracted package names/versions before filename construction
- Implement allowlist validation for package name and version formats according to NuGet specifications
- Add integration tests specifically for path traversal payloads in package upload workflows
- Consider using secure temporary directories and atomic move operations
- Implement rate limiting on package upload endpoints to mitigate race condition exploitation

## Variant hunting
Search for similar patterns in other package registry implementations (npm, pypi, maven, etc.) where user-supplied metadata from package manifests is used in file operations. Check for path traversal in version/name/author fields across package managers. Review other services using Nokogiri XML parsing with user input.

## MITRE ATT&CK
- T1190
- T1083
- T1526

## Notes
This report chains multiple vulnerabilities: (1) path traversal in package metadata handling, (2) inadequate input validation on version field, (3) race condition in Gitaly service. The exploit demonstrates understanding of package manager internals and infrastructure-level race conditions. Report references similar npm registry issue (#762421) indicating pattern recognition by researcher.

## Full report
<details><summary>Expand</summary>

### Summary
There's a path traversal issue in Nuget package registry which was released to GitLab-EE recently. The issue allows an attacker to create any file with an extension “.nupkg” in the filesystem. By combining the bug with a race condition in Gitaly which I used several times before (#762421, #732330). It could finally be used to read sensitive files in a GitLab instance.

For some context, a large part of the exploit were explained in #762421, the npm registry issue. Here I will focus on the simple path traversal part which makes a little bit difference.

The root cause of the path traversal lies at `ee/app/services/packages/nuget/metadata_extraction_service.rb`
```
      XPATHS = {                                                               
        package_name: '//xmlns:package/xmlns:metadata/xmlns:id',               
        package_version: '//xmlns:package/xmlns:metadata/xmlns:version'        
      }.freeze 
...
      def extract_metadata(file)                                               
        doc = Nokogiri::XML(file)                                              
                                                                               
        XPATHS.map do |key, query|                                             
          [key, doc.xpath(query).text]                                         
        end.to_h 
```
It extracts the uploaded nupkg (which is in zip format) for the contained nuspec file (which is an XML). And then looks for attribute `id` and `version`. Then the extracted package_name(id), and package_version(version) will be concatenated into a new filename in `ee/app/services/packages/nuget/update_package_from_metadata_service.rb`
```                                                                      
        @package_file.transaction do                                           
          @package_file.update!(                                               
            file_name: package_filename,                                       
            file: @package_file.file                                           
          )      
...
      def package_filename                                                     
        "#{package_name.downcase}.#{package_version.downcase}.nupkg"           
      end    
```
So my payload is:
```                                                                  
  <?xml version="1.0" encoding="utf-8"?>                                       
  <package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">  
    <metadata>                                                                 
      <id>DummyProject.DummyPackage</id>                                       
      <version>../../../../../nyangawa</version>                                            
    </metadata>                                                                
  </package>                                                                   
```
name the file above as `dummy.nuspec` and zip it into `dummy.nupkg` and upload it through `PUT /api/v4/projects/#{id}/packages/nuget/` endpoint  will make GitLab to create a `nyangawa.nupkg` somewhere in the filesystem.

Then I wrote a script (I used in #762421) to combine this issue and the race in Gitaly. I could finally read any file I want in my GitLab instance.

### Steps to reproduce

1. Download the attached exploit.tar.gz and extract it.
2. Install some requirements by gem install faraday and gem install rubyzip
3. Edit exp.rb to update some url and credentials
4. Execute the exp.rb to watch the result of .gitlab_shell_secret of target GitLab instance.

### Examples
{F750878}

#### Results of GitLab environment info
```
root@localhost:/# gitlab-rake gitlab:env:info

System information
System:		
Proxy:		no
Current User:	git
Using RVM:	no
Ruby Version:	2.6.5p114
Gem Version:	2.7.10
Bundler Version:1.17.3
Rake Version:	12.3.3
Redis Version:	5.0.7
Git Version:	2.24.1
Sidekiq Version:5.2.7
Go Version:	unknown

GitLab information
Version:	12.8.7-ee
Revision:	2643fd87200
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	10.12
URL:		http://10.26.0.5
HTTP Clone URL:	http://10.26.0.5/some-group/some-project.git
SSH Clone URL:	git@10.26.0.5:some-group/some-project.git
Elasticsearch:	no
Geo:		no
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	11.0.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

ps. I changed my username because of a lost bet, don't be strange :p

Best regards,
SaltyYolk

## Impact

Common arbitrary file read issue caused by path traversal similar to my previous reports.

</details>

---
*Analysed by Claude on 2026-05-24*
