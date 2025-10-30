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

✅ **Policy Search Engine** — Retrieve government policies using natural language
⚡ **Quantum + Classical NLP** — Compare QML and TF-IDF retrievals
🧭 **FastAPI Backend** — High-performance REST server
🎨 **Interactive Frontend** — Jinja2 responsive templates
📊 **Explainable Results** — Summaries, eligibility, application details
🌐 **Modular Expansion** — Extendable to new datasets and models

---

## 🖼️ Live Demo & Screenshots

> Add your screenshots or demo GIFs inside an `assets/` or `docs/` folder.
> Example layout shown below — replace image names with your own.

| 🏠 Dashboard                       | 🎓 Education NLP                         | ⚛️ Quantum Education NLP                |
| ---------------------------------- | ---------------------------------------- | ------------------------------------ |
| ![Dashboard](images/index_page.png) | ![Education](images/education_policy.png) | ![Quantum](images\quantum_edu_policy.png) |

| 💰 Poverty NLP                       | 🏛️ Government_Scheme NLP                  |                 
| ------------------------------------ | ---------------------------------- | 
| ![Poverty](images/poverty.png) | ![Scheme](images/government_scheme.png) | 



## ⚙️ Installation & Setup

```bash
git clone https://github.com/PradeeshVasu/Quantum_Public_Policy-Project.git
cd Quantum_Public_Policy-Project
python -m venv venv
venv\Scripts\activate          # Windows
# or
source venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
uvicorn app:app --reload
```

Visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 🧠 Model Overview

| Model             | Description                                     | Technique                              |
| ----------------- | ----------------------------------------------- | -------------------------------------- |
| **Classical NLP** | Text-based recommendation                       | TF-IDF + Cosine Similarity             |
| **Quantum NLP**   | Quantum state embedding for semantic similarity | PennyLane (AmplitudeEmbedding + QNode) |
| **Poverty Model** | Socioeconomic analysis                          | TF-IDF + NLP                           |
| **Scheme Model**  | Government welfare search                       | NLP tagging + metadata extraction      |

---

## 🧩 Folder Structure

<details>
<summary>Click to expand</summary>

```bash
Quantum_Public_Policy-Project/
├── app/                     → FastAPI backend
├── templates/               → HTML UIs (education, poverty, quantum, scheme)
├── static/                  → CSS/JS assets
├── *tfidf_matrix.pkl        → Saved TF-IDF vectors
├── *vectorizer.pkl          → Trained vectorizers
├── requirements.txt
├── README.md
└── venv/
```

</details>

---

## 🧾 Example Flow

1️⃣ User query → “Educational policies for rural development”
2️⃣ TF-IDF + Quantum vectors generated
3️⃣ Similarities computed (cosine + quantum kernel)
4️⃣ Top matching policies returned with explanations

---

## 🚀 Future Roadmap

* 🤖 **LLM integration** (LangChain / GPT)
* 🌏 **Multilingual policy search**
* 📊 **Impact visualization dashboard**
* 🧠 **Hybrid Quantum-Classical embeddings**
* 🧾 **Performance analytics module**

---

## 👨‍💻 Author

**Pradeesh Vasu**
📧 [pradeeshvasu22@gmail.com](mailto:pradeeshvasu22@gmail.com)
💼 [linkedin.com/in/pradeesh-vasu-03486b319](https://www.linkedin.com/in/pradeesh-vasu-03486b319)
🐙 [github.com/PradeeshVasu](https://github.com/PradeeshVasu)

---

## 🏁 License

Licensed under the **MIT License** — free for use and modification with attribution.

