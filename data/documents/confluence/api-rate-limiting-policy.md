# API Rate Limiting Policy

**Document Type:** Technical Policy
**Version:** 3.1
**Effective Date:** January 1, 2024
**Owner:** Platform Engineering

## Overview

This document defines rate limiting policies for Skyro's public and partner APIs to ensure fair usage, system stability, and optimal performance for all users.

## Rate Limit Tiers

### Free Tier
**Target Audience:** Individual developers, testing, small-scale integrations

- **Requests per minute:** 60
- **Requests per hour:** 1,000
- **Requests per day:** 10,000
- **Concurrent connections:** 5
- **Burst allowance:** 10 requests

### Standard Tier
**Target Audience:** Small to medium businesses

- **Requests per minute:** 300
- **Requests per hour:** 10,000
- **Requests per day:** 100,000
- **Concurrent connections:** 20
- **Burst allowance:** 50 requests
- **Cost:** $99/month

### Premium Tier
**Target Audience:** Large enterprises, high-volume partners

- **Requests per minute:** 1,000
- **Requests per hour:** 50,000
- **Requests per day:** 500,000
- **Concurrent connections:** 100
- **Burst allowance:** 200 requests
- **Cost:** $499/month

### Enterprise Tier
**Target Audience:** Strategic partners, custom agreements

- **Custom limits** based on business needs
- **Dedicated support**
- **SLA guarantees**
- **Contact sales** for pricing

## Endpoint-Specific Limits

Some endpoints have additional restrictions:

### POST /api/v1/payments
- **Additional limit:** 10 requests per second
- **Reason:** High resource consumption, fraud prevention

### POST /api/v1/users/create
- **Additional limit:** 5 requests per minute per IP
- **Reason:** Spam prevention

### GET /api/v1/statements/generate
- **Additional limit:** 20 requests per hour
- **Reason:** CPU-intensive operation

## Rate Limit Headers

All API responses include rate limit information:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1708534800
X-RateLimit-Tier: standard
```

### Header Definitions
- **X-RateLimit-Limit:** Maximum requests allowed in current window
- **X-RateLimit-Remaining:** Requests remaining in current window
- **X-RateLimit-Reset:** Unix timestamp when limit resets
- **X-RateLimit-Tier:** Your current rate limit tier

## Rate Limit Exceeded Response

When rate limit is exceeded, the API returns:

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 45 seconds.",
    "retry_after": 45,
    "tier": "free",
    "upgrade_url": "https://skyro.com/pricing"
  }
}
```

**HTTP Status Code:** 429 Too Many Requests

**Retry-After Header:** Seconds until next allowed request

## Burst Handling

Short bursts above the rate limit are allowed using a token bucket algorithm:

1. Bucket starts full with burst allowance tokens
2. Each request consumes one token
3. Tokens refill at the rate limit per second
4. Requests fail when bucket is empty

**Example:** Standard tier (300 req/min = 5 req/sec)
- Can burst 50 requests immediately
- Then limited to 5 requests per second

## Best Practices

### 1. Respect Rate Limit Headers
Always check `X-RateLimit-Remaining` before making requests.

### 2. Implement Exponential Backoff
```python
def make_request_with_backoff(url):
    max_retries = 3
    base_delay = 1

    for attempt in range(max_retries):
        response = requests.get(url)

        if response.status_code != 429:
            return response

        retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** attempt)))
        time.sleep(retry_after)

    raise Exception("Max retries exceeded")
```

### 3. Batch Requests
Use batch endpoints when available:
- `POST /api/v1/payments/batch` - Up to 100 payments
- `GET /api/v1/transactions/batch` - Up to 50 transaction IDs

### 4. Use Webhooks
Instead of polling, subscribe to webhooks for event-driven updates.

### 5. Cache Responses
Implement caching for frequently accessed, slowly changing data.

## Monitoring & Alerts

### For API Consumers
Monitor your rate limit usage in the developer dashboard:
- Real-time usage graphs
- Historical trends
- Alerts at 80% and 95% of limit

### For Skyro Operations
Internal monitoring for:
- Overall API health
- Abuse detection
- Capacity planning

## Temporary Limit Increases

For special events (product launches, marketing campaigns), contact support 48 hours in advance to request temporary limit increases.

**Requirements:**
- Business justification
- Expected request volume
- Duration needed
- Endpoint details

## IP-Based Throttling

Additional protection against abuse:

- **Failed authentication attempts:** 5 per minute per IP
- **Suspicious patterns:** Automatic temporary block
- **DDoS protection:** Cloudflare-based (separate from API limits)

## Rate Limit Bypass

The following are NOT rate limited:
- Health check endpoint (`GET /health`)
- Webhook delivery confirmations
- Internal service-to-service calls

## Contact & Support

**Questions about rate limits:**
- Email: api-support@skyro.com
- Slack: #api-support
- Documentation: https://docs.skyro.com/api/rate-limits

**Upgrade tier:**
- Visit: https://skyro.com/pricing
- Email: sales@skyro.com
