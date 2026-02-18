# Outline CLI - Agent Usage Guide

## Overview

The **Outline CLI** is a comprehensive Python command-line tool for interacting with the Outline wiki API. It provides access to 100+ API endpoints through an organized command-line interface, making it easy to manage documents, collections, users, and more programmatically.

This tool is designed to be used by AI agents and automation scripts to manage wiki content.

## Setup & Prerequisites

### Installation

The tool must be installed before use:

```bash
pip install outline-cli
```

Or from source:
```bash
git clone https://github.com/outline/outline-cli.git
cd outline-cli
pip install -e .
```

### Configuration

The tool requires two pieces of information:
- **Base URL**: The Outline wiki instance URL (e.g., `https://wiki.example.com`)
- **API Key**: Authentication token from your Outline account

Configure via environment variables:
```bash
export OUTLINE_BASE_URL="https://wiki.example.com"
export OUTLINE_API_KEY="your-api-key-here"
```

Or via config file at `~/.outline-cli.yml`:
```yaml
base_url: https://wiki.example.com
api_key: your-api-key-here
```

## Command Structure

All commands follow this pattern:
```
outline <group> <command> [options]
```

### Command Groups

The CLI is organized into logical command groups:

- **attachments** - Upload, list, and delete file attachments
- **auth** - Manage API authentication and keys
- **collections** - Create, list, update, manage wiki collections
- **comments** - Create and manage document comments
- **data-attributes** - Manage custom data attributes
- **documents** - Core document operations (CRUD, search, publish)
- **events** - View audit logs and system events
- **file-operations** - Monitor file import/export tasks
- **groups** - Manage user groups
- **integrations** - Manage third-party integrations
- **invites** - Send and track invitations
- **pins** - Manage pinned documents
- **policies** - Manage access policies
- **revisions** - View document revision history
- **search** - Full-text search across documents
- **shares** - Create and manage public shares
- **subscriptions** - Manage notification subscriptions
- **teams** - View team/workspace information
- **user-attributes** - Manage user profile attributes
- **users** - Manage user accounts and permissions

## Common Usage Patterns

### 1. Document Operations

#### List all documents
```bash
outline documents list
```

#### List documents with pagination
```bash
outline documents list --limit 10 --offset 0
```

#### Fetch all documents (auto-paginate)
```bash
outline documents list --all
```

#### Get document by ID
```bash
outline documents info --id <doc-id>
```

#### Create a new document
```bash
outline documents create \
  --title "My New Document" \
  --text "Document content in markdown" \
  --collection-id <collection-id>
```

#### Update a document
```bash
outline documents update \
  --id <doc-id> \
  --title "Updated Title" \
  --text "Updated content"
```

#### Delete a document
```bash
outline documents delete --id <doc-id>
```

#### Permanently delete a document (skip trash)
```bash
outline documents delete --id <doc-id> --permanent
```

#### Search documents
```bash
outline documents search --query "search terms"
```

### 2. Collection Operations

#### List collections
```bash
outline collections list
```

#### Get collection details
```bash
outline collections info --id <collection-id>
```

#### Create a collection
```bash
outline collections create --name "New Collection" --description "Collection description"
```

#### Update collection
```bash
outline collections update --id <collection-id> --name "Updated Name"
```

### 3. User & Permission Management

#### List users
```bash
outline users list --all
```

#### Get user information
```bash
outline users info --id <user-id>
```

#### Grant collection access
```bash
outline collection-memberships add \
  --collection-id <collection-id> \
  --user-id <user-id>
```

### 4. Sharing & Public Access

#### Create a public share
```bash
outline shares create --document-id <doc-id>
```

#### List document shares
```bash
outline shares list --document-id <doc-id>
```

#### Delete a share
```bash
outline shares delete --id <share-id>
```

### 5. Revisions & History

#### Get document revision history
```bash
outline revisions list --document-id <doc-id>
```

#### Restore a previous revision
```bash
outline revisions restore --id <revision-id>
```

## Output Formats

Commands support multiple output formats:

### JSON (default)
```bash
outline documents list --format json
```

Returns raw API response as JSON. Useful for parsing with `jq` or other tools.

### Table
```bash
outline documents list --format table
```

Returns formatted table output suitable for human reading.

## Pagination

For commands that support pagination:

- `--limit N` - Number of results per page (default: 25)
- `--offset N` - Starting position (default: 0)
- `--all` - Automatically fetch all results across all pages

Example:
```bash
outline documents list --all  # Fetch everything
outline documents list --limit 5 --offset 10  # Get 5 items starting at position 10
```

## Error Handling

The CLI provides clear error messages when operations fail:

```
Configuration error: OUTLINE_API_KEY not found
```

Common errors:
- **Authentication errors**: Check API key and base URL are correct
- **Not found errors**: Verify document/collection/user IDs exist
- **Permission errors**: User may lack access to the resource
- **Validation errors**: Check required parameters are provided

## Tips for Agent Usage

### 1. Always Verify Configuration
Before making API calls, ensure environment variables are set:
```bash
echo $OUTLINE_BASE_URL
echo $OUTLINE_API_KEY | cut -c1-10)...  # Show only first 10 chars for security
```

### 2. Use JSON Format for Parsing
When writing scripts or agents, always use `--format json` to get structured output:
```bash
outline documents list --format json > documents.json
```

### 3. Batch Operations
Combine list and filter operations to batch process multiple items:
```bash
# Get all documents, then process each
outline documents list --all --format json | jq '.data[].id' | while read id; do
  outline documents update --id "$id" --title "Processed"
done
```

### 4. Handle Large Result Sets
For operations returning many results, always use `--limit` and `--offset` or `--all`:
```bash
# Good - will fetch everything
outline documents list --all

# Avoid - may hit rate limits or memory issues
outline documents list  # No limit specified
```

### 5. Extract IDs from Responses
JSON responses include all data needed to chain operations:
```bash
# Create document and extract ID
DOC_ID=$(outline documents create --title "Test" --collection-id <coll-id> --format json | jq -r '.data.id')

# Use the ID in subsequent operations
outline documents update --id "$DOC_ID" --title "Updated"
```

### 6. Check Required Parameters
Always verify which parameters are required (marked with `required`) before executing commands. Use `--help` for any command:
```bash
outline documents create --help
outline collections info --help
```

### 7. Safely Delete Documents
Use without `--permanent` flag first to move to trash, then verify before permanent deletion:
```bash
# Move to trash
outline documents delete --id <doc-id>

# Later, permanently delete if needed
outline documents delete --id <doc-id> --permanent
```

## Common Workflows

### Import Documents from External Source

```bash
# 1. Create target collection
COLL_ID=$(outline collections create --name "Imported Items" --format json | jq -r '.data.id')

# 2. Import each document
cat documents.json | jq -r '.[]' | while read item; do
  TITLE=$(echo $item | jq -r '.title')
  TEXT=$(echo $item | jq -r '.content')
  
  outline documents create \
    --title "$TITLE" \
    --text "$TEXT" \
    --collection-id "$COLL_ID" \
    --format json
done
```

### Bulk Update Documents

```bash
# Update all documents in a collection
outline documents list --collection-id <coll-id> --all --format json | \
jq '.data[].id' | \
while read id; do
  outline documents update --id "$id" --title "[Updated] $TITLE"
done
```

### Export Collection Structure

```bash
# Export all documents from a collection with their hierarchy
outline documents list --collection-id <coll-id> --all --format json | jq '.'
```

### Set Up Public Sharing

```bash
# Create shares for all documents in a collection
outline documents list --collection-id <coll-id> --all --format json | \
jq '.data[].id' | \
while read id; do
  outline shares create --document-id "$id" --format json
done
```

## Debugging

### Enable Verbose Output
Most commands show errors clearly. For more detailed investigation:

1. Check the API key is correct
2. Verify the base URL is accessible
3. Try the operation manually with explicit parameters
4. Check API response with `--format json`

### Test Authentication
```bash
outline teams info --format json
```

If this succeeds, authentication is working. If it fails, check credentials.

## API Documentation

For detailed parameter information and additional options, refer to:
- Official Outline API Docs: https://docs.getoutline.com/API
- Command help: `outline <group> <command> --help`

## Security Considerations

1. **Never commit API keys** to version control
2. **Use environment variables** or secure config files only
3. **Audit log access** using the `events` command group
4. **Restrict shares** to require password or expiration
5. **Limit collection access** to only necessary users
