# Security Policy

## Reporting a vulnerability

If you believe you've found a security vulnerability in Azeroth Herald, please **do not open a public issue**.

Instead, report it privately via [GitHub's private vulnerability reporting](https://github.com/Deetss/AzerothHerald/security/advisories/new), or email the maintainer.

When reporting, include:

- A description of the issue and its potential impact
- Steps to reproduce (proof-of-concept if possible)
- The affected version or commit hash
- Any suggested remediation

We aim to acknowledge reports within 72 hours and provide a fix or mitigation timeline shortly after.

## Scope

This project is a Discord bot. Issues that are in scope:

- Token or credential leakage paths
- Command injection or unsafe handling of external API responses (Raider.IO, Wowhead)
- Discord permission escalation via the bot
- Dependency vulnerabilities in `requirements.txt`

Out of scope:

- Vulnerabilities in Discord itself, Wowhead, or Raider.IO — report those upstream
- Social engineering or Discord server misconfiguration on the operator's side

## Supported versions

Only the `main` branch is actively maintained. Run a recent commit.
