<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/b/b6/Wikipedia-logo-v2-hi.svg" width="120" alt="Hindi Wikipedia Logo" />
</p>

<h1 align="center">AalekhakBot (आलेखकबॉट)</h1>

<p align="center">
  <strong>An automated Pywikibot framework for Hindi Wikipedia (hi.wikipedia.org)</strong> <br />
  Designed to enhance article quality through automated Wikidata integration and structural data visualization.
</p>

<p align="center">
  <a href="https://hi.wikipedia.org"><img src="https://img.shields.io/badge/Platform-Hindi%20Wikipedia-9C27B0?style=flat-square" alt="Hindi Wiki" /></a>
  <a href="https://www.mediawiki.org/wiki/Manual:Pywikibot"><img src="https://img.shields.io/badge/Framework-Pywikibot-007ACC?style=flat-square" alt="Pywikibot" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-4CAF50?style=flat-square" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/Status-Development%20%2F%20Testing-FF9800?style=flat-square" alt="Status" />
</p>

---

## Overview

**AalekhakBot** is a high-utility automation agent built on top of the Python `pywikibot` library. Rather than executing simple string-replacement runs, the bot performs semantic structural edits to improve the encyclopedic quality, readability, and information density of Hindi Wikipedia articles.

### Core Functions

*   **Semantic Infobox Ingestion:** Automatically cross-references page targets with their respective global Wikidata Item IDs (QIDs). It retrieves verified, real-time parameters (e.g., coordinates, populations, demographics, birth files) and constructs localized, structured Hindi Infoboxes (`{{ज्ञानसंदूक}}`).
*   **Data Visualization Rendering:** Parses static numerical matrices within articles and automatically translates them into clean, responsive, and mobile-friendly graphics (Bar, Line, and Pie charts) via Wikipedia's native `{{Graph:Chart}}` engine.
*   **Stub Consolidation:** Enhances micro-articles (stubs) by systematically injecting missing structural properties, raising the total byte size and structural rating of the articles.

---

## System Architecture & Security

To ensure safety and respect community boundaries, the bot uses a modular design:

*   **Credential Masking:** Configured local system credentials (`user-config.py` and `user-password.py`) are permanently ignored by Git to prevent leakages.
*   **Dry-Run Debugging Engine:** Integrates a global `DRY_RUN` switch. When enabled, all parsed edits are redirected to the local console output rather than being written to the live Wikipedia database.
*   **Community Integration compliance:** Every direct write request operates with `minor=True` and `botflag=True` parameter bindings to keep the Recent Changes stream uncluttered.

---

## Directory Structure

```text
hi-wiki-advanced-bot/
├── .gitignore             # Blocks tracking of credentials and local system locks
├── requirements.txt       # Project Python dependencies
├── README.md              # Project documentation
├── user-config.py         # Pywikibot main configuration (Local machine only)
├── user-password.py       # Bot authentication file (Local machine only)
└── advanced_wiki_bot.py   # Main engine executing infobox/graph algorithms
