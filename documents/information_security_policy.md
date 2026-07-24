---
document_id: DOC-ISP-001
title: Information Security Policy
department: Security Engineering
category: Security and Compliance
version: 4.1
owner: Chief Information Security Officer
last_updated: 2024-02-28
tags:
  - security
  - access-control
  - data-protection
  - encryption
  - incident-response
---

# Information Security Policy

## Purpose

The Information Security Policy establishes comprehensive security standards to protect .MDAI's critical assets, customer data, and intellectual property. This policy is mandatory for all employees, contractors, and third-party vendors who access company systems or handle sensitive information.

## Scope

This policy applies to all systems, networks, devices, and data managed or utilized by .MDAI. This includes cloud infrastructure, on-premises servers, personal devices accessing corporate networks, and all data in transit or at rest.

## Information Classification

### Classification Levels

.MDAI classifies information into four categories:

**Public**: Information suitable for public release with no restrictions. Examples include marketing materials and published documentation.

**Internal**: Information intended for use within .MDAI only. Examples include internal communications, policies, and non-sensitive operational data.

**Confidential**: Sensitive business information whose disclosure would harm competitive position. Examples include pricing, business plans, and unpublished API documentation.

**Restricted**: Highest classification including customer personal data, payment information, and authentication credentials. Restricted data requires encryption at rest and in transit.

### Handling Requirements by Classification

Restricted data access is limited to employees with documented business justification. All access is logged and monitored. Confidential data may be shared internally with appropriate authorization. Internal and public data have standard access controls.

## Access Control and Authentication

### Multi-Factor Authentication

All employees must enable multi-factor authentication (MFA) for accessing:

- Corporate email and collaboration platforms
- Version control and development systems
- Cloud infrastructure and deployment tools
- Monitoring and logging dashboards

MFA must utilize authenticator apps (TOTP) or hardware security keys. SMS-based MFA is not permitted for sensitive systems.

### Principle of Least Privilege

Access rights are granted based on job function. Access reviews occur quarterly. Managers must certify that direct reports retain appropriate access levels. Access removal follows the offboarding procedures documented in the **Employee Handbook** (DOC-EH-001).

### Password Requirements

- Minimum 16 characters with complexity requirements
- No dictionary words or sequential patterns
- Rotation required annually or upon suspected compromise
- Previous 5 passwords cannot be reused

## Data Protection and Encryption

### Encryption Standards

All Restricted and Confidential data must be encrypted using:

- AES-256 for symmetric encryption
- RSA-4096 or elliptic curve cryptography for asymmetric encryption
- TLS 1.3 for all network communications

Customer data encryption keys are managed by the key management service documented in the **API Documentation** (DOC-AD-001).

### Database Security

Production databases storing customer data must:

- Implement row-level security with customer tenant isolation
- Enable audit logging of all data access and modifications
- Perform encrypted backups stored in geographically separate regions
- Restrict access to database credentials to authorized engineering staff only

### Incident Response Integration

Data breaches or suspected unauthorized access must immediately trigger the **Incident Response Playbook** (DOC-IRP-001). Security team response procedures supersede standard escalation paths during active security incidents.

## Vendor and Third-Party Management

Vendors and contractors accessing company systems or handling customer data must:

- Execute data processing agreements
- Provide evidence of security controls aligned to this policy
- Submit to annual security assessments and audits
- Maintain cyber liability insurance with minimum $5M coverage

Vendor assessments are coordinated with procurement and documented in a vendor registry maintained by the security team.

## Monitoring and Audit

### Logging and Monitoring

All systems maintain comprehensive logs of authentication events, data access, configuration changes, and administrative actions. Logs are retained for a minimum of 90 days and archived for 7 years for compliance purposes.

Security monitoring tools alert on:

- Unusual access patterns or login attempts
- Excessive failed authentication events
- Configuration changes to security settings
- Unauthorized attempts to access restricted data

### Penetration Testing

Annual third-party penetration testing assesses security controls and identifies vulnerabilities. Critical findings must be remediated within 30 days. Penetration test reports are reviewed by the CISO and shared with executive leadership.

## Security Incident Reporting

All employees must report suspected security incidents to security@mdai.com immediately. Incidents include:

- Unauthorized access or suspected compromises
- Exposure of Restricted or Confidential data
- Malware detection on endpoints
- Denial of service events

Failure to report known security issues may result in disciplinary action. The Incident Response Playbook (DOC-IRP-001) defines response procedures and escalation.

## Related Documents

- Employee Handbook (DOC-EH-001)
- API Documentation (DOC-AD-001)
- Incident Response Playbook (DOC-IRP-001)
- Deployment Runbook (DOC-DR-001)
