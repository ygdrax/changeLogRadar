"""
HTML generator for creating the ChangeLog Radar index page.
"""

from jinja2 import Template
from typing import Dict, List
from datetime import datetime, timezone
import re
import markdown


class HTMLGenerator:
    """Generates HTML pages for displaying release information."""
    
    def __init__(self):
        """Initialize the HTML generator."""
        self.template = self._get_template()
    
    def generate_index_page(self, projects_data: Dict) -> str:
        """
        Generate the main index HTML page.
        
        Args:
            projects_data: Dictionary containing project release data
            
        Returns:
            HTML content as string
        """
        # Sort projects by name
        sorted_projects = dict(sorted(projects_data.items()))
        
        # Process markdown in release bodies
        for project_name, project_data in sorted_projects.items():
            if "releases" in project_data:
                for release in project_data["releases"]:
                    if "body" in release and release["body"]:
                        release["body_html"] = self._markdown_to_html(release["body"])
        
        # Calculate statistics
        stats = self._calculate_stats(sorted_projects)
        
        # Generate HTML
        html = self.template.render(
            projects=sorted_projects,
            stats=stats,
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            title="ChangeLog Radar - Open Source Release Notes"
        )
        
        return html
    
    def _calculate_stats(self, projects_data: Dict) -> Dict:
        """Calculate statistics from the projects data."""
        total_projects = len(projects_data)
        total_releases = sum(len(data["releases"]) for data in projects_data.values())
        projects_with_errors = sum(1 for data in projects_data.values() if "error" in data)
        
        return {
            "total_projects": total_projects,
            "total_releases": total_releases,
            "projects_with_errors": projects_with_errors,
            "success_rate": ((total_projects - projects_with_errors) / total_projects * 100) if total_projects > 0 else 0
        }
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown text to HTML."""
        if not markdown_text:
            return ""
        
        # Pre-process GitHub-specific markdown features
        markdown_text = self._preprocess_github_markdown(markdown_text)
        
        # Configure markdown with extensions for better formatting
        md = markdown.Markdown(
            extensions=[
                'fenced_code',
                'tables',
                'toc',
                'nl2br',
                'sane_lists'
            ],
            extension_configs={
                'toc': {
                    'baselevel': 3,  # Start TOC from h3
                    'anchorlink': True
                }
            }
        )
        
        # Limit content length for display
        if len(markdown_text) > 2000:
            markdown_text = markdown_text[:2000] + "\n\n... (content truncated)"
        
        return md.convert(markdown_text)
    
    def _preprocess_github_markdown(self, text: str) -> str:
        """Pre-process GitHub-specific markdown features."""
        # Convert GitHub issue/PR references to links
        text = re.sub(
            r'#(\d+)',
            r'[#\1](https://github.com/owner/repo/issues/\1)',
            text
        )
        
        # Convert GitHub user mentions to links (simple version)
        text = re.sub(
            r'@(\w+)',
            r'[@\1](https://github.com/\1)',
            text
        )
        
        # Clean up HTML comments that appear in some releases
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        
        # Handle GitHub's diff syntax
        text = re.sub(r'^```diff\n', '```\n', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def _get_template(self) -> Template:
        """Get the Jinja2 template for the HTML page."""
        template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }

        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            color: #666;
            margin-top: 5px;
        }

        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
        }

        .project-card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            flex-direction: column;
            min-height: 400px;
        }

        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }

        .project-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .project-title {
            font-size: 1.8rem;
            color: #333;
            text-decoration: none;
            font-weight: bold;
        }

        .project-title:hover {
            color: #667eea;
        }

        .project-description {
            color: #666;
            margin-bottom: 20px;
            font-style: italic;
        }

        .releases {
            margin-top: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .releases-title {
            font-size: 1.3rem;
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 5px;
        }

        .release {
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .release-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }

        .release-name {
            font-weight: bold;
            font-size: 1.1rem;
            color: #333;
        }

        .release-version {
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .release-date {
            color: #666;
            font-size: 0.9rem;
        }

        .release-body {
            color: #555;
            line-height: 1.6;
            max-height: 250px;
            overflow-y: auto;
            background: white;
            padding: 15px;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        .release-body h1, .release-body h2, .release-body h3 {
            color: #333;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }

        .release-body h1 { font-size: 1.2em; }
        .release-body h2 { font-size: 1.1em; }
        .release-body h3 { font-size: 1.05em; }

        .release-body ul, .release-body ol {
            margin: 0.5em 0;
            padding-left: 2em;
        }

        .release-body li {
            margin: 0.25em 0;
        }

        .release-body p {
            margin: 0.5em 0;
        }

        .release-body code {
            background: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
        }

        .release-body pre {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 0.5em 0;
        }

        .release-body pre code {
            background: none;
            padding: 0;
        }

        .release-body blockquote {
            border-left: 4px solid #667eea;
            padding-left: 10px;
            margin: 0.5em 0;
            color: #666;
        }

        .release-body table {
            border-collapse: collapse;
            width: 100%;
            margin: 0.5em 0;
        }

        .release-body th, .release-body td {
            border: 1px solid #ddd;
            padding: 6px 8px;
            text-align: left;
        }

        .release-body th {
            background: #f8f9fa;
            font-weight: bold;
        }

        .release-body a {
            color: #667eea;
            text-decoration: none;
        }

        .release-body a:hover {
            text-decoration: underline;
        }

        .release-body .highlight {
            background: #fff3cd;
            padding: 2px 4px;
            border-radius: 3px;
        }

        .release-body hr {
            border: none;
            border-top: 1px solid #eee;
            margin: 1em 0;
        }

        .release-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            font-size: 0.8rem;
            color: #666;
        }

        .release-link {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }

        .release-link:hover {
            text-decoration: underline;
        }

        .prerelease {
            background: #ffc107;
            color: #333;
        }

        .error-message {
            color: #dc3545;
            font-style: italic;
            padding: 15px;
            background: #f8d7da;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
        }

        .no-releases {
            color: #666;
            font-style: italic;
            text-align: center;
            padding: 20px;
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: rgba(255, 255, 255, 0.8);
        }

        .generated-at {
            font-size: 0.9rem;
            opacity: 0.8;
        }

        @media (max-width: 1200px) {
            .projects-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .project-header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .release-header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .projects-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .project-card {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>ChangeLog Radar</h1>
            <p>Stay updated with the latest releases from popular open-source projects</p>
        </header>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_projects }}</div>
                <div class="stat-label">Projects Tracked</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_releases }}</div>
                <div class="stat-label">Total Releases</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ "%.1f"|format(stats.success_rate) }}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>

        <div class="projects-grid">
            {% for project_name, project_data in projects.items() %}
            <div class="project-card">
                <div class="project-header">
                    <a href="{{ project_data.repo_url }}" class="project-title" target="_blank">
                        {{ project_name }}
                    </a>
                </div>
                
                {% if project_data.description %}
                <div class="project-description">
                    {{ project_data.description }}
                </div>
                {% endif %}

                {% if project_data.error %}
                <div class="error-message">
                    ERROR: Error fetching releases: {{ project_data.error }}
                </div>
                {% elif project_data.releases %}
                <div class="releases">
                    <h3 class="releases-title">Latest Releases</h3>
                    
                    {% for release in project_data.releases %}
                    <div class="release">
                        <div class="release-header">
                            <div class="release-name">{{ release.name }}</div>
                            <div class="release-version {% if release.prerelease %}prerelease{% endif %}">
                                {{ release.version }}
                                {% if release.prerelease %} (Pre-release){% endif %}
                            </div>
                        </div>
                        
                        <div class="release-date">
                            Published: {{ release.published_at_str }}
                        </div>
                        
                        {% if release.body_html %}
                        <div class="release-body">{{ release.body_html|safe }}</div>
                        {% endif %}
                        
                        <div class="release-meta">
                            <span>Author: {{ release.author.login }}</span>
                            <a href="{{ release.html_url }}" class="release-link" target="_blank">View Release →</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="no-releases">
                    No releases found
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>

        <footer class="footer">
            <div class="generated-at">
                Last updated: {{ generated_at }}
            </div>
            <div style="margin-top: 10px;">
                Built by ChangeLog Radar
            </div>
        </footer>
    </div>
</body>
</html>
        """
        
        return Template(template_content)