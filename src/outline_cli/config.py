"""Configuration management for Outline CLI."""

import os
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import yaml
except ImportError:
    yaml = None


class Config:
    """Configuration handler for Outline CLI."""

    def __init__(self):
        self.base_url: Optional[str] = None
        self.api_key: Optional[str] = None
        self._load_config()

    def _load_config(self):
        """Load configuration from environment variables or config file."""
        # Try environment variables first
        self.base_url = os.environ.get('OUTLINE_BASE_URL')
        self.api_key = os.environ.get('OUTLINE_API_KEY')

        # If not in env vars, try config file
        if not self.base_url or not self.api_key:
            config_file = Path.home() / '.outline-cli.yml'
            if config_file.exists():
                if yaml is None:
                    raise ImportError(
                        "PyYAML is required to read config file. "
                        "Install it with: pip install pyyaml"
                    )
                with open(config_file, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
                    self.base_url = self.base_url or config_data.get('base_url')
                    self.api_key = self.api_key or config_data.get('api_key')

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.base_url:
            return False, (
                "Missing base URL. Set OUTLINE_BASE_URL environment variable "
                "or add 'base_url' to ~/.outline-cli.yml"
            )

        if not self.api_key:
            return False, (
                "Missing API key. Set OUTLINE_API_KEY environment variable "
                "or add 'api_key' to ~/.outline-cli.yml"
            )

        return True, None

    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def get_base_url(self) -> str:
        """Get the base URL, ensuring it doesn't end with a slash."""
        url = self.base_url or ''
        return url.rstrip('/')
