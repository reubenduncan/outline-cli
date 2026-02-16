"""Remaining commands for Outline CLI."""

import click
from .cli import format_option, pagination_options, handle_request, handle_paginated_request


# ============================================================================
# EVENTS
# ============================================================================

@click.group()
def events():
    """View events."""
    pass


@events.command('list')
@click.option('--name', help='Filter by event name')
@click.option('--actor-id', help='Filter by actor ID')
@click.option('--document-id', help='Filter by document ID')
@click.option('--collection-id', help='Filter by collection ID')
@click.option('--audit-log', is_flag=True, help='Include audit log events')
@pagination_options
@format_option
def events_list(name, actor_id, document_id, collection_id, audit_log, limit, offset, all_results, format):
    """List events."""
    params = {
        'name': name,
        'actorId': actor_id,
        'documentId': document_id,
        'collectionId': collection_id,
        'auditLog': audit_log,
    }
    handle_paginated_request('events.list', params, format, limit, offset, all_results)


# ============================================================================
# FILE OPERATIONS
# ============================================================================

@click.group(name='file-operations')
def file_operations():
    """File operation management."""
    pass


@file_operations.command('info')
@click.option('--id', required=True, help='File operation ID')
@format_option
def file_operations_info(id, format):
    """Retrieve a file operation."""
    handle_request('fileOperations.info', {'id': id}, format)


@file_operations.command('list')
@click.option('--type', 'op_type', help='Filter by operation type')
@pagination_options
@format_option
def file_operations_list(op_type, limit, offset, all_results, format):
    """List file operations."""
    params = {'type': op_type}
    handle_paginated_request('fileOperations.list', params, format, limit, offset, all_results)


@file_operations.command('redirect')
@click.option('--id', required=True, help='File operation ID')
@format_option
def file_operations_redirect(id, format):
    """Get redirect URL for file operation."""
    handle_request('fileOperations.redirect', {'id': id}, format)


@file_operations.command('delete')
@click.option('--id', required=True, help='File operation ID')
@format_option
def file_operations_delete(id, format):
    """Delete a file operation."""
    handle_request('fileOperations.delete', {'id': id}, format)


# ============================================================================
# GROUPS
# ============================================================================

@click.group()
def groups():
    """Manage groups."""
    pass


@groups.command('info')
@click.option('--id', required=True, help='Group ID')
@format_option
def groups_info(id, format):
    """Retrieve a group."""
    handle_request('groups.info', {'id': id}, format)


@groups.command('list')
@pagination_options
@format_option
def groups_list(limit, offset, all_results, format):
    """List all groups."""
    handle_paginated_request('groups.list', {}, format, limit, offset, all_results)


@groups.command('create')
@click.option('--name', required=True, help='Group name')
@format_option
def groups_create(name, format):
    """Create a group."""
    handle_request('groups.create', {'name': name}, format)


@groups.command('update')
@click.option('--id', required=True, help='Group ID')
@click.option('--name', required=True, help='New group name')
@format_option
def groups_update(id, name, format):
    """Update a group."""
    handle_request('groups.update', {'id': id, 'name': name}, format)


@groups.command('delete')
@click.option('--id', required=True, help='Group ID')
@format_option
def groups_delete(id, format):
    """Delete a group."""
    handle_request('groups.delete', {'id': id}, format)


@groups.command('add-user')
@click.option('--id', required=True, help='Group ID')
@click.option('--user-id', required=True, help='User ID')
@format_option
def groups_add_user(id, user_id, format):
    """Add a user to a group."""
    handle_request('groups.add_user', {'id': id, 'userId': user_id}, format)


@groups.command('remove-user')
@click.option('--id', required=True, help='Group ID')
@click.option('--user-id', required=True, help='User ID')
@format_option
def groups_remove_user(id, user_id, format):
    """Remove a user from a group."""
    handle_request('groups.remove_user', {'id': id, 'userId': user_id}, format)


@groups.command('memberships')
@click.option('--id', required=True, help='Group ID')
@click.option('--query', help='Search query')
@pagination_options
@format_option
def groups_memberships(id, query, limit, offset, all_results, format):
    """List group memberships."""
    params = {'id': id, 'query': query}
    handle_paginated_request('groups.memberships', params, format, limit, offset, all_results)


# ============================================================================
# OAUTH CLIENTS
# ============================================================================

@click.group(name='oauth-clients')
def oauth_clients():
    """Manage OAuth clients."""
    pass


@oauth_clients.command('info')
@click.option('--id', required=True, help='OAuth client ID')
@format_option
def oauth_clients_info(id, format):
    """Retrieve an OAuth client."""
    handle_request('oauthClients.info', {'id': id}, format)


@oauth_clients.command('list')
@pagination_options
@format_option
def oauth_clients_list(limit, offset, all_results, format):
    """List OAuth clients."""
    handle_paginated_request('oauthClients.list', {}, format, limit, offset, all_results)


@oauth_clients.command('create')
@click.option('--name', required=True, help='Client name')
@click.option('--redirect-uris', required=True, help='Redirect URIs (comma-separated)')
@format_option
def oauth_clients_create(name, redirect_uris, format):
    """Create an OAuth client."""
    uris = [uri.strip() for uri in redirect_uris.split(',')]
    params = {'name': name, 'redirectUris': uris}
    handle_request('oauthClients.create', params, format)


@oauth_clients.command('update')
@click.option('--id', required=True, help='OAuth client ID')
@click.option('--name', help='Client name')
@click.option('--redirect-uris', help='Redirect URIs (comma-separated)')
@format_option
def oauth_clients_update(id, name, redirect_uris, format):
    """Update an OAuth client."""
    params = {'id': id}
    if name:
        params['name'] = name
    if redirect_uris:
        params['redirectUris'] = [uri.strip() for uri in redirect_uris.split(',')]
    handle_request('oauthClients.update', params, format)


@oauth_clients.command('delete')
@click.option('--id', required=True, help='OAuth client ID')
@format_option
def oauth_clients_delete(id, format):
    """Delete an OAuth client."""
    handle_request('oauthClients.delete', {'id': id}, format)


@oauth_clients.command('rotate-secret')
@click.option('--id', required=True, help='OAuth client ID')
@format_option
def oauth_clients_rotate_secret(id, format):
    """Rotate OAuth client secret."""
    handle_request('oauthClients.rotate_secret', {'id': id}, format)


# ============================================================================
# OAUTH AUTHENTICATIONS
# ============================================================================

@click.group(name='oauth-authentications')
def oauth_authentications():
    """Manage OAuth authentications."""
    pass


@oauth_authentications.command('list')
@pagination_options
@format_option
def oauth_authentications_list(limit, offset, all_results, format):
    """List OAuth authentications."""
    handle_paginated_request('oauthAuthentications.list', {}, format, limit, offset, all_results)


@oauth_authentications.command('delete')
@click.option('--id', required=True, help='OAuth authentication ID')
@format_option
def oauth_authentications_delete(id, format):
    """Delete an OAuth authentication."""
    handle_request('oauthAuthentications.delete', {'id': id}, format)


# ============================================================================
# REVISIONS
# ============================================================================

@click.group()
def revisions():
    """View document revisions."""
    pass


@revisions.command('info')
@click.option('--id', required=True, help='Revision ID')
@format_option
def revisions_info(id, format):
    """Retrieve a revision."""
    handle_request('revisions.info', {'id': id}, format)


@revisions.command('list')
@click.option('--document-id', required=True, help='Document ID')
@pagination_options
@format_option
def revisions_list(document_id, limit, offset, all_results, format):
    """List document revisions."""
    params = {'documentId': document_id}
    handle_paginated_request('revisions.list', params, format, limit, offset, all_results)


# ============================================================================
# SHARES
# ============================================================================

@click.group()
def shares():
    """Manage shares."""
    pass


@shares.command('info')
@click.option('--id', required=True, help='Share ID')
@format_option
def shares_info(id, format):
    """Retrieve a share."""
    handle_request('shares.info', {'id': id}, format)


@shares.command('list')
@pagination_options
@format_option
def shares_list(limit, offset, all_results, format):
    """List shares."""
    handle_paginated_request('shares.list', {}, format, limit, offset, all_results)


@shares.command('create')
@click.option('--document-id', required=True, help='Document ID')
@click.option('--published', is_flag=True, help='Make share published')
@format_option
def shares_create(document_id, published, format):
    """Create a share."""
    params = {'documentId': document_id, 'published': published}
    handle_request('shares.create', params, format)


@shares.command('update')
@click.option('--id', required=True, help='Share ID')
@click.option('--published', type=bool, help='Published status')
@format_option
def shares_update(id, published, format):
    """Update a share."""
    params = {'id': id}
    if published is not None:
        params['published'] = published
    handle_request('shares.update', params, format)


@shares.command('revoke')
@click.option('--id', required=True, help='Share ID')
@format_option
def shares_revoke(id, format):
    """Revoke a share."""
    handle_request('shares.revoke', {'id': id}, format)


# ============================================================================
# STARS
# ============================================================================

@click.group()
def stars():
    """Manage stars."""
    pass


@stars.command('list')
@pagination_options
@format_option
def stars_list(limit, offset, all_results, format):
    """List starred documents."""
    handle_paginated_request('stars.list', {}, format, limit, offset, all_results)


@stars.command('create')
@click.option('--document-id', required=True, help='Document ID')
@format_option
def stars_create(document_id, format):
    """Star a document."""
    handle_request('stars.create', {'documentId': document_id}, format)


@stars.command('update')
@click.option('--id', required=True, help='Star ID')
@click.option('--index', required=True, type=int, help='New index position')
@format_option
def stars_update(id, index, format):
    """Update star position."""
    handle_request('stars.update', {'id': id, 'index': index}, format)


@stars.command('delete')
@click.option('--id', required=True, help='Star ID')
@format_option
def stars_delete(id, format):
    """Remove a star."""
    handle_request('stars.delete', {'id': id}, format)


# ============================================================================
# USERS
# ============================================================================

@click.group()
def users():
    """Manage users."""
    pass


@users.command('info')
@click.option('--id', help='User ID')
@format_option
def users_info(id, format):
    """Retrieve a user (current user if no ID specified)."""
    params = {'id': id} if id else {}
    handle_request('users.info', params, format)


@users.command('list')
@click.option('--query', help='Search query')
@click.option('--filter', 'filter_type', help='Filter type (all, admins, members, suspended, invited)')
@pagination_options
@format_option
def users_list(query, filter_type, limit, offset, all_results, format):
    """List users."""
    params = {'query': query, 'filter': filter_type}
    handle_paginated_request('users.list', params, format, limit, offset, all_results)


@users.command('invite')
@click.option('--email', required=True, help='User email')
@click.option('--name', required=True, help='User name')
@click.option('--role', help='User role (admin, member, viewer)')
@format_option
def users_invite(email, name, role, format):
    """Invite a user."""
    params = {'email': email, 'name': name, 'role': role}
    handle_request('users.invite', params, format)


@users.command('update')
@click.option('--id', required=True, help='User ID')
@click.option('--name', help='User name')
@click.option('--avatar-url', help='Avatar URL')
@click.option('--language', help='Language code')
@format_option
def users_update(id, name, avatar_url, language, format):
    """Update a user."""
    params = {
        'id': id,
        'name': name,
        'avatarUrl': avatar_url,
        'language': language,
    }
    handle_request('users.update', params, format)


@users.command('update-role')
@click.option('--id', required=True, help='User ID')
@click.option('--role', required=True, help='New role (admin, member, viewer)')
@format_option
def users_update_role(id, role, format):
    """Update user role."""
    handle_request('users.update_role', {'id': id, 'role': role}, format)


@users.command('activate')
@click.option('--id', required=True, help='User ID')
@format_option
def users_activate(id, format):
    """Activate a suspended user."""
    handle_request('users.activate', {'id': id}, format)


@users.command('suspend')
@click.option('--id', required=True, help='User ID')
@format_option
def users_suspend(id, format):
    """Suspend a user."""
    handle_request('users.suspend', {'id': id}, format)


@users.command('delete')
@click.option('--id', required=True, help='User ID')
@format_option
def users_delete(id, format):
    """Delete a user."""
    handle_request('users.delete', {'id': id}, format)


# ============================================================================
# VIEWS
# ============================================================================

@click.group()
def views():
    """View document views."""
    pass


@views.command('list')
@click.option('--document-id', required=True, help='Document ID')
@pagination_options
@format_option
def views_list(document_id, limit, offset, all_results, format):
    """List document views."""
    params = {'documentId': document_id}
    handle_paginated_request('views.list', params, format, limit, offset, all_results)


@views.command('create')
@click.option('--document-id', required=True, help='Document ID')
@format_option
def views_create(document_id, format):
    """Create a view (track document view)."""
    handle_request('views.create', {'documentId': document_id}, format)
