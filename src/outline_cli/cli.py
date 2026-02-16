"""Main CLI entry point for Outline CLI."""

import sys
import click

from .client import OutlineClient, OutlineError
from .config import Config


# Global client instance
_client = None


def get_client() -> OutlineClient:
    """Get or create the global client instance."""
    global _client
    if _client is None:
        _client = OutlineClient(Config())
    return _client


def handle_request(endpoint: str, params: dict, format_type: str = 'json'):
    """Handle an API request and output the result.

    Args:
        endpoint: API endpoint path
        params: Request parameters
        format_type: Output format ('json' or 'table')
    """
    client = get_client()
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = client.request(endpoint, params)
        client.print_output(response, format_type)
    except OutlineError as e:
        client.handle_error(e)
    except Exception as e:
        client.handle_error(e)


def handle_paginated_request(
    endpoint: str,
    params: dict,
    format_type: str = 'json',
    limit: int = 25,
    offset: int = 0,
    all_results: bool = False
):
    """Handle a paginated API request.

    Args:
        endpoint: API endpoint path
        params: Request parameters
        format_type: Output format ('json' or 'table')
        limit: Results per page
        offset: Starting offset
        all_results: If True, fetch all results
    """
    client = get_client()
    params = {k: v for k, v in params.items() if v is not None}

    try:
        if all_results:
            results = client.paginate(endpoint, params, limit=limit)
            client.print_output({'data': results}, format_type)
        else:
            params['limit'] = limit
            params['offset'] = offset
            response = client.request(endpoint, params)
            client.print_output(response, format_type)
    except OutlineError as e:
        client.handle_error(e)
    except Exception as e:
        client.handle_error(e)


# Common options
format_option = click.option(
    '--format',
    type=click.Choice(['json', 'table']),
    default='json',
    help='Output format'
)

# Pagination options
def pagination_options(f):
    """Decorator to add pagination options to a command."""
    f = click.option('--limit', type=int, default=25, help='Number of results per page')(f)
    f = click.option('--offset', type=int, default=0, help='Starting offset')(f)
    f = click.option('--all', 'all_results', is_flag=True, help='Fetch all results (auto-paginate)')(f)
    return f


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Outline CLI - Command-line tool for the Outline wiki API."""
    pass


# ============================================================================
# ATTACHMENTS
# ============================================================================

@cli.group()
def attachments():
    """Manage attachments."""
    pass


@attachments.command('create')
@click.option('--name', required=True, help='File name')
@click.option('--content-type', required=True, help='MIME type (e.g., image/png)')
@click.option('--size', required=True, type=int, help='File size in bytes')
@click.option('--document-id', help='Associated document ID')
@format_option
def attachments_create(name, content_type, size, document_id, format):
    """Create an attachment."""
    params = {
        'name': name,
        'contentType': content_type,
        'size': size,
        'documentId': document_id,
    }
    handle_request('attachments.create', params, format)


@attachments.command('redirect')
@click.option('--id', required=True, help='Attachment ID')
@format_option
def attachments_redirect(id, format):
    """Retrieve an attachment URL."""
    handle_request('attachments.redirect', {'id': id}, format)


@attachments.command('delete')
@click.option('--id', required=True, help='Attachment ID')
@format_option
def attachments_delete(id, format):
    """Delete an attachment."""
    handle_request('attachments.delete', {'id': id}, format)


# ============================================================================
# AUTH
# ============================================================================

@cli.group()
def auth():
    """Authentication operations."""
    pass


@auth.command('info')
@format_option
def auth_info(format):
    """Retrieve authentication details."""
    handle_request('auth.info', {}, format)


@auth.command('config')
@format_option
def auth_config(format):
    """Retrieve authentication configuration."""
    handle_request('auth.config', {}, format)


# ============================================================================
# COLLECTIONS
# ============================================================================

@cli.group()
def collections():
    """Manage collections."""
    pass


@collections.command('info')
@click.option('--id', required=True, help='Collection ID')
@format_option
def collections_info(id, format):
    """Retrieve a collection."""
    handle_request('collections.info', {'id': id}, format)


@collections.command('list')
@pagination_options
@format_option
def collections_list(limit, offset, all_results, format):
    """List all collections."""
    handle_paginated_request('collections.list', {}, format, limit, offset, all_results)


@collections.command('create')
@click.option('--name', required=True, help='Collection name')
@click.option('--description', help='Collection description')
@click.option('--color', help='Color hex code')
@click.option('--icon', help='Icon name')
@click.option('--permission', help='Default permission (read_write or read)')
@click.option('--private', is_flag=True, help='Make collection private')
@format_option
def collections_create(name, description, color, icon, permission, private, format):
    """Create a collection."""
    params = {
        'name': name,
        'description': description,
        'color': color,
        'icon': icon,
        'permission': permission,
        'private': private,
    }
    handle_request('collections.create', params, format)


@collections.command('update')
@click.option('--id', required=True, help='Collection ID')
@click.option('--name', help='Collection name')
@click.option('--description', help='Collection description')
@click.option('--color', help='Color hex code')
@click.option('--icon', help='Icon name')
@click.option('--permission', help='Default permission')
@click.option('--sharing', is_flag=True, help='Enable sharing')
@format_option
def collections_update(id, name, description, color, icon, permission, sharing, format):
    """Update a collection."""
    params = {
        'id': id,
        'name': name,
        'description': description,
        'color': color,
        'icon': icon,
        'permission': permission,
        'sharing': sharing,
    }
    handle_request('collections.update', params, format)


@collections.command('delete')
@click.option('--id', required=True, help='Collection ID')
@format_option
def collections_delete(id, format):
    """Delete a collection."""
    handle_request('collections.delete', {'id': id}, format)


@collections.command('add-group')
@click.option('--id', required=True, help='Collection ID')
@click.option('--group-id', required=True, help='Group ID')
@click.option('--permission', help='Permission level (read_write or read)')
@format_option
def collections_add_group(id, group_id, permission, format):
    """Add a group to a collection."""
    params = {'id': id, 'groupId': group_id, 'permission': permission}
    handle_request('collections.add_group', params, format)


@collections.command('remove-group')
@click.option('--id', required=True, help='Collection ID')
@click.option('--group-id', required=True, help='Group ID')
@format_option
def collections_remove_group(id, group_id, format):
    """Remove a group from a collection."""
    handle_request('collections.remove_group', {'id': id, 'groupId': group_id}, format)


@collections.command('add-user')
@click.option('--id', required=True, help='Collection ID')
@click.option('--user-id', required=True, help='User ID')
@click.option('--permission', help='Permission level')
@format_option
def collections_add_user(id, user_id, permission, format):
    """Add a user to a collection."""
    params = {'id': id, 'userId': user_id, 'permission': permission}
    handle_request('collections.add_user', params, format)


@collections.command('remove-user')
@click.option('--id', required=True, help='Collection ID')
@click.option('--user-id', required=True, help='User ID')
@format_option
def collections_remove_user(id, user_id, format):
    """Remove a user from a collection."""
    handle_request('collections.remove_user', {'id': id, 'userId': user_id}, format)


@collections.command('memberships')
@click.option('--id', required=True, help='Collection ID')
@click.option('--query', help='Search query')
@pagination_options
@format_option
def collections_memberships(id, query, limit, offset, all_results, format):
    """List collection memberships."""
    params = {'id': id, 'query': query}
    handle_paginated_request('collections.memberships', params, format, limit, offset, all_results)


@collections.command('group-memberships')
@click.option('--id', required=True, help='Collection ID')
@click.option('--query', help='Search query')
@click.option('--permission', help='Filter by permission')
@pagination_options
@format_option
def collections_group_memberships(id, query, permission, limit, offset, all_results, format):
    """List collection group memberships."""
    params = {'id': id, 'query': query, 'permission': permission}
    handle_paginated_request('collections.group_memberships', params, format, limit, offset, all_results)


@collections.command('documents')
@click.option('--id', required=True, help='Collection ID')
@pagination_options
@format_option
def collections_documents(id, limit, offset, all_results, format):
    """List documents in a collection."""
    params = {'id': id}
    handle_paginated_request('collections.documents', params, format, limit, offset, all_results)


@collections.command('export')
@click.option('--id', required=True, help='Collection ID')
@click.option('--format-type', help='Export format')
@format_option
def collections_export(id, format_type, format):
    """Export a collection."""
    params = {'id': id}
    if format_type:
        params['format'] = format_type
    handle_request('collections.export', params, format)


@collections.command('export-all')
@click.option('--format-type', help='Export format')
@format_option
def collections_export_all(format_type, format):
    """Export all collections."""
    params = {}
    if format_type:
        params['format'] = format_type
    handle_request('collections.export_all', params, format)


# ============================================================================
# COMMENTS
# ============================================================================

@cli.group()
def comments():
    """Manage comments."""
    pass


@comments.command('create')
@click.option('--document-id', required=True, help='Document ID')
@click.option('--data', required=True, help='Comment data (JSON)')
@click.option('--parent-comment-id', help='Parent comment ID for replies')
@format_option
def comments_create(document_id, data, parent_comment_id, format):
    """Create a comment."""
    import json
    params = {
        'documentId': document_id,
        'data': json.loads(data) if isinstance(data, str) else data,
        'parentCommentId': parent_comment_id,
    }
    handle_request('comments.create', params, format)


@comments.command('info')
@click.option('--id', required=True, help='Comment ID')
@format_option
def comments_info(id, format):
    """Retrieve a comment."""
    handle_request('comments.info', {'id': id}, format)


@comments.command('list')
@click.option('--document-id', help='Filter by document ID')
@click.option('--collection-id', help='Filter by collection ID')
@pagination_options
@format_option
def comments_list(document_id, collection_id, limit, offset, all_results, format):
    """List comments."""
    params = {'documentId': document_id, 'collectionId': collection_id}
    handle_paginated_request('comments.list', params, format, limit, offset, all_results)


@comments.command('update')
@click.option('--id', required=True, help='Comment ID')
@click.option('--data', required=True, help='Comment data (JSON)')
@format_option
def comments_update(id, data, format):
    """Update a comment."""
    import json
    params = {
        'id': id,
        'data': json.loads(data) if isinstance(data, str) else data,
    }
    handle_request('comments.update', params, format)


@comments.command('delete')
@click.option('--id', required=True, help='Comment ID')
@format_option
def comments_delete(id, format):
    """Delete a comment."""
    handle_request('comments.delete', {'id': id}, format)


# ============================================================================
# DATA ATTRIBUTES
# ============================================================================

@cli.group(name='data-attributes')
def data_attributes():
    """Manage data attributes."""
    pass


@data_attributes.command('create')
@click.option('--document-id', required=True, help='Document ID')
@click.option('--key', required=True, help='Attribute key')
@click.option('--value', required=True, help='Attribute value')
@format_option
def data_attributes_create(document_id, key, value, format):
    """Create a data attribute."""
    params = {'documentId': document_id, 'key': key, 'value': value}
    handle_request('dataAttributes.create', params, format)


@data_attributes.command('info')
@click.option('--id', required=True, help='Data attribute ID')
@format_option
def data_attributes_info(id, format):
    """Retrieve a data attribute."""
    handle_request('dataAttributes.info', {'id': id}, format)


@data_attributes.command('list')
@click.option('--document-id', help='Filter by document ID')
@pagination_options
@format_option
def data_attributes_list(document_id, limit, offset, all_results, format):
    """List data attributes."""
    params = {'documentId': document_id}
    handle_paginated_request('dataAttributes.list', params, format, limit, offset, all_results)


@data_attributes.command('update')
@click.option('--id', required=True, help='Data attribute ID')
@click.option('--value', required=True, help='New value')
@format_option
def data_attributes_update(id, value, format):
    """Update a data attribute."""
    handle_request('dataAttributes.update', {'id': id, 'value': value}, format)


@data_attributes.command('delete')
@click.option('--id', required=True, help='Data attribute ID')
@format_option
def data_attributes_delete(id, format):
    """Delete a data attribute."""
    handle_request('dataAttributes.delete', {'id': id}, format)


# Import and register additional command groups
from .commands_documents import documents
from .commands_remaining import (
    events,
    file_operations,
    groups,
    oauth_clients,
    oauth_authentications,
    revisions,
    shares,
    stars,
    users,
    views,
)

# Register all command groups
cli.add_command(documents)
cli.add_command(events)
cli.add_command(file_operations)
cli.add_command(groups)
cli.add_command(oauth_clients)
cli.add_command(oauth_authentications)
cli.add_command(revisions)
cli.add_command(shares)
cli.add_command(stars)
cli.add_command(users)
cli.add_command(views)


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
