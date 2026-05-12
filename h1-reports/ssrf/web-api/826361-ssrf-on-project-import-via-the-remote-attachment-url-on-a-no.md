# SSRF on Project Import via remote_attachment_url on Note

## Metadata
- **Source:** HackerOne
- **Report:** 826361 | https://hackerone.com/reports/826361
- **Submitted:** 2020-03-22
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** $10,000 USD
- **Severity:** high
- **Vuln:** Server-Side Request Forgery (SSRF), Insecure Deserialization, Missing Input Validation, Insufficient Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's project import feature failed to sanitize CarrierWave uploader attributes (remote_attachment_url) on Note models, allowing attackers to trigger arbitrary HTTP requests from the server during project import. This SSRF vulnerability could be exploited to access internal services, cloud metadata endpoints, or achieve RCE via exposed services like Redis.

## Attack scenario
1. Attacker creates a legitimate GitLab project with issues and notes
2. Attacker exports the project to obtain the project.json export file
3. Attacker extracts the export archive and modifies the note's JSON to include 'remote_attachment_url' pointing to an internal service (e.g., http://localhost:9090/api/v1/targets, AWS metadata endpoint, or Google Cloud metadata endpoint)
4. Attacker optionally adds 'remote_attachment_request_header' with custom headers to bypass metadata service protections
5. Attacker recompresses the modified export and imports it into a target GitLab instance
6. Server downloads the file from the attacker-specified URL, exposing internal service responses or sensitive metadata

## Root cause
The AttributeCleaner failed to blacklist CarrierWave uploader seed attributes (remote_attachment_url and remote_attachment_request_header) during project import. When Note models were created from imported JSON, CarrierWave's mount_uploader hook automatically invoked the download! method to fetch files from untrusted URLs without validation.

## Attacker mindset
An attacker with project export/import capabilities seeks to leverage the project import workflow as a covert request smuggling mechanism. By embedding malicious CarrierWave attributes in project.json, they bypass authentication and network controls to probe internal infrastructure, enumerate services, or exploit local elevation paths (Redis RCE, cloud metadata theft).

## Defensive takeaways
- Implement strict attribute whitelisting in AttributeCleaner - explicitly define which attributes are safe for import rather than blacklisting
- Disable automatic file downloads from user-supplied URLs in CarrierWave configurations; require explicit user interaction or admin approval
- Validate all URLs against a whitelist before allowing remote fetches (reject localhost, private IP ranges, cloud metadata endpoints)
- Audit all mount_uploader directives across importable models to identify similar SSRF vectors
- Implement network egress controls and request logging to detect anomalous outbound connections during import operations
- Add security tests for project import that validate no unauthorized HTTP requests are triggered
- Isolate import processing in sandboxed environments with restricted network access

## Variant hunting
Check other importable models with mount_uploader directives (e.g., Avatar, ProjectAvatar) for similar attributes - test if remote_avatar_url is sanitized
Verify if other file upload gems (Paperclip, ActiveStorage) have similar remote URL features in importable models
Test if other import formats (e.g., CI/CD pipeline imports, wiki imports) have similar attribute-cleaning gaps
Investigate whether remote_attachment_request_header allows header injection to bypass authentication on internal services
Test if the vulnerability affects nested associations or deeply nested JSON structures in project exports
Check if group/namespace imports have the same vulnerability
Review merge request approvals, wiki pages, and other user-generated content models for similar patterns

## MITRE ATT&CK
- T1190
- T1498
- T1557
- T1539
- T1552

## Notes
This vulnerability demonstrates the risk of implicit security assumptions in third-party gems. The project import feature intended to provide convenience but inadvertently created an unauthenticated tunnel for SSRF. The researcher demonstrated real-world impact by showing integration with public request logging service (postbin) and detailing cloud-specific exploitation paths (AWS metadata, Google Cloud metadata). The fix required both sanitizing imports and potentially disabling automatic remote URL downloads in CarrierWave configuration.

## Full report
<details><summary>Expand</summary>

### Summary

The Note model has an `attachment` which is provided by a CarrierWave uploader:

```ruby
mount_uploader :attachment, AttachmentUploader
```

One of the features this provides is the ability to download and attach a file via a url, see https://github.com/carrierwaveuploader/carrierwave/blob/v1.3.1/lib/carrierwave/mount.rb#L80. This means that the Note model has a method `remote_attachment_url=` which can be used to perform this action.

As this attribute isn't removed by the `AttributeCleaner` on project import, it can be set in the `project.json` for a note and will be set when the note is created, downloading the file:

https://github.com/carrierwaveuploader/carrierwave/blob/v1.3.1/lib/carrierwave/mounter.rb#L72
```ruby
  def remote_urls=(urls)
      return if not urls or urls == "" or urls.all?(&:blank?)

      @remote_urls = urls
      @download_error = nil
      @integrity_error = nil

      @uploaders = urls.zip(remote_request_headers || []).map do |url, header|
        uploader = blank_uploader
        uploader.download!(url, header || {})
        uploader
      end
```

https://github.com/carrierwaveuploader/carrierwave/blob/v1.3.1/lib/carrierwave/uploader/download.rb#L43
```ruby
    def file
          if @file.blank?
            headers = @remote_headers.
              reverse_merge('User-Agent' => "CarrierWave/#{CarrierWave::VERSION}")

            @file = Kernel.open(@uri.to_s, headers)
            @file = @file.is_a?(String) ? StringIO.new(@file) : @file
          end
```

The downloaded file is then attached to the note and can be viewed from the newly imported project.

Any model that has a `mount_uploader` and is importable is potentially vulnerable to the same attack, although the majority of the others are `AvatarUploader` which checks the file type and prevents the response from being viewed.

### Steps to reproduce

1. Create a new project
1. Create an issue in the project
1. Add a note to the issue
1. Export the project
1. Extract the export
1. Add  `remote_attachment_url` to the `note` hash with a url
1. Recompress the export and import it
1. View the note on the issue

Demo {F756257}

### Examples

Example of project import on gitlab.com hitting postbin:

https://gitlab.com/wbowling/ssrf1/-/issues/1#note_309127303
{F756269}

### What is the current *bug* behavior?
When importing a model that has a mount_uploader it's possible to use the carrierwave uploader seed attributes to download a file from any host: https://github.com/carrierwaveuploader/carrierwave/wiki/How-to:-Upload-remote-image-urls-to-your-seedfile

### What is the expected *correct* behavior?
The attributes should be prohibited and removed via the `AttributeCleaner`

### Output of checks
This bug happens on gitlab.com

#### Results of GitLab environment info
```
System information
System:		Ubuntu 18.04
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
URL:		http://gitlab-vm.local
HTTP Clone URL:	http://gitlab-vm.local/some-group/some-project.git
SSH Clone URL:	git@gitlab-vm.local:some-group/some-project.git
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

## Impact

* Allows an attacker to access internal services, for example the Omnibus GitLab has all of the exporters, Prometheus, Alertmanager exposed on localhost. 
* If GitLab is hosted on AWS it allows for the instance metadata to be accessed.
* Redis is running locally or accessible via tcp (address could be found by looking at the targets in Prometheus at http://localhost:9090/api/v1/targets) it could be possible to obtain RCE (similar to https://github.com/jas502n/gitlab-SSRF-redis-RCE#poc). A POST request is not possible here, but as `remote_attachment_request_header=` is also available (https://github.com/carrierwaveuploader/carrierwave/blob/v1.3.1/lib/carrierwave/mount.rb#L169) and not blacklisted, the payload could be set via a header.
* If GitLab is hosted on Google Cloud, the above could be used to set the `Metadata-Flavor: Google` header and access `http://metadata.google.internal/`

</details>

---
*Analysed by Claude on 2026-05-11*
