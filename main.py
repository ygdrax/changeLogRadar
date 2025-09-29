#!/usr/bin/env python3
"""
ChangeLog Radar - GitHub Release Scrapper

A CLI tool to scrape release notes from popular open source projects
and generate an index.yaml file for tracking changes.
"""
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from scrapper import GitHubScrapper
from yaml_generator import YAMLGenerator

app = typer.Typer(
    name="changelogradar",
    help="Track release notes from popular open source projects",
    add_completion=False
)

console = Console()


@app.command()
def scrape(
    output: str = typer.Option(
        "index.yaml", 
        "--output", 
        "-o", 
        help="Output file path for the generated index.yaml"
    ),
    limit: int = typer.Option(
        5, 
        "--limit", 
        "-l", 
        help="Number of latest releases to fetch per repository",
        min=1,
        max=20
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        "-t", 
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )
) -> None:
    """Scrape release notes and generate index.yaml file."""
    
    console.print("🔍 Starting ChangeLog Radar scrape...", style="bold blue")
    
    # Initialize scrapper
    scrapper = GitHubScrapper(github_token=token)
    
    # Show rate limit info
    try:
        rate_info = scrapper.get_rate_limit_info()
        if "error" in rate_info:
            console.print(f"Warning: Could not fetch rate limit info: {rate_info['error']}", style="yellow")
        else:
            console.print(f"GitHub API Rate Limit: {rate_info['core']['remaining']}/{rate_info['core']['limit']} remaining")
    except Exception as e:
        console.print(f"Warning: Could not fetch rate limit info: {e}", style="yellow")
    
    # Fetch releases
    console.print(f"Fetching latest {limit} releases from tracked repositories...")
    releases_data = scrapper.fetch_latest_releases(limit=limit)
    
    # Display summary
    total_releases = sum(len(releases) for releases in releases_data.values())
    console.print(f"✅ Fetched {total_releases} releases from {len(releases_data)} repositories")
    
    # Generate index.yaml
    generator = YAMLGenerator()
    index_data = generator.generate_index(releases_data)
    generator.save_to_file(index_data, output)
    
    console.print(f"📄 Index file generated: {output}", style="bold green")


@app.command()
def status() -> None:
    """Show status of tracked repositories and rate limits."""
    
    console.print("📊 ChangeLog Radar Status", style="bold")
    
    scrapper = GitHubScrapper()
    
    # Show tracked repositories
    table = Table(title="Tracked Repositories")
    table.add_column("Repository", style="cyan")
    table.add_column("Status", style="green")
    
    for repo in scrapper.REPOSITORIES:
        table.add_row(repo, "✅ Active")
    
    console.print(table)
    
    # Show rate limit
    try:
        rate_info = scrapper.get_rate_limit_info()
        if "error" in rate_info:
            console.print(f"❌ Error fetching rate limit: {rate_info['error']}", style="red")
        else:
            console.print(f"\n🔑 GitHub API Rate Limit: {rate_info['core']['remaining']}/{rate_info['core']['limit']}")
            console.print(f"⏰ Reset time: {rate_info['core']['reset']}")
    except Exception as e:
        console.print(f"❌ Error fetching rate limit: {e}", style="red")


@app.command()
def repos() -> None:
    """List all tracked repositories."""
    scrapper = GitHubScrapper()
    
    console.print("📦 Tracked Repositories:", style="bold")
    for i, repo in enumerate(scrapper.REPOSITORIES, 1):
        console.print(f"  {i}. {repo}")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
