# SnapPic

## Overview

SnapPic is a web application that allows users to upload images with optional comments. The images are displayed in a gallery and automatically deleted after 15 seconds.

## Features

- Upload images with optional comments.
- View uploaded images in a gallery.
- Images are automatically deleted after 15 seconds.
- Link back to the upload page from the gallery.

## Built With

SnapPic was built using:

- **Aider**: Version 0.85.0 (aider.chat)
- **Model**: Devstral (https://ollama.com/library/devstral, updated 04.07.2025)
- **Hardware**: NVIDIA GeForce RTX 3090 Ti provided by vast.ai
- **Template/Docker Image**: vastai/openwebui "Open Webui (Ollama)"

## Devstral Model Details

**Devstral** is an agentic LLM for software engineering tasks built under a collaboration between [Mistral AI](https://mistral.ai/) and [All Hands AI](https://www.all-hands.dev/) 🙌. Devstral excels at using tools to explore codebases, editing multiple files and powering software engineering agents. The model achieves remarkable performance on SWE-bench which positions it as the #1 open source model.

### Key Features:

- **Agentic coding**: Devstral is designed to excel at agentic coding tasks, making it a great choice for software engineering agents.
- **Lightweight**: with its compact size of just 24 billion parameters, Devstral is light enough to run on a single RTX 4090 or a Mac with 32GB RAM, making it an appropriate model for local deployment and on-device use.
- **Apache 2.0 License**: Open license allowing usage and modification for both commercial and non-commercial purposes.
- **Context Window**: A 128k context window.

### SWE-Bench

Devstral achieves a score of **46.8% on SWE-Bench Verified**, outperforming prior open-source state-of-the-art by 6%.

| Model              | Scaffold             | SWE-Bench Verified (%) |
|--------------------|----------------------|------------------------|
| Devstral           | OpenHands Scaffold   | **46.8**               |
| GPT-4.1-mini       | OpenAI Scaffold      | 23.6                   |
| Claude 3.5 Haiku   | Anthropic Scaffold   | 40.6                   |
| SWE-smith-LM 32B   | SWE-agent Scaffold   | 40.2                   |

When evaluated under the same test scaffold (OpenHands, provided by All Hands AI 🙌), Devstral exceeds far larger models such as Deepseek-V3-0324 and Qwen3 232B-A22B.

In the chart below, we also compare Devstral to closed and open models evaluated under any scaffold (including ones custom for the model). Here, we find that Devstral achieves substantially better performance than a number of closed-source alternatives. For example, Devstral surpasses the recent GPT-4.1-mini by over 20%.

### Reference

[Blog](https://mistral.ai/news/devstral)
