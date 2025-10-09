# ChangeLog Radar

A Python CLI tool that automatically crawls and displays release notes from popular open-source projects. Built with Typer and designed to run in GitHub Actions with GitHub Pages deployment.

## Features

- **Multi-project tracking**: Monitors 10 popular open-source projects including vLLM, uv, Ruff, Kubernetes, Homebrew, FastAPI, Polars, Typer, Helm, and kubectx
- **Beautiful HTML output**: Generates a responsive, mobile-friendly index page
- **Markdown rendering**: Converts GitHub release notes from Markdown to properly formatted HTML
- **GitHub Actions integration**: Automated daily updates via GitHub workflows
- **GitHub Pages deployment**: Automatically publishes to GitHub Pages
- **JSON API**: Provides structured data in JSON format
- **Rate limiting**: Handles GitHub API rate limits gracefully
- **Error handling**: Robust error handling and retry mechanisms
- **Rich CLI**: Beautiful command-line interface with progress bars

## Quick Start

### Prerequisites

- Python 3.13+
- pip package manager
- Git
- GitHub account (for Actions and Pages)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/changeLogRadar.git
cd changeLogRadar
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

Or install from PyPI (when published):
```bash
pip install changelog-radar
```

### Usage

#### Basic usage:
```bash
# Generate index.html and releases.json in current directory
python main.py crawl
```

#### Advanced options:
```bash
# Specify custom output directory
python main.py crawl --output-dir ./custom-output

# Limit number of releases per project  
python main.py crawl --max-releases 3

# Force overwrite existing files
python main.py crawl --force

# List all configured projects
python main.py list-projects
```

#### Command help:
```bash
python main.py --help
python main.py crawl --help
```

## Project Structure

```
changeLogRadar/
├── .github/
│   └── workflows/
│       └── update-changelog.yml    # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   ├── config.py                   # Project configurations
│   ├── github_crawler.py          # GitHub API client
│   └── html_generator.py          # HTML template generator
├── tests/                         # Test files
│   ├── __init__.py
│   └── conftest.py
├── index.html                     # Generated HTML (GitHub Pages)
├── releases.json                  # Generated JSON data
├── main.py                        # CLI entry point
├── pyproject.toml                 # Project configuration
└── README.md
```

## Configuration

### Projects Configuration

Edit `src/config.py` to add or modify tracked projects:

```python
PROJECTS = {
    "Project Name": {
        "owner": "github-owner",
        "repo": "repository-name", 
        "description": "Project description"
    }
}
```

### GitHub Token (Optional)

For higher rate limits, set the `GITHUB_TOKEN` environment variable:

```bash
export GITHUB_TOKEN=your_personal_access_token
```

## GitHub Actions Setup

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" section  
3. Set source to "GitHub Actions"
4. The generated `index.html` will be served from the root directory

### 2. Workflow Configuration

The included workflow (`.github/workflows/update-changelog.yml`) will:
- Run daily at 6:00 AM UTC
- Fetch latest releases for all configured projects
- Generate updated HTML and JSON files
- Commit changes to the repository
- Deploy to GitHub Pages

### 3. Manual Trigger

You can manually trigger the workflow from the Actions tab in your GitHub repository.

## Customization

### HTML Styling

Modify the CSS in `src/html_generator.py` to customize the appearance:
- Colors and gradients
- Typography and spacing
- Layout and responsiveness
- Animation effects

### Adding New Projects

1. Add project configuration in `src/config.py`
2. Ensure the project has GitHub releases
3. Test locally before deploying

### Rate Limiting

The crawler includes built-in rate limiting and retry logic. For heavy usage:
- Use a GitHub personal access token
- Adjust `MAX_RETRIES` and `RETRY_DELAY` in `src/config.py`

## Output

### HTML Page Features

- **Responsive design**: Works on desktop, tablet, and mobile
- **Project cards**: Each project displayed in a clean card layout  
- **Release information**: Version, date, author, and description
- **Markdown rendering**: Release notes are properly formatted with headings, lists, code blocks, and tables
- **Statistics**: Total projects, releases, and success rate
- **Direct links**: Links to GitHub releases and repositories
- **Error handling**: Displays errors gracefully when projects fail to load

### JSON API

The generated `releases.json` provides structured data for:
- API integrations
- Custom dashboard development
- Data analysis and reporting

## Development

### Running Tests

```bash
# Test the crawler functionality
python main.py crawl --max-releases 1

# Check project configurations
python main.py list-projects
```

### Local Development

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run with development settings  
python main.py crawl --output-dir ./test-output --max-releases 2

# Serve locally (requires Python 3.13+)
python -m http.server 8000
# Open http://localhost:8000
```

### Code Quality

The project includes modern Python tooling for code quality:

```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Type checking with MyPy
mypy src/

# Run tests
pytest
```

### Adding Features

1. **New data sources**: Extend `GitHubCrawler` for additional APIs
2. **Output formats**: Add new generators alongside `HTMLGenerator`
3. **Filters**: Add project filtering and search capabilities
4. **Analytics**: Integrate tracking and metrics

## Monitored Projects

Current projects being tracked:

| Project | Description |
|---------|-------------|
| **vLLM** | High-throughput LLM inference engine |
| **uv** | Extremely fast Python package manager |
| **Ruff** | Fast Python linter and formatter |
| **Kubernetes** | Container orchestration platform |
| **Homebrew** | Package manager for macOS/Linux |
| **FastAPI** | Modern Python web framework |
| **Polars** | Fast DataFrame library |
| **Typer** | CLI framework for Python |
| **Helm** | Kubernetes package manager |
| **kubectx** | Faster way to switch between clusters and namespaces in kubectl |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Links

- **Live Demo**: [Your GitHub Pages URL]
- **Repository**: [GitHub Repository URL]
- **Issues**: [GitHub Issues URL]

---

Built using Python, Typer, and GitHub Actions.
