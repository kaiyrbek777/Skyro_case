# Security Incident Postmortem - API Key Exposure

**Incident ID:** INC-2024-001
**Date of Incident:** January 28, 2024
**Postmortem Date:** February 1, 2024
**Severity:** P1 (High)
**Status:** Resolved

## Attendees
- Tom Chen (Security Lead)
- James Wilson (Engineering Lead)
- Kevin Patel (DevOps Lead)
- Rachel Kim (Compliance Officer)
- David Brown (CTO)

## Executive Summary

On January 28, 2024, at 14:32 PST, a production API key for our payment gateway was accidentally committed to a public GitHub repository. The key was detected by our automated scanning tools 23 minutes after the commit. All potentially compromised keys were immediately rotated, and no unauthorized transactions were detected.

**Impact:** Low (no customer data compromised)
**Duration:** 23 minutes from exposure to remediation
**Root Cause:** Human error + insufficient pre-commit validation

## Timeline

**All times in PST**

**14:32** - Developer commits code with API key to public repo
**14:38** - GitHub Advanced Security alert triggered
**14:42** - PagerDuty alert sent to security team
**14:47** - Tom Chen acknowledges alert and begins investigation
**14:50** - Confirmed: Production Stripe API key exposed
**14:52** - Incident escalated to P1, war room initiated
**14:55** - API key rotated in Stripe dashboard
**15:00** - New API key deployed to production
**15:03** - Offending commit removed from git history
**15:15** - Repository temporarily made private
**15:45** - Audit of Stripe API logs completed (no suspicious activity)
**16:30** - Repository returned to public with cleaned history
**17:00** - All-clear declared

## What Happened

### Sequence of Events

1. Junior engineer working on payment integration feature
2. Created test script with hardcoded API key for debugging
3. Forgot to remove key before committing
4. Pre-commit hooks did NOT catch the key (failure point)
5. Code pushed to public GitHub repository
6. GitHub Advanced Security detected secret 6 minutes later
7. Alert routed through monitoring system

### What Went Well ✅

1. **Automated Detection:** GitHub Advanced Security worked as expected
2. **Rapid Response:** Security team responded within 5 minutes
3. **Clear Runbook:** Incident response procedures followed correctly
4. **Fast Remediation:** Key rotated within 23 minutes
5. **No Impact:** No fraudulent transactions detected
6. **Communication:** Stakeholders notified promptly

### What Went Wrong ❌

1. **Pre-commit hooks failed:** Should have caught hardcoded secrets
2. **Developer training gap:** Engineer unaware of secret management best practices
3. **No secrets scanner in CI:** Additional safety layer missing
4. **Alert delay:** 6-minute delay between commit and detection

## Root Cause Analysis

### Primary Cause
Human error - developer accidentally committed hardcoded API key to version control.

### Contributing Factors

1. **Insufficient pre-commit validation**
   - Pre-commit hook not configured on developer's machine
   - Hook pattern didn't match this key format

2. **Lack of developer awareness**
   - Junior engineer not trained on secret management
   - No visible warnings in IDE

3. **Missing CI/CD gates**
   - No automated secret scanning in pull request checks
   - Manual code review didn't catch the issue

## Impact Assessment

### Customer Impact
**None.** No customer data was compromised, and no unauthorized transactions were detected.

### Business Impact
- 23 minutes of potential exposure
- 2 hours of engineer time for remediation
- Minor reputational risk (mitigated by fast response)

### Financial Impact
- Estimated cost: $800 (engineer time)
- No actual losses incurred

### Compliance Impact
- Incident reported to compliance team
- No regulatory reporting required (no data breach)
- Added to SOC 2 incident log

## Action Items

### Immediate (Completed ✅)

1. ✅ **Rotate all API keys** (Done: Jan 28)
   - Owner: Tom Chen
   - All payment gateway keys rotated
   - All team members notified

2. ✅ **Remove exposed key from git history** (Done: Jan 28)
   - Owner: Kevin Patel
   - Used BFG Repo-Cleaner
   - Force-pushed cleaned history

3. ✅ **Audit API logs** (Done: Jan 28)
   - Owner: Tom Chen
   - No suspicious activity found
   - Generated audit report

### Short-term (In Progress 🔄)

4. 🔄 **Deploy gitleaks to all repositories** (Due: Feb 5)
   - Owner: Kevin Patel
   - Status: 60% complete
   - Pre-commit hooks for all engineers

5. 🔄 **Implement secrets scanner in CI** (Due: Feb 8)
   - Owner: James Wilson
   - Status: In development
   - Block PRs with detected secrets

6. 🔄 **Mandatory security training** (Due: Feb 15)
   - Owner: Tom Chen
   - Status: Content being prepared
   - All engineers must complete

### Medium-term (Planned 📝)

7. 📝 **Migrate to centralized secret management** (Due: Mar 1)
   - Owner: Kevin Patel
   - Tool: HashiCorp Vault
   - Eliminate hardcoded secrets entirely

8. 📝 **Implement automated key rotation** (Due: Mar 15)
   - Owner: Tom Chen
   - Rotate keys every 90 days
   - Automated process

9. 📝 **Enhanced IDE plugins** (Due: Feb 28)
   - Owner: James Wilson
   - Real-time secret detection in VSCode
   - Warn before commit

### Long-term (Roadmap 🗺️)

10. 🗺️ **Zero-trust architecture** (Due: Q3 2024)
    - Owner: David Brown
    - Service mesh with mTLS
    - No long-lived credentials

## Lessons Learned

### What We Learned

1. **Defense in depth is critical**
   - Single layer of protection is insufficient
   - Need multiple overlapping controls

2. **Automation > Human vigilance**
   - Humans make mistakes
   - Automated tools are more reliable

3. **Fast detection = reduced impact**
   - 23-minute exposure is excellent
   - Goal: reduce to <10 minutes

4. **Clear runbooks are invaluable**
   - Response was smooth due to documented procedures
   - Regular drills keep team prepared

### Changes to Process

**Before:**
- Optional pre-commit hooks
- Manual code review only
- Secrets in environment variables

**After:**
- Mandatory pre-commit hooks (enforced)
- Automated secret scanning + manual review
- Centralized secret management (Vault)
- Automated key rotation
- Enhanced monitoring and alerting

## Prevention Measures

### Technical Controls

1. **Pre-commit hooks** (gitleaks) - REQUIRED
2. **CI/CD secret scanning** (GitHub Advanced Security)
3. **Centralized secret management** (HashiCorp Vault)
4. **Automated key rotation** (every 90 days)
5. **Real-time monitoring** (alerts for unusual API activity)

### Process Controls

1. **Mandatory security training** (onboarding + annual)
2. **Code review checklist** (includes secret check)
3. **Security champions program** (1 per team)
4. **Regular security drills** (quarterly)

### Monitoring Controls

1. **GitHub Advanced Security** (secret scanning)
2. **SIEM alerts** (unusual API key usage)
3. **Rate limiting** (on API keys)
4. **Audit logging** (all API key operations)

## Communication

### Internal
- Incident reported to engineering team (Slack)
- CTO briefed immediately
- Post-mortem shared company-wide

### External
- No customer notification required (no data exposure)
- No regulatory reporting required

## Follow-up

**Next Review:** February 15, 2024
**Owner:** Tom Chen

**Success Metrics:**
- Zero secrets committed to repos (tracked monthly)
- 100% pre-commit hook adoption
- <10 minute detection for any future incidents

## Appendix

### References
- Incident Response Runbook: wiki/security/incident-response
- Secret Management Policy: wiki/security/secret-management
- GitHub Advanced Security Docs: https://docs.github.com/advanced-security

### Tools Used
- GitHub Advanced Security
- BFG Repo-Cleaner
- gitleaks
- HashiCorp Vault (planned)
