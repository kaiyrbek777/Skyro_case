# Customer Onboarding Flow v2.0

**Product:** Skyro Personal Banking
**Version:** 2.0
**Launch Date:** March 1, 2024
**Product Owner:** Alex Martinez

## Overview

Version 2.0 of our customer onboarding flow reduces time-to-first-transaction from 48 hours to under 20 minutes while maintaining compliance with KYC/AML regulations.

## Key Improvements from v1.0

- ✅ **Instant virtual card** issuance upon signup
- ✅ **Progressive disclosure** - collect information as needed
- ✅ **AI-powered document verification** (replaces manual review)
- ✅ **Gamified progress** indicators
- ✅ **Mobile-first** redesign

## Onboarding Stages

### Stage 1: Account Creation (2 minutes)
**Goal:** Get user into the app quickly

**Required Information:**
- Email address
- Phone number (with SMS verification)
- Password (min 8 characters, complexity requirements)

**Process:**
1. User lands on signup page
2. Enters email and creates password
3. Receives SMS code for phone verification
4. Account created → redirect to app

**Success Criteria:**
- 95% completion rate
- <2 minutes average time

### Stage 2: Profile Setup (3 minutes)
**Goal:** Collect basic personal information

**Required Information:**
- Full legal name
- Date of birth
- Residential address
- Last 4 digits of SSN

**Features:**
- Address autocomplete (Google Places API)
- Real-time validation
- Progress bar (Step 1 of 3)

**Success Criteria:**
- 90% completion rate
- <3 minutes average time

### Stage 3: Identity Verification (5 minutes)
**Goal:** Complete KYC compliance

**Methods Available:**

**Option A: Instant Verification (70% of users)**
- Integration with Plaid/Alloy
- Soft credit check
- Real-time approval
- No document upload needed

**Option B: Document Upload (25% of users)**
- Photo ID (driver's license, passport)
- Selfie for liveness check
- AI-powered OCR and facial matching
- Approval in 5-10 minutes

**Option C: Manual Review (5% of users)**
- Failed automated verification
- Escalated to human reviewers
- 2-4 hour turnaround

**Success Criteria:**
- 85% pass rate for Option A
- 90% accuracy for Option B
- <4 hour review time for Option C

### Stage 4: Funding Setup (5 minutes)
**Goal:** Link external bank account or add funds

**Options:**

**Bank Account Linking:**
- Plaid integration
- Instant micro-deposit verification
- Support for 10,000+ banks

**Debit Card Funding:**
- Instant transfer
- $5 minimum, $500 maximum initial deposit
- Stripe payment processing

**Wire Transfer:**
- For larger amounts
- Instructions provided in-app
- 1-2 business day settlement

**Success Criteria:**
- 75% link external account
- 20% use debit card funding
- $50 average initial deposit

### Stage 5: Activation & First Transaction (5 minutes)
**Goal:** Complete first successful transaction

**Instant Benefits:**
- Virtual card available immediately (after Step 3)
- Physical card ordered (arrives in 5-7 days)
- $5 signup bonus added to account

**Guided First Transaction:**
- Suggested action: Add to digital wallet (Apple Pay/Google Pay)
- Alternative: Make a small purchase
- Tutorial: How to use virtual card

**Success Criteria:**
- 60% activation within 24 hours
- 40% make first transaction within 1 hour

## Progressive Disclosure Strategy

Not all information is collected upfront. Additional details requested when needed:

**Triggered by first transaction >$500:**
- Employment information
- Annual income range

**Triggered by wire transfer:**
- Full SSN
- Additional ID verification

**Triggered by international transaction:**
- Citizenship status
- Tax residency

## Gamification Elements

### Progress Tracking
Visual progress bar with celebrations:
- 🎉 25% - "Great start!"
- 🎉 50% - "Halfway there!"
- 🎉 75% - "Almost done!"
- 🎉 100% - "Welcome to Skyro! Here's $5"

### Onboarding Checklist
Post-signup checklist in app:
- ✅ Link bank account (+$5 bonus)
- ✅ Set up direct deposit (+$25 bonus)
- ✅ Make first transaction
- ✅ Invite a friend (+$10 bonus)
- ✅ Enable notifications

## Error Handling & Drop-off Recovery

### Common Drop-off Points

**Email/SMS verification (15% drop-off):**
- **Recovery:** Resend code button, troubleshooting tips
- **Automation:** Email sent after 10 minutes of inactivity

**Identity verification (20% drop-off):**
- **Recovery:** Live chat support, alternative verification methods
- **Automation:** SMS reminder after 1 hour

**Bank linking (25% drop-off):**
- **Recovery:** Skip option, debit card alternative
- **Automation:** Email with benefits of linking sent next day

### Abandoned Flow Recovery
- **Day 1:** Email reminder with progress saved
- **Day 3:** SMS with exclusive offer
- **Day 7:** Push notification (if app installed)

## Compliance & Security

### KYC/AML Requirements
- OFAC screening (real-time)
- Customer Identification Program (CIP) compliance
- Enhanced due diligence for high-risk customers

### Data Protection
- PII encryption at rest and in transit
- SOC 2 Type II certified
- GDPR and CCPA compliant

### Fraud Prevention
- Device fingerprinting (Fingerprint.js)
- Email/phone risk scoring (IPQS)
- Behavior analytics (Mixpanel)

## A/B Tests & Experiments

### Active Experiments (March 2024)

**Test 1: Sign-up Form Length**
- **Variant A:** Single-page form
- **Variant B:** Multi-step wizard
- **Metric:** Completion rate
- **Status:** Running (50/50 split)

**Test 2: Instant Virtual Card Messaging**
- **Variant A:** "Get your virtual card now!"
- **Variant B:** "Shop online immediately"
- **Metric:** Time-to-first-transaction
- **Status:** Running (50/50 split)

**Test 3: Signup Bonus Amount**
- **Variant A:** $5 bonus
- **Variant B:** $10 bonus
- **Variant C:** $15 bonus
- **Metric:** CAC vs. LTV
- **Status:** Planned for April

## Metrics & KPIs

### Funnel Metrics (Target)
- **Signup start → Account created:** 85%
- **Account created → Profile complete:** 80%
- **Profile complete → ID verified:** 75%
- **ID verified → Funded:** 70%
- **Funded → First transaction:** 60%

**Overall signup → first transaction:** 25% (target: 30% by Q2)

### Time Metrics (Target)
- **Time to account creation:** <2 min
- **Time to ID verification:** <10 min
- **Time to first transaction:** <20 min
- **Time to activation:** <24 hours (60% of users)

## Support & Resources

**User Support:**
- In-app chat
- Help center articles
- Video tutorials
- Phone support (for verification issues)

**Internal Resources:**
- Onboarding dashboard (Mixpanel)
- Drop-off analysis (Amplitude)
- User session recordings (FullStory)
