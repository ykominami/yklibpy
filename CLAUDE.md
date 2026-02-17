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
- Format code: `black src/`
- Lint code: `ruff check src/`
- Type check: `mypy src/yklibpy`
  - Configuration is split between `pyproject.toml` (strict mode, Python 3.14) and `mypy.ini` (module-specific settings with namespace packages enabled)
  - Type checking uses strict mode by default

### Building and Testing
- Build package: `uv build` or `hatch build`
- Run tests: `pytest` (test directory: `tests/`, configured in pyproject.toml)
- Run a single test: `pytest tests/test_foo.py` or `pytest tests/test_foo.py::test_bar`
- Run with coverage: `pytest --cov`

### Publishing
- Build distribution: `python -m build`
- Upload to PyPI: `twine upload dist/*`

## Architecture

### Module Structure (`src/yklibpy/`)

The library is organized into six modules:

#### 1. `common/` - Core Utilities
- `Env`: Configuration and path management from YAML files, extracts scraper modes and base paths
- `Info`: Data container for parsed HTML information
- `Util`: General utilities including file operations and encoding detection
- `UtilYaml`/`UtilJson`: YAML/JSON operations with custom tag registration support
- `SafeDict`: Safe dictionary wrapper with type checking
- `Timex`: Timezone-aware timestamp utility (JST)

#### 2. `htmlparser/` - Web Scraping Framework
- **Base Class**: `Scraper` - core scraping logic with link extraction and deduplication
- **Concrete Scrapers**: `UdemyScraper`, `KUScraper`, `AmazonSavedCartScraper`, `FanzaDoujinPurchasedScraper`, `FanzaDoujinBasketScraper`
- **App**: Factory/orchestrator that creates the appropriate scraper based on a mode string from configuration. Processes HTML via BeautifulSoup (bs4 + html5lib parser, not lxml).
- **Supporting**: `HtmlOp`, `Preparex`, `Progress`, and `misc/` helpers (`AnchorTagInfo`, `AnchorTagx`, `PriceInfo`, `Tagx`)

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
- `Command`: Subprocess runner with timeout support and output capture, plus `array_to_dict` utility

#### 7. `config/` - Application Configuration
- `AppConfig`: File type constants, file association mappings, and default field definitions for config/db files

### Key Patterns

**Scraper Pattern**: All scrapers inherit from `Scraper` and implement site-specific parsing. `App` is the factory that selects the scraper via a mode string from YAML config.

**Storage Pattern**: `AppConfig` defines file associations (config vs db, YAML vs JSON) → `AppStore` resolves platform-specific paths → `Storex` handles file I/O. Config files go to APPDATA/%XDG_CONFIG_HOME, data files go to LOCALAPPDATA/XDG_DATA_HOME.

**Entry Points**: Multiple CLI entry points in pyproject.toml under `[project.scripts]` for scrapers, TOML tools, and DB utilities.

## Important Notes

### Type Annotations
- Strict mypy checking enabled
- Uses modern Python 3.14+ type syntax: `dict[str, Any]` not `Dict`, `X | None` not `Optional[X]`

### Encoding
- Uses `chardet` to detect file encodings with explicit encoding on all file operations
- Falls back to default encoding when detection fails

### Ruff Configuration
- Ignores E501 (line length) — no line length enforcement
- Checks: E (pycodestyle errors), F (pyflakes), I (isort), N (naming)
