# Project Agents: Chapter Conversion Workflow

This document defines the roles of the automated agents responsible for the lossless EPUB-to-HTML conversion process. Each agent has a specific, non-overlapping task to ensure maximum accuracy and adherence to the project standards.

---

## Agent 1: `ExtractorAgent`

* **Role**: To perform the initial, raw conversion of an EPUB chapter into plain text, ensuring absolute fidelity to the source.
* **Primary Directives**:
    * **ZERO HALLUCINATION**: Content must be copied exactly as written, with no paraphrasing, corrections, or additions.
    * **WORD COUNT PRECISION**: The output word count must match the source chapter's word count exactly.
    * **COMPLETE PRESERVATION**: All text, including paragraphs, lists, bold/italic markers, quotes, and endnote content, must be extracted. The structure is not the priority here, only the raw content.
* **Inputs**: A single chapter file from the source EPUB.
* **Outputs**: A plain text file (`.txt`) containing all extracted content and a JSON file with metadata (e.g., `{"source_word_count": 4097}`).
* **Tools**: EPUB parsing libraries (e.g., `epub-parser` for Node.js).

---

## Agent 2: `StructureAgent`

* **Role**: To take the raw, verified text and build a valid HTML5 document according to the project's strict structural template.
* **Primary Directives**:
    * Must follow the **UNIVERSAL CHAPTER STRUCTURE TEMPLATE** in the exact specified order (Title Page, Main Content, Endnotes, Quiz, Worksheet, Image Footer).
    * Injects raw content from the `ExtractorAgent` into the correct HTML sections.
    * Constructs the drop cap, chapter titles, and page breaks (`<hr>`) as defined.
    * Formats endnotes, quizzes, and worksheet containers correctly.
* **Inputs**: The `.txt` and `.json` files from `ExtractorAgent`.
* **Outputs**: A structured but uncleaned HTML file (`Chapter-I-structured.html`).
* **Tools**: Template-building scripts, `npx prettier` for initial formatting.

---

## Agent 3: `SvgEliminatorAgent`

* **Role**: To surgically remove all SVG elements from the structured HTML and replace them with the specified CSS decorative classes.
* **Primary Directives**:
    * Must adhere strictly to the **SVG ELIMINATION PROTOCOL**.
    * All `<svg>`, `<path>`, `<circle>`, and `<rect>` tags and their content must be deleted.
    * The specified CSS classes (`.decorative-top-accent`, `.decorative-line`, etc.) must be applied where appropriate.
* **Inputs**: The structured HTML file from `StructureAgent`.
* **Outputs**: A cleaned HTML file with no SVG elements (`Chapter-I-cleaned.html`).
* **Tools**: `npx htmlclean-cli`, advanced find-and-replace with regular expressions (`<svg[\s\S]*?<\/svg>`).

---

## Agent 4: `QaAgent` (Quality Assurance)

* **Role**: To perform a final, automated verification against the master checklist before a chapter is marked as complete. This agent does not modify files; it only reports success or failure.
* **Primary Directives**:
    * **Verify Word Count**: Compares the final HTML's word count (excluding tags) against the target from the master list.
    * **Verify SVG Removal**: Scans the final file for any remaining `<svg>` tags. A single instance results in failure.
    * **Verify HTML Validity**: Checks the final file for structural errors against the project's rules.
    * **Verify Content Fidelity**: Performs an automated "diff" check between the text content of the final HTML and the raw text from `ExtractorAgent`.
* **Inputs**: The cleaned HTML file from `SvgEliminatorAgent`, the source text from `ExtractorAgent`, and the master word count target.
* **Outputs**: A JSON report: `{"status": "SUCCESS"}` or `{"status": "FAILURE", "errors": ["Word count mismatch: expected 4097, got 4096", "SVG element found at line 52"]}`.
* **Tools**: Word counting tools, file content comparison (`diff`), `npx htmllint`.

---

## Agent 5: `BatchManagerAgent`

* **Role**: To orchestrate the entire workflow, manage progress tracking, and deploy the other agents in the correct sequence.
* **Primary Directives**:
    * Initiates the workflow for the current batch (e.g., **BATCH 1: Chapters I-IV**).
    * For each chapter, sequentially deploys `ExtractorAgent`, `StructureAgent`, and `SvgEliminatorAgent`.
    * Deploys `QaAgent` to validate the final output.
    * If QA passes, updates the chapter's status to `✅ COMPLETE` in the master report, updates progress percentages, and moves to the next chapter.
    * If QA fails, logs the error report and halts the process for that chapter pending manual review.
* **Inputs**: The master workflow document/report.
* **Outputs**: An updated workflow document with new progress, and error logs if any failures occur.
* **Tools**: Workflow orchestration scripts (e.g., a master shell or Python script).
