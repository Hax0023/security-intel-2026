# Permanent Denial of Service via Physical Destruction

## Metadata
- **Source:** HackerOne
- **Report:** 5534 | https://hackerone.com/reports/5534
- **Submitted:** 2014-04-01
- **Reporter:** prakharprasad
- **Program:** Unknown/Generic
- **Bounty:** Unknown
- **Severity:** informational
- **Vuln:** Physical Damage, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
This report describes a permanent denial of service condition where MS DOS 2.0 becomes non-functional after physical destruction via vehicular impact. The vulnerability is not a software defect but rather the inevitable failure of hardware when subjected to extreme physical force.

## Attack scenario
1. Attacker gains physical access to a computer running MS DOS 2.0
2. Attacker obtains a motor vehicle
3. Attacker drives vehicle over the computer hardware
4. Physical destruction of computer components occurs
5. Operating system cannot boot or function
6. Service becomes permanently unavailable

## Root cause
Physical destruction of hardware components. This is not a software vulnerability but rather the expected behavior of computing hardware when subjected to extreme physical force exceeding design parameters.

## Attacker mindset
Satirical or humorous submission highlighting the distinction between actual software vulnerabilities and physical damage. The reporter appears to be testing program boundaries or making a joke about what constitutes a valid security issue.

## Defensive takeaways
- Physical security and access controls are foundational to system security
- Environmental protections and secure facility design prevent hardware destruction
- Bug bounty programs should establish clear criteria distinguishing software vulnerabilities from physical damage
- Severity rating systems should account for attack feasibility and required threat actor resources

## Variant hunting
Similar satirical submissions might describe DoS via fire, submersion in water, electromagnetic pulses, or other physical destruction methods. Organizations should clearly define 'vulnerability' scope in their bug bounty policies.

## MITRE ATT&CK
- T1561 - Disk Wipe
- T1529 - System Shutdown/Reboot

## Notes
This appears to be a non-serious or satirical submission testing the program's screening process. While physically destructive attacks are valid security concerns for critical infrastructure, they fall outside the scope of typical software-focused bug bounty programs. The submission demonstrates why clear vulnerability definitions and scope guidelines are essential for security programs.

## Full report
<details><summary>Expand</summary>

Steps to Reproduce:

1. Install MS DOS 2.0 on a computer 
2. Start your car and run it over that computer. 
3. Now MS DOS would not start. 

Possible Fix: MSDOS owners shouldn't own a car for sake of proper functioning of the operating system


I've attached proof of concept 
 

</details>

---
*Analysed by Claude on 2026-05-24*
