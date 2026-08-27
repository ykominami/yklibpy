# Storex — 内部仕様書

**ファイル**: `src/yklibpy/db/storex.py`
**継承**: なし

## 概要

ファイル種別（YAML/JSON/TOML/プレーンテキスト）に応じた読み書きを抽象化するストレージラッパー。`AppStore` が解決したパス要素列から保存先パスを組み立て、`load()`/`output()` で入出力を行う。

---

## クラス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `_file_type_dict` | `ClassVar[dict[str, str]]` | ファイル種別と拡張子の対応辞書（既定値は空辞書）。`set_file_type_dict()` で外部から設定する。 |

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_type` | `str` | このインスタンスが扱うファイル種別（`AppConfig.FILE_TYPE_*`）。 |
| `file_name_array` | `list[Path] \| list[str]` | コンストラクタに渡されたパス要素列（組み立て後は破壊的に消費される）。 |
| `file_path` | `Path` | 組み立てられた保存先の完全パス。 |
| `store` | `Any` | 保持データ（`data` が未指定の場合は空辞書、それ以外は渡された値）。 |

---

## メソッド

### `set_file_type_dict(file_type_dict: dict[str, str]) -> None` (classmethod)

拡張子解決に使うファイル種別辞書をクラス変数として設定する。

### `get_ext_name(file_type: str) -> str` (classmethod)

ファイル種別に対応する拡張子を返す。

### `__init__(file_type: str, file_name_array: list[Path] | list[str], data: Any = None) -> None`

パス要素列（呼び出し元で組み立て済みの完全なパス要素配列を想定）から保存先パスを組み立て、保持データを初期化する。

```
処理フロー:
  1. file_name_array の先頭要素を pop(0) してトップディレクトリとする
  2. 残りの要素を Path として順に結合し、file_path を組み立てる（要素ごとに Loggerx.debug でトレース出力）
  3. store を data（未指定なら空辞書）で初期化する
```

### `set_data(data: Any) -> None`

内部に保持するデータを置き換える。

### `get_value(key: str) -> Any`

保持データ（`store` が辞書である前提）からキーに対応する値を返す。

### `get_store() -> Any`

保持データ全体を返す。

### `load() -> Any`

保存先ファイルを読み込み、ファイル種別に応じて復元する。

```
処理フロー:
  1. self.file_path が存在しなければ何もせず現在の store を返す
  2. UTF-8 で開き、file_type が YAML なら yaml.safe_load、JSON なら json.load、TOML なら toml.load
  3. それ以外の種別（プレーンテキスト等）は {"_lines": f.readlines()} として保持
```

**Returns**: 復元後（または未読み込み時はそのままの）`store`。

### `output(data: Any = None) -> None`

保持データまたは指定データをファイルへ書き出す。

```
処理フロー:
  1. data が未指定なら self.store を書き出し対象とする
  2. file_path.parent が存在しなければ mkdir(parents=True, exist_ok=True) で作成
  3. UTF-8 で開き、file_type に応じて YAML（allow_unicode=True）/JSON（ensure_ascii=False, indent=2）/TOML/文字列（str(data)）で書き出す
```

### `get_name() -> str`

保存先ファイル名だけを返す。

### `get_path() -> Path`

保存先の完全パスを返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppConfig` | ファイル種別定数（`FILE_TYPE_YAML` 等）の参照 |
| `Loggerx` | デバッグログ出力 |
| `yaml`/`json`/`toml` | 各形式の読み書き |

---

## 設計上の注意

- `__init__()` は引数 `file_name_array` を `pop(0)` で破壊的に変更する。呼び出し元がこの配列を再利用すると意図しない挙動になる。
- `load()` の YAML 読み込みは `yaml.safe_load` を使う一方、`UtilYaml.load_yaml` は `yaml.FullLoader` を使っており、モジュール間で YAML ローダーの安全性レベルが統一されていない。
- `get_value()` は `store` が辞書型であることを前提にしており、`load()` が非辞書型（プレーンテキスト時の `{"_lines": ...}` は辞書だが、他の型が代入された場合）を返すケースとの整合が呼び出し元の責任になっている。
