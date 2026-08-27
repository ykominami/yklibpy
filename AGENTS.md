# Repository Guidelines

## Project Structure & Module Organization

`src/yklibpy/` contains the package code. Current subpackages are grouped by purpose: `common/` for shared helpers, `htmlparser/` for scraping and parsing utilities, `tomlop/` for TOML/YAML conversion, `db/` for storage helpers, plus `cli/`, `command/`, and `config/`. Generated or reference documentation lives under `docs/`, with per-module pages such as `docs/common/` and `docs/htmlparser/`. Package metadata, tool configuration, console scripts, and build settings are centralized in `pyproject.toml`.

## Build, Test, and Development Commands

Use `uv` for local workflows.

- `uv sync --dev`: install runtime and development dependencies.
- `uv run pytest`: run the configured pytest suite (`testpaths = ["tests"]`).
- `uv run ruff check ./src`: lint imports, naming, and common Python errors.
- `uv run black --check ./src`: verify formatting without rewriting files.
- `uv run mypy ./src`: run strict type checks against the `src` tree.
- `uv build`: create source and wheel distributions through Hatchling.

Console entry points are declared in `[project.scripts]`; for example, `uv run yklibpy-toml2yaml` exercises the TOML-to-YAML command.

## Coding Style & Naming Conventions

Python targets 3.13. Use 4-space indentation for Python, UTF-8, LF line endings, and a final newline. Black uses an 88-character line length. Ruff checks `E`, `F`, `I`, and `N`; keep imports sorted and use descriptive snake_case names for modules, functions, and variables. Public CLI entry functions generally follow the existing `xmain`, `ymain`, or command-specific naming pattern.

## Testing Guidelines

Pytest is configured with `-ra -q` and expects tests under `tests/`. Add tests alongside new behavior using files named `test_*.py` and functions named `test_*`. Prefer focused tests for conversions, parsing edge cases, and CLI entry points. Run `uv run pytest` before submitting changes.

## Commit & Pull Request Guidelines

Recent history uses short, imperative commit subjects such as `Unify Python version to 3.13 across all tool configs`; avoid vague subjects like `fix` when possible. Keep commits scoped to one logical change. Pull requests should summarize the change, list verification commands and results, and link related issues when applicable. Include CLI examples or doc updates when behavior or entry points change.

## Agent-Specific Instructions

Before editing, check `git status` and preserve unrelated user changes. Do not overwrite existing generated docs or local data files unless the task explicitly asks for regeneration.
