# Multiple Path Disclosure in WordPress Plugins

## Metadata
- **Source:** HackerOne
- **Report:** 9485 | https://hackerone.com/reports/9485
- **Submitted:** 2014-04-24
- **Reporter:** anant
- **Program:** WordPress Plugin Developers (Multiple)
- **Bounty:** None - Informational Report
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Full Path Disclosure (FPD)
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple WordPress plugins expose full filesystem paths through error messages and direct file access, revealing the installation directory structure. While not a critical vulnerability, this represents a deviation from security best practices and could aid attackers in reconnaissance efforts.

## Attack scenario
1. Attacker accesses publicly accessible plugin files or triggers error conditions
2. Server responds with full filesystem paths (e.g., /var/www/html/wpcheck/wp-content/plugins/...)
3. Attacker collects complete directory structure and plugin versions
4. Attacker maps out the WordPress installation layout for targeted exploitation
5. Information is correlated with known plugin vulnerabilities to identify attack vectors
6. Reconnaissance data informs subsequent targeted attacks on identified plugins

## Root cause
Plugin developers failed to implement proper error handling and prevented direct file access. Files lack security headers or direct execution protection, and error messages display absolute file paths instead of generic messages.

## Attacker mindset
Information gathering phase - attackers value reconnaissance data to reduce attack surface uncertainty and identify specific plugin versions for targeted exploitation. Full paths confirm plugin presence and version, enabling precise vulnerability matching.

## Defensive takeaways
- Implement .htaccess rules (deny direct access) or PHP checks (die/exit on direct inclusion) in all plugin files
- Configure error_reporting and display_errors in php.ini to prevent path disclosure in error messages
- Use generic error messages without revealing filesystem paths
- Implement proper exception handling that logs detailed errors server-side while showing sanitized messages to users
- Use define('ABSPATH') constants instead of hardcoded paths
- Regularly audit plugins for information disclosure issues during development
- Set appropriate file permissions and disable directory listing

## Variant hunting
Search for uncaught exceptions in plugin code that may output stack traces with paths
Look for direct file execution via $_GET parameters without guards
Check for error log files exposed in web-accessible directories
Scan for debug files (unit-tests.php, test files) left in production code
Find plugins using require_once() without __FILE__ guards
Identify plugins with verbose error messages in hooks and filters

## MITRE ATT&CK
- T1217 - Browser Information Discovery
- T1592.004 - Gather Victim Host Information: Client Configurations
- T1518.001 - Software Discovery: Security Software Discovery

## Notes
This is a systematic scan of multiple plugins rather than a single vulnerability. Reporter demonstrates good security hygiene by acknowledging WordPress may not classify FPD as critical but correctly identifying it as a best practice violation. The report includes 30+ affected files across 7+ plugins, showing widespread issue. Reporter explicitly states they expect no bounty, indicating genuine security research contribution. Some paths appear truncated in original report.

## Full report
<details><summary>Expand</summary>

Hi Ian,

I have downloaded all the latest version's of plugin's from your wp profile and did a quick check for FPD. I know you may point out that WP does'nt consider it as a issue however i personally for plugin i look at it as a miss on best practice from plugin developers part.

I do not expect a reward for this but informing so that issue could be corrected.

List of FPD spotted (I know some of these you have already stated you may not be able to modify : but putting it out as its not a big risk however its good to know such error exists).

http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/basic-google-maps-placemarks.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/unit-tests.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/front-end-head.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/message.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/meta-address.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/meta-re-abolish-slavery.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/meta-z-index.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/settings-marker-clusterer.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/settings.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/shortcode-bgmp-list-marker.php
 http://localhost/wpcheck/wp-content/plugins/basic-google-maps-placemarks.1.10.3/basic-google-maps-placemarks/views/shortcode-bgmp-map.php
 http://localhost/wpcheck/wp-content/plugins/camptix-network-tools.0.1/camptix-network-tools/camptix-network-tools.php
 http://localhost/wpcheck/wp-content/plugins/camptix-network-tools.0.1/camptix-network-tools/includes/class-camptix-network-attendees-list-table.php
 http://localhost/wpcheck/wp-content/plugins/camptix-network-tools.0.1/camptix-network-tools/includes/class-camptix-network-dashboard-list-table.php
 http://localhost/wpcheck/wp-content/plugins/camptix-network-tools.0.1/camptix-network-tools/includes/class-camptix-network-log-list-table.php
 http://localhost/wpcheck/wp-content/plugins/camptix-network-tools.0.1/camptix-network-tools/network-dashboard.php
 http://localhost/wpcheck/wp-content/plugins/email-post-changes.1.7/email-post-changes/class.email-post-changes.php
 http://localhost/wpcheck/wp-content/plugins/email-post-changes.1.7/email-post-changes/email-post-changes.php
 http://localhost/wpcheck/wp-content/plugins/email-post-changes.1.7/email-post-changes/unified.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-encourage-user-activation.0.1/google-authenticator-encourage-user-activation/bootstrap.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-encourage-user-activation.0.1/google-authenticator-encourage-user-activation/views/force-notice.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-encourage-user-activation.0.1/google-authenticator-encourage-user-activation/views/nag-notice.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-encourage-user-activation.0.1/google-authenticator-encourage-user-activation/views/requirements-error.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-encourage-user-activation.0.1/google-authenticator-encourage-user-activation/views/settings-fields.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-encourage-user-activation.0.1/google-authenticator-encourage-user-activation/views/settings-section.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-per-user-prompt.0.4/google-authenticator-per-user-prompt/bootstrap.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-per-user-prompt.0.4/google-authenticator-per-user-prompt/views/requirements-error.php
 http://localhost/wpcheck/wp-content/plugins/google-authenticator-per-user-prompt.0.4/google-authenticator-per-user-prompt/views/token-prompt.php http://localhost/wpcheck/wp-content/plugins/google-authenticator-encourage-user-activation.0.1/google-authenticator-encourage-user-activation/views/settings-fields.php
 http://localhost/wpcheck/wp-content/plugins/manage-tags-capability.1.1.1/manage-tags-capability/manage_tags_capability.php
 http://localhost/wpcheck/wp-content/plugins/manage-tags-capability.1.1.1/manage-tags-capability/views/meta_box.php
 http://localhost/wpcheck/wp-content/plugins/overwrite-uploads.1.1/overwrite-uploads/bootstrap.php
 http://localhost/wpcheck/wp-content/plugins/overwrite-uploads.1.1/overwrite-uploads/classes/overwrite-uploads.php
 http://localhost/wpcheck/wp-content/plugins/overwrite-uploads.1.1/overwrite-uploads/views/requirements-error.php
 http://localhost/wpcheck/wp-content/plugins/p2-new-post-categories.0.3/p2-new-post-categories/p2-new-post-categories.php
 http://localhost/wpcheck/wp-content/plugins/re-abolish-slavery-ribbon.1.0.4/re-abolish-slavery-ribbon/re-abolish-slavery-ribbon.php
 http://localhost/wpcheck/wp-content/plugins/re-abolish-slavery-ribbon.1.0.4/re-abolish-slavery-ribbon/views/ribbon-markup.php
 http://localhost/wpcheck/wp-content/plugins/re-abolish-slavery-ribbon.1.0.4/re-abolish-slavery-ribbon/views/setting-fields.php
 http://localhost/wpcheck/wp-content/plugins/re-abolish-slavery-ribbon.1.0.4/re-abolish-slavery-ribbon/views/settings.php
 http://localhost/wpcheck/wp-content/plugins/rescue-children-banner.1.0/rescue-children-banner/bootstrap.php
 http://localhost/wpcheck/wp-content/plugins/rescue-children-banner.1.0/rescue-children-banner/views/banner-markup.php
 http://localhost/wpcheck/wp-content/plugins/rescue-children-banner.1.0/rescue-children-banner/views/requirements-not-met.php
 http://localhost/wpcheck/wp-content/plugins/rescue-children-banner.1.0/rescue-children-banner/views/setting-fields.php
 http://localhost/wpcheck/wp-content/plugins/rescue-children-banner.1.0/rescue-children-banner/views/settings.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/bootstrap.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/classes/tagregator.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/classes/tggr-media-source.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/classes/tggr-settings.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/classes/tggr-shortcode-tagregator.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/classes/tggr-source-flickr.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/classes/tggr-source-instagram.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/classes/tggr-source-twitter.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/views/requirements-error.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/views/tggr-settings/page-settings.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/views/tggr-shortcode-tagregator/shortcode-tagregator.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/views/tggr-source-flickr/page-settings-fields.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/views/tggr-source-flickr/page-settings-section-header.php
 http://localhost/wpcheck/wp-content/plugins/tagregator.0.4/tagregator/views/tggr-source-flickr/shortcode-tagrega

</details>

---
*Analysed by Claude on 2026-05-24*
