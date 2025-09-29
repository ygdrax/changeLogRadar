# ChangeLog Radar 🔍

A Python CLI tool that scrapes release notes from popular open source projects and generates a structured index.yaml file for tracking changes.

## Features

- 🚀 Tracks releases from major open source projects:
  - Kubernetes
  - vLLM 
  - TensorFlow
  - Ruff
  - uv
- 📄 Generates structured YAML index with release metadata
- ⚡ Built with Typer for a rich CLI experience
- 🤖 Automated daily updates via GitHub Actions
- 🔑 GitHub API integration with rate limit monitoring

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
# Clone the repository
git clone <your-repo-url>
cd changeLogRadar

# Install dependencies
uv sync
```

## Usage

### Basic Commands

```bash
# Scrape latest releases and generate index.yaml
uv run python main.py scrape

# Scrape with custom limit (default: 5 releases per repo)
uv run python main.py scrape --limit 10

# Show tracked repositories
uv run python main.py repos

# Show status and rate limits
uv run python main.py status

# Get help
uv run python main.py --help
```

### GitHub Token (Optional)

For higher rate limits, set a GitHub personal access token:

```bash
export GITHUB_TOKEN=your_token_here
# or pass it directly
uv run python main.py scrape --token your_token_here
```

## Output

The tool generates an `index.yaml` file with the following structure:

```yaml
metadata:
  generated_at: '2025-09-29T18:54:04.709664'
  version: '1.0'
  description: ChangeLog Radar - Open Source Release Tracker
repositories:
  kubernetes_kubernetes:
    name: kubernetes/kubernetes
    total_releases: 5
    latest_releases:
      - tag: v1.34.1
        name: Kubernetes v1.34.1
        published_at: '2025-09-10T03:28:09+00:00'
        url: https://github.com/kubernetes/kubernetes/releases/tag/v1.34.1
        is_prerelease: false
        body_preview: "Release notes preview..."
```

## Automation

The project includes a GitHub Action that runs daily at 6:00 AM UTC to automatically update the index.yaml file. The workflow:

- Fetches latest releases
- Generates updated index.yaml
- Commits changes if any updates are found
- Uploads the index as an artifact

## Development

### Project Structure

```
├── main.py              # CLI application entry point
├── scrapper.py          # GitHub release scraping logic  
├── yaml_generator.py    # YAML generation utilities
├── pyproject.toml       # Project dependencies
└── .github/workflows/   # GitHub Action automation
    └── daily-scrape.yml
```

### Adding New Repositories

To track additional repositories, edit the `REPOSITORIES` list in `scrapper.py`:

```python
REPOSITORIES = [
    "kubernetes/kubernetes",
    "vllm-project/vllm", 
    "tensorflow/tensorflow",
    "astral-sh/ruff",
    "astral-sh/uv",
    "your-org/your-repo"  # Add new repos here
]
```

## License

This project is a POC (Proof of Concept) for demonstration purposes.
