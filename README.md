# 🧠 Quantum_Public_Policy-Project

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PennyLane](https://img.shields.io/badge/Quantum-PennyLane-purple?logo=pytorch)](https://pennylane.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

> ⚛️ *AI + Quantum Intelligence for Smarter Public Policy Discovery*

---

## 🌍 Overview

The **Quantum_Public_Policy-Project** is an **AI-powered platform** that integrates **Natural Language Processing (NLP)** and **Quantum Machine Learning (QML)** to analyze, compare, and recommend **Indian public policies** and **government schemes**.

Users can query the system to discover **relevant education, poverty, and welfare policies**, view summaries, and compare results from **classical** and **quantum-enhanced** models through a clean, web-based interface powered by **FastAPI**.

---

## ✨ Features

✅ **Policy Search Engine** — Retrieve government policies and schemes using natural language.
⚡ **Quantum + Classical NLP** — Compare QML and traditional TF-IDF based retrievals.
🧭 **FastAPI Backend** — High-performance REST server with HTML integration.
🎨 **Interactive Frontend** — Jinja2-based responsive web pages for each model.
📊 **Explainable Results** — Shows summaries, benefits, eligibility, and application details.
🌐 **Modular Expansion** — Easily extendable to new datasets and models.

---

## 🧩 Folder Structure

<details>
<summary>📂 Click to view full structure</summary>

```bash
Quantum_Public_Policy-Project/
│
├── static/                              → CSS, JS, and static assets
│
├── templates/                           → HTML (Jinja2) templates
│   ├── index.html                       → Main dashboard
│   ├── education.html                   → Education policy model UI
│   ├── poverty.html                     → Poverty analysis UI
│   ├── gov_scheme.html                  → Government scheme interface
│   └── quantum_edu.html                 → Quantum-enhanced policy view
│
├── app/                                 → FastAPI backend logic
│
├── edu_quantum/                         → Quantum education model
├── ind_gov_scheme.NLP/                  → Government scheme NLP logic
├── infosys_nlp/                         → Education NLP engine
├── infosys_nlp_poverty/                 → Poverty NLP engine
│
├── education_policies/                  → Raw education dataset
├── education_policies_quantum/          → Quantum education dataset
├── ind_poverty/                         → Poverty dataset
│
├── train_policies/                      → Training data for education model
├── train_policies_quantum/              → Quantum training data
├── train_poverty/                       → Poverty model training data
├── train_scheme/                        → Government scheme training data
│
├── test_policies/                       → Testing data (education)
├── test_policies_quantum/               → Testing data (quantum)
├── test_poverty/                        → Testing data (poverty)
├── test_scheme/                         → Testing data (schemes)
│
├── updated_data/                        → Cleaned and preprocessed datasets
│
├── policy_tfidf_matrix.pkl
├── policy_tfidf_matrix_quantum.pkl
├── policy_vectorizer.pkl
├── policy_vectorizer_quantum.pkl
├── poverty_tfidf_matrix.pkl
├── poverty_vectorizer.pkl
├── scheme_tfidf_matrix.pkl
├── scheme_vectorizer.pkl
│
├── requirements.txt                     → Python dependencies
├── README.md                            → Project documentation
├── .gitattributes                       → Git configuration
└── venv/                                → Virtual environment
```

</details>

---

## ⚙️ Installation & Setup

### 🧾 1. Clone the Repository

```bash
git clone https://github.com/PradeeshVasu/Quantum_Public_Policy-Project.git
cd Quantum_Public_Policy-Project
```

### 🧱 2. Create a Virtual Environment

```bash
python -m venv venv
# Activate it
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🚀 4. Run the FastAPI Server

```bash
uvicorn app:app --reload
```

### 🌐 5. Open the App

Visit → [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧠 Models Used

| 🧩 Model Type     | ⚙️ Description                                  | 🔬 Technique                             |
| ----------------- | ----------------------------------------------- | ---------------------------------------- |
| **Classical NLP** | Text-based policy recommendation                | TF-IDF + Cosine Similarity               |
| **Quantum NLP**   | Quantum state embedding for semantic similarity | PennyLane (AmplitudeEmbedding + QNode)   |
| **Poverty Model** | Socioeconomic indicators & data analysis        | TF-IDF + NLP                             |
| **Scheme Model**  | Searchable government welfare schemes           | NLP with tagging and metadata extraction |

---

## 💻 Frontend Overview

Built using **HTML**, **CSS**, and **Jinja2**, the frontend includes:

* 🏠 **index.html** → Central dashboard
* 🎓 **education.html** → Classical policy model
* 💡 **quantum_edu.html** → Quantum-enhanced model
* 💰 **poverty.html** → Poverty analytics
* 🏛️ **gov_scheme.html** → Scheme-based recommendations

  ## Project Working Prototye
  
  ### Dashboard

<img width="1912" height="1045" alt="Screenshot 2025-11-26 220839" src="https://github.com/user-attachments/assets/157b3195-ca72-4114-a3b3-7ca8ec318b6f" />


  ### Education_Policy NLP 
  <img width="1908" height="1040" alt="Screenshot 2025-11-26 222922" src="https://github.com/user-attachments/assets/13882ed7-962b-4597-915d-ed62c27dab9b" />
<img width="1879" height="1039" alt="Screenshot 2025-11-26 223322" src="https://github.com/user-attachments/assets/e80188ea-2329-4343-9e22-f152ae616932" />

<img width="1880" height="1043" alt="Screenshot 2025-11-26 223334" src="https://github.com/user-attachments/assets/cef9e84d-674b-4c64-956f-45357a62160d" />

### Indian_Government_Scheme NLP
<img width="1901" height="1035" alt="Screenshot 2025-11-26 222948" src="https://github.com/user-attachments/assets/858e68fb-e318-4cdb-8bd3-226cd359e535" />

<img width="1822" height="1056" alt="Screenshot 2025-10-30 135822" src="https://github.com/user-attachments/assets/12c174c1-2f80-4e9d-bb3e-a3d6f117a679" />
<img width="1883" height="1041" alt="Screenshot 2025-11-26 220718" src="https://github.com/user-attachments/assets/fe749551-8310-4856-b0e6-d5d56dc7e7b4" />

### Poverty_IN_India NLP
<img width="1897" height="1034" alt="Screenshot 2025-11-26 223111" src="https://github.com/user-attachments/assets/e622f2bb-c98e-456e-aa71-648a203dde49" />

<img width="1881" height="1036" alt="Screenshot 2025-11-26 223139" src="https://github.com/user-attachments/assets/b78e07fc-4709-42fb-9cf1-2568e4c07547" />
<img width="1888" height="1036" alt="Screenshot 2025-11-26 223152" src="https://github.com/user-attachments/assets/fd50db07-9efc-4d8b-9351-bb458436dbdc" />


### Quantum_Education_Policy NLP
<img width="1913" height="1038" alt="Screenshot 2025-11-26 223210" src="https://github.com/user-attachments/assets/7112c633-0ba3-4f7a-bd2b-b5103e7c2de0" />

<img width="1844" height="1040" alt="Screenshot 2025-10-30 140149" src="https://github.com/user-attachments/assets/8459c727-4fdb-48fd-af86-1df4f975a623" />
<img width="1887" height="1035" alt="Screenshot 2025-11-26 223226" src="https://github.com/user-attachments/assets/8d3281dc-e3b9-41db-ad65-1ec676b2d5c5" />

Each page dynamically renders FastAPI results using Jinja2 templates.

---

## 📦 Dependencies

| Library               | Purpose                    |
| --------------------- | -------------------------- |
| **FastAPI**           | Backend web framework      |
| **Uvicorn**           | ASGI server                |
| **Scikit-learn**      | TF-IDF, similarity metrics |
| **Pandas**, **NumPy** | Data processing            |
| **PennyLane**         | Quantum circuit simulation |
| **Joblib**            | Model persistence          |
| **Jinja2**            | HTML templating            |

---

## 🔮 Example Workflow

1️⃣ User enters: `"Educational policies for rural development"`
2️⃣ Query is vectorized using **TF-IDF**.
3️⃣ Similarity scores are computed via **Cosine Similarity** and **Quantum Kernel Circuits**.
4️⃣ Top matching policies or schemes are displayed with summaries and metadata.
5️⃣ Results appear in **Education**, **Poverty**, or **Quantum** tabs accordingly.

---

## 🚀 Future Roadmap

* 🤖 **Integrate LLMs (LangChain / GPT) for deeper Q&A**
* 🌏 **Add multilingual support for Indian languages**
* 📊 **Dashboard visualization for impact scores**
* 🧾 **Model performance analytics**
* 🧠 **Hybrid Quantum-Classical embeddings**

---

## 👨‍💻 Author & Contact

**👤 Developer:** *Pradeesh Vasu*                              
📧 **Email:** [pradeeshvasu22@gmail.com](mailto:pradeeshvasu22@gmail.com)                                  
💼 **LinkedIn:** [linkedin.com/in/pradeesh-vasu-03486b319](https://www.linkedin.com/in/pradeesh-vasu-03486b319)                                                    
🐙 **GitHub:** [github.com/PradeeshVasu](https://github.com/PradeeshVasu)

---

## 🏁 License

📝 Licensed under the **MIT License** — Free to use, modify, and distribute with attribution.

---


