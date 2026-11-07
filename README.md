# <img width="55" height="50" alt="image" src="https://github.com/user-attachments/assets/39cd6a11-6a3b-4ae6-9829-d4e9f39a2f0a" /> deCYPher 

> [!WARNING]
> **Patent Notice**
> The technology, algorithms, and implementations contained in this repository (deCYPher) are subject to an active provisional patent application. The software code is licensed under the Apache License 2.0, which includes explicit patent terms. For commercial licensing inquiries or uses outside the scope of this license, please contact Ting-Yu Chang at r13455012@ntu.edu.tw.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
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
### 2. One-Step Automated Setup
This script automates the following tasks:
#### Creates the Conda environment (```deCYPher_env```).
#### Installs all dependencies (```k8, paftools.js, biopython, pandas```).
#### Downloads and extracts the required reference data (```ref/```) from GitHub Releases.
#### Configures the ```decypher``` command for your environment.
```bash
bash env/setup.sh
```
### 3. Activate the Environment
Always activate the Conda environment before using the tool:
```bash
conda activate deCYPher_env
```
### 4. Run Analysis
You can now run the decypher command from any directory.
```bash
decypher --input <assembly.fasta> --name <sample_id> --outdir <output_dir>
```
Command Line Arguments:
```bash
--input: Path to the assembly fasta file (.fa or .gz). (Required)

--name: Sample name used for prefixing output files. (Required)

--outdir: Directory to save the analysis results. (Required)

--threads: Number of CPU threads for alignment. (Default: 18)
```
