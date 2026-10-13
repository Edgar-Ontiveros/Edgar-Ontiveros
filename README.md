# Edgar Ontiveros

**Machine Learning Engineer and Software Developer** · Physics Engineer · Chihuahua, Mexico

I design, build and deploy production systems: REST APIs, web applications and the machine learning models inside them. I am currently building the internal software platform used across the 11 branches of [Herinox](https://github.com/Herinox), covering sales reporting, quoting, pricing and purchasing on top of SAP data. Before that, I worked on automation and production data systems in the aerospace industry at Safran Aerosystems.

I also take on freelance projects through my independent practice, [Edgar Ontiveros](https://github.com/Edgar-Onti).

[Website](https://edgar-ontiveros.com) · [LinkedIn](https://www.linkedin.com/in/edgaronti) · [Email](mailto:edgarontiverosfm@gmail.com)

---

## Featured projects

### Sales Reporting Platform

*Herinox · In production · Private repository*

Web application that automates the commercial division's sales report from SAP data. It gives the sales director and branch managers sales, budget, profitability, customer and price–volume analysis, with role-based access by branch.

`FastAPI` `SQLAlchemy` `PostgreSQL` `React` `TypeScript` `Docker` `AWS`

### Quotation Management System

*Herinox · In production · Private repository*

Internal platform where sales reps in 11 branches request special-order quotes from purchasing. It measures response times in business hours across time zones and tracks quoted versus confirmed revenue by branch, buyer, sales rep and customer. Includes database migrations, a background scheduler, tests against a real PostgreSQL instance and CI/CD.

`FastAPI` `SQLAlchemy` `PostgreSQL` `React` `TypeScript` `Mantine` `Docker` `GitHub Actions`

### Automated Pricing Engine

*Herinox · In production · Private repository*

Turns SAP master data into branch price lists, cost sheets and variance reports under supplier-priority rules and fail-closed validation. Migrated from a Streamlit prototype to FastAPI and React, keeping the original pipeline frozen as a parity reference so the new version produces identical output.

`FastAPI` `pandas` `openpyxl` `React` `Mantine` `Docker`

### [Melanoma Triage](https://github.com/Edgar-Ontiveros/melanoma-triage)

*Thesis project · Public repository*

Skin-lesion classifier trained on ISIC 2020. EfficientNetV2-S was selected from a model comparison with patient-level splits and a locked test set. Grad-CAM explainability is validated with sanity checks, and the model is packaged in ONNX with verified PyTorch parity, served by a FastAPI and ONNX Runtime API in a 152 MB Docker image with a React interface. Clinical evaluation is in progress. It is an educational triage aid, not a diagnostic device.

`PyTorch` `Lightning` `timm` `Hydra` `ONNX Runtime` `FastAPI` `React` `Docker` `GitHub Actions`

### More projects

- [SAP Article Code Generator](https://github.com/Edgar-Ontiveros/Generador-de-Codigos): infers SAP codes, product hierarchy, unit of measure and weight for new items from similar historical records. FastAPI, scikit-learn, RapidFuzz, AWS EC2.
- [Purchase Order Processor](https://github.com/Edgar-Ontiveros/Ordenes-Compra): parses CFDI XML invoices and PDF proformas into SAP-ready Excel files. FastAPI, Pydantic, lxml, pdfplumber; 97 tests.
- [Sales Discount Analytics](https://github.com/Edgar-Ontiveros/app-descuentos): ETL pipeline and Streamlit dashboard reconciled to the cent against the manual Excel report. pandas, Streamlit, Plotly.
- [edgar-ontiveros.com](https://github.com/Edgar-Ontiveros/edgar-ontiveros.com): personal website. React, TypeScript, Vite, Tailwind CSS, Cloudflare Pages.

---

## Technical stack

| Area | Technologies |
| --- | --- |
| Languages | Python, TypeScript, SQL |
| Backend | FastAPI, Pydantic, SQLAlchemy, Alembic, Django |
| Databases | PostgreSQL, SAP HANA, SQLite, Supabase |
| Machine learning | PyTorch, Lightning, timm, scikit-learn, TensorFlow, Keras, ONNX Runtime |
| Data and BI | pandas, NumPy, Streamlit, Power BI |
| Frontend | React, Vite, Tailwind CSS, Mantine, TanStack Query |
| Cloud and DevOps | AWS, Docker, GitHub Actions, nginx, Linux |
| Quality | pytest, Ruff, mypy |

---

Open to freelance projects and new opportunities. Reach me by [email](mailto:edgarontiverosfm@gmail.com) or through [my website](https://edgar-ontiveros.com).
