---
document_id: DOC-DR-001
title: Deployment Runbook
department: DevOps and Infrastructure
category: Operations and Procedures
version: 3.7
owner: VP of Infrastructure
last_updated: 2024-03-18
tags:
  - deployment
  - infrastructure
  - kubernetes
  - monitoring
  - rollback
---

# Deployment Runbook

## Purpose

The Deployment Runbook provides step-by-step procedures for deploying, monitoring, and rolling back .MDAI platform releases. This document is the authoritative reference for operations and platform engineers performing production deployments.

## Scope

This runbook applies to all production deployments across all environments. This includes application code releases, infrastructure changes, configuration updates, and database migrations. Non-production deployments follow simplified procedures at engineer discretion.

## Pre-Deployment Checklist

### Requirements Validation

Before beginning deployment, verify:

1. All changes pass continuous integration tests in the CI/CD pipeline
2. Code review approved by at least two senior engineers
3. Database migrations tested against production data snapshot
4. Rollback plan documented and validated
5. Change advisory board (CAB) approval for infrastructure changes
6. Customer impact assessment completed

### Access and Permissions

Deployment requires:

- Valid AWS credentials with appropriate IAM permissions
- Kubernetes cluster kubeconfig configured
- Multi-factor authentication enabled on all accounts
- PagerDuty on-call rotation checked to identify incident commander

Deployment credentials are managed through the secrets manager documented in the Information Security Policy (DOC-ISP-001).

## Production Deployment Procedure

### Blue-Green Deployment Strategy

.MDAI uses blue-green deployments to minimize downtime:

1. **Blue Environment**: Current production serving 100% of traffic
2. **Green Environment**: New release staged with identical infrastructure
3. **Cutover**: Traffic switches from blue to green after validation
4. **Retention**: Blue environment maintained for 24 hours enabling fast rollback

### Step-by-Step Deployment

1. **Pre-flight Checks**: Run automated infrastructure validation script
   - Verify all services are running in the green environment
   - Check database connectivity and replication lag
   - Validate external service dependencies (payment processor, SMS provider)

2. **Database Migrations**: Execute required schema changes
   - Migrations run automatically at green environment startup
   - Monitor migration logs for errors
   - Verify data integrity post-migration using validation queries
   - Validate rollback migration script before proceeding

3. **Health Checks**: Run comprehensive health check suite
   - API endpoint availability
   - Database query response times
   - Cache layer connectivity
   - Message queue processing

4. **Smoke Tests**: Execute quick functional validation
   - Create test customer account
   - Ingest sample data via API
   - Execute queries and verify results
   - Retrieve reports and validate formatting

5. **Load Balancer Cutover**: Route traffic to green environment
   - Begin with 10% traffic shift for 5 minutes
   - Monitor error rates and latency metrics
   - Increase to 50% traffic for 10 minutes
   - Shift remaining 40% traffic after validation

6. **Post-Deployment Validation**: Confirm production stability
   - Monitor error rates for 30 minutes
   - Check customer-reported issues in support tickets
   - Validate key metrics against baseline
   - Confirm no unusual resource consumption

### Monitoring During Deployment

Critical metrics are monitored during deployment:

- API response time p99 latency (target: < 500ms)
- Error rate on critical endpoints (target: < 0.5%)
- CPU and memory utilization (target: < 75%)
- Database connection pool utilization (target: < 60%)
- Queue depth for background jobs (target: < 1000)

Alert thresholds are temporarily widened during deployment to avoid false positives. Incident commander maintains dashboards visible throughout the deployment window.

## Rollback Procedures

### Automatic Rollback

Automatic rollback is triggered if:

- Error rate exceeds 5% for 2+ consecutive minutes
- API p99 latency exceeds 2000ms for 3+ consecutive minutes
- Database connection pool exhaustion detected
- Out-of-memory errors on critical services

Automatic rollback reverses traffic to the blue environment within 30 seconds.

### Manual Rollback

Incident commander may initiate manual rollback by:

1. Notifying affected teams via Slack #incidents channel
2. Running: `deployment-cli rollback --environment production --target blue`
3. Monitoring cutover metrics
4. Updating status page for customer communication

Rollback completion is confirmed when 100% of traffic is routed to blue environment and error rates normalize.

### Post-Rollback Analysis

After rollback:

1. Incident commander documents rollback reason and timeline
2. Engineering team analyzes root cause of deployment failure
3. Pre-deployment validation procedures are updated to catch similar issues
4. Blameless postmortem is scheduled within 48 hours

## Configuration and Secrets Management

### Environment Variables

Configuration is managed via AWS Systems Manager Parameter Store:

- `MDAI_ENVIRONMENT`: Deployment environment identifier
- `MDAI_LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `MDAI_ENABLE_FEATURE_FLAG_X`: Feature flag controls

Secrets (API keys, database passwords) are stored in AWS Secrets Manager and rotated every 90 days per the Information Security Policy.

### Feature Flags

Feature flags enable gradual rollout and A/B testing:

- `enable_new_analytics_engine`: Percentage of users seeing new engine
- `enable_webhook_v2`: New webhook implementation
- `maintenance_mode`: Entire platform maintenance

Feature flags are managed in the control plane and updated without redeployment.

## Incident Response During Deployment

If an incident occurs during deployment, procedures defined in the **Incident Response Playbook** (DOC-IRP-001) take precedence. Incident commander assumes control and may override normal deployment procedures to mitigate customer impact.

## Access Control and Audit

Deployment actions are logged in an immutable audit log including:

- Deploying engineer username and timestamp
- Specific files and configuration changes
- Pre and post-deployment metric snapshots
- Approval chain and CAB decisions

Access to production deployment tools requires employee handbook compliance (DOC-EH-001) and valid security clearance.

## Post-Deployment Reporting

Deployment reports are generated and shared with:

- Engineering leadership
- Customer success team (for major features)
- All on-call personnel

Reports include deployment duration, metric changes, and any customer impact.

## Related Documents

- Information Security Policy (DOC-ISP-001)
- Incident Response Playbook (DOC-IRP-001)
- Employee Handbook (DOC-EH-001)
- API Documentation (DOC-AD-001)
