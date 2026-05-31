# QuickSight Authorization Bypass: Chat Agents Accessible Despite Custom Permissions Denial

## Metadata
- **Source:** HackerOne
- **Report:** 3577145 | https://hackerone.com/reports/3577145
- **Submitted:** 2026-03-04
- **Reporter:** jcow
- **Program:** AWS Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authorization Bypass, Access Control Bypass, Client-Side Security Controls, API Security Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
AWS QuickSight's custom permissions mechanism fails to enforce restrictions on AI Chat agents at the backend level, allowing users to interact with chat agents despite explicit authorization denials. The vulnerability affects all QuickSight roles except Reader, and is exacerbated by a default system chat agent that is always present and predictable.

## Attack scenario
1. Administrator configures custom permissions to deny chat agent access for a user or role in QuickSight
2. Attacker observes that UI components for chat agents are hidden but backend APIs remain accessible
3. Attacker inspects network traffic to identify the backend API endpoints used for chat agent interactions
4. Attacker crafts direct API requests to the chat agent endpoints, bypassing the UI restrictions
5. Attacker uses the default SYSTEM chat agent (always present with predictable resource format) to interact with organizational data
6. Attacker gains unauthorized access to knowledge bases, data sources, and organizational information despite permission restrictions

## Root cause
AWS QuickSight implements authorization controls only at the frontend UI layer by hiding chat agent components, but does not enforce corresponding backend API-level access controls. The custom permissions framework lacks proper validation on API endpoints, allowing direct backend calls to bypass frontend restrictions.

## Attacker mindset
An insider or compromised account holder recognizing that UI-level security controls are insufficient, leveraging browser developer tools and network inspection to discover unprotected backend APIs. The predictable naming of the default SYSTEM agent makes it trivial to target without requiring agent discovery.

## Defensive takeaways
- Implement authorization checks at both frontend and backend layers; never rely solely on UI hiding for security
- Validate all API requests against the same custom permissions framework that controls UI visibility
- Ensure custom permissions are enforced at the API gateway or service entry point, not just in client applications
- Create comprehensive audit logs for all AI Chat agent interactions regardless of authorization state
- Provide granular IAM policy support for QuickSight capabilities instead of relying solely on service-specific custom permissions
- Consider disabling or restricting the default SYSTEM agent programmatically rather than relying on UI controls
- Implement rate limiting and anomaly detection on chat agent APIs to detect unauthorized access patterns
- Use API authentication tokens that respect custom permissions and expire appropriately

## Variant hunting
Search for similar authorization bypass patterns in other AWS QuickSight features (Amazon Q, executive summaries, data actions); examine other AWS services that implement custom permissions frameworks; test whether other hidden UI components lack backend enforcement; investigate if IAM policy denies are properly evaluated alongside custom permissions

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1552 - Unsecured Credentials
- T1526 - Reconnaissance
- T1566 - Phishing

## Notes
Report demonstrates critical gap between documented security capabilities and actual implementation. AWS documentation explicitly states chat agents can be 'completely disabled' but this is false. Only Reader role prevents access but is too restrictive for normal QuickSight usage. No IAM/SCP/policy controls available. Affects 5 out of 6 QuickSight roles. Compliance and audit implications are significant for regulated organizations.

## Full report
<details><summary>Expand</summary>

We found authorization bypass issues with AI Chat agents in AWS Quick Suite (Quicksight).  We discovered that chat agent capabilities cannot be disabled in AWS Quick Suite, allowing users to access and use AI chat agents regardless of authorization settings.  Thus, users can always interact with chat agents despite configuring AWS Quick Suite authorization to explicitly deny access to AI Chat agents.  

Quick Suite offers chat agents defined as "AI-powered conversational interfaces that provide instant access to your organization’s knowledge base."  These agents may have access to data across your organization including access to specific data sources and actions with the capability for contextual experience derived from team or organization data.  (https://aws.amazon.com/quick/chat-agents/)

To manage Quick Suite capabilities, AWS offers "custom permissions" as an authorization mechanism to restrict the functionality that people can access in Amazon Quick Suite.  Custom permissions can be configured for all identity types in Quick Suite (at multiple levels including account for all users, role, and individual user level).   (https://docs.aws.amazon.com/quick/latest/userguide/create-custom-permisions-profile.html)

These custom permissions and restriction of functionality are documented in multiple different places in documentation and in AWS console:

AWS states that these custom permissions can be configured to:

> You can completely disable all chat agent functionality for users, including chatting with the default agent, chatting with custom agents, and creating new agents. This can be done by restricting the Chat agent capability.

███

https://docs.aws.amazon.com/quick/latest/userguide/working-with-agents.html#custom-permissions-chat-agents

Another example states that "Chat functionality is disabled at the system level":

█████████

We found that these custom permissions do not work and were able to continue interacting with AWS Quick Suite chat agents.  Thus, we found authorization bypass in Quick Suite where AI chat agents can always be used regardless of any security setting in Quick Suite (including AWS IAM and Quick Suite Custom Permissions).  What happens is AWS "hides" the front-end components or the UI, but does not appropriately control the back end capabilities.  Thus, by inspecting our network traffic or by leaving UI windows open after custom permissions have been applied - we're able to continue interacting with AI Chat Agents.

Impact is exacerbated since there is always a default system chat agent created by Quick Suite whenever the Quick Suite service is setup, this is standardized by name (SYSTEM) and thus even if no chat agents are created, users can always use an AI chat agent.   Thus, there is no chat agent creation required for someone to bypass authorization and use AI chat agents in Quick Suite.  There is no scenario (outside of severely and broadly limiting functionality for a user to a Reader role) where an administrator can prevent chat agent access.  Therefore, an attacker can easily use the SYSTEM chat agent even if discovery of custom chat agents may be more difficult as the SYSTEM chat agent follows the same predictable resource format.


## Impact

As described by AWS, Quick Suite is a Business Intelligence and Analytics platform that provides unified intelligence across enterprise data sources.  QuickSight's documentation mentions bridging the gap between insights and action, exploring data, taking actions from dashboards, leveraging application integrations while maintaining enterprise-grade security and governance.

This creates audit and compliance gaps for organizations that need to disable chat agent access.

Currently, the only method to restrict granular access to capabilities including AI Agents is to use Custom Permissions.  Custom Permissions are the only control mechanism for certain Quicksight actions including usage of AI Chat agents; AWS IAM cannot restrict chat agent access..  Additionally, AWS IAM cannot be used to restrict access to Quick Suite's AI Agent chat functionality.  SCPs, RCPs, IAM policies, explicit denies, etc cannot be used to restrict access to Quick Suite's AI Agent chat functionality.

There is the ability to assign a different role, but out of all of Quicksight's roles - only the Reader role does not have access to chat agents and is an extremely limited and thus potentially un-utilized role.   The other 5 roles: Reader Pro, Author, Author Pro, Admin, Admin Pro are much more suited towards QuickSuite usage.  The Reader role only has "read-only access to dashboards". They do not have access to generate executive summaries, cannot build stories with Amazon Q, and cannot access Amazon Q in Quick Sight.  Additionally, they cannot create data sources, datasets, analyses, and dashboards.  Thus, this security affects a large population of users as it applies to:
- Reader Pro Users
- Author Users
- Author Pro Users
- Admin Users
- Admin Pro Users

█████████

https://docs.aws.amazon.com/quicksight/latest/APIReference/API_User.html

The ability to restrict the usage of AI Agents is crucial as it could have audit, compliance, and security implications.  Organizations may want or need to restrict the usage of AI Agents, specifically in highly regulated or other industries.  

For example, there's an EU Artificial Intelligence Act that states certain AI systems may not be used in regulated jurisdictions.  In certail sections such as finance or healthcare, GDPR and HIPAA - certain AI use can be off-limits unless strict conditions are met.  This finding impacts frameworks such as NIST SP 800‑53 AC‑3  for Access Enforcement, NIST AI RMF, ISO 42001, among others.

Thus, we see many use cases where organizations may need to disable the usage of AI Chat Agents within Quick Suite.

From our testing, this is broken authorization and not session staleness.  We're able to procure fresh credentials and still see the same authorization bypass for AI Chat Agent usage despite disabling chat agent functionality.  This will be shown in the walkthrough as well.

## Background


### System Chat Agent

By default, Amazon QuickSight comes with a default chat agent.  This system chat agent is automatically created when someone signs up for Quick and is intended as a primary interface for users to interact with their data and perform tasks within the Quick environment.

Documentation here specifies that "Admins can disable chatting with chat agents including the system chat agent using custom permissions."

This agent comes with:
- Large language model (LLM) knowledge chat enabled.
- Access to all spaces, topics, dashboards, knowledge bases, and actions based on user permissions
- Web search capabilities
- File upload in chat capability enabled 


██████

https://docs.aws.amazon.com/quick/latest/userguide/default-assistant.html


### Custom Permissions

Custom Permissions are used to restrict functionality that people can access in Amazon Quick.  These can be configured at the account, role, and user levels for all identity types in Quick.  For chat agents, custom permission profiles can be used to manage granular feature access including the ability to "Restrict all chat agent-related features".

████████

https://docs.aws.amazon.com/quick/latest/userguide/create-custom-permisions-profile.html#parent-capabilities

## Walkthrough

For this, we will need an active Amazon QuickSuite account setup.  In order to do so, we require an AWS Account and an IAM Principal with appropriate permissions to setup. 

### Setup

We're logged in as an AWS IAM Role for now.  This can be done via an AWS IAM User.

1.  Set up Amazon QuickSuite.  We're doing this in one of my personal account (AWS Account # ███).  This can be done via https://us-east-1.quicksight.aws.amazon.com/sn/console/signup.  

I set this up with the following settings (use your own account name and email):
- Account name: ███████
- Email: ██████████
- Region: 

</details>

---
*Analysed by Claude on 2026-05-31*
