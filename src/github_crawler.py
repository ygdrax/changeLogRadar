"""
GitHub API crawler for fetching release information.
"""

import requests
import time
from typing import List, Dict, Optional
from datetime import datetime, timezone
from dateutil.parser import parse as parse_date

from .config import GITHUB_API_BASE_URL, MAX_RETRIES, RETRY_DELAY


class GitHubCrawler:
    """GitHub API client for fetching release information."""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub crawler.
        
        Args:
            token: Optional GitHub personal access token for higher rate limits
        """
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})
        
        # Set User-Agent header
        self.session.headers.update({
            "User-Agent": "ChangeLog-Radar/1.0",
            "Accept": "application/vnd.github.v3+json"
        })
    
    def get_releases(self, owner: str, repo: str, max_releases: int = 5) -> List[Dict]:
        """
        Fetch releases for a given repository.
        
        Args:
            owner: Repository owner/organization
            repo: Repository name
            max_releases: Maximum number of releases to fetch
            
        Returns:
            List of release dictionaries
        """
        url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/releases"
        params = {
            "per_page": min(max_releases, 100),
            "page": 1
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                releases_data = response.json()
                
                # Process and format releases
                releases = []
                for release_data in releases_data[:max_releases]:
                    # Skip drafts
                    if release_data.get("draft", False):
                        continue
                        
                    release = self._format_release(release_data)
                    releases.append(release)
                
                return releases
                
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    raise requests.exceptions.RequestException(f"Failed to fetch releases after {MAX_RETRIES} attempts: {e}")
                
                time.sleep(RETRY_DELAY * (attempt + 1))
        
        return []
    
    def _format_release(self, release_data: Dict) -> Dict:
        """
        Format raw GitHub release data into a cleaner structure.
        
        Args:
            release_data: Raw release data from GitHub API
            
        Returns:
            Formatted release dictionary
        """
        # Parse the published date
        published_at = None
        if release_data.get("published_at"):
            published_at = parse_date(release_data["published_at"])
        
        # Clean up the body text
        body = release_data.get("body", "").strip()
        
        # Extract version from tag_name if available
        tag_name = release_data.get("tag_name", "")
        version = tag_name
        
        # Try to clean up version number
        if tag_name.startswith("v"):
            version = tag_name[1:]
        
        return {
            "name": release_data.get("name") or tag_name,
            "tag_name": tag_name,
            "version": version,
            "body": body,
            "html_url": release_data.get("html_url", ""),
            "published_at_str": published_at.strftime("%Y-%m-%d %H:%M UTC") if published_at else "Unknown",
            "published_date": published_at.strftime("%Y-%m-%d") if published_at else "Unknown",
            "prerelease": release_data.get("prerelease", False),
            "author": {
                "login": release_data.get("author", {}).get("login", "Unknown"),
                "html_url": release_data.get("author", {}).get("html_url", "")
            },
            "assets_count": len(release_data.get("assets", [])),
            "download_count": sum(asset.get("download_count", 0) for asset in release_data.get("assets", []))
        }
    
    def get_rate_limit_info(self) -> Dict:
        """
        Get current rate limit information.
        
        Returns:
            Rate limit information dictionary
        """
        url = f"{GITHUB_API_BASE_URL}/rate_limit"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return {}