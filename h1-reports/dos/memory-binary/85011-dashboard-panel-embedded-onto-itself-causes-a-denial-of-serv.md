# Dashboard panel embedded onto itself causes a denial of service

## Metadata
- **Source:** HackerOne
- **Report:** 85011 | https://hackerone.com/reports/85011
- **Submitted:** 2015-08-27
- **Reporter:** jbeta
- **Program:** Phabricator
- **Bounty:** Not awarded (DoS classification)
- **Severity:** medium
- **Vuln:** Infinite Recursion, Denial of Service, Circular Reference
- **CVEs:** None
- **Category:** memory-binary

## Summary
A dashboard panel can be embedded onto itself using Remarkup syntax, creating an infinite recursion loop during rendering. This causes the application to hang or crash when attempting to display the affected panel, which can be embedded in comments to affect multiple views site-wide.

## Attack scenario
1. Attacker creates a new Text Panel in Dashboards, receiving object reference W1
2. Attacker uses Remarkup syntax {W1} to embed the panel reference within the panel itself
3. Attacker saves the panel, triggering recursive rendering logic
4. Phabricator's rendering engine attempts to render W1, which contains {W1}, which contains {W1}...
5. The application chokes under infinite recursion, causing denial of service
6. Attacker embeds this malicious panel in Maniphest comments or other high-visibility locations, breaking task, feed, and homepage views for all users

## Root cause
Phabricator's Remarkup parser and dashboard rendering system does not implement circular reference detection or recursion depth limits when processing panel embeddings. When a panel contains a Remarkup reference to itself, the renderer enters an infinite loop with no base case to terminate recursion.

## Attacker mindset
A resourceful attacker exploiting weak input validation and lack of recursion safeguards. The attacker recognizes that Remarkup syntax allows object references and tests embedding a panel into itself. Upon discovering the DoS vector, they consider amplification through high-visibility placements (comments, dashboards) to maximize disruption across the platform.

## Defensive takeaways
- Implement circular reference detection in Remarkup parser before rendering begins
- Enforce recursion depth limits with configurable maximum nesting levels
- Maintain a rendering context stack to track objects currently being processed and reject self-references
- Add pre-rendering validation to detect and reject panels that reference themselves
- Consider sandboxing panel rendering with timeouts to prevent indefinite hangs
- Implement rate limiting on dashboard/panel creation for users if DoS prevention is resource-constrained
- Add security warnings when Remarkup references are detected within the same object

## Variant hunting
Embed Panel A into Panel B and Panel B into Panel A (mutual recursion)
Create longer recursion chains: W1 → W2 → W3 → W1
Embed panels in other Remarkup contexts (Maniphest descriptions, commit messages, blog posts)
Test with deeply nested legitimate references to find recursion depth limits
Attempt embedding via indirect references or URL manipulation
Check if same vulnerability exists in other Phabricator objects (documents, pastes, etc.)
Test recursive embedding in feed, timeline, and other rendering contexts

## MITRE ATT&CK
- T1190
- T1499
- T1561

## Notes
The submitter acknowledged this may not qualify for bounty due to DoS classification, showing awareness of typical bounty program policies that deprioritize availability issues. The polymorphic impact (affecting multiple views and having post-compromise amplification through comment embedding) makes this higher severity than typical DoS. The 'mongoose' PS reference appears to be an inside joke/reference. This demonstrates the importance of recursive structure validation in templating and rendering engines.

## Full report
<details><summary>Expand</summary>

I know this may not qualify for a bounty since it's a DoS, but I believe you'd rather get sensitive reports through HackerOne rather than Maniphest. (PS: mongoose.)

Steps to reproduce
================
* In Dashboards, create a new **Text Panel** (let's say it would get the object reference `W1` on creation).
* In the **Create New Panel** dialog, embed the panel view onto itself with Remarkup: `{W1}`
* Phabricator should now bravely attempt to render this, and choke.

Impact
======
Significantly disruptive in an install where any user may create a dashboard (I think that's true by default), since they would then be able to embed this eldritch panel in, say, a Maniphest comment, forever ruining rendering for all of task, feed, and likely homepage, views.

</details>

---
*Analysed by Claude on 2026-05-24*
