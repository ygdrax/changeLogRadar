"""
GitHub Release Scrapper Module

This module fetches release notes from specified GitHub repositories.
"""
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
import requests
from github import Github


@dataclass
class Release:
    """Data class for representing a release."""
    repo_name: str
    tag_name: str
    name: str
    published_at: datetime
    body: str
    html_url: str
    is_prerelease: bool


class GitHubScrapper:
    """Scrapper for fetching release notes from GitHub repositories."""
    
    # List of repositories to track
    REPOSITORIES = [
        "kubernetes/kubernetes",
        "vllm-project/vllm", 
        "tensorflow/tensorflow",
        "astral-sh/ruff",
        "astral-sh/uv"
    ]
    
    def __init__(self, github_token: Optional[str] = None):
        """Initialize the scrapper with optional GitHub token for higher rate limits."""
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        if self.github_token:
            self.github = Github(self.github_token)
        else:
            self.github = Github()  # Anonymous access with lower rate limits
    
    def fetch_latest_releases(self, limit: int = 5) -> Dict[str, List[Release]]:
        """
        Fetch the latest releases for all tracked repositories.
        
        Args:
            limit: Number of latest releases to fetch per repository
            
        Returns:
            Dictionary mapping repository name to list of releases
        """
        all_releases = {}
        
        for repo_name in self.REPOSITORIES:
            try:
                print(f"Fetching releases for {repo_name}...")
                releases = self._fetch_repo_releases(repo_name, limit)
                all_releases[repo_name] = releases
            except Exception as e:
                print(f"Error fetching releases for {repo_name}: {e}")
                all_releases[repo_name] = []
        
        return all_releases
    
    def _fetch_repo_releases(self, repo_name: str, limit: int) -> List[Release]:
        """
        Fetch releases for a specific repository.
        
        Args:
            repo_name: Repository name in format "owner/repo"
            limit: Number of releases to fetch
            
        Returns:
            List of Release objects
        """
        releases = []
        
        try:
            repo = self.github.get_repo(repo_name)
            github_releases = repo.get_releases()
            
            count = 0
            for release in github_releases:
                if count >= limit:
                    break
                
                # Skip draft releases and pre-releases for main tracking
                if release.draft:
                    continue
                    
                # Only include releases that have actual tag names (not just commit hashes)
                if not release.tag_name or release.tag_name.startswith('commit-'):
                    continue
                
                releases.append(Release(
                    repo_name=repo_name,
                    tag_name=release.tag_name,
                    name=release.name or release.tag_name,
                    published_at=release.published_at,
                    body=release.body or "",
                    html_url=release.html_url,
                    is_prerelease=release.prerelease
                ))
                count += 1
                
        except Exception as e:
            print(f"Error fetching releases from {repo_name}: {e}")
            # For unauthenticated access, we might hit rate limits
            if "rate limit" in str(e).lower():
                print(f"Rate limit hit for {repo_name}. Consider using GITHUB_TOKEN for higher limits.")
        
        return releases
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get current GitHub API rate limit information."""
        try:
            rate_limit = self.github.get_rate_limit()
            # Handle different PyGithub versions and rate limit structure
            if hasattr(rate_limit, 'core'):
                core = rate_limit.core
            else:
                # Fallback for older versions
                core = rate_limit
            
            return {
                "core": {
                    "limit": getattr(core, 'limit', 'Unknown'),
                    "remaining": getattr(core, 'remaining', 'Unknown'),
                    "reset": str(getattr(core, 'reset', 'Unknown'))
                }
            }
        except Exception as e:
            # Fallback for unauthenticated access or API issues
            return {
                "core": {
                    "limit": "Unknown",
                    "remaining": "Unknown", 
                    "reset": "Unknown"
                },
                "error": f"Rate limit unavailable: {str(e)}"
            }