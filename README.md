# Behavioral Biometrics for Continuous Authentication in Internet Banking

This repository hosts the source code, datasets, and experimental analysis for the research study on **continuous authentication using behavioral biometrics** in an online banking environment. The project was conducted with Tanzanian working adults using a Django-based simulation of an internet banking platform.

## 🧠 Project Overview

Traditional authentication methods like passwords are increasingly vulnerable. This project explores continuous authentication based on users' **keystroke dynamics**, **mouse movements**, and **contextual questionnaire responses** to detect intrusions and simulate behavioral attacks in a realistic setting.

The repository contains:

- A Django-based online banking simulation system.
- Cleaned and anonymized datasets from real user sessions.
- Python notebooks and scripts for:
  - Feature engineering
  - Data cleaning
  - Visualization
  - Simulated attack generation
  - Classifier training and evaluation

## 📂 Repository Structure

banking_CA/
│
├── datasets/ # Cleaned and simulated datasets (CSV format)
│ ├── cleaned_pre_questionnaire.csv
│ ├── combined_user_features.csv
│ ├── simulated_attack_dataset.csv
│ └── ...
│
├── analysis_scripts/ # Jupyter notebooks and PDFs for data processing and visualization
│ ├── feature_engineering_script_for_keystrokes.ipynb
│ ├── behavioral_feature_correlation_heatmap.pdf
│ ├── Confusion_Matrix.pdf
│ ├── t-SNE_Clustering_of_User_Behavior.pdf
│ └── ...
│
├── banking-system/ # Django source code (web simulation)
│
├── requirements.txt # Python dependencies
│
└── README.md # This file

## 📊 Datasets

The dataset consists of over:

- **23,000 keystroke events**
- **319,000 mouse action logs**
- **180+ questionnaire responses** (pre-, during-, post-session)

Additionally, **simulated attack data** has been generated to validate classifier robustness.

## 🧪 Experiment Highlights

- Random Forest classifier trained on real vs simulated data
- Achieved **100% accuracy, precision, and recall**
- Visualization includes:
  - Confusion Matrix
  - t-SNE Clustering
  - ROC and Precision-Recall Curves

## 🛠️ Tools & Technologies

- **Web System**: Django, PostgreSQL, Gunicorn, Nginx, python-decouple
- **Data Analysis**: Python, Pandas, scikit-learn, Matplotlib, Jupyter Notebook
- **Deployment**: Ubuntu VPS (Hostinger), domain managed via TCRA and TzNIC

## 📈 Citation

If you use this project or dataset, please cite our work:

```bibtex
@misc{ndalama2025banking,
  author       = { Ndalama Festus Edward, Patrick Mutabazi},
  title        = {Behavioral Biometrics Dataset for Continuous Authentication in Online Banking},
  year         = {2025},
  howpublished = {\url{https://github.com/ztn-iplab/banking_CA}},
  note         = {Dataset and experiment code for continuous authentication using keystroke and mouse dynamics}
}

