# Env — 内部仕様書

**ファイル**: `src/yklibpy/common/env.py`
**継承**: なし

## 概要

YAML 設定ファイルからスクレイピング対象の環境情報（基準パス、パターン別設定、対象ファイル一覧）を組み立てる。`App`/`Scraper` 系の実行前に、処理対象ファイルとモードを解決する役割を担う。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `sequence` | `int` | 現在選択中の設定ディレクトリ名（数値）から得た連番。未設定時は `-1`。 |
| `base_path` | `Path` | 探索の基準となるパス。既定値は `Path(".")`。`__init__()` に `config_path` が指定された場合のみ、設定ファイル内の `base_path` 配列から組み立て直される。 |
| `pattern` | `str \| None` | `set_pattern()` に最後に渡されたパターン名。`assoc` に存在しない無効な値でも検証前に無条件で代入されるため、必ずしも `config` と対応しているとは限らない。 |
| `config` | `dict[str, Any]` | `pattern` に対応する設定ブロック。 |
| `assoc` | `dict[str, Any]` | 設定ファイル全体をロードした連想配列。既定値は空辞書 `{}`。`__init__()` に `config_path` が指定された場合のみ YAML から読み込まれる。ただし `__init__()` 内の `make_path()` 呼び出しにより `base_path` キーの内容は先頭要素が失われる（詳細は「設計上の注意」）。 |

---

## メソッド

### `__init__(config_path: Path | None = None) -> None`

設定パスを読み込み、基準パスとパターン情報を初期化する。`config_path` が指定された場合は YAML を `yaml.FullLoader` で読み込み、`base_path` を配列から組み立てる。

### `make_path(path_array: list[str]) -> Path`

パス要素の配列から実際の `Path` を組み立てる。先頭要素をトップディレクトリとして扱い、残りを結合する。

**Args**: `path_array` — 破壊的に `pop(0)` されるため呼び出し後は要素が 1 つ減る。

### `mode() -> str`

現在の設定に対応するスクレイパーモードを返す。`config["mode"]` が無ければ既定値 `"H3"` を返す。

### `set_base_path(base_path: Path) -> None`

探索の基準となるパスを設定する。

### `set_pattern(pattern: str) -> dict[str, Any] | None`

指定パターンに対応する設定ブロックを `assoc` から選択し `config` に反映する。`self.pattern` は妥当性検証より前に無条件で代入されるため、`pattern` が `assoc` に存在しない場合でも `self.pattern` は更新される。一方この場合 `None` を返し `config` は更新しないため、失敗時は `self.pattern`（無効な要求値）と `self.config`（前回までの値のまま）が食い違った状態になる。

### `get_files() -> list[Path]`

現在の設定から処理対象ファイル一覧を解決する。

```
処理フロー:
  1. self.config が空なら sequence を -1 にリセットし空配列を返す
  2. config["dir"] からディレクトリパスを組み立て、そのディレクトリ名（stem）を sequence に採用
  3. config["kind"] が "file" の場合は config["files"] に列挙された各ファイルへのパスを返す
  4. それ以外の場合はディレクトリ直下のファイルを列挙してソートして返す（ディレクトリが存在しなければ空配列）
```

**Returns**: 処理対象ファイルパスの一覧。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Loggerx` | エラー・デバッグログの出力 |
| `yaml` (PyYAML) | 設定ファイルの読み込み |

---

## 設計上の注意

- `make_path()` は引数の `path_array` を `pop(0)` で破壊的に変更するため、呼び出し元で再利用する場合は注意が必要。`__init__()` 自身もこの呼び出し元の 1 つであり、`self.assoc["base_path"]` への参照をそのまま `make_path()` に渡している（コピーしていない）ため、`__init__()` 完了時点で `self.assoc["base_path"]` は先頭要素が失われた状態になる。つまり `assoc` は「設定ファイル全体をロードした連想配列」のまま保持されるわけではなく、`base_path` キーの内容だけが構築完了後に破壊される。
- `get_files()` の `Loggerx.error` 呼び出しはデバッグ目的の情報ログであり、実際のエラー発生時の呼び出しではない箇所が混在している（ログレベルの使い方が不整合）。
