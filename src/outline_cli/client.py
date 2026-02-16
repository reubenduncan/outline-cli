"""API client for Outline."""

import sys
import json
from typing import Any, Dict, Optional, List
import requests
from tabulate import tabulate

from .config import Config


class OutlineError(Exception):
    """Base exception for Outline API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class OutlineClient:
    """Client for interacting with the Outline API."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the client.

        Args:
            config: Configuration object. If None, will create a new one.
        """
        self.config = config or Config()
        self._validate_config()

    def _validate_config(self):
        """Validate configuration and exit if invalid."""
        is_valid, error_message = self.config.validate()
        if not is_valid:
            print(f"Configuration error: {error_message}", file=sys.stderr)
            sys.exit(1)

    def request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Make a request to the Outline API.

        Args:
            endpoint: API endpoint (e.g., 'documents.list')
            params: Request parameters (will be sent as JSON body)
            timeout: Request timeout in seconds

        Returns:
            Response data as dictionary

        Raises:
            OutlineError: If the request fails
        """
        base = self.config.get_base_url()
        # Ensure /api/ path is present
        if not base.endswith('/api'):
            base = f"{base}/api"
        url = f"{base}/{endpoint}"
        headers = self.config.get_headers()
        payload = params or {}

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=timeout
            )

            # Handle different status codes
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 302:
                # For redirect endpoints (like attachments.redirect)
                return {
                    'success': True,
                    'location': response.headers.get('Location', ''),
                    'data': {'url': response.headers.get('Location', '')}
                }
            elif response.status_code == 400:
                error_data = self._parse_error(response)
                raise OutlineError(
                    f"Validation error: {error_data}",
                    status_code=400
                )
            elif response.status_code == 401:
                raise OutlineError(
                    "Unauthenticated: Invalid or missing API key",
                    status_code=401
                )
            elif response.status_code == 403:
                raise OutlineError(
                    "Unauthorized: You don't have permission for this action",
                    status_code=403
                )
            elif response.status_code == 404:
                raise OutlineError(
                    "Not found: The requested resource does not exist",
                    status_code=404
                )
            elif response.status_code == 429:
                raise OutlineError(
                    "Rate limited: Too many requests",
                    status_code=429
                )
            else:
                error_data = self._parse_error(response)
                raise OutlineError(
                    f"API error ({response.status_code}): {error_data}",
                    status_code=response.status_code
                )

        except requests.exceptions.Timeout:
            raise OutlineError(f"Request timed out after {timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise OutlineError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise OutlineError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> str:
        """Parse error message from response.

        Args:
            response: HTTP response object

        Returns:
            Error message string
        """
        try:
            data = response.json()
            if 'message' in data:
                return data['message']
            if 'error' in data:
                return data['error']
            return json.dumps(data)
        except Exception:
            return response.text or f"HTTP {response.status_code}"

    def paginate(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        limit: int = 25,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Auto-paginate through results.

        Args:
            endpoint: API endpoint
            params: Request parameters
            limit: Number of results per page
            max_results: Maximum total results to return (None for all)

        Returns:
            List of all results
        """
        all_results = []
        offset = 0
        params = params or {}

        while True:
            params['limit'] = limit
            params['offset'] = offset

            response = self.request(endpoint, params)
            data = response.get('data', [])

            # Handle both list and dict responses
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                # Try common pagination keys
                items = (
                    data.get('items') or
                    data.get('documents') or
                    data.get('collections') or
                    data.get('users') or
                    data.get('groups') or
                    []
                )
            else:
                break

            if not items:
                break

            all_results.extend(items)

            if max_results and len(all_results) >= max_results:
                return all_results[:max_results]

            # Check if there are more results
            pagination = response.get('pagination', {})
            if not pagination.get('more', False):
                break

            offset += limit

        return all_results

    def format_output(
        self,
        data: Any,
        format_type: str = 'json',
        table_keys: Optional[List[str]] = None
    ) -> str:
        """Format output data.

        Args:
            data: Data to format
            format_type: Output format ('json' or 'table')
            table_keys: Keys to include in table output (for dict items)

        Returns:
            Formatted string
        """
        if format_type == 'json':
            return json.dumps(data, indent=2)

        elif format_type == 'table':
            return self._format_table(data, table_keys)

        else:
            raise ValueError(f"Unknown format type: {format_type}")

    def _format_table(
        self,
        data: Any,
        table_keys: Optional[List[str]] = None
    ) -> str:
        """Format data as a table.

        Args:
            data: Data to format
            table_keys: Keys to include in table (for dict items)

        Returns:
            Table string
        """
        if isinstance(data, dict):
            # Handle API response with 'data' key
            if 'data' in data:
                data = data['data']

            # If it's still a dict, format as key-value pairs
            if isinstance(data, dict):
                # Check for common list keys
                list_keys = ['items', 'documents', 'collections', 'users', 'groups', 'events']
                for key in list_keys:
                    if key in data and isinstance(data[key], list):
                        return self._format_table(data[key], table_keys)

                # Format single dict as key-value
                rows = [[k, v] for k, v in data.items()]
                return tabulate(rows, headers=['Key', 'Value'], tablefmt='grid')

        if isinstance(data, list):
            if not data:
                return "No results"

            # Get headers from first item or use provided keys
            if table_keys:
                headers = table_keys
            elif isinstance(data[0], dict):
                headers = list(data[0].keys())
            else:
                # Simple list
                return '\n'.join(str(item) for item in data)

            # Extract rows
            rows = []
            for item in data:
                if isinstance(item, dict):
                    row = [self._format_cell(item.get(key, '')) for key in headers]
                else:
                    row = [str(item)]
                rows.append(row)

            return tabulate(rows, headers=headers, tablefmt='grid')

        # For simple values
        return str(data)

    def _format_cell(self, value: Any, max_length: int = 50) -> str:
        """Format a cell value for table display.

        Args:
            value: Cell value
            max_length: Maximum cell length

        Returns:
            Formatted string
        """
        if value is None:
            return ''

        if isinstance(value, (dict, list)):
            value_str = json.dumps(value, separators=(',', ':'))
        else:
            value_str = str(value)

        # Truncate long values
        if len(value_str) > max_length:
            return value_str[:max_length-3] + '...'

        return value_str

    def print_output(
        self,
        data: Any,
        format_type: str = 'json',
        table_keys: Optional[List[str]] = None
    ):
        """Print formatted output.

        Args:
            data: Data to print
            format_type: Output format ('json' or 'table')
            table_keys: Keys to include in table output
        """
        output = self.format_output(data, format_type, table_keys)
        print(output)

    def handle_error(self, error: Exception, exit_code: int = 1):
        """Handle and display error.

        Args:
            error: Exception to handle
            exit_code: Exit code to use
        """
        if isinstance(error, OutlineError):
            print(f"Error: {error.message}", file=sys.stderr)
            if error.status_code:
                sys.exit(error.status_code if error.status_code < 128 else 1)
            else:
                sys.exit(exit_code)
        else:
            print(f"Unexpected error: {str(error)}", file=sys.stderr)
            sys.exit(exit_code)
