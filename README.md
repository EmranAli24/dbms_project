# 🧠 DBMS Project: Automated Normalization Pipeline

A Python-based system for discovering **Functional Dependencies (FDs)**, identifying **Candidate Keys**, performing **Normal Form Analysis**, and **automatically decomposing** relational schemas into **Third Normal Form (3NF)**. This modular and extensible pipeline is ideal for academic research, DBMS lab projects, and learning normalization in depth.

---

## 📋 Table of Contents

- [📌 Overview](#-overview)
- [⚙️ Prerequisites](#️-prerequisites)
- [📁 Project Structure](#-project-structure)
- [🚀 Workflow](#-workflow)
  - [Step 1: Functional Dependency Discovery](#step-1-functional-dependency-discovery)
  - [Step 2: Candidate Key Discovery](#step-2-candidate-key-discovery)
  - [Step 3: Key & Normal Form Analysis](#step-3-key--normal-form-analysis)
  - [Step 4: 3NF Decomposition](#step-4-3nf-decomposition)
- [📤 Outputs](#-outputs)
- [👥 Authors](#-authors)
- [📝 License](#-license)

---

## 📌 Overview

This project automates the normalization of relational datasets through a four-stage process:

1. **Functional Dependency Extraction**
2. **Candidate Key Discovery**
3. **Normal Form Analysis**
4. **3NF Decomposition**

Each stage is implemented in a separate Python script for modularity, ease of debugging, and reproducibility.

---

## ⚙️ Prerequisites

Ensure you have the following installed:

- **Python** 3.8 or higher
- Python libraries:
  - `pandas` (`pip install pandas`)

You also need a **CSV dataset** with a header row (`cleaned_data.csv`).

---

## 📁 Project Structure

```
dbms_project/
│
├── data/
│   ├── processed/
│   │   └── cleaned_data.csv          # Input dataset after cleaning
│   └── fds/
│       ├── fds.json                  # Discovered functional dependencies
│       ├── cks.json                  # Candidate keys
│       ├── keys_nf_analysis.json     # NF and key validation
│       └── 3nf_relations.json        # Final 3NF relations
│
├── scripts/
│   ├── 02_fd_discovery.py            # Step 1: FD Discovery
│   ├── 03_ck_discovery.py            # Step 2: Candidate Key Discovery
│   ├── 03_key_nf_analysis.py         # Step 3: Normal Form Analysis
│   └── 04_3nf_decomposition.py       # Step 4: 3NF Decomposition
│
└── README.md                         # Project documentation
```

---

## 🚀 Workflow

### ✅ Step 1: Functional Dependency Discovery

Extract non-trivial FDs from the cleaned dataset.

```bash
python scripts/02_fd_discovery.py \
    --input_file data/processed/cleaned_data.csv \
    --output_file data/fds/fds.json \
    --max_lhs 2
```

- `--max_lhs`: Maximum number of attributes allowed on the LHS of an FD.

---

### ✅ Step 2: Candidate Key Discovery

Identify all minimal candidate keys from the discovered FDs.

```bash
python scripts/03_ck_discovery.py \
    --input_file data/processed/cleaned_data.csv \
    --fd_file data/fds/fds.json \
    --output_file data/fds/cks.json
```

---

### ✅ Step 3: Key & Normal Form Analysis

Analyze the keys and check which normal forms the schema satisfies.

```bash
python scripts/03_key_nf_analysis.py \
    --input_file data/processed/cleaned_data.csv \
    --fd_file data/fds/fds.json \
    --output_file data/fds/keys_nf_analysis.json \
    --max_key_size 3 \
    --known_keys known_keys.txt
```

- `--max_key_size`: Max size for generated candidate keys.
- `--known_keys`: *(Optional)* Path to known key file for validation.

---

### ✅ Step 4: 3NF Decomposition

Decompose the schema into 3NF while preserving dependencies and ensuring losslessness.

```bash
python scripts/04_3nf_decomposition.py \
    --input_file data/processed/cleaned_data.csv \
    --fd_file data/fds/fds.json \
    --key_file data/fds/cks.json \
    --output_file data/fds/3nf_relations.json
```

---

## 📤 Outputs

| File | Description |
|------|-------------|
| `fds.json` | Discovered functional dependencies |
| `cks.json` | Minimal candidate keys |
| `keys_nf_analysis.json` | Keys and normal form analysis |
| `3nf_relations.json` | Final 3NF relations with attribute groupings |

---

## 👥 Authors

- **Emran Ali**  
- **Anik Kirtania**  
- **Omar Faruk Seiam**

---

## 📝 License

This project is intended for academic and educational use. For other applications or licensing inquiries, please contact the authors.
