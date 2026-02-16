"""Document commands for Outline CLI."""

import click
from .cli import format_option, pagination_options, handle_request, handle_paginated_request


@click.group()
def documents():
    """Manage documents."""
    pass


@documents.command('info')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--share-id', help='Share ID for public access')
@format_option
def documents_info(doc_id, share_id, format):
    """Retrieve a document."""
    params = {'id': doc_id, 'shareId': share_id}
    handle_request('documents.info', params, format)


@documents.command('list')
@click.option('--collection-id', help='Filter by collection')
@click.option('--parent-document-id', help='Filter by parent document')
@click.option('--backlinkDocumentId', help='Filter by backlink document')
@click.option('--template', is_flag=True, help='Filter templates only')
@pagination_options
@format_option
def documents_list(collection_id, parent_document_id, backlinkdocumentid, template, limit, offset, all_results, format):
    """List all documents."""
    params = {
        'collectionId': collection_id,
        'parentDocumentId': parent_document_id,
        'backlinkDocumentId': backlinkdocumentid,
        'template': template,
    }
    handle_paginated_request('documents.list', params, format, limit, offset, all_results)


@documents.command('create')
@click.option('--title', required=True, help='Document title')
@click.option('--text', help='Document content (markdown)')
@click.option('--collection-id', required=True, help='Collection ID')
@click.option('--parent-document-id', help='Parent document ID')
@click.option('--template', is_flag=True, help='Create as template')
@click.option('--template-id', help='Template to use')
@click.option('--publish', is_flag=True, help='Publish immediately')
@format_option
def documents_create(title, text, collection_id, parent_document_id, template, template_id, publish, format):
    """Create a document."""
    params = {
        'title': title,
        'text': text,
        'collectionId': collection_id,
        'parentDocumentId': parent_document_id,
        'template': template,
        'templateId': template_id,
        'publish': publish,
    }
    handle_request('documents.create', params, format)


@documents.command('update')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--title', help='Document title')
@click.option('--text', help='Document content')
@click.option('--append', is_flag=True, help='Append to existing content')
@click.option('--publish', is_flag=True, help='Publish document')
@click.option('--done', is_flag=True, help='Mark as done')
@format_option
def documents_update(doc_id, title, text, append, publish, done, format):
    """Update a document."""
    params = {
        'id': doc_id,
        'title': title,
        'text': text,
        'append': append,
        'publish': publish,
        'done': done,
    }
    handle_request('documents.update', params, format)


@documents.command('delete')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--permanent', is_flag=True, help='Permanently delete (skip trash)')
@format_option
def documents_delete(doc_id, permanent, format):
    """Delete a document."""
    params = {'id': doc_id, 'permanent': permanent}
    handle_request('documents.delete', params, format)


@documents.command('search')
@click.option('--query', required=True, help='Search query')
@click.option('--collection-id', help='Limit to collection')
@click.option('--user-id', help='Filter by user')
@click.option('--include-archived', is_flag=True, help='Include archived documents')
@click.option('--date-filter', help='Date filter (day, week, month, year)')
@pagination_options
@format_option
def documents_search(query, collection_id, user_id, include_archived, date_filter, limit, offset, all_results, format):
    """Search documents."""
    params = {
        'query': query,
        'collectionId': collection_id,
        'userId': user_id,
        'includeArchived': include_archived,
        'dateFilter': date_filter,
    }
    handle_paginated_request('documents.search', params, format, limit, offset, all_results)


@documents.command('search-titles')
@click.option('--query', required=True, help='Search query')
@click.option('--collection-id', help='Limit to collection')
@pagination_options
@format_option
def documents_search_titles(query, collection_id, limit, offset, all_results, format):
    """Search document titles."""
    params = {'query': query, 'collectionId': collection_id}
    handle_paginated_request('documents.search_titles', params, format, limit, offset, all_results)


@documents.command('archive')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@format_option
def documents_archive(doc_id, format):
    """Archive a document."""
    handle_request('documents.archive', {'id': doc_id}, format)


@documents.command('archived')
@pagination_options
@format_option
def documents_archived(limit, offset, all_results, format):
    """List archived documents."""
    handle_paginated_request('documents.archived', {}, format, limit, offset, all_results)


@documents.command('deleted')
@pagination_options
@format_option
def documents_deleted(limit, offset, all_results, format):
    """List deleted documents."""
    handle_paginated_request('documents.deleted', {}, format, limit, offset, all_results)


@documents.command('drafts')
@click.option('--collection-id', help='Filter by collection')
@pagination_options
@format_option
def documents_drafts(collection_id, limit, offset, all_results, format):
    """List draft documents."""
    params = {'collectionId': collection_id}
    handle_paginated_request('documents.drafts', params, format, limit, offset, all_results)


@documents.command('viewed')
@pagination_options
@format_option
def documents_viewed(limit, offset, all_results, format):
    """List recently viewed documents."""
    handle_paginated_request('documents.viewed', {}, format, limit, offset, all_results)


@documents.command('move')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--collection-id', help='Target collection ID')
@click.option('--parent-document-id', help='Target parent document ID')
@click.option('--index', type=int, help='Position index')
@format_option
def documents_move(doc_id, collection_id, parent_document_id, index, format):
    """Move a document."""
    params = {
        'id': doc_id,
        'collectionId': collection_id,
        'parentDocumentId': parent_document_id,
        'index': index,
    }
    handle_request('documents.move', params, format)


@documents.command('duplicate')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--title', help='Title for the duplicate')
@click.option('--collection-id', help='Target collection ID')
@click.option('--parent-document-id', help='Parent document ID')
@click.option('--recursive', is_flag=True, help='Duplicate child documents')
@click.option('--publish', is_flag=True, help='Publish the duplicate')
@format_option
def documents_duplicate(doc_id, title, collection_id, parent_document_id, recursive, publish, format):
    """Duplicate a document."""
    params = {
        'id': doc_id,
        'title': title,
        'collectionId': collection_id,
        'parentDocumentId': parent_document_id,
        'recursive': recursive,
        'publish': publish,
    }
    handle_request('documents.duplicate', params, format)


@documents.command('restore')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--revision-id', help='Revision ID to restore to')
@click.option('--collection-id', help='Collection to restore to')
@format_option
def documents_restore(doc_id, revision_id, collection_id, format):
    """Restore a document from trash."""
    params = {
        'id': doc_id,
        'revisionId': revision_id,
        'collectionId': collection_id,
    }
    handle_request('documents.restore', params, format)


@documents.command('unpublish')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@format_option
def documents_unpublish(doc_id, format):
    """Unpublish a document."""
    handle_request('documents.unpublish', {'id': doc_id}, format)


@documents.command('import')
@click.option('--file', 'file_path', type=click.Path(exists=True), help='File to import')
@click.option('--data', help='Document data (JSON string)')
@click.option('--collection-id', required=True, help='Collection ID')
@click.option('--parent-document-id', help='Parent document ID')
@click.option('--publish', is_flag=True, help='Publish after import')
@format_option
def documents_import(file_path, data, collection_id, parent_document_id, publish, format):
    """Import a document."""
    import json

    if file_path:
        with open(file_path, 'r') as f:
            data = f.read()

    params = {
        'data': data,
        'collectionId': collection_id,
        'parentDocumentId': parent_document_id,
        'publish': publish,
    }
    handle_request('documents.import', params, format)


@documents.command('export')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@format_option
def documents_export(doc_id, format):
    """Export a document."""
    handle_request('documents.export', {'id': doc_id}, format)


@documents.command('templatize')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@format_option
def documents_templatize(doc_id, format):
    """Convert a document to a template."""
    handle_request('documents.templatize', {'id': doc_id}, format)


@documents.command('add-user')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--user-id', required=True, help='User ID')
@click.option('--permission', help='Permission level')
@format_option
def documents_add_user(doc_id, user_id, permission, format):
    """Add a user to a document."""
    params = {'id': doc_id, 'userId': user_id, 'permission': permission}
    handle_request('documents.add_user', params, format)


@documents.command('remove-user')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--user-id', required=True, help='User ID')
@format_option
def documents_remove_user(doc_id, user_id, format):
    """Remove a user from a document."""
    params = {'id': doc_id, 'userId': user_id}
    handle_request('documents.remove_user', params, format)


@documents.command('add-group')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--group-id', required=True, help='Group ID')
@click.option('--permission', help='Permission level')
@format_option
def documents_add_group(doc_id, group_id, permission, format):
    """Add a group to a document."""
    params = {'id': doc_id, 'groupId': group_id, 'permission': permission}
    handle_request('documents.add_group', params, format)


@documents.command('remove-group')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--group-id', required=True, help='Group ID')
@format_option
def documents_remove_group(doc_id, group_id, format):
    """Remove a group from a document."""
    params = {'id': doc_id, 'groupId': group_id}
    handle_request('documents.remove_group', params, format)


@documents.command('memberships')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--query', help='Search query')
@pagination_options
@format_option
def documents_memberships(doc_id, query, limit, offset, all_results, format):
    """List document memberships."""
    params = {'id': doc_id, 'query': query}
    handle_paginated_request('documents.memberships', params, format, limit, offset, all_results)


@documents.command('group-memberships')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@click.option('--query', help='Search query')
@pagination_options
@format_option
def documents_group_memberships(doc_id, query, limit, offset, all_results, format):
    """List document group memberships."""
    params = {'id': doc_id, 'query': query}
    handle_paginated_request('documents.group_memberships', params, format, limit, offset, all_results)


@documents.command('users')
@click.option('--id', 'doc_id', required=True, help='Document ID')
@pagination_options
@format_option
def documents_users(doc_id, limit, offset, all_results, format):
    """List users with access to a document."""
    params = {'id': doc_id}
    handle_paginated_request('documents.users', params, format, limit, offset, all_results)


@documents.command('documents')
@click.option('--id', 'doc_id', required=True, help='Parent document ID')
@pagination_options
@format_option
def documents_documents(doc_id, limit, offset, all_results, format):
    """List child documents."""
    params = {'id': doc_id}
    handle_paginated_request('documents.documents', params, format, limit, offset, all_results)


@documents.command('empty-trash')
@format_option
def documents_empty_trash(format):
    """Empty the trash."""
    handle_request('documents.empty_trash', {}, format)


@documents.command('answer-question')
@click.option('--document-id', required=True, help='Document ID')
@click.option('--question', required=True, help='Question to answer')
@format_option
def documents_answer_question(document_id, question, format):
    """Answer a question about a document (AI-powered)."""
    params = {'documentId': document_id, 'question': question}
    handle_request('documents.answerQuestion', params, format)
