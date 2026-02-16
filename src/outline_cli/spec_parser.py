"""Parse OpenAPI spec to extract endpoint information."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def load_spec() -> Dict[str, Any]:
    """Load the OpenAPI spec file."""
    if not HAS_YAML:
        # Return empty if yaml not available - commands will still work
        # but won't have detailed parameter info
        return {'paths': {}}

    spec_path = Path(__file__).parent.parent.parent / 'outline-spec3.yml'
    if not spec_path.exists():
        return {'paths': {}}

    with open(spec_path, 'r') as f:
        return yaml.safe_load(f)


def get_endpoint_info(endpoint: str, spec: Optional[Dict] = None) -> Dict[str, Any]:
    """Get information about an endpoint from the spec.

    Args:
        endpoint: Endpoint path (e.g., 'documents.list')
        spec: OpenAPI spec dict (will load if not provided)

    Returns:
        Dictionary with endpoint information including parameters
    """
    if spec is None:
        spec = load_spec()

    path = f"/{endpoint}"
    if path not in spec.get('paths', {}):
        return {}

    endpoint_data = spec['paths'][path].get('post', {})

    # Extract parameters from request body
    params = []
    request_body = endpoint_data.get('requestBody', {})
    schema = (
        request_body.get('content', {})
        .get('application/json', {})
        .get('schema', {})
    )

    properties = schema.get('properties', {})
    required = schema.get('required', [])

    for param_name, param_info in properties.items():
        params.append({
            'name': param_name,
            'type': param_info.get('type', 'string'),
            'description': param_info.get('description', ''),
            'required': param_name in required,
            'example': param_info.get('example'),
            'format': param_info.get('format'),
            'enum': param_info.get('enum'),
        })

    return {
        'summary': endpoint_data.get('summary', ''),
        'description': endpoint_data.get('description', ''),
        'operationId': endpoint_data.get('operationId', ''),
        'parameters': params,
    }


def get_all_endpoints(spec: Optional[Dict] = None) -> Dict[str, List[str]]:
    """Get all endpoints grouped by tag.

    Args:
        spec: OpenAPI spec dict (will load if not provided)

    Returns:
        Dictionary mapping tags to lists of endpoint paths
    """
    if spec is None:
        spec = load_spec()

    endpoints_by_tag = {}

    for path, methods in spec.get('paths', {}).items():
        for method, details in methods.items():
            if method == 'post':
                tags = details.get('tags', ['Other'])
                tag = tags[0]

                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []

                endpoint_path = path.lstrip('/')
                endpoints_by_tag[tag].append(endpoint_path)

    return endpoints_by_tag
