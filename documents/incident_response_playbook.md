---
document_id: DOC-IRP-001
title: Incident Response Playbook
department: Site Reliability Engineering
category: Emergency Procedures
version: 2.5
owner: Chief Reliability Officer
last_updated: 2024-03-12
tags:
  - incident-response
  - escalation
  - communication
  - outage
  - emergency-procedures
---

# Incident Response Playbook

## Purpose

The Incident Response Playbook establishes procedures for responding to production incidents at .MDAI. Incidents include system outages, security breaches, data loss, and significant performance degradation affecting customer services. This playbook ensures consistent, rapid response and effective communication during emergencies.

## Scope

This playbook applies to all production incidents impacting customer-facing services. Severity levels from SEV1 (critical) to SEV4 (minor) determine escalation and communication requirements. Incidents in non-production environments follow simplified procedures at team discretion.

## Incident Severity Levels

### SEV1: Critical Outage

Complete service unavailability for all customers or major platform component failure affecting 25%+ of customers.

- **Response Time**: Incident commander on-site (or remote) within 5 minutes
- **Communication**: All-hands page immediately
- **Escalation**: VP of Engineering, CEO, and CFO paged
- **Communication Cadence**: Status updates every 15 minutes until mitigation begins
- **Postmortem**: Mandatory within 24 hours

### SEV2: Major Degradation

Significant performance impact or feature unavailability affecting 10-25% of customers, or any security incident.

- **Response Time**: On-call engineer responds within 15 minutes
- **Communication**: Slack #incidents and support team notified
- **Escalation**: VP of Engineering and incident commander paged
- **Communication Cadence**: Updates every 30 minutes
- **Postmortem**: Scheduled within 48 hours

### SEV3: Moderate Impact

Limited feature degradation or performance issues affecting less than 10% of customers.

- **Response Time**: On-call engineer responds within 30 minutes
- **Communication**: Slack #incidents notification
- **Escalation**: On-call engineer manages, escalates if not resolved in 2 hours
- **Communication Cadence**: Updates every 60 minutes
- **Postmortem**: Optional, summary documented

### SEV4: Minor Issue

Cosmetic issues, customer edge cases, or minimal impact to platform operations.

- **Response Time**: Normal business hours support response
- **Communication**: Support team ticket tracking
- **Escalation**: Engineering manager reviews daily
- **Postmortem**: Not required

## Incident Initiation and Declaration

### How Incidents Are Detected

Incidents may be discovered through:

- Automated alerting via monitoring systems
- Customer reports via support channels
- Employee discovery during testing or operations
- Security team detection of anomalous activity

### Declaring an Incident

Any employee discovering a potential incident must:

1. Post to #incidents Slack channel with subject line: `[INCIDENT DECLARED] SEVERITY: [SEV1-4], Issue Description`
2. Include current observations: affected services, customer count, error rates, logs
3. Provide initial severity assessment
4. Alert on-call incident commander if severity unclear

The on-call incident commander confirms severity classification and activates incident response procedures.

## Incident Command Structure

### Roles and Responsibilities

**Incident Commander (IC)**: Directs response efforts, makes critical decisions, and coordinates all teams. ICs are trained responders listed in PagerDuty rotation.

**Technical Lead**: Leads troubleshooting, identifies root cause, and directs mitigation efforts.

**Customer Communications Lead**: Manages status page updates and customer notifications.

**Scribe**: Documents timeline, key decisions, and actions for postmortem analysis.

For SEV1 incidents, separate individuals fill these roles. SEV2-4 incidents may combine roles based on available resources.

## Escalation and Notification

### On-Call Rotation

On-call engineer rotation is managed via PagerDuty. Rotations include:

- **L1 Engineer**: First responder, handles initial troubleshooting
- **Incident Commander**: On-call IC available 24/7
- **Engineering Manager**: Escalation point for complex issues
- **VP of Engineering**: SEV1 incidents always escalated

On-call handoff occurs at 9 AM PT daily. Outgoing on-call engineer briefs incoming engineer on active issues.

### Escalation Criteria

Escalate to incident commander if:

- Incident not mitigated within 15 minutes
- Root cause not identified within 30 minutes
- Customer communication required
- Any SEV1 or SEV2 incident declared

## Investigation and Mitigation

### Initial Assessment

1. **Verify the incident**: Confirm actual impact via monitoring dashboards and customer reports
2. **Determine scope**: Identify affected services, geographic regions, customer accounts
3. **Assess severity**: Confirm correct severity classification
4. **Establish communication**: Update Slack, page necessary on-call members

### Troubleshooting Approach

1. **Check recent deployments**: Review last 24 hours of code and infrastructure changes via the Deployment Runbook (DOC-DR-001)
2. **Review monitoring data**: Examine error logs, latency metrics, resource utilization
3. **Query application logs**: Search for relevant errors and warning messages
4. **Inspect infrastructure**: Check database replication, queue depths, container health
5. **Verify external dependencies**: Confirm payment processors, SMS providers, third-party APIs operational

### Common Mitigation Actions

**Database Issues**:
- Check for long-running queries blocking operations
- Verify replication lag on read replicas
- Review connection pool exhaustion
- Execute kill-query commands if queries are hung

**Deployment Failures**:
- Execute rollback procedures per Deployment Runbook
- Restore previous stable database schema if migrations caused issues
- Clear application caches if stale data is served

**Security Incidents**:
- Follow Information Security Policy (DOC-ISP-001) breach procedures
- Isolate affected systems from network
- Preserve logs and system state for forensics
- Engage security team immediately for CISO notification

**Third-Party Dependencies**:
- Switch to backup provider if available
- Enable graceful degradation for optional features
- Implement temporary circuit breakers to prevent cascading failures

## Communication During Incidents

### Internal Communication

- **Slack #incidents**: Real-time status and action items
- **Zoom bridge**: Audio/video conference for complex incidents, link posted in Slack
- **War room phone line**: Backup audio bridge for accessibility

### Customer Communication

**Status Page Updates** (status.mdai.com):

- Update every 15 minutes for SEV1 incidents
- Every 30 minutes for SEV2 incidents
- Describe impact clearly, avoid technical jargon
- Provide estimated resolution time if known
- Post resolution confirmation and apology for impact

**Email Notifications**:

- Affected customers receive email when incident exceeds 30 minutes
- Email includes incident summary, workarounds if available
- Customer success team follows up 24 hours post-resolution

### Executive Reporting

- SEV1 incidents: Brief CEO and CFO immediately upon declaration
- Incident duration exceeding 1 hour: Executive update every 30 minutes
- Post-resolution: Executive summary emailed within 2 hours

## Recovery and Validation

### Mitigation Confirmation

Before declaring incident resolved:

1. Verify affected services are returning normal response times
2. Confirm error rates on critical endpoints below baseline + 1%
3. Check database replication lag under 1 second
4. Manually test critical user journeys end-to-end
5. Monitor for 10+ minutes to confirm stability

### Service Restoration Checklist

For each affected service:
- [ ] Application service health checks passing
- [ ] Database queries responding normally
- [ ] Cache layers populated with fresh data
- [ ] Message queues processing backlog
- [ ] External API integrations working
- [ ] Customer reports of issues stopped

### Incident Closure

Incident commander closes incident once:

1. Root cause identified or mitigated
2. Customer communication completed
3. Service monitoring normalized
4. Incident documentation started

Status page is updated to "resolved" and postmortem scheduled.

## Post-Incident Activities

### Blameless Postmortem

Postmortems occur within 24 hours (SEV1) or 48 hours (SEV2) of incident resolution. Attendance includes IC, technical lead, and relevant team members. Discussion covers:

- Incident timeline and key events
- Root cause analysis
- Preventive measures to avoid recurrence
- Process improvements identified

Postmortems are recorded (with sensitive information redacted) and shared with engineering organization.

### Action Items

Each postmortem generates action items tracked in Jira:

- **Immediate** (P1): Critical fixes preventing recurrence, due within 1 week
- **Short-term** (P2): Important improvements, due within 1 month
- **Long-term** (P3): Nice-to-have improvements, due within 3 months

Engineering leadership reviews action item completion in weekly standups.

### Incident Reporting

The Customer Communications Lead compiles incident report including:

- Incident duration and customer impact count
- Root cause summary
- Preventive measures implemented or planned
- Report sent to customer success team and executive staff

## Incident Prevention

### Monitoring and Alerting

Automated alerting prevents incidents by detecting anomalies:

- Error rate spikes on critical endpoints
- API response time degradation
- Database connection pool exhaustion
- Unusual disk space consumption
- Message queue depth growth

Alert tuning occurs after each major incident to reduce false positives.

### Chaos Engineering

Monthly chaos engineering exercises test incident response readiness:

- Simulated database outage scenarios
- Network partition simulations
- Third-party dependency failures
- Load spike scenarios

Exercises validate runbook accuracy and team preparedness.

### Security Incident Response

For security incidents involving data breach or unauthorized access:

1. Follow Information Security Policy breach procedures
2. CISO assumes incident command from operations
3. Law enforcement and regulatory bodies notified per legal requirements
4. Affected customers notified within required timeframes
5. Forensics investigation initiated immediately

## Related Documents

- Information Security Policy (DOC-ISP-001)
- Deployment Runbook (DOC-DR-001)
- Employee Handbook (DOC-EH-001)
- API Documentation (DOC-AD-001)
