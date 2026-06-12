# AI-Powered Research Report Maker

A multi-agent AI system that autonomously searches the web, scrapes sources, writes structured research reports, and critiques its own output.

## Architecture

```
User Input (Topic)
      ↓
Search Agent (Tavily) → finds top web results
      ↓
Reader Agent (BeautifulSoup) → scrapes top URLs
      ↓
Writer Chain (Mistral LLM) → generates structured report
      ↓
Critic Chain (Mistral LLM) → reviews and scores the report
      ↓
Final Output (Report + Feedback)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Mistral (via LangChain) |
| Agents | LangGraph (create_react_agent) |
| Search | Tavily API |
| Scraping | BeautifulSoup4 |
| Backend | FastAPI |
| Frontend | Streamlit |
| Containerization | Docker + Docker Compose |
| Deployment | AWS EC2 (t3.small) |

## Features

- Multi-agent pipeline with 4 distinct roles
- User-provided API keys (no hardcoded secrets)
- Dockerized full-stack deployment
- Live on AWS EC2

## Quick Start

### Prerequisites
- Mistral API key (console.mistral.ai)
- Tavily API key (tavily.com)

### Run Locally

```bash
git clone https://github.com/DeepanshuSharma1607/Ai-Powered-Research-Report-Maker.git
cd Ai-Powered-Research-Report-Maker
docker compose up --build
```

- Frontend: http://localhost:8501
- Backend: http://localhost:8000/docs

### Usage

1. Open the Streamlit UI
2. Enter your Mistral and Tavily API keys in the sidebar
3. Type a research topic
4. Click Generate — report arrives in ~60 seconds

## Docker Hub

```bash
docker pull deepanshu1607/research-backend:v1
docker pull deepanshu1607/research-frontend:v1
```

## Live Demo

http://13.49.183.32:8501 *(active for limited time)*

## Project Structure

```
├── agents.py          # LangGraph agent definitions
├── tools.py           # Web search + URL scraper tools
├── pipeline.py        # 4-step research pipeline
├── app_backend.py     # FastAPI backend
├── app.py             # Streamlit frontend
├── Dockerfile.backend
├── Dockerfile.frontend
└── docker-compose.yml
```

## Author

Deepanshu Sharma — [GitHub](https://github.com/DeepanshuSharma1607)
