# Stage 1: PM Creates Requirements

## 👔 Role: Project Manager

You are starting as PM to define what FinCat needs to do.

---

## 📖 Reading Order (ALWAYS follow this order)

Before starting ANY work, read these folders/files in this exact order:

### 1. Your Role Overview
**Read:** `../../PM/Job Description.md`
- Understand your responsibilities as PM

### 2. Your Current Task
**Read:** `../../PM/Read Instructions/FinCat/create_requirements_stage1.md`
- This file contains your specific task (created by human or previous stage)

### 3. Your Methods & References
**Read:** `../../PM/Sources & Methods.md`
- Methodologies for writing requirements
- Templates to use

### 4. Your Previous Work (if any)
**Check:** `../../PM/Branch (Version) Management/FinCat/`
- Look for any previous versions (requirements_v1.md, requirements_v2.md, etc.)
- Read the LATEST version only for reference
- If this is the first time, folder will be empty

### 5. How to Communicate
**Read:** `../../PM/Agent Interfaces.md`
- How to pass work to Architect
- What format Architect expects

---

## 🎯 Your Task

### Read Project Context
**Location:** `../../Projects/FinCat - Active Version/App Description.md`

Understand:
- What FinCat does (5 stages: file detection → parsing → AI → Excel → archive)
- Technology preference (Python, local execution)
- Expected users and volume

### Create Requirements Document

**Save your work to:** `../../PM/Branch (Version) Management/FinCat/requirements_v1.md`

Include these sections:

#### 1. Project Overview
- Name: FinCat
- Purpose: Automate Hebrew credit card expense categorization
- Technology: Python 3.8+ (Mac & Windows compatible)

#### 2. Functional Requirements

**FR-1: File Detection & Monitoring**
- Monitor input folder continuously
- Detect new .xls files
- Wait for file to be fully written
- Trigger processing automatically

**FR-2: XLS Parsing (Hebrew)**
- Read Hebrew credit card statements
- Extract: date, card number, business name (שם העסק), amount, details
- Convert Excel serial dates (epoch: 1899-12-30)
- Handle multiple cards in one file
- Parse installment info (תשלום X מתוך Y)
- Handle foreign currency transactions
- Detect refunds (זיכויים)

**FR-3: AI Categorization**
- Send business names to Claude AI
- Match against predefined categories
- Return category for each transaction
- Handle Hebrew text correctly
- Minimize token usage (cost optimization)

**FR-4: Excel Output**
- Load master tracking file
- Append new transactions with categories
- Preserve Hebrew text encoding (UTF-8)
- Handle file if doesn't exist (auto-create)
- Include columns: תאריך, כרטיס, שם העסק, סכום, מטבע, קטגוריה, תשלומים, הערות

**FR-5: File Archiving**
- Move processed file to "processed" folder
- Preserve original filename
- Add timestamp if needed

**FR-6: Configuration Management**
- Use config.yaml for settings
- Use .env for API keys
- Support environment overrides

**FR-7: Logging & Monitoring**
- Log all operations
- Include timestamps
- Rotate logs (max 10MB, keep 5 backups)
- Do NOT log sensitive data (amounts, card numbers, API keys)

**FR-8: Error Recovery**
- Retry API calls (3 attempts, exponential backoff)
- If API fails: mark as "uncategorized"
- Continue processing (don't crash)
- Log errors for manual review

#### 3. Non-Functional Requirements

**NFR-1: Performance**
- Process file in < 10 seconds
- Handle up to 100 transactions per file

**NFR-2: Cost**
- AI cost < $0.01 per file
- Monthly cost < $1 for ~10 files

**NFR-3: Cross-Platform Compatibility**
- Works on macOS
- Works on Windows
- Single codebase

**NFR-4: Reliability**
- 99% uptime (local execution)
- Graceful error handling
- No duplicate processing

**NFR-5: Accuracy**
- 95%+ correct categorization
- Handle edge cases (refunds, installments, foreign currency)

#### 4. User Stories

```markdown
**US-1: Automatic Processing**
As a user
I want to drop XLS files in input folder
So that they get automatically categorized

**US-2: Hebrew Support**
As a Hebrew-speaking user
I want correct Hebrew text handling
So that my categories and data are readable

**US-3: AI Categorization**
As a user
I want automatic expense categorization
So that I save time on manual classification

**US-4: Master Tracking**
As a user
I want all transactions in one Excel file
So that I can analyze spending over time
```

#### 5. Acceptance Criteria

- [ ] System detects new files automatically
- [ ] Hebrew text displays correctly
- [ ] All transactions extracted accurately
- [ ] AI categorizes with 95%+ accuracy
- [ ] Master file updates correctly
- [ ] Files archived properly
- [ ] Works on Mac and Windows
- [ ] Processing < 10 seconds
- [ ] Cost < $0.01 per file

#### 6. Constraints

**Technical:**
- Python 3.8+ only
- Local execution (no cloud except AI API)
- Must work offline (except AI calls)

**Business:**
- Low cost (< $1/month)
- Simple setup (< 30 min)
- No ongoing maintenance needed

**Timeline:**
- Complete in 1-2 weeks
- Ready for personal use

---

## 📤 Pass Work to Architect

### Create Task for Architect

**Save to:** `../../Architect/Read Instructions/FinCat/FinCat_review_stage2.md`

**Content:**
```markdown
# Task: Review FinCat Requirements (Stage 2)

## From: PM
## To: Architect
## Project: FinCat

## Your Mission

Review the requirements I created and provide technical guidance.

## My Work Location

**Read my requirements here:**
`PM/Branch (Version) Management/FinCat/requirements_v1.md`

## What I Need From You

1. **Technical Feasibility Assessment**
   - Can this be built with Python?
   - Any technical blockers?

2. **Technology Stack Recommendations**
   - Which libraries for file monitoring?
   - Which libraries for XLS parsing (old format)?
   - Which libraries for Excel writing (modern format)?
   - Which libraries for AI integration?

3. **Architecture Proposal**
   - High-level system design
   - Module structure
   - Data flow diagram

4. **Cross-Platform Strategy**
   - How to ensure Mac + Windows compatibility?

5. **Hebrew Text Handling**
   - Any special considerations?
   - Encoding requirements?

6. **Risk Analysis**
   - What technical risks do you see?
   - Mitigation strategies?

## Save Your Work To

`Architect/Branch (Version) Management/FinCat/technical_review_v1.md`

## When Done

Create my next task in:
`PM/Read Instructions/FinCat/FinCat_finalize_stage3.md`

Tell me what to do with your feedback.

---

**Timeline:** Need review within 1 day
**Priority:** High
```

---

## ✅ Completion Checklist

- [ ] Read all 5 folders in order
- [ ] Read App Description.md
- [ ] Created requirements_v1.md in my Branch (Version) Management/FinCat/
- [ ] All functional requirements defined
- [ ] All non-functional requirements defined
- [ ] User stories written
- [ ] Acceptance criteria listed
- [ ] Created task for Architect in their Read Instructions/FinCat/
- [ ] Specified where my work is located

---

## 📍 Your Output

**Your Work:** `PM/Branch (Version) Management/FinCat/requirements_v1.md`
**Next Task:** `Architect/Read Instructions/FinCat/FinCat_review_stage2.md`

---

## 🔄 Status Report

After completing, report:

```
Stage 1 complete.

Created:
- PM/Branch (Version) Management/FinCat/requirements_v1.md
- Architect/Read Instructions/FinCat/FinCat_review_stage2.md

Next: Architect should execute Stage 2 (review requirements)

Awaiting human approval to proceed.
```

**STOP HERE. Do not proceed to Stage 2 until human approves.**
