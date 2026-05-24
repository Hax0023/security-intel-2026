# Slowvote and Countdown Recursive Inclusion DoS

## Metadata
- **Source:** HackerOne
- **Report:** 1563142 | https://hackerone.com/reports/1563142
- **Submitted:** 2022-05-09
- **Reporter:** dyls
- **Program:** Mongoose (HackerOne)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Infinite Recursion, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Denial of Service vulnerability exists in Slowvote and Countdown objects where including an object's own ID in its description field causes infinite recursive inclusion, preventing page loads. The vulnerability can be amplified by embedding the affected object in other objects or the feed to disable the entire home page.

## Attack scenario
1. Attacker identifies a Slowvote or Countdown object with a specific ID
2. Attacker edits the object and includes its own object ID in the description field
3. The rendering engine attempts to process the description and encounters a recursive reference
4. The system infinitely includes the object within itself, consuming resources
5. The page fails to load due to infinite recursion or timeout
6. Attacker optionally embeds the poisoned object in the feed to disable the home page for all users

## Root cause
The application lacks proper validation to detect and prevent self-referential object inclusions. The rendering engine does not check for circular dependencies before processing object references in description fields, allowing a object to include itself recursively without termination conditions.

## Attacker mindset
An attacker seeks to cause widespread service disruption with minimal effort. By poisoning a single object with a self-reference, they can leverage the application's object embedding features to cascade the DoS across multiple pages, including high-traffic areas like the home feed, maximizing impact.

## Defensive takeaways
- Implement circular dependency detection before rendering objects with embedded references
- Validate that an object cannot reference itself directly or indirectly in any field
- Use a visited set or recursion depth limit during object inclusion/rendering
- Sanitize and validate all user input that can affect object relationships
- Implement proper error handling for infinite loops with graceful degradation
- Add automated tests for self-referential object scenarios
- Consider using a whitelist approach for allowed object references
- Monitor and log suspicious object modification patterns

## Variant hunting
Check other objects that support embedding/inclusion features for similar recursive vulnerabilities
Test if circular chains (A includes B, B includes A) also cause DoS
Verify if indirect self-references through multiple objects are properly handled
Examine other description/content fields that might support object references
Test embedding in comments, replies, or other user-generated content fields
Investigate if the vulnerability affects API responses or only UI rendering

## MITRE ATT&CK
- T1499
- T1498

## Notes
This is a follow-up to a similar issue (#85011), indicating a systemic pattern of improper recursion handling in the application. The reference to mongoose suggests this is a MongoDB-based application. The vulnerability is particularly severe when the affected object can be embedded in widely-viewed content like the feed.

## Full report
<details><summary>Expand</summary>

Similar to #85011, if you edit a Slowvote or Countdown object and include its own object ID in the description, then it will recursively include and prevent the page from loading.

mongoose

## Impact

Denial of Service. You can include the Slowvote or Countdown object on any other object to also prevent it from loading. If it is included in the feed, you could also prevent the home page from loading.

</details>

---
*Analysed by Claude on 2026-05-24*
