
# 📊 DBMS Project: Automated Database Design Pipeline

This project transforms a **raw, noisy dataset** into a cleaned, normalized relational schema, and finally generates an **Entity-Relationship Diagram (ERD)** in **Chen Notation**.

It simulates how a DBMS designer might go from real-world data to a formal database model with minimal manual effort.

---

## 📁 Project Structure

```
dbms_project/
├── .gitignore                      # Files/folders to exclude from version control
├── README.md                       # Project overview and instructions

├── data/
│   ├── raw/                        # Contains the original noisy dataset
│   │   └── noisy_dataset.csv
│   └── processed/                  # Contains the cleaned version of the dataset
│       └── cleaned_dataset.csv

├── scripts/
│   ├── 01_data_cleaning.py         # Cleans and preprocesses the noisy data
│   └── 02_fd_discovery.py          # Discovers functional dependencies from cleaned data

├── notebooks/
│   └── exploratory_analysis.ipynb  # Jupyter notebook for visual analysis or experimentation

└── docs/
    └── er_diagram.png              # Final Chen Notation ER diagram (auto-generated or manual)
```

---

## 🚀 Features

- ✅ Load and clean real-world noisy data.
- ✅ Discover **Functional Dependencies (FDs)** using attribute grouping and closure.
- ✅ Normalize schema to **3NF or BCNF** (to be implemented).
- ✅ Generate a **Chen Notation ER Diagram** using Graphviz or Draw.io.

---

## 🛠️ How to Run

### 1. Clean the Dataset
```bash
python scripts/01_data_cleaning.py
```

### 2. Discover Functional Dependencies
```bash
python scripts/02_fd_discovery.py
```

> Upcoming scripts:
- `03_normalization.py`: Normalize based on FDs
- `04_generate_er.py`: Auto-generate ER Diagram

---

## 🧪 Requirements

Install required packages using:

```bash
pip install pandas graphviz numpy
```

---

## ✅ To Do

- [ ] Implement schema normalization (3NF / BCNF)
- [ ] Generate ERD automatically using Graphviz
- [ ] Add GUI interface for automation
- [ ] Export normalized schema to SQL

---

## 📄 License

This project is open-source and free to use under the **MIT License**.

---

## 🙋‍♂️ Author

**Emran Ali**  
💼 CSE, University of Chittagong  
📬 [LinkedIn](www.linkedin.com/in/emran-ali-3b53342a7) *(Replace with actual link)*
