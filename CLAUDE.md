# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

yklibpy is a Python utility library focused on HTML parsing/scraping, data format conversion (TOML/YAML), and application storage management. It targets Python 3.14+ and uses `uv` for dependency management with `hatchling` as the build backend.

## Development Commands

### Package Management
- Install dependencies: `uv sync`
- Add dependency: `uv add <package>`
- Add dev dependency: `uv add --dev <package>`

### Code Quality
- Format code: `uv run black src/`
- Lint code: `uv run ruff check src/`
- Type check: `uv run mypy src/yklibpy`
  - All mypy configuration is in `pyproject.toml` (strict mode, Python 3.14, `namespace_packages = true`, `explicit_package_bases = true`)
  - Type checking uses strict mode by default

### Building and Testing
- Build package: `uv build` or `hatch build`
- Run tests: `uv run pytest` (test directory: `tests/`, configured in pyproject.toml)
- Run a single test: `uv run pytest tests/test_foo.py` or `uv run pytest tests/test_foo.py::test_bar`
- Run with coverage: `uv run pytest --cov`

### Publishing
- Build distribution: `python -m build`
- Upload to PyPI: `twine upload dist/*`

## Architecture

### Module Structure (`src/yklibpy/`)

The library is organized into seven modules:

#### 1. `common/` - Core Utilities
- `Env`: Configuration and path management from YAML files, extracts scraper modes and base paths
- `Info`: Data container for parsed HTML information
- `Util`: General utilities including file operations and encoding detection
- `UtilYaml`/`UtilJson`: YAML/JSON operations with custom tag registration support
- `SafeDict`: Safe dictionary wrapper with type checking
- `Timex`: Timezone-aware timestamp utility (JST)
- `Loggerx`: Centralized logging wrapper — use `Loggerx.debug(msg, __name__)` etc. throughout the codebase instead of direct `logging` calls. Log level defaults to INFO; call `Loggerx.set_log_level(logging.DEBUG)` to enable debug output.

#### 2. `htmlparser/` - Web Scraping Framework
- **Base Class**: `Scraper` - core scraping logic with link extraction and deduplication
- **Concrete Scrapers**: `UdemyScraper`, `KUScraper`, `AmazonSavedCartScraper`, `FanzaDoujinPurchasedScraper`, `FanzaDoujinBasketScraper`
- **App**: Factory/orchestrator that creates the appropriate scraper based on a mode string from configuration. Processes HTML via BeautifulSoup (bs4 + html5lib parser, not lxml).
- **Supporting**: `HtmlOp`, `Preparex`, `ConfigPrepare`, `Progress`, and `misc/` helpers (`AnchorTagInfo`, `AnchorTagx`, `PriceInfo`, `Tagx`)

#### 3. `tomlop/` - TOML/YAML Conversion
- `Tomlop`: Bidirectional TOML ↔ YAML conversion with deep dictionary comparison
- `FileItem`: File metadata and operations wrapper

#### 4. `db/` - Database and Storage Abstraction
- `DbBase`/`DbYaml`: YAML-backed key-value store with `chardet` encoding detection and custom YAML tag constructors
- `Storex`: File-backed storage supporting YAML, JSON, and plain text formats with auto-creation of parent directories
- `AppStore`: Cross-platform config/data file manager using OS conventions (APPDATA/LOCALAPPDATA on Windows, XDG on Unix)

#### 5. `cli/` - CLI Framework
- `Cli`: argparse wrapper for building command-line interfaces

#### 6. `command/` - Command Execution
- `Command`: Subprocess runner with timeout support and output capture
- `CommandGhUser`: Fetches the authenticated GitHub CLI username via `gh api user`
- `fetchcount.py`: Standalone fetch-count helper

#### 7. `config/` - Application Configuration
- `AppConfig`: File type constants, file association mappings, and default field definitions for config/db files

### Key Patterns

**Scraper Pattern**: All scrapers inherit from `Scraper` and implement site-specific parsing. `App` is the factory that selects the scraper via a mode string from YAML config.

**Storage Pattern**: `AppConfig` defines file associations (config vs db, YAML vs JSON) → `AppStore` resolves platform-specific paths → `Storex` handles file I/O. Config files go to APPDATA/%XDG_CONFIG_HOME, data files go to LOCALAPPDATA/XDG_DATA_HOME.

**Entry Points**: Multiple CLI entry points in pyproject.toml under `[project.scripts]` for scrapers, TOML tools, and DB utilities.

## Important Notes

### Type Annotations
- Strict mypy checking enabled (sole config in `pyproject.toml`)
- Use modern Python 3.14+ syntax: `dict[str, Any]` not `Dict`, `X | None` not `Optional[X]`, `-> None` on all `__init__`
- Legacy `Optional`/`List`/`Dict` imports may exist in older files — replace when touching those files
- For dynamic data (YAML/JSON/TOML parse results, BeautifulSoup elements) `Any` or broad union types are acceptable

### Encoding
- Uses `chardet` to detect file encodings with explicit encoding on all file operations
- Falls back to default encoding when detection fails

### Ruff Configuration
- Ignores E501 (line length) — no line length enforcement
- Checks: E (pycodestyle errors), F (pyflakes), I (isort), N (naming)

### Docstring Convention
The canonical spec is `jp-docstring-spec.md` at the repo root. Key rules:
- All docstrings in **Japanese**; class/method/argument names stay in English
- Simple accessors/thin wrappers: one-line summary only
- Methods with conditions, state changes, I/O, or exceptions: add `Args`, `Returns`, `Raises` sections in Japanese Google style
- Describe intent, constraints, and failure conditions — do not repeat type-hint information
- Never write English docstrings; never translate identifier names to Japanese
