# FinCat Workflow

## Overview
Name of the workflow: **FinCat**

**Technology Stack**: Google Drive + Google Sheets

---

## Folder Structure

- **Folder 1**: "חיובים חדשים" (New Charges)
- **Folder 2**: "חיובים שעובדו" (Processed Charges)
- **Master File**: "מעקב חיובים" (Charges Tracking)
- **Reference File**: "קטגוריות" (Categories)

---

## Workflow Stages

### Stage 1: File Detection
A new XLS file arrives in Folder 1 ("חיובים חדשים")

### Stage 2: File Reading
FinCat reads the new XLS file and extracts the data

### Stage 3: AI Model Processing
1. FinCat sends rows of the "שם העסק" (Business Name) column to an AI Model
2. AI Model is connected to the Reference file "קטגוריות" (available categories)
3. For each charge, the AI Model:
   - Reads the business name with its row index
   - Matches the business to the correct category from the reference file
   - Creates a new column "קטגוריה" (Category) with the matched category

### Stage 4: Master File Update
FinCat appends the new file rows (including the new "קטגוריה" column) to the Master file "מעקב חיובים"

### Stage 5: File Organization
FinCat moves the processed file from Folder 1 ("חיובים חדשים") to Folder 2 ("חיובים שעובדו")

---

## Data Flow
```
New XLS File
    ↓
Folder 1: "חיובים חדשים"
    ↓
FinCat reads file
    ↓
Extract "שם העסק" column
    ↓
Send to AI Model
    ↓
AI Model + Reference file "קטגוריות"
    ↓
Create "קטגוריה" column
    ↓
Append to Master file "מעקב חיובים"
    ↓
Move file to Folder 2: "חיובים שעובדו"
```
