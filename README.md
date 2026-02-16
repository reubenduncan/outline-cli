# Outline CLI

A comprehensive Python CLI tool for interacting with the Outline wiki API. This tool wraps all 100+ endpoints from the Outline API, providing an easy-to-use command-line interface.

## Installation

```bash
pip install outline-cli
```

Or install from source:

```bash
git clone https://github.com/outline/outline-cli.git
cd outline-cli
pip install -e .
```

## Configuration

Configure the CLI using environment variables or a config file.

### Environment Variables

```bash
export OUTLINE_BASE_URL="https://your-instance.getoutline.com"
export OUTLINE_API_KEY="your-api-key-here"
```

### Config File

Create `~/.outline-cli.yml`:

```yaml
base_url: https://your-instance.getoutline.com
api_key: your-api-key-here
```

## Usage

The CLI is organized into command groups matching the Outline API structure:

- `outline attachments` - Manage attachments
- `outline auth` - Authentication operations
- `outline collections` - Manage collections
- `outline comments` - Manage comments
- `outline data-attributes` - Manage data attributes
- `outline documents` - Manage documents
- `outline events` - View events
- `outline file-operations` - File operation management
- `outline groups` - Manage groups
- `outline oauth-clients` - Manage OAuth clients
- `outline oauth-authentications` - Manage OAuth authentications
- `outline revisions` - View document revisions
- `outline shares` - Manage shares
- `outline stars` - Manage stars
- `outline users` - Manage users
- `outline views` - View document views

### Examples

#### Get authentication info

```bash
outline auth info
```

#### List all collections

```bash
outline collections list
```

#### Get collection details

```bash
outline collections info --id <collection-id>
```

#### Create a document

```bash
outline documents create \
  --title "My Document" \
  --text "Document content here" \
  --collection-id <collection-id>
```

#### Search documents

```bash
outline documents search --query "search term"
```

#### List documents with pagination

```bash
# Get first 25 documents
outline documents list --limit 25

# Get next page
outline documents list --limit 25 --offset 25

# Get all documents (auto-paginate)
outline documents list --all
```

### Output Formats

By default, output is JSON. Use `--format table` for human-readable tables:

```bash
# JSON output (default)
outline collections list

# Table output
outline collections list --format table
```

### Getting Help

Get help for any command:

```bash
# General help
outline --help

# Command group help
outline documents --help

# Specific command help
outline documents create --help
```

## Command Groups

### Attachments

- `create` - Create an attachment
- `redirect` - Retrieve an attachment
- `delete` - Delete an attachment

### Auth

- `info` - Retrieve auth information
- `config` - Retrieve auth config

### Collections

- `info` - Retrieve a collection
- `list` - List all collections
- `create` - Create a collection
- `update` - Update a collection
- `delete` - Delete a collection
- `add-group` - Add a group to a collection
- `remove-group` - Remove a group from a collection
- `add-user` - Add a user to a collection
- `remove-user` - Remove a user from a collection
- `memberships` - List collection memberships
- `group-memberships` - List group memberships
- `documents` - List collection documents
- `export` - Export a collection
- `export-all` - Export all collections

### Documents

- `info` - Retrieve a document
- `list` - List all documents
- `create` - Create a document
- `update` - Update a document
- `delete` - Delete a document (move to trash)
- `search` - Search documents
- `search-titles` - Search document titles
- `archive` - Archive a document
- `unarchive` - Unarchive a document
- `move` - Move a document
- `duplicate` - Duplicate a document
- `import` - Import a document
- `export` - Export a document
- `restore` - Restore from trash
- `empty-trash` - Empty trash
- And more...

### And Many More

See `outline <group> --help` for complete command lists in each group.

## API Reference

This CLI wraps the [Outline API](https://www.getoutline.com/developers). All endpoints are POST requests with JSON bodies.

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Lint
flake8 src/
```

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
