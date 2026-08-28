# Preparex — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/preparex.py`
**継承**: なし

## 概要

設定情報からスクレイピング関連ディレクトリ（コマンド用・HTML パーサ用）を作成し、対象ファイル名の列挙・検索を行う。コンストラクタ内でディレクトリ走査とディレクトリ作成の副作用を持つ点が特徴。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parts` | `Any` | `ConfigPrepare.get_utility_category()` の結果（ユーティリティカテゴリ一覧）。 |
| `top_path` | `Path` | 探索の起点ディレクトリ。 |
| `bat1_path` | `Path` | コマンド関連ファイルの配置ディレクトリ（作成済み）。 |
| `htmlparser_path` | `Path` | HTML パーサ出力ディレクトリ（作成済み）。 |

---

## メソッド

### `__init__(top_dir: str, category: str, config_parent_dir: str, assoc: dict[str, Any]) -> None`

設定値から探索対象ディレクトリ群を初期化する。

```
処理フロー:
  1. ConfigPrepare を組み立て、bat1_path/htmlparser_path をそれぞれ mkdir(parents=True, exist_ok=True) で作成
  2. カテゴリ設定ファイルの拡張子から正規表現（拡張子$）を組み立てる
  3. top_path 配下を Util.find_paths で走査し、拡張子を除いたファイル名（stem）を "-" で分割
  4. 分割結果がちょうど 2 要素の場合、左側の要素を UniqueList（ul）へ登録（右側は現状ログ出力のみで未使用）
```

### `list_files_containing(path: Path | str, search_string: str) -> List[Path]`

指定ディレクトリ直下で名前に `search_string` を含むファイルを列挙する。`path` が存在しない、またはディレクトリでない場合は空配列。

### `list_files(path: Path, name: str) -> List[Path]`

指定パス直下から条件一致ファイルを取得してデバッグログへ出力しつつ返す（`list_files_containing` の薄いラッパー）。

### `list_htmlparser_files(name: str) -> List[Path]`

`self.htmlparser_path` から対象ファイルを列挙する。

### `list_bat1_files(name: str) -> List[Path]`

`self.bat1_path` から対象ファイルを列挙する。

### `list_utility_files(name: str, suffix: str) -> list[str]`

`self.parts`（ユーティリティカテゴリ一覧）から想定ファイル名候補を組み立てる（`Util.list_files` に委譲）。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `ConfigPrepare` | 設定値の読み出し |
| `Util` | パス探索（`Util.find_paths`）、ファイル名組み立て（`Util.list_files`）、`UniqueList` |
| `Loggerx` | デバッグログ出力 |

---

## 設計上の注意

- コンストラクタ内でディレクトリ作成というファイルシステムへの副作用を持つため、テストや再利用時に注意が必要（副作用を避けたい場面では別途 factory メソッド化が望ましい）。
- コンストラクタ内で構築される `ul`（`UniqueList`）はローカル変数のままインスタンス変数として保持されておらず、走査結果が呼び出し元から参照できない（未使用に近い実装）。
- `self.htmlparser_path.mkdir(parents=True, exist_ok=True)` はコンストラクタ内で 2 回（`bat1_path`/`htmlparser_path` 作成前と、その直後の再作成）呼ばれており、`bat1_path` の 1 回に対して非対称かつ冗長（`exist_ok=True` のため実害は無いが整理の余地あり）。
