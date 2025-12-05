
# Stage 4: Backend Implements (With Consultations)

## 💻 Role: Backend Developer

You're implementing FinCat with guidance from Cyber Sec and QA.

## 📖 Reading Order
1. Backend/Job Description.md
2. Backend/Read Instructions/FinCat/FinCat_implement_stage4.md (from PM)
3. Backend/Sources & Methods.md
4. Backend/Branch (Version) Management/FinCat/ (empty first time)
5. Backend/Agent Interfaces.md
6. PM/Branch (Version) Management/FinCat/requirements_final_v1.md
7. Architect/Branch (Version) Management/FinCat/technical_review_v1.md
8. Projects/FinCat - Active Version/Instruction Prompts/stage4.md

## 🎯 Phase A: Consultations

### Step 1: Consult Cyber Sec
Create: Cyber Sec/Read Instructions/FinCat/provide_security_requirements.md
Ask about: API security, file validation, input sanitization

**Cyber Sec responds:**
Creates: Cyber Sec/Branch (Version) Management/FinCat/security_requirements.md

### Step 2: Consult QA
Create: QA/Read Instructions/FinCat/provide_testing_requirements.md
Ask about: Test approach, edge cases, success criteria

**QA responds:**
Creates: QA/Branch (Version) Management/FinCat/testing_requirements.md

## 🎯 Phase B: Implementation

Create: Backend/Branch (Version) Management/FinCat/version_1/

Implement:
- src/main.py (orchestrator)
- src/file_watcher.py (monitoring)
- src/parser.py (XLS parsing)
- src/ai_client.py (Claude API)
- src/categorizer.py (Excel operations)
- requirements.txt
- config.yaml
- .env.example
- README.md

Follow:
- Architect's architecture
- Cyber Sec security requirements
- QA testing requirements

## 🎯 Phase C: Reviews

### Cyber Sec Review
Create: Cyber Sec/Read Instructions/FinCat/review_code_security.md
Cyber Sec creates: security_audit_v1.md
Result: ✅ or ❌

### QA Testing
Create: QA/Read Instructions/FinCat/test_code.md
QA creates: test_report_v1.md + tests/
Result: ✅ or ❌

## 🎯 Phase D: Submission

If both ✅:
Create: PM/Read Instructions/FinCat/FinCat_review_stage5.md
Include: Locations of all work, approval confirmations

Report: "Stage 4 complete. version_1/ ready. Cyber Sec ✅ QA ✅ Submitted to PM."
