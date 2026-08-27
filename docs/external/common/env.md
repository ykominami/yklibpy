# Env — 外部仕様書

## 概要

`yklibpy.common.env.Env`

YAML 設定ファイルを読み込み、スクレイピング対象の環境情報（ベースパス・モード・対象ファイル一覧）を組み立てるクラス。

## 責務

- コンストラクタで指定された YAML ファイルから `base_path` と関連設定を読み込む。
- `set_pattern` でパターン名を選択し、そのパターンに対応する設定ブロックを有効化する。
- `get_files` で有効化されたパターンに基づいて処理対象ファイルの一覧を返す。
- `mode` で現在有効なパターンのスクレイパーモード文字列を返す。

## コンストラクタ

```python
Env(config_path: Path | None = None)
```

`config_path` が `None` の場合は空の設定を持つインスタンスを生成する。
`config_path` が指定された場合、YAML ファイルを読み込んで `base_path` を初期化する。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `sequence` | `int` | 現在のディレクトリ連番（ディレクトリ名から抽出）。初期値 `-1` |
| `base_path` | `Path` | 探索の基準ディレクトリ。初期値 `Path(".")` |
| `pattern` | `str \| None` | 現在選択されているパターン名 |
| `config` | `dict[str, Any]` | 現在有効なパターンの設定ブロック |
| `assoc` | `dict[str, Any]` | YAML ファイル全体の内容 |

## パブリック API

### `make_path(path_array: list[str]) -> Path`

パス要素の配列から `Path` を組み立てる。先頭要素をルートとし、残りを順に結合する。
**注意**: `path_array` の先頭要素を `pop` で取り出すため、呼び出し後に元のリストは変更される。

### `mode() -> str`

現在の設定ブロックの `mode` キーを返す。未設定の場合はデフォルト値 `"H3"` を返す。

### `set_base_path(base_path: Path) -> None`

探索基準となるベースパスを外部から上書きする。

### `set_pattern(pattern: str) -> dict[str, Any] | None`

指定パターン名に対応する設定ブロックを選択する。
`assoc` にパターンが存在しない場合は `None` を返し、`config` は更新しない。

### `get_files() -> list[Path]`

現在の設定ブロックから処理対象ファイル一覧を解決して返す。

- `kind == "file"` の場合: 設定に列挙されたファイル名をパスへ変換して返す。
- それ以外: `dir` が示すディレクトリ直下のファイルを昇順で返す。

設定ブロックが空の場合や対象ディレクトリが存在しない場合は空リストを返す。
副作用として `self.sequence` にディレクトリ名から取り出した連番を設定する。

## YAML 設定の期待する構造

```yaml
base_path:
  - /top/dir
  - sub
  - dir

pattern_name:
  mode: H3
  kind: file        # "file" または "dir"
  dir:
    - subdir
    - 001
  files:
    - foo.html
```

## 依存関係

- `yaml` (`pyyaml`)
- `yklibpy.common.loggerx.Loggerx`
