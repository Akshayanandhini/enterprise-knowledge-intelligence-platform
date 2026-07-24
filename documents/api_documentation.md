---
document_id: DOC-AD-001
title: API Documentation
department: Engineering
category: Technical Reference
version: 5.0
owner: VP of Engineering
last_updated: 2024-03-20
tags:
  - api
  - authentication
  - rate-limiting
  - data-encryption
  - integration
---

# API Documentation

## Purpose

This document provides comprehensive technical specifications for .MDAI REST API. The API enables programmatic access to core platform functionality including data ingestion, query execution, and analytics retrieval. All API integrations must comply with security and compliance requirements defined in the Information Security Policy (DOC-ISP-001).

## Scope

This documentation covers API v2.5, the current production version. API v1.0 and v2.0 are deprecated as of March 2024 and will be decommissioned June 2024. All customers must migrate to v2.5 before the deprecation deadline.

## Authentication and Authorization

### API Key Management

All requests must include a valid API key in the Authorization header:

```
Authorization: Bearer <api_key>
```

API keys are issued per customer account and rotated annually. Compromised keys must be revoked immediately by contacting security@mdai.com. Disabled keys are archived but cannot be reactivated.

### OAuth 2.0 Integration

Customers integrating with third-party platforms may use OAuth 2.0 with the following flow:

1. Customer redirects end-user to `https://auth.mdai.com/oauth/authorize`
2. User authenticates and grants permissions
3. .MDAI redirects with authorization code
4. Customer backend exchanges code for access token

Access tokens expire after 3600 seconds. Refresh tokens remain valid for 90 days. OAuth credentials are managed in the customer dashboard and require MFA verification for changes.

### Token Scope Restrictions

API keys and OAuth tokens inherit scope from the customer account. Scopes include:

- `data:read` - Read access to ingested data
- `data:write` - Create and modify data ingestion
- `queries:execute` - Run analysis queries
- `reports:generate` - Create and schedule reports
- `admin:account` - Manage team members and billing (admin only)

## Rate Limiting and Quotas

### Standard Rate Limits

All customers have the following default rate limits:

- 100 requests per minute for data queries
- 10 requests per minute for data ingestion
- 5 concurrent requests per API key

Enterprise customers may request higher limits via support. Exceeding limits results in HTTP 429 responses with Retry-After headers.

### Monthly API Call Quotas

Quotas reset on the first of each month at 00:00 UTC:

- Starter tier: 100,000 API calls
- Professional tier: 1,000,000 API calls
- Enterprise tier: Unlimited (subject to rate limits)

Reaching 80% quota triggers a warning email. At 100% quota, subsequent requests are rejected until the next billing cycle.

## Request and Response Formats

### Request Structure

All requests must include Content-Type: application/json header. Request bodies must contain valid JSON. Maximum request payload size is 10MB.

Example request:
```
POST /api/v2.5/data/ingest
Authorization: Bearer api_key_xyz
Content-Type: application/json

{
  "dataset_id": "ds_123",
  "records": [
    {
      "timestamp": "2024-03-20T10:00:00Z",
      "metrics": {"cpu_usage": 45.2}
    }
  ]
}
```

### Response Structure

All responses include standard fields:

- `status`: "success", "error", or "partial"
- `data`: Response payload (null on errors)
- `error`: Error details including code and message
- `request_id`: Unique identifier for request tracing
- `timestamp`: Server-generated response time

HTTP status codes follow REST conventions:
- 200: Successful request
- 201: Resource created
- 400: Invalid request
- 401: Authentication failure
- 403: Insufficient permissions
- 429: Rate limit exceeded
- 500: Server error

## Data Encryption and Security

### Encryption in Transit

All API communications use TLS 1.3 with AES-256 encryption. Endpoints without TLS are not available. Customers must validate SSL certificates.

### Encryption at Rest

Customer data stored via API is encrypted using AES-256 with encryption keys managed by the Key Management Service (KMS). Customers may optionally provide their own encryption keys via the KMS configuration endpoint. Key rotation occurs automatically every 90 days.

### Sensitive Data Handling

API responses containing sensitive fields (e.g., authentication tokens, passwords) are redacted by default. Customers must explicitly request unredacted responses via the `include_sensitive=true` query parameter. Such requests are logged and audited per the Incident Response Playbook (DOC-IRP-001).

## Webhook Integration

### Webhook Configuration

Customers may subscribe to events via webhooks. Webhook endpoints must:

- Return HTTP 2xx status within 30 seconds
- Accept JSON payloads with Content-Type: application/json
- Support event signature verification using HMAC-SHA256

### Supported Events

- `data.ingested`: New data records received
- `query.completed`: Analysis query finished executing
- `api_key.rotated`: API key rotation occurred
- `alert.triggered`: Monitoring alert activated

Webhooks are retried up to 5 times with exponential backoff if the endpoint fails. Failed deliveries are logged and accessible via the webhook dashboard.

## Pagination and Data Retrieval

### Cursor-Based Pagination

Large result sets are paginated using cursor-based navigation:

```
GET /api/v2.5/data/query?limit=100&cursor=next_page_token
```

The response includes a `next_cursor` field for fetching subsequent pages. `limit` parameter accepts values from 10 to 10,000 (default: 100).

## Error Handling and Debugging

### Common Error Codes

- `INVALID_API_KEY`: Provided API key does not exist or is disabled
- `RATE_LIMIT_EXCEEDED`: Request rate limit or quota exceeded
- `INSUFFICIENT_SCOPE`: API key lacks required permissions
- `INVALID_REQUEST`: Request format does not match specification
- `INTERNAL_SERVER_ERROR`: Unexpected server error

### Request Tracing

All error responses include a `request_id` for debugging. Customers experiencing persistent errors should contact support@mdai.com with the request ID and relevant timestamps.

## API Deprecation Policy

API versions are supported for 12 months following a major release. Deprecation notices appear in response headers 6 months before decommissioning. Customers must migrate to current versions before support ends.

## Related Documents

- Information Security Policy (DOC-ISP-001)
- Incident Response Playbook (DOC-IRP-001)
- Deployment Runbook (DOC-DR-001)
