# Creating Your Own Telegram Bot For Recon Bug Bounty

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** N/A
- **Bounty:** N/A
- **Severity:** INFORMATIONAL
- **Vuln types:** Submitted by:Santosh bobade
- **Category:** uncategorised
- **Writeup:** https://santoshdbobade.medium.com/creating-your-own-telegram-bot-for-recon-bug-bounty-8c3fd3dfcbcf

## Summary
This article is a tutorial on setting up a Telegram bot for security reconnaissance purposes, not a vulnerability disclosure. It provides step-by-step instructions for configuring the 'notify' tool to send reconnaissance findings (e.g., subdomain enumeration results) directly to a Telegram chat, enabling automated notifications during bug hunting workflows.

## Attack scenario (step by step)
1. Attacker installs Go language and the notify tool from ProjectDiscovery
2. Attacker creates a Telegram bot via BotFather and extracts the API token and chat ID
3. Attacker configures provider-config.yaml with telegram credentials in ~/.config/notify/
4. Attacker copies the notify binary to /usr/local/bin for system-wide access
5. Attacker runs reconnaissance tools like subfinder piped to notify: 'subfinder -d target.com | notify'
6. Attacker receives automated Telegram messages with reconnaissance results for faster analysis

## Root cause
Not applicable - this is a tool configuration guide, not a vulnerability report. The article demonstrates legitimate use of automation in security testing workflows.

## Attacker mindset
Efficiency-focused reconnaissance operator seeking to streamline information gathering during bug bounty campaigns by automating result notifications through Telegram, reducing manual monitoring of command outputs.

## Defensive takeaways
- Monitor for suspicious Telegram bot creation and API token usage on systems
- Audit ~/.config/notify/ and similar tool configuration directories for unauthorized bot credentials
- Implement API rate limiting on reconnaissance tool outputs and Telegram integrations
- Log and alert on execution of reconnaissance tools (subfinder, notify) in environments
- Review Telegram bot activity logs for unauthorized data exfiltration via reconnaissance result notifications
- Restrict installation of ProjectDiscovery tools and similar reconnaissance frameworks in production environments

## Variant hunting
Search for similar integration tutorials involving cloud messaging services (Slack, Discord webhooks), alternative notification systems, or automation frameworks combined with reconnaissance tools. Look for other ProjectDiscovery tool integrations with external notification channels.

## MITRE ATT&CK
- T1592 - Gather Victim Information
- T1589 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information
- T1046 - Network Service Discovery
- T1598 - Phishing for Information

## Notes
This is educational content demonstrating reconnaissance workflow optimization, not a bug bounty writeup disclosing a vulnerability. The article contains incomplete token examples (redacted with X's) showing proper security practice in publishing. Relevant for understanding attacker tooling and automation practices in reconnaissance phases of attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
