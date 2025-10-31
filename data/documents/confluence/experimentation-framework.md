# Experimentation & A/B Testing Framework

**Owner:** Growth & Data Science Team
**Last Updated:** February 12, 2024
**Version:** 1.5

## Overview

Skyro's experimentation framework enables data-driven product decisions through rigorous A/B testing and multivariate experiments. This document outlines our process, tools, and best practices.

## Experimentation Platform

### Tools
- **Primary:** Optimizely
- **Analytics:** Amplitude (event tracking)
- **Metrics Dashboard:** Looker
- **Statistical Analysis:** Python (scipy, statsmodels)

### Integration Points
- Web app (React)
- Mobile apps (iOS/Android native)
- Backend API (feature flags)
- Email campaigns (SendGrid)

## Experiment Lifecycle

### 1. Hypothesis Formation

**Template:**
```
We believe that [change] will result in [outcome] because [rationale].

We will measure success using [metric] and expect to see [X% improvement].
```

**Example:**
```
We believe that showing social proof on the signup page will increase
conversion rate because users trust recommendations from others.

We will measure success using signup conversion rate and expect to see
a 15% improvement.
```

### 2. Experiment Design

**Required Elements:**
- **Hypothesis:** Clear, testable prediction
- **Primary Metric:** One key metric to optimize (e.g., conversion rate)
- **Secondary Metrics:** Supporting metrics (e.g., time on page, bounce rate)
- **Guardrail Metrics:** Metrics that should NOT degrade (e.g., page load time)
- **Target Audience:** Who will see the experiment
- **Traffic Allocation:** Percentage split (typically 50/50)
- **Duration:** How long to run (minimum 1 week)
- **Sample Size:** Calculated to achieve statistical significance

**Sample Size Calculator:**
```
Required users per variant = (Z_α/2 + Z_β)² × 2 × p × (1-p) / (MDE)²

Where:
- Z_α/2 = 1.96 (for 95% confidence)
- Z_β = 0.84 (for 80% power)
- p = baseline conversion rate
- MDE = minimum detectable effect (typically 5-10%)
```

### 3. Implementation

**Development Process:**
1. Create feature flag in Optimizely
2. Implement variation code with flag checks
3. Add event tracking for all metrics
4. QA test both variations
5. Launch to 5% of users (smoke test)
6. If stable, ramp to full traffic allocation

**Code Example:**
```javascript
// React component
import { useExperiment } from '@optimizely/react-sdk';

function SignupPage() {
  const [variation, clientReady] = useExperiment('signup_social_proof');

  return (
    <div>
      {variation === 'control' && <ControlSignup />}
      {variation === 'treatment' && <TreatmentSignup />}
    </div>
  );
}
```

### 4. Monitoring

**Daily Checks:**
- Sample size progress
- Metric trends
- Statistical significance
- Technical errors (data quality)

**Alerts:**
- Significant degradation in guardrail metrics
- Data collection failures
- Sample ratio mismatch (SRM)

### 5. Analysis & Decision

**Statistical Criteria:**
- **Confidence Level:** 95% (p-value < 0.05)
- **Statistical Power:** 80%
- **Minimum Runtime:** 1 week (capture weekly patterns)
- **Minimum Sample Size:** Calculated based on MDE

**Decision Framework:**

| Outcome | Action |
|---------|--------|
| Statistically significant win | Ship to 100% |
| Statistically significant loss | Ship control (don't launch) |
| No significant difference | Requires judgment (context matters) |
| Inconclusive (insufficient data) | Extend experiment or redesign |

**Considerations Beyond Stats:**
- Engineering cost to maintain
- Impact on technical debt
- Qualitative user feedback
- Strategic alignment

## Current Active Experiments (Feb 2024)

### EXP-2024-001: Onboarding Progress Bar
**Hypothesis:** Adding a visual progress bar will increase onboarding completion

**Setup:**
- **Control:** No progress indicator
- **Treatment:** Step-by-step progress bar
- **Primary Metric:** Onboarding completion rate
- **Traffic:** 50/50 split
- **Start Date:** Feb 1, 2024
- **Planned End:** Feb 29, 2024
- **Status:** 🟢 Running (55% sample collected)

**Early Results (not significant yet):**
- Control: 67.2% completion
- Treatment: 69.8% completion
- Lift: +2.6 percentage points
- P-value: 0.08 (not yet significant)

### EXP-2024-002: Virtual Card CTA Messaging
**Hypothesis:** Emphasizing "instant" will drive faster activation

**Setup:**
- **Control:** "Get your virtual card"
- **Treatment A:** "Get your card instantly"
- **Treatment B:** "Shop online in seconds"
- **Primary Metric:** Time to first transaction
- **Traffic:** 33/33/33 split
- **Start Date:** Feb 5, 2024
- **Planned End:** Mar 5, 2024
- **Status:** 🟢 Running (40% sample collected)

### EXP-2024-003: Referral Bonus Amount
**Hypothesis:** Higher bonus increases referral rate but need to optimize for LTV

**Setup:**
- **Control:** $5/$5 bonus
- **Treatment A:** $10/$10 bonus
- **Treatment B:** $15/$15 bonus
- **Primary Metric:** Referral conversion rate
- **Secondary:** Cost per acquisition, 6-month LTV
- **Traffic:** 33/33/33 split
- **Start Date:** Feb 12, 2024
- **Planned End:** Mar 12, 2024
- **Status:** 🟢 Running (25% sample collected)

## Past Experiments & Learnings

### EXP-2024-Q1-WIN: Simplified Signup Form
**Result:** ✅ 12% increase in signup conversion

**Change:** Reduced signup form from 8 fields to 3 (email, phone, password)
**Lesson:** Progressive disclosure works - collect information as needed
**Shipped:** January 15, 2024

### EXP-2024-Q1-LOSS: Gamified Spending Insights
**Result:** ❌ 8% decrease in engagement, no impact on retention

**Change:** Added game-like achievements for spending categories
**Lesson:** Users want utility, not gamification in fintech
**Decision:** Did not ship

### EXP-2024-Q1-NEUTRAL: Dark Mode Default
**Result:** ⚪ No significant difference in any metrics

**Change:** Default to dark mode based on system settings vs. always light
**Lesson:** Users appreciate choice but it doesn't move key metrics
**Decision:** Shipped anyway (table stakes feature)

## Best Practices

### Do's ✅
1. **Run one experiment per page/flow** - Avoid interaction effects
2. **Set clear success criteria upfront** - No p-hacking
3. **Wait for statistical significance** - Don't stop early on "good news"
4. **Check for Sample Ratio Mismatch (SRM)** - Indicates implementation issues
5. **Segment analysis** - Mobile vs. Web, new vs. existing users
6. **Document everything** - Future you will thank you

### Don'ts ❌
1. **Don't peek too early** - Multiple testing inflates false positives
2. **Don't ignore guardrail metrics** - A "win" that hurts retention is bad
3. **Don't test too many things at once** - Hard to attribute causality
4. **Don't test without a hypothesis** - "Let's see what happens" rarely works
5. **Don't ignore qualitative data** - Numbers don't tell the whole story
6. **Don't forget about novelty effects** - Some changes work temporarily

## Experiment Prioritization (PIE Framework)

Score experiments 1-10 on:
- **Potential:** How much improvement possible?
- **Importance:** How valuable is this metric?
- **Ease:** How easy to implement?

**PIE Score = (Potential + Importance + Ease) / 3**

Prioritize experiments with highest PIE score.

### Q1 2024 Experiment Backlog

| Experiment | Potential | Importance | Ease | PIE Score | Priority |
|-----------|-----------|------------|------|-----------|----------|
| Instant card activation | 9 | 10 | 7 | 8.7 | 1 |
| Enhanced fraud alerts | 7 | 9 | 8 | 8.0 | 2 |
| Personalized budgeting | 8 | 7 | 6 | 7.0 | 3 |
| Social sharing features | 5 | 4 | 9 | 6.0 | 4 |
| Cryptocurrency integration | 10 | 3 | 2 | 5.0 | 5 |

## Velocity Metrics

**Target:** 8-10 experiments per quarter

**Q1 2024 Results:**
- Experiments launched: 12
- Wins (shipped): 5
- Losses (not shipped): 4
- Neutral (judgment call): 3
- Win rate: 42%

## Tools & Resources

**Internal:**
- Experiment tracker: [Airtable link]
- Results dashboard: [Looker link]
- Optimizely admin: [app.optimizely.com]

**External:**
- Statistical calculator: [evany tools]
- A/B test duration calculator: [optimizely.com/sample-size]
- Reading list: [Trustworthy Online Experiments book]

## Contacts

**Experiment Owners:**
- Growth experiments: Sarah Chen
- Product experiments: Alex Martinez
- Infrastructure experiments: James Wilson

**Data Science Support:**
- Statistical consulting: data-science@skyro.com
- Analysis requests: analytics@skyro.com

**Questions?**
Join #experimentation on Slack
