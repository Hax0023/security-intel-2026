# Persistent XSS in Note Objects via Project Import

## Metadata
- **Source:** HackerOne
- **Report:** 508184 | https://hackerone.com/reports/508184
- **Submitted:** 2019-03-12
- **Reporter:** saltyyolk
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Persistent/Stored XSS, Improper Input Validation, Cache Invalidation Logic Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's project import functionality fails to properly validate and sanitize Note object attributes, allowing attackers to inject persistent XSS payloads into merge request discussions and other locations where Note objects exist. The vulnerability exploits flaws in cache invalidation logic that prevent GitLab from regenerating and sanitizing the `note_html` field during import.

## Attack scenario
1. Attacker exports a legitimate GitLab project containing merge requests with discussions
2. Attacker modifies the exported project.json file to inject XSS payload in the `note_html` field of Note objects (e.g., '<img src="test" onerror="alert(document.domain)"></img>')
3. Attacker sets `cached_markdown_version` to the magic value 917504 to bypass cache validation checks
4. Attacker imports the modified project into the target GitLab instance
5. When users view the imported project's merge request discussions, the malicious JavaScript executes in their browsers with the security context of the GitLab application
6. The XSS payload persists and executes for all users viewing the compromised discussion

## Root cause
Three compounding issues: (1) Project import allows arbitrary modification of all Note object attributes including `note_html` and `cached_markdown_version`; (2) Cache invalidation logic in `CacheMarkdownField` checks for `author` and `project` fields in `changed_attributes`, but receives `author_id` and `project_id` instead, causing the invalidation check to fail; (3) The `cached_html_up_to_date?` check compares versions but the attacker can set `cached_markdown_version` to match the hardcoded `latest_cached_markdown_version` value (917504), preventing cache regeneration and sanitization

## Attacker mindset
Attacker identifies GitLab's project import as a trusted data path and reverse-engineers the cache validation mechanism to understand how to bypass sanitization. By setting specific field values that match internal cache version calculations, the attacker exploits the assumption that cached HTML is safe without re-validating imported data.

## Defensive takeaways
- Never trust imported data even when it contains pre-computed cached values; always regenerate and re-sanitize HTML content during import
- Fix cache invalidation logic to check for actual field names (author_id/project_id) rather than relying on field aliases (author/project)
- Implement whitelist-based validation for cache version fields rather than accepting arbitrary values from imports
- Consider treating all imported Note objects as having invalidated cache to force regeneration
- Add integration tests that specifically verify XSS payloads are sanitized during project import workflows
- Implement Content Security Policy (CSP) headers as defense-in-depth against XSS execution
- Audit all import functionality to identify similar cache bypass patterns in other object types

## Variant hunting
Similar vulnerabilities likely exist in other cached markdown fields throughout GitLab (Issues, Commits, Snippets, Wiki pages). Check import logic for: (1) Other `*_html` cached fields that can be directly set during import, (2) Cache invalidation checks that rely on field names not present in imports, (3) Hard-coded cache version values that can be trivially matched by attackers, (4) Any object type supporting markdown that uses the CacheMarkdownField concern

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link
- T1566: Phishing - Phishing - Email Attachment (project export)
- T1204: User Execution
- T1059: Command and Scripting Interpreter - JavaScript

## Notes
The vulnerability is particularly severe because: (1) Requires no special privileges beyond ability to export/import projects, (2) Affects all users viewing the imported project, (3) Persists in the database, (4) Publicly demonstrable on gitlab.com. The attacker's discovery of the hardcoded cache version value (917504) was the key breakthrough that made this exploitable. This represents a case where defensive layering (sanitization + cache regeneration) should have both been required, but both were bypassable through a single coordinated attack.

## Full report
<details><summary>Expand</summary>

**Summary:**
Some cache invalidation and project import logic issues enable an attacker to import a project with XSS payloads in places like MR discussions and similar places where a Note object exists.

**Description:**
There are basically 3 issues causing the XSS here:
All attributes of Note objects are controllable in `project.json`, for example `note_html` and `cached_markdown_version`.

Now I can control the value of `note_html` to contain my XSS payload, but the problem is that the value of this field is a `CacheMarkdownField`, it's regenerated from the value of `note` during new object creation (when `note_object.note_html_invalidated?` returns true). The next question is how to trick GitLab that the field does not need to be regenerated.

in `app/models/concerns/cache_markdown_field.rb`
```
      define_method(invalidation_method) do
        changed_fields = changed_attributes.keys
        invalidations  = changed_fields & [markdown_field.to_s, *INVALIDATED_BY]
        invalidations.delete(markdown_field.to_s) if changed_fields.include?("#{markdown_field}_html")

        !invalidations.empty? || !cached_html_up_to_date?(markdown_field)
      end
```

There are 2 checks here (also the last 2 issues):
the first one is:
```
        INVALIDATED_BY = %w[author project].freeze
...
        invalidations  = changed_fields & [markdown_field.to_s, *INVALIDATED_BY]
        invalidations.delete(markdown_field.to_s) if changed_fields.include?("#{markdown_field}_html")
```

```
note_object.changed_attributes.keys
=> ["note", "noteable_type", "author_id", "created_at", "updated_at", "project_id", "line_code", "position", "original_position", "note_html", "cached_markdown_version", "change_position", "attachment"]
```

This check is, unfortunately, voided because
+ Neither `author` nor `project` is in the changed_attributes list, but `author_id` and `project_id`
+ `note` is deleted from `invalidations` because `note_html` is also changed
So invalidations is empty.

and the other one is:
```
!cached_html_up_to_date?(markdown_field)
```
It basically checks whether attribute `cached_markdown_version` equals to `latest_cached_markdown_version`
This is really interesting, because I found that `latest_cached_markdown_version` is always 917504 in my GitLab instance (also gitlab.com). Looks like `local_version` is always 0 for at least Notes in MR.

```
  def latest_cached_markdown_version
    @latest_cached_markdown_version ||= (CacheMarkdownField::CACHE_COMMONMARK_VERSION << 16) | local_version
  end

  def local_version
    return local_markdown_version if has_attribute?(:local_markdown_version)

    settings = Gitlab::CurrentSettings.current_application_settings

    if settings.respond_to?(:local_markdown_version)
      settings.local_markdown_version
    else
      0
    end
  end
```

Finally, I could set `note_html` to the XSS payload, and `cached_markdown_version` to the magic number to avoid my payload being overwritten by GitLab. :P


## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1. Create an export of a project with at least 1 discussion in at least 1 merge request.
  1. Modify the project.json, add field `note_html` and `cached_markdown_version`

```
      "notes": [
        {
          "id": 1,
          "note": "interesting note here",
          "note_html": "<img src=\"test\" onerror=\"alert(document.domain)\"></img>html overwritten",
          "cached_markdown_version": 917504,
```

  1. Import the modified project
  1. View the only discussion of the imported project.

## Supporting Material/References:

Check `https://gitlab.com/Nyangawa/xss/merge_requests/1`, you should be able to see a pop-up.

## Impact

This is a typical persistent XSS issue and the link I mentioned above is accessible publicly, so all GitLab users are vulnerable theoretically.

</details>

---
*Analysed by Claude on 2026-05-12*
