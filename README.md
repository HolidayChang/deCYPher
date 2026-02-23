# deCYPher 🧬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**deCYPher** is a specialized genotyping pipeline designed for pharmacogenes (e.g., CYP2D6, CYP2B6) using high-fidelity (HiFi) assembly data. It integrates variant calling, haplotype alignment, and custom annotation logic to handle complex structural variants like gene deletions and hybrids.

---

## ✨ Key Features

- **High Precision**
- **Structural Variant Support**
- **Automated Workflow**
- **Clean Output**
---

## 🛠 Installation & Usage Guide

### 1. Clone the Repository
Start by cloning the project from GitHub to your local machine:
```bash
git clone https://github.com/HolidayChang/deCYPher.git
cd deCYPher
```
### 2. One-Step Automated SetupRun the setup script located in the env/ folder. 
This script automates the following tasks:
#### Creates the Conda environment (```deCYPher_env```).
Installs all dependencies (k8, paftools.js, biopython, pandas).Downloads and extracts the required reference data (ref/) from GitHub Releases.Configures the decypher command for your environment.Bashbash env/setup.sh
### 3. Activate the EnvironmentAlways activate the Conda environment before using the tool:Bashconda activate deCYPher_env
4. Run AnalysisYou can now run the decypher command from any directory.Bashdecypher --input <assembly.fasta> --name <sample_id> --outdir <output_dir>
Command Line Arguments:ArgumentDescriptionDefault--inputPath to the assembly fasta file (.fa or .fa.gz)Required--nameSample name used for prefixing output filesRequired--outdirDirectory to save the analysis resultsRequired--threadsNumber of CPU threads for alignment18
