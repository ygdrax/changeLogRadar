#!/usr/bin/env python3
"""
ChangeLog Radar - A tool to fetch and display release notes from popular open-source projects.
"""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime, timezone
import json

from src.github_crawler import GitHubCrawler
from src.html_generator import HTMLGenerator
from src.config import PROJECTS

app = typer.Typer(
    name="changelog-radar",
    help="Fetch and display release notes from popular open-source projects",
    rich_markup_mode="rich"
)
console = Console()

@app.command()
def crawl(
    output_dir: Optional[Path] = typer.Option(
        Path("."),
        "--output-dir", "-o",
        help="Output directory for generated files"
    ),
    max_releases: int = typer.Option(
        5,
        "--max-releases", "-n",
        help="Maximum number of releases to fetch per project"
    ),
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Force overwrite existing files"
    )
):
    """
    Crawl GitHub repositories for release notes and generate an HTML index page.
    """
    console.print("[bold blue]ChangeLog Radar[/bold blue]")
    console.print(f"Fetching last {max_releases} releases for {len(PROJECTS)} projects...")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    crawler = GitHubCrawler()
    html_generator = HTMLGenerator()
    
    all_releases = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for project_name, repo_info in PROJECTS.items():
            task = progress.add_task(f"Fetching {project_name}...", total=1)
            
            try:
                releases = crawler.get_releases(
                    repo_info["owner"], 
                    repo_info["repo"], 
                    max_releases
                )
                all_releases[project_name] = {
                    "releases": releases,
                    "repo_url": f"https://github.com/{repo_info['owner']}/{repo_info['repo']}",
                    "description": repo_info.get("description", "")
                }
                console.print(f"SUCCESS {project_name}: {len(releases)} releases fetched")
                
            except Exception as e:
                console.print(f"ERROR {project_name}: Failed to fetch releases - {e}")
                all_releases[project_name] = {
                    "releases": [],
                    "repo_url": f"https://github.com/{repo_info['owner']}/{repo_info['repo']}",
                    "description": repo_info.get("description", ""),
                    "error": str(e)
                }
            
            progress.update(task, completed=1)
    
    # Generate HTML
    console.print("\n[bold green]Generating HTML page...[/bold green]")
    
    html_content = html_generator.generate_index_page(all_releases)
    
    # Save HTML file
    html_file = output_dir / "index.html"
    html_file.write_text(html_content, encoding="utf-8")
    
    # Save JSON data for potential API use
    json_file = output_dir / "releases.json"
    json_data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "projects": all_releases
    }
    json_file.write_text(json.dumps(json_data, indent=2), encoding="utf-8")
    
    console.print("Generated files:")
    console.print(f"   - HTML: {html_file}")
    console.print(f"   - JSON: {json_file}")
    
    console.print(f"\n[bold green]Done! Open {html_file} in your browser to view the results.[/bold green]")
    
    # If generating in root directory, mention GitHub Pages compatibility
    if output_dir == Path("."):
        console.print("[dim]Note: Files generated in root directory are ready for GitHub Pages deployment.[/dim]")

@app.command()
def list_projects():
    """List all configured projects."""
    console.print("[bold blue]Configured Projects[/bold blue]\n")
    
    for project_name, repo_info in PROJECTS.items():
        console.print(f"[bold green]{project_name}[/bold green]")
        console.print(f"   Repository: {repo_info['owner']}/{repo_info['repo']}")
        console.print(f"   URL: https://github.com/{repo_info['owner']}/{repo_info['repo']}")
        if repo_info.get("description"):
            console.print(f"   Description: {repo_info['description']}")
        console.print()

if __name__ == "__main__":
    app()