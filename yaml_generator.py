"""
YAML Generator Module

This module handles generating the index.yaml file from release data.
"""
import yaml
from datetime import datetime
from typing import Dict, List, Any
from scrapper import Release


class YAMLGenerator:
    """Generator for creating index.yaml from release data."""
    
    def __init__(self):
        self.generated_at = datetime.now()
    
    def generate_index(self, releases_data: Dict[str, List[Release]]) -> Dict[str, Any]:
        """
        Generate the index structure from releases data.
        
        Args:
            releases_data: Dictionary mapping repo names to release lists
            
        Returns:
            Dictionary structure for the index.yaml
        """
        index_data = {
            "metadata": {
                "generated_at": self.generated_at.isoformat(),
                "version": "1.0",
                "description": "ChangeLog Radar - Open Source Release Tracker"
            },
            "repositories": {}
        }
        
        for repo_name, releases in releases_data.items():
            repo_data = {
                "name": repo_name,
                "total_releases": len(releases),
                "latest_releases": []
            }
            
            for release in releases:
                release_data = {
                    "tag": release.tag_name,
                    "name": release.name,
                    "published_at": release.published_at.isoformat(),
                    "url": release.html_url,
                    "is_prerelease": release.is_prerelease,
                    "body_preview": self._truncate_body(release.body, 200)
                }
                repo_data["latest_releases"].append(release_data)
            
            # Use repo name as key (replace slashes with underscores for YAML)
            safe_repo_name = repo_name.replace("/", "_")
            index_data["repositories"][safe_repo_name] = repo_data
        
        return index_data
    
    def save_to_file(self, index_data: Dict[str, Any], filepath: str = "index.yaml") -> None:
        """
        Save index data to YAML file.
        
        Args:
            index_data: The index data structure
            filepath: Path to save the YAML file
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                yaml.dump(
                    index_data, 
                    file, 
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=2
                )
            print(f"Index file saved to {filepath}")
        except Exception as e:
            print(f"Error saving index file: {e}")
    
    def _truncate_body(self, body: str, max_length: int = 200) -> str:
        """
        Truncate release body to specified length.
        
        Args:
            body: Original release body text
            max_length: Maximum length for preview
            
        Returns:
            Truncated body text
        """
        if not body:
            return ""
        
        # Clean up the body (remove excessive whitespace)
        clean_body = " ".join(body.split())
        
        if len(clean_body) <= max_length:
            return clean_body
        
        return clean_body[:max_length].rsplit(' ', 1)[0] + "..."