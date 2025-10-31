# Skyro Infrastructure & Architecture

**Team:** Platform Engineering
**Owner:** Kevin Patel (VP of Infrastructure)
**Last Updated:** February 25, 2024
**Version:** 3.0

## Architecture Overview

Skyro operates a cloud-native microservices architecture hosted on AWS, designed for high availability, scalability, and security.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  Web App (React) | iOS App (Swift) | Android App (Kotlin)       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CDN LAYER                                │
│                    CloudFront + WAF                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│         Kong API Gateway + Rate Limiting + Auth                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MICROSERVICES LAYER                           │
│                     (EKS Kubernetes)                             │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐              │
│  │  Auth      │  │  Accounts  │  │  Transactions│              │
│  │  Service   │  │  Service   │  │  Service     │              │
│  └────────────┘  └────────────┘  └──────────────┘              │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐              │
│  │  Cards     │  │  Payments  │  │  Fraud       │              │
│  │  Service   │  │  Service   │  │  Detection   │              │
│  └────────────┘  └────────────┘  └──────────────┘              │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐              │
│  │  KYC/AML   │  │  Notifications│ │  Analytics  │              │
│  │  Service   │  │  Service   │  │  Service     │              │
│  └────────────┘  └────────────┘  └──────────────┘              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│  PostgreSQL (RDS) | Redis (ElastiCache) | S3 (Storage)         │
│  Kafka (MSK) | Elasticsearch | Data Warehouse (Snowflake)      │
└─────────────────────────────────────────────────────────────────┘
```

## Core Services

### 1. Auth Service
**Tech Stack:** Node.js, Express, Redis
**Purpose:** User authentication, session management, OAuth

**Key Features:**
- JWT token generation and validation
- Multi-factor authentication (MFA)
- OAuth 2.0 / OpenID Connect
- Session management with Redis
- Biometric authentication support

**Scalability:** Auto-scales 5-50 pods based on CPU (target: 70%)
**SLA:** 99.99% uptime

### 2. Accounts Service
**Tech Stack:** Java Spring Boot, PostgreSQL
**Purpose:** Account management, balance tracking

**Key Features:**
- Account CRUD operations
- Balance management (real-time updates)
- Account statements generation
- Interest calculation
- Account closure workflows

**Database:** PostgreSQL (RDS Multi-AZ)
- Read replicas: 3
- Backup retention: 30 days
- Automated failover: <60 seconds

**Scalability:** Auto-scales 10-100 pods
**SLA:** 99.95% uptime

### 3. Transactions Service
**Tech Stack:** Go, PostgreSQL, Kafka
**Purpose:** Transaction processing, ledger management

**Key Features:**
- Double-entry bookkeeping
- Transaction authorization
- Transaction history
- Real-time balance updates
- Idempotency handling

**Performance:**
- Peak throughput: 10,000 TPS
- P95 latency: <100ms
- P99 latency: <200ms

**Data Flow:**
```
Client → API Gateway → Transactions Service → Kafka Topic
                                            ↓
                         [Fraud Service, Analytics, Notifications]
```

### 4. Payments Service
**Tech Stack:** Python (FastAPI), PostgreSQL, Celery
**Purpose:** Payment processing, gateway integration

**Key Features:**
- Payment gateway orchestration (Stripe, Adyen, PayPal)
- ACH transfers
- Wire transfers
- International payments (SWIFT, SEPA)
- Payment status tracking
- Webhook handling

**Async Processing:**
- Celery workers for long-running tasks
- Redis as message broker
- Retry logic with exponential backoff

**Scalability:**
- API pods: 15-75 (auto-scale)
- Celery workers: 20-100 (auto-scale)

### 5. Fraud Detection Service
**Tech Stack:** Python, TensorFlow, PostgreSQL, Redis
**Purpose:** Real-time fraud detection and prevention

**Key Features:**
- ML-based risk scoring
- Rule engine (120+ rules)
- Velocity checks
- Device fingerprinting
- Geographic anomaly detection
- OFAC screening

**Performance:**
- Scoring latency: <50ms (p95)
- Model retraining: Weekly (automated)
- AUC: 0.94

**ML Pipeline:**
```
Training Data (90 days) → Feature Engineering → Model Training
                                                      ↓
                                    Model Registry (MLflow)
                                                      ↓
                             Production Deployment (TensorFlow Serving)
```

### 6. Cards Service
**Tech Stack:** Java Spring Boot, PostgreSQL
**Purpose:** Card issuance, management, transaction authorization

**Key Features:**
- Virtual card issuance (instant)
- Physical card ordering
- Card controls (freeze, limits, restrictions)
- Card tokenization (Apple Pay, Google Pay)
- Authorization decisions (approve/decline)

**Integration:**
- Card processor: Marqeta API
- Tokenization: Visa Token Service

### 7. KYC/AML Service
**Tech Stack:** Python, PostgreSQL, Airflow
**Purpose:** Customer verification, compliance monitoring

**Key Features:**
- Identity verification (Alloy, Plaid)
- Document verification
- OFAC screening (Dow Jones)
- Ongoing monitoring
- SAR generation
- Compliance reporting

**Batch Jobs (Airflow):**
- Daily OFAC screening
- Weekly model retraining (fraud)
- Monthly compliance reports

### 8. Notifications Service
**Tech Stack:** Node.js, Kafka, SNS, SendGrid, Twilio
**Purpose:** Multi-channel notifications

**Channels:**
- Push notifications (FCM, APNS)
- Email (SendGrid)
- SMS (Twilio)
- In-app notifications
- Webhooks

**Event-Driven:**
- Consumes events from Kafka
- Templates stored in S3
- Personalization engine
- Delivery tracking and analytics

## Data Infrastructure

### Databases

**PostgreSQL (Amazon RDS)**
- **Version:** 15.4
- **Instance Type:** db.r6g.2xlarge (8 vCPU, 64 GB RAM)
- **Deployment:** Multi-AZ for HA
- **Read Replicas:** 3 (different AZs)
- **Backup:** Automated daily, 30-day retention
- **Encryption:** At-rest (KMS), in-transit (SSL)

**Schemas:**
- `accounts` - Account data
- `transactions` - Transaction ledger
- `users` - User profiles
- `cards` - Card information
- `compliance` - KYC/AML data

**Redis (Amazon ElastiCache)**
- **Version:** 7.0
- **Node Type:** cache.r6g.large
- **Deployment:** Cluster mode (3 shards, 2 replicas each)
- **Use Cases:**
  - Session storage
  - Rate limiting
  - Caching (account balances, user profiles)
  - Pub/Sub (real-time notifications)

**Elasticsearch (Amazon OpenSearch)**
- **Version:** 2.5
- **Cluster:** 6 nodes (3 masters, 3 data)
- **Storage:** 2 TB
- **Use Cases:**
  - Transaction search
  - Audit logs
  - Application logs
  - Metrics visualization (Kibana)

### Messaging & Streaming

**Apache Kafka (Amazon MSK)**
- **Version:** 3.4
- **Cluster:** 6 brokers across 3 AZs
- **Topics:** 50+
- **Throughput:** 100 MB/s peak
- **Retention:** 7 days (most topics), 90 days (audit logs)

**Key Topics:**
- `transactions.created`
- `transactions.updated`
- `payments.events`
- `fraud.alerts`
- `user.events`
- `notifications.dispatch`

### Storage

**Amazon S3**
- **Buckets:**
  - `skyro-documents` - User-uploaded documents (encrypted)
  - `skyro-statements` - Monthly statements
  - `skyro-backups` - Database backups
  - `skyro-logs` - Application logs (lifecycle: 90 days)
  - `skyro-data-lake` - Analytics data warehouse

**Lifecycle Policies:**
- Transition to Glacier after 90 days
- Delete after 7 years (regulatory requirement)

## Container Orchestration

**Amazon EKS (Kubernetes)**
- **Version:** 1.28
- **Node Groups:**
  - General: 20-100 nodes (c6i.2xlarge)
  - Memory-intensive: 5-20 nodes (r6i.2xlarge) for ML
  - GPU: 2-5 nodes (g4dn.xlarge) for ML training

**Deployment Strategy:**
- Blue-green deployments (zero downtime)
- Canary releases (5% → 25% → 50% → 100%)
- Automatic rollback on error rate spike

**Service Mesh:** Istio
- Traffic management
- Load balancing
- mTLS between services
- Observability

## Networking

**VPC Configuration:**
- **Regions:** us-east-1 (primary), us-west-2 (DR)
- **Subnets:**
  - Public (3 AZs) - Load balancers, NAT gateways
  - Private (3 AZs) - Application servers
  - Database (3 AZs) - RDS, ElastiCache

**Security Groups:**
- Least privilege principle
- Application tier: Only from ALB
- Database tier: Only from application tier

**Load Balancing:**
- Application Load Balancer (ALB) for HTTP/HTTPS
- Network Load Balancer (NLB) for TCP traffic
- Cross-zone load balancing enabled

## Monitoring & Observability

### Metrics
**Prometheus + Grafana**
- 200+ custom metrics
- 50+ dashboards
- Infrastructure metrics (CPU, memory, disk)
- Application metrics (latency, error rate, throughput)
- Business metrics (transactions/min, signups, revenue)

### Logging
**ELK Stack (Elasticsearch, Logstash, Kibana)**
- Centralized logging for all services
- 10 TB daily log volume
- 90-day retention
- Full-text search

### Tracing
**Jaeger (distributed tracing)**
- End-to-end request tracing
- Performance bottleneck identification
- Dependency mapping

### Alerting
**PagerDuty + Slack**
- On-call rotation (24/7)
- Escalation policies
- Alert fatigue reduction (deduplication, correlation)

**Key Alerts:**
- Error rate >1%
- API latency p95 >500ms
- Database CPU >80%
- Disk space <20%
- Failed deployments

## Security

### Encryption
- **At-rest:** All databases encrypted (AES-256)
- **In-transit:** TLS 1.3 for all external connections, mTLS for internal
- **Application:** Sensitive data encrypted at application layer (KMS)

### Access Control
- **IAM:** Least privilege, role-based access
- **MFA:** Required for all production access
- **Bastion Host:** Required for SSH access (no direct access)
- **Audit Logging:** CloudTrail for all AWS API calls

### Secrets Management
- **HashiCorp Vault** (migrating from AWS Secrets Manager)
- Automatic secret rotation (90 days)
- Secrets injected at runtime (not in code/config)

### Compliance
- **PCI DSS Level 1** (certified)
- **SOC 2 Type II** (certified)
- **GDPR** compliant
- **CCPA** compliant

## Disaster Recovery

### Backup Strategy
- **Databases:** Automated daily backups, 30-day retention
- **Cross-region replication:** Real-time replication to us-west-2
- **Point-in-time recovery:** Up to 35 days

### RTO & RPO
- **Recovery Time Objective (RTO):** 4 hours
- **Recovery Point Objective (RPO):** 15 minutes

### DR Drills
- Quarterly DR drills
- Documented runbooks
- Last drill: January 15, 2024 (successful, RTO: 2.5 hours)

## Performance Benchmarks

**Current Performance (Feb 2024):**
- **Uptime:** 99.97% (target: 99.95%)
- **API Latency (p95):** 342ms (target: <500ms)
- **API Latency (p99):** 1,024ms (target: <2s)
- **Throughput:** 8,500 req/sec peak (capacity: 15,000 req/sec)
- **Error Rate:** 0.08% (target: <0.1%)

## Cost Optimization

**Monthly AWS Spend:** $180,000

**Breakdown:**
- Compute (EKS, EC2): $75,000 (42%)
- Databases (RDS, ElastiCache): $45,000 (25%)
- Storage (S3, EBS): $18,000 (10%)
- Data Transfer: $22,000 (12%)
- Other (CloudFront, MSK, etc.): $20,000 (11%)

**Optimization Initiatives:**
- Reserved Instances: 60% coverage (saves 30%)
- Spot Instances: 20% of compute (saves 70% on those)
- S3 lifecycle policies: $5K/month savings
- Right-sizing: Ongoing (10% savings identified)

## Roadmap (2024)

**Q2:**
- ✅ Complete Vault migration (secret management)
- 🔄 Implement service mesh (Istio)
- 📝 Multi-region active-active (eliminate DR failover)

**Q3:**
- Database sharding (horizontal scaling)
- GraphQL API gateway
- Chaos engineering (Gremlin)

**Q4:**
- Serverless migration (selected services)
- Edge computing (Lambda@Edge)
- ML inference optimization (GPU → Inferentia)

## Contacts

**Team:**
- VP Infrastructure: Kevin Patel (kevin.patel@skyro.com)
- SRE Lead: Marcus Johnson (marcus.johnson@skyro.com)
- Security Lead: Tom Chen (tom.chen@skyro.com)

**Slack Channels:**
- #infrastructure
- #incidents
- #on-call

**Oncall:** PagerDuty rotation (24/7)
