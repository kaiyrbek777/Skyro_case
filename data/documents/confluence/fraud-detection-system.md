# Fraud Detection System Documentation

**System:** Skyro Fraud Prevention Platform
**Version:** 2.0
**Last Updated:** February 20, 2024
**Owner:** Security & Risk Team

## System Overview

Skyro's fraud detection system uses machine learning and rule-based engines to identify and prevent fraudulent transactions in real-time. The system processes over 10,000 transactions per minute with sub-100ms latency.

## Architecture

### Components

1. **Real-time Detection Engine**
   - Evaluates every transaction
   - Response time: <50ms (p95)
   - Decision: approve, review, decline

2. **ML Risk Scoring Model**
   - XGBoost-based model
   - 350+ features
   - Retrained weekly
   - AUC: 0.94

3. **Rule Engine**
   - 120+ business rules
   - Configurable thresholds
   - A/B testing capability

4. **Manual Review Queue**
   - For medium-risk transactions
   - SLA: 2-hour review time
   - Staff: 15 reviewers (24/7)

## Risk Scoring

### Score Ranges
- **0-30:** Low risk → Auto-approve
- **31-70:** Medium risk → Manual review
- **71-100:** High risk → Auto-decline

### Key Risk Factors

**Device & Behavioral:**
- Device fingerprint match
- IP geolocation consistency
- Velocity checks (transactions per hour/day)
- Browser & OS patterns

**Transaction Patterns:**
- Amount compared to user history
- Merchant category consistency
- Time of day patterns
- Geographic anomalies

**User Account:**
- Account age
- Verification status
- Historical fraud rate
- Email/phone validation

**Network Analysis:**
- Shared device connections
- Linked accounts
- Known fraudster networks

## Rule Examples

### Rule: Velocity Check
```
IF transaction_count_24h > 10 AND account_age_days < 7
THEN risk_score += 25
```

### Rule: Geographic Mismatch
```
IF ip_country != billing_country AND vp n_detected == false
THEN risk_score += 30
```

### Rule: High-Risk Merchant
```
IF merchant_category IN ['crypto', 'gambling', 'adult']
   AND account_age_days < 30
THEN require_manual_review
```

## Fraud Types Detected

### 1. Account Takeover (ATO)
**Indicators:**
- Login from new device/location
- Password reset followed by transaction
- Change in transaction patterns

**Prevention:** Multi-factor authentication, device fingerprinting

### 2. Synthetic Identity Fraud
**Indicators:**
- Newly created SSN
- Inconsistent personal information
- No credit history

**Prevention:** Identity verification, document validation

### 3. Card Testing
**Indicators:**
- Multiple small transactions in rapid succession
- High decline rate
- Sequential card numbers

**Prevention:** Velocity limits, CAPTCHA challenges

### 4. Friendly Fraud (Chargeback Abuse)
**Indicators:**
- High chargeback rate
- Patterns of dispute claims
- Suspicious dispute timing

**Prevention:** Clear communication, detailed transaction logs

## Performance Metrics

### Current Performance (Feb 2024)
- **True Positive Rate:** 87%
- **False Positive Rate:** 2.3%
- **Precision:** 91%
- **Recall:** 87%
- **F1 Score:** 0.89

### Monthly Fraud Statistics
- **Total Transactions:** 3.2M
- **Flagged for Review:** 64,000 (2%)
- **Confirmed Fraud:** 8,500
- **Prevented Loss:** $4.2M
- **Chargebacks:** 0.12% (industry avg: 0.5%)

## Alert System

### Alert Levels

**Critical (P0):**
- Fraud ring detected
- Data breach suspected
- System failure

**High (P1):**
- Unusual spike in fraud rate
- ML model degradation

**Medium (P2):**
- Individual high-risk transaction
- Rule threshold breach

### On-Call Rotation
24/7 coverage with escalation path:
1. On-call analyst (15 min response)
2. Senior analyst (30 min)
3. Risk director (1 hour)

## Model Retraining

### Schedule
- **Full retrain:** Weekly (Sunday 2 AM PST)
- **Incremental update:** Daily
- **Feature engineering:** Bi-weekly

### Data Pipeline
- Training data: Last 90 days
- Positive samples: All confirmed fraud
- Negative samples: Random 10% of legitimate transactions
- Data labeling: 7-day delay for chargeback discovery

## Integration Points

### Upstream Systems
- Payment processing service
- User authentication service
- KYC/AML verification

### Downstream Systems
- Transaction monitoring dashboard
- Manual review queue
- Reporting & analytics
- Chargeback management

## Future Enhancements

**Q2 2024 Roadmap:**
- Implement graph neural network for network analysis
- Add biometric authentication
- Deploy behavioral biometrics
- Enhance cryptocurrency fraud detection
