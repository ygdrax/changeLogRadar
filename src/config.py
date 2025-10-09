"""
Configuration file for ChangeLog Radar.
Contains project definitions and settings.
"""

# Project configurations
PROJECTS = {
    "vLLM": {
        "owner": "vllm-project",
        "repo": "vllm",
        "description": "A high-throughput and memory-efficient inference and serving engine for LLMs"
    },
    "uv": {
        "owner": "astral-sh",
        "repo": "uv",
        "description": "An extremely fast Python package and project manager, written in Rust"
    },
    "Ruff": {
        "owner": "astral-sh", 
        "repo": "ruff",
        "description": "An extremely fast Python linter and code formatter, written in Rust"
    },
    "Kubernetes": {
        "owner": "kubernetes",
        "repo": "kubernetes",
        "description": "Production-Grade Container Scheduling and Management"
    },
    "Homebrew": {
        "owner": "Homebrew",
        "repo": "brew",
        "description": "The Missing Package Manager for macOS (or Linux)"
    },
    "FastAPI": {
        "owner": "fastapi",
        "repo": "fastapi", 
        "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production"
    },
    "Polars": {
        "owner": "pola-rs",
        "repo": "polars",
        "description": "Dataframes powered by a multithreaded, vectorized query engine, written in Rust"
    },
    "Typer": {
        "owner": "fastapi",
        "repo": "typer",
        "description": "Typer, build great CLIs. Easy to code. Based on Python type hints"
    },
    "Helm": {
        "owner": "helm",
        "repo": "helm",
        "description": "The Kubernetes Package Manager"
    },
    "kubectx": {
        "owner": "ahmetb",
        "repo": "kubectx",
        "description": "Faster way to switch between clusters and namespaces in kubectl"
    }
}

# GitHub API settings
GITHUB_API_BASE_URL = "https://api.github.com"
RELEASES_PER_PAGE = 10
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds

# HTML generation settings
HTML_TITLE = "ChangeLog Radar - Open Source Release Notes"
HTML_DESCRIPTION = "Stay updated with the latest releases from popular open-source projects"