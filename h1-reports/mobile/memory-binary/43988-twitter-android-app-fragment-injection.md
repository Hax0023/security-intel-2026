# Twitter Android App Fragment Injection via Exported PreferenceActivity

## Metadata
- **Source:** HackerOne
- **Report:** 43988 | https://hackerone.com/reports/43988
- **Submitted:** 2015-01-16
- **Reporter:** miantaiduo
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Fragment Injection, Intent-based Activity Hijacking, Exported Component Misuse, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
Twitter's WidgetSettingsActivity is exported and extends PreferenceActivity, allowing arbitrary apps to invoke internal fragments via Intent extras. An attacker can specify malicious fragments through the ':android:show_fragment' extra parameter, leading to application crashes and potential arbitrary code execution.

## Attack scenario
1. Attacker crafts malicious Intent targeting com.twitter.android.WidgetSettingsActivity
2. Attacker sets ':android:show_fragment' extra to reference a non-existent or adversarial Fragment class
3. Attacker includes FLAG_ACTIVITY_CLEAR_TASK to manipulate activity stack
4. Twitter application receives Intent and attempts to instantiate specified Fragment without validation
5. Fragment injection causes ClassNotFoundException or instantiation of malicious fragment code
6. Application crashes or executes attacker-controlled fragment logic with Twitter's permissions

## Root cause
WidgetSettingsActivity exports PreferenceActivity without properly validating or restricting which fragments can be instantiated via Intent extras. The activity trusts the ':android:show_fragment' extra parameter to load arbitrary Fragment classes without whitelist validation.

## Attacker mindset
An attacker would exploit this to: (1) DoS the Twitter app repeatedly, (2) escalate to code execution if they can craft a malicious fragment, (3) potentially hijack user workflows by injecting fragments containing phishing UI or data harvesting forms, (4) bypass authentication checks if fragments handle sensitive operations.

## Defensive takeaways
- Never export PreferenceActivity or similar framework activities without explicit fragment whitelist validation
- Implement strict whitelist of allowed Fragment classes that can be dynamically loaded
- Override onIsMultiPane() or validate fragment names against approved list before instantiation
- Use intent-filter restrictions or explicit intent handling rather than exported implicit activities
- Sanitize and validate all Intent extras that influence dynamic class loading
- Consider using non-exported service or explicit intent recipients for internal fragment navigation
- Regularly audit exported components with tools like MobSF or Drozer

## Variant hunting
Search for other exported activities extending PreferenceActivity, ListActivity, or FragmentActivity. Review any activity accepting ':android:show_fragment', ':android:show_fragment_args', or similar dynamic loading extras. Check for custom activities that implement similar fragment instantiation patterns without validation.

## MITRE ATT&CK
- T1190
- T1203
- T1204

## Notes
This is a framework-level vulnerability affecting multiple Android apps using PreferenceActivity pattern. The PoC demonstrates DoS but fragment injection could potentially achieve RCE depending on available fragment implementations. Related to CVE patterns in Android framework documented by IBM Security Intelligence. Fix requires either unexporting the activity or implementing strict fragment class validation.

## Full report
<details><summary>Expand</summary>

com.twitter.android.WidgetSettingsActivity extend PreferenceActivity and export.
By entering the appropriate extra intent can call any of its internal fragment.
So do not export com.twitter.android.WidgetSettingsActivity
（http://securityintelligence.com/new-vulnerability-android-framework-fragment-injection）

POC：(can make app crash)
private void testtwitter(){
        Intent i = new Intent();
        i.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
        i.setClassName("com.twitter.android","com.twitter.android.WidgetSettingsActivity");
        i.putExtra(":android:show_fragment","com.samsung.android.sdk.pen.objectruntime.preload.VideoIntentFragment");
        //i.putExtra("confirmcredentials",false);
        startActivity(i);
	}

</details>

---
*Analysed by Claude on 2026-05-24*
