# ActiveStorage Direct Upload Fails to Sign Content-Length Header for S3 Service

## Metadata
- **Source:** HackerOne
- **Report:** 789579 | https://hackerone.com/reports/789579
- **Submitted:** 2020-02-05
- **Reporter:** travispew
- **Program:** Rails
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper Input Validation, Signature/Authorization Bypass, Resource Exhaustion
- **CVEs:** CVE-2020-8162
- **Category:** memory-binary

## Summary
Rails ActiveStorage's S3 direct upload feature fails to include the content-length header in presigned URLs due to silent blacklisting by the aws-sdk-s3 gem. This allows attackers to upload files of arbitrary size, bypassing intended size restrictions and potentially causing financial damage through excessive S3 storage costs.

## Attack scenario
1. Attacker identifies a Rails application using ActiveStorage with S3 direct uploads and size restrictions
2. Attacker initiates a direct upload request claiming a small file size (e.g., 1MB) to pass validation
3. Application generates a presigned URL intended to restrict uploads to the claimed size
4. Attacker receives presigned URL without the content-length constraint (due to sdk blacklisting)
5. Attacker uploads a much larger file (e.g., 10GB) directly to S3 using the presigned URL
6. Upload succeeds because content-length validation was never enforced in the signed URL

## Root cause
The aws-sdk-s3 gem's presigner silently blacklists the 'content-length' header by default, preventing it from being included in generated presigned URLs. Rails' S3Service.url_for_direct_upload() did not use the whitelist_headers parameter to explicitly allow content-length, resulting in this critical security header being omitted from the signature.

## Attacker mindset
An attacker exploiting this would aim to maximize costs to the target organization by uploading massive files to S3, or to disrupt service by consuming quota limits. The attack is trivial once the vulnerability is understood—simply claim a small file size and upload large content.

## Defensive takeaways
- Always explicitly whitelist required security headers in presigned URL generation, do not rely on defaults
- Validate file sizes at multiple layers: client-side, presigned URL, and S3 bucket policies
- Implement S3 bucket policies that enforce content-length restrictions independently of presigned URLs
- Monitor S3 upload metrics and set up alerts for unusually large uploads
- Review upstream library behavior changes and security implications when updating dependencies
- Document security assumptions about presigned URLs and validate them through testing
- Implement server-side validation of uploaded content even with presigned URLs

## Variant hunting
Look for similar header-stripping behavior in other cloud SDKs (Azure, GCP) when generating signed URLs. Check for other Rails features that generate presigned URLs without explicit header whitelisting. Investigate whether other security-critical headers (content-md5, content-type) are similarly affected.

## MITRE ATT&CK
- T1190
- T1499
- T1657

## Notes
This vulnerability demonstrates the danger of implicit security behavior in libraries—the aws-sdk-s3 gem silently discarding headers is a footgun. The fix is a one-line addition (whitelist_headers parameter). The issue affects all Rails versions with ActiveStorage direct uploads until patched. Developers implementing size restrictions likely believed they were protected when they were not.

## Full report
<details><summary>Expand</summary>

When a user makes a direct upload using ActiveStorage, the browser makes a request to the DirectUploadsController containing the direct_upload parameters filename, content_type, byte_size, and checksum. These are used to generate a presigned url that is then passed back to the browser, allowing the user to upload directly to S3.

In particular, the byte_size parameter is intended to be encoded in the url for content-length, preventing the user from uploading a file of a different size. Although Rails does not currently provide any built in validations, developers have been encouraged to modify the controller or provide their own controller if they want to create a validation. For example, a developer might decide to prohibit uploads greater than 10MB in size.

in all current version of Rails with ActiveStorage and direct uploads `active_storage/lib/active_storage/service/s3_service.rb`, the code generates the presigned_url as follows:

```ruby
    def url_for_direct_upload(key, expires_in:, content_type:, content_length:, checksum:)
      instrument :url, key: key do |payload|
        generated_url = object_for(key).presigned_url :put, expires_in: expires_in.to_i,
          content_type: content_type, content_length: content_length, content_md5: checksum

        payload[:url] = generated_url

        generated_url
      end
    end
```

However, the aws-sdk-s3 gem *silently blacklists* the "content-length" header:

https://github.com/aws/aws-sdk-ruby/blob/master/gems/aws-sdk-s3/lib/aws-sdk-s3/presigner.rb#L22

This issue is also raised here: https://github.com/aws/aws-sdk-ruby/issues/2098

As a result, the content-length header is never actually part of the presigned url. As a result, a malicious user can select a file of arbitrary size, tell the direct uploads controller that the file is a different size, and then proceed to upload the file, bypassing the intended protection of the signed url.

The solution is to add the whitelist_headers argument:

```ruby
    def url_for_direct_upload(key, expires_in:, content_type:, content_length:, checksum:)
      instrument :url, key: key do |payload|
        generated_url = object_for(key).presigned_url :put, expires_in: expires_in.to_i,
          content_type: content_type, content_length: content_length, content_md5: checksum,
          whitelist_headers: ['content-length']

        payload[:url] = generated_url

        generated_url
      end
    end
```
After this is added, the content-length will be included in the presigned url and the client will be unable to upload a file of arbitrary size.

## Impact

The attacker could upload a file of any size, unless the S3 service is configured separately to prevent this, whereas the developer believes they have protected themselves against this. This could allow an attacker to upload a very large file to S3, incurring additional costs to the website owner or causing other harm.

</details>

---
*Analysed by Claude on 2026-05-24*
