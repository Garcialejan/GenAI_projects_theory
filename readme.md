# 🧠 GenAI Research & Projects

A curated collection of projects, experiments, and theoretical explorations in **Generative AI (GenAI)**, with a focus on practical applications using open-source and cloud-native technologies.

## 🎯 Focus Areas

- **Retrieval-Augmented Generation (RAG)** systems
- **AI Agents** with autonomous reasoning and tool use
- **Foundational Large Language Models (LLMs)** from Hugging-Face
- **Embedding pipelines** using Hugging-Face Transformers and LangChain
- **Cloud-native deployment** and orchestration on **AWS**

## 🛠️ Core Technologies

- **Models**: Hugging-Face Transformers, foundational LLMs (e.g., GPT, Llama, Mistral, Zephyr, etc.)
- **Embeddings & Orchestration**: LangChain, Hugging-Face Sentence Transformers
- **Cloud Platform**: AWS (S3, Bedrock, Lambda, ECS/EKS, SageMaker)
- **Evaluation & Monitoring**: Custom metrics, LangSmith (optional), Weights & Biases
- **Agent Frameworks**: LangGraph, CrewAI, or custom agent loops

## 📂 Repository Structure

genai-research/
├── rag/ # RAG implementations (dense/sparse/hybrid retrieval)
├── agents/ # AI agent designs and multi-agent workflows
├── embeddings/ # Embedding model comparisons and pipelines
├── llm_evaluation/ # Benchmarks and qualitative assessments
├── aws/ # AWS-specific deployment templates (CDK/CloudFormation)
├── notebooks/ # Exploratory Jupyter notebooks
└── docs/ # Theory notes, architecture diagrams, and references

## ☁️ AWS Integration
This repo leverages AWS services for scalable, secure GenAI applications:

- **S3**: Store documents and vector indexes
- **Bedrock (optional)**: Compare open-source models with AWS-provided LLMs
- **Lambda/ECS**: Serve inference endpoints or agent workflows
- **IAM & Secrets Manager**: Secure model and API access
- **Infrastructure-as-Code (IaC) templates** using **AWS CDK** are provided in the aws/ directory.

## 📚 Theory & References
See the docs/ folder for:

- Comparative analysis of embedding models
- RAG architecture patterns
- Agent design principles
- Cost/performance trade-offs on AWS


This repository is a living lab—expect frequent updates as GenAI evolves.