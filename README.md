# AgileAI: Cognitive Load-Aware Project Management

AgileAI is an AI-powered system that automatically converts project descriptions into **Epics → Features → User Stories**, helping streamline Agile planning.  
The system includes a Gradio frontend, a TinyLLaMA inference model, performance monitoring, and a fully containerized local deployment setup.  
Initial experiments were done with GPT-2, and the final model uses TinyLLaMA for improved structure and accuracy.

---

## 1. Project Overview

AgileAI simplifies early-stage Agile decomposition by using an LLM to understand project requirements and generate structured Agile artifacts.

**Key Features:**
- Automatic generation of Epics, Features, and User Stories  
- Interactive review and feedback (thumbs-up/down)  
- Local monitoring using Prometheus and Grafana  
- Local, Docker-based deployment  
- Planned Azure DevOps integration (automatic work item creation)

---

## 2. Repository Contents

app/ → Gradio frontend (UI) data/ → datasets, cleaned text, training data templates/ → universal + domain-specific prompt templates training_eg/ → example project descriptions for model training playground1.ipynb→ main notebook for model development and inference deployment/ → Dockerfile and docker-compose setup monitoring/ → Prometheus + Grafana configuration documentation/ → final project report (single file) videos/ → demo video of the complete system


**Documentation Folder:**
- `AIS_Shrimayee.pdf` — full project report (proposal, development, data, deployment, monitoring, HCI, risks, evaluation)

---

## 3. System Entry Point

**Notebook entry point:**  
`playground1.ipynb`

Includes:
- GPT-2 experiments  
- TinyLLaMA fine-tuning  
- Inference pipeline  
- Prompt engineering  
- Evaluation workflow  

## 4. Video Demo
Will be available soon

## 5. Deployment Strategy
5. Deployment Strategy
AgileAI uses a local, multi-container Docker deployment with:
- Model container – TinyLLaMA inference
- Frontend container – Gradio UI
- Prometheus container – collects system metrics
- Grafana container – visualizes performance + feedback

docker-compose up --build

Services:

Gradio → http://localhost:7860

Prometheus → http://localhost:9090

Grafana → http://localhost:3000

## 6. Monitoring and Metrics
Tools:
- Prometheus
- Grafana

Metrics tracked:
- Inference latency (main metric)
- Request counts
- CPU/memory usage
- User feedback (thumbs up/down)
  
Monitoring configuration files are located in the monitoring/ folder.

## 7. Project Documentation
All system documentation is contained in a single file: documentation/AIS_Shrimayee.pdf

## 8. Version Control and Collaboration
Version control practices used in this project:
- main branch holds stable updates
- Clear commit messages document incremental progress
- Notebook checkpoints and Docker updates tracked in Git history

Future Enhancements:
- Azure DevOps integration
- Sprint planning model
  
