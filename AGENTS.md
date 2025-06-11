
Introduction
This document defines the conceptual agents that constitute our professional EPUB production workflow. Each agent represents a distinct phase of responsibility, designed to collaboratively produce a flawless, "best-seller worthy" digital book. The framework's primary objective is to ensure that every EPUB is semantically rich, universally compatible across all reading platforms, fully accessible, and free of technical errors.

1. Content Preparation Agent
Role: The guardian of textual integrity. This agent ingests the raw manuscript and refines it into a clean, consistent, and structurally primed text, forming the bedrock of the entire production process.

Core Responsibilities:

Linguistic & Typographical Correction: Performs a deep analysis to identify and correct grammatical errors, spelling and punctuation inconsistencies, and common typographical mistakes.
Stylistic Unification: Enforces a consistent style guide for elements such as capitalization, abbreviations, and project-specific terminology to ensure a professional reading experience.
Semantic Priming: Analyzes the text to identify logical structures (chapters, sections, lists, blockquotes) in preparation for semantic HTML conversion.
Issue Reporting: Generates a comprehensive report detailing all corrections made and flagging any ambiguities that require manual author or editor review.
Associated Tools & Scripts:

src/examine_content.py: Executes the initial content analysis and reporting.
src/correct_content.py: Applies automated corrections based on predefined rules.
Manual Review Tools: Standard text editors or specialized software (e.g., Grammarly, ProWritingAid) for addressing flagged issues.
2. Formatting & Structure Agent
Role: The architect of the digital book. This agent transforms the prepared text into a structurally sound and semantically rich XHTML foundation, adhering strictly to W3C and EPUB standards.

Core Responsibilities:

Semantic HTML Generation: Converts the clean text into valid, semantic HTML5, utilizing the correct tags for all structural elements (h1-h6, p, ul, blockquote, etc.).
Template Integration: Injects the content into standardized XHTML templates to ensure structural consistency across all sections of the book.
Structural Segmentation: Divides the content into logical XHTML files (typically one per chapter), as mandated by EPUB best practices for performance and navigation.
CSS Class Application: Applies meaningful CSS classes to HTML elements, enabling precise and flexible styling in the subsequent stages.
Media & Link Integration: Properly embeds media assets with appropriate alt text for accessibility and ensures all internal cross-references and footnotes are functional.
Associated Tools & Scripts:

pandoc-py / markdown: For robust conversion of Markdown (or other formats) to a structured HTML baseline.
BeautifulSoup4 / lxml: For parsing, manipulating, and refining the generated XHTML to enforce quality and adherence to templates.
3. Quality Assurance & Validation Agent
Role: The rigorous inspector and final gatekeeper. This agent meticulously audits the entire pre-compiled EPUB package to certify its technical compliance, accessibility, and readiness for publication.

Core Responsibilities:

Code Validation: Performs strict validation of all XHTML, CSS, and internal XML files (e.g., OPF, NCX) to ensure they are well-formed and syntactically correct.
Accessibility Audit: Conducts a thorough check for accessibility compliance (WCAG standards), verifying alt text, semantic structure, language declarations, and logical reading order.
Link Integrity Check: Traverses the entire book to confirm that all internal and external hyperlinks are valid and resolve correctly.
Asset Verification: Checks that all media assets (images, fonts) are in supported formats, optimized for size, and correctly referenced.
Compliance Reporting: Produces a detailed report of all validation errors or warnings that must be resolved before final packaging.
Associated Tools & Scripts:

src/validate_files.py: A custom script utilizing lxml and other libraries for pre-compilation structural and HTML checks.
epubcheck (External Gold Standard): Execution of the official epubcheck tool is a mandatory final step to guarantee compliance with global EPUB standards for all retail platforms.
4. Metadata & Packaging Agent
Role: The final assembler and archivist. This agent gathers all book-defining metadata and orchestrates the assembly of all validated components into the final, complete .epub file.

Core Responsibilities:

Metadata Embedding: Populates the OPF file with comprehensive metadata (Title, Author, ISBN, Publisher, Date, Language, Description) based on the Dublin Core standard.
Cover Integration: Assigns and correctly embeds the cover image, ensuring it is properly declared in the manifest.
Table of Contents Generation: Creates both the user-facing Navigable TOC (NAV) and the backward-compatible NCX TOC, ensuring they are accurate and hierarchical.
Manifest & Spine Definition: Accurately builds the manifest of all book assets (XHTML files, CSS, images, fonts) and defines the linear reading order in the spine.
Associated Tools & Scripts:

src/compile_epub.py: The primary script that leverages EbookLib to programmatically build the final EPUB package.
Metadata Configuration: Structured data files (e.g., book.json, metadata.yaml) that provide a single source of truth for all book metadata.
5. Orchestrator Agent
Role: The master conductor of the workflow. This agent automates the end-to-end production process, executing all other agents in the correct sequence to ensure a repeatable, efficient, and error-free build.

Core Responsibilities:

Environment Management: Prepares the working environment by creating necessary directories and verifying dependencies.
Workflow Execution: Sequentially invokes the Preparation, Formatting, Validation, and Packaging agents.
Error Handling & Logging: Implements robust error handling to halt the process on critical failures and maintains a detailed log of the entire build for diagnostics.
Output Finalization: Manages the storage of the final .epub file and all associated validation reports in a clean, organized output directory.
Associated Tools & Scripts:

Makefile or a master Python script (main.py): Serves as the high-level orchestrator that runs the entire build process with a single command.
setup_environment.sh: An initial setup script to configure the environment for a new project.
