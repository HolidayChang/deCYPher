# deCYPher 🧬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**deCYPher** is a specialized genotyping pipeline designed for pharmacogenes (e.g., CYP2D6, CYP2C19) using high-fidelity (HiFi) assembly data. It integrates variant calling, haplotype alignment, and custom annotation logic to handle complex structural variants like gene deletions and hybrids.

---

## ✨ Key Features

- **High Precision**: Tailored for HiFi assembly data using `minimap2` and `paftools.js`.
- **Structural Variant Support**: 
  - **CYP2D6*5**: Intelligent detection and simplified reporting for gene deletions.
  - **CYP2D6*13**: Specialized VCF-based exclusion logic for hybrid genes.
- **Automated Workflow**: One-step environment setup and reference data retrieval.
- **Clean Output**: Consolidated JSON reports for easy downstream analysis.

---

## 🛠 Installation & Usage Guide

### 1. Clone the Repository
Start by cloning the project from GitHub to your local machine:
```bash
git clone [https://github.com/HolidayChang/deCYPher.git](https://github.com/HolidayChang/deCYPher.git)
cd deCYPher
