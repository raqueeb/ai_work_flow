# Enterprise AI Automations Documentation

Welcome to the Enterprise AI Automations documentation. This site is built for ISP/Service Company and enterprise teams who want to understand how local LLMs can replace rule-based systems and act as the "brain" behind everyday applications. But, we want to start with baby steps.

All guides here use **local LLM setups** via LM Studio, keeping your data private and your work to be delivered fast.

## Quick Links

- [Why Local Inference?](why-local-inference.md)
- [Getting Started with Qwen 2.5](getting-started-qwen.md)
- [Qwen 2.5 Demos](qwen-demos.md)
- [Streamlit Applications](streamlit-apps.md)
- [ISP Classification (Qwen)](isp-classification-qwen.md)
- [Stress Testing (Qwen)](stress-testing-qwen.md)
- [Upgrading to Gemma 4 E4B](upgrading-to-gemma.md)
- [Gemma 4 E4B Demos](gemma-demos.md)
- [ISP Classification (Gemma)](isp-classification-gemma.md)
- [Network Monitoring](network-monitoring.md)
- [Cybersecurity Analysis](cybersec-analysis.md)
- [Advanced Reasoning](advanced-reasoning.md)
- [MCP Servers](mcp-servers.md)
- [Enterprise Applications](enterprise-apps.md)
- [Model Comparison](model-comparison.md)

## বাংলা ডকুমেন্টেশন

এই ডকুমেন্টেশনটি বাংলাতেও পাওয়া যায়: [বাংলা হোম](bangla/index.md)

## Overview

This documentation covers the full lifecycle of local LLM-powered applications:

- **Installation** of LM Studio and required Python packages
- **Configuration** of the local LLM server (`http://localhost:1234`)
- **Running** scripts and Streamlit apps (`streamlit run app-name.py`)
- **Extending** the scripts with custom prompts, rules, or additional models
- **Deploying** the documentation site to GitHub Pages for easy sharing

---

### Documentation Structure

The documentation is organized into thematic sections that correspond to the main Python scripts in the repository. Each section includes:

- A brief description of the script's purpose
- Installation and configuration steps
- Example command-line usage
- Sample output and interpretation
- Tips for extending or customizing the script

Feel free to explore sections in order, or jump directly to the topic matching your current learning goal.

---

### Key Features

- **Privacy-First**: All processing happens locally — no data leaves your machine
- **Model Flexibility**: Supports both Qwen2.5-1.5B and Google Gemma 4 E4B models
- **Educational**: Designed for teaching students and team members about local LLM inference
- **Practical**: Real-world ISP automation use cases with working code
- **Well-Documented**: Comprehensive guides for each component
- **Streamlit-Powered**: Interactive web dashboards that anyone can run without deep coding experience

---

*Start with [Why Local Inference?](why-local-inference.md) to understand the shift from rule-based to brain-based systems, then follow the Qwen-specific guide to set up your environment.*

---
I am Rakibul Hassan, CTO of Link3 Technologies, the leading ISP (Internet Service Provider) in Bangladesh. This repository is where I do my tinkering — a production-ready collection of local LLM-powered enterprise automations built for an ISP/Telecom environment.