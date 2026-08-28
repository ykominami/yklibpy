# Storex — 内部仕様書

**ファイル**: `src/yklibpy/db/storex.py`  
**継承**: なし

## 概要

パスとデータを保持し、設定されたファイル種別に応じて YAML・JSON・TOML・テキストの入出力を切り替える。

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `_file_type_dict` | `dict[str, str]` | ファイル種別から拡張子への共有対応表。 |

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_type` | `str` | 入出力形式。 |
| `file_name_array` | `list[Path] \| list[str]` | 呼び出し側から渡されたパス要素列。 |
| `file_path` | `Path` | 組み立て済み保存先。 |
| `store` | `Any` | 保持データ。 |

---

## メソッド

### `set_file_type_dict(file_type_dict) -> None` (classmethod)

共有の拡張子対応表を置き換える。

### `get_ext_name(file_type: str) -> str` (classmethod)

対応表から拡張子を返す。未登録時は `KeyError` が伝播する。

### `__init__(file_type, file_name_array, data=None) -> None`

先頭要素を起点に残りの要素を連結して保存先を作り、データを初期化する。

### `set_data(data) -> None` / `get_store() -> Any`

保持データを置換または取得する。

### `get_value(key: str) -> Any`

保持データの `get` を呼び、キーの値を返す。

### `load() -> Any`

ファイルが存在するとき種別に応じて復元し、存在しないときは現在値をそのまま返す。

1. UTF-8 でファイルを開く。
2. YAML・JSON・TOML は各ライブラリで復元し、その他は `_lines` の行配列とする。
3. 復元した `store` を返す。

### `output(data=None) -> None`

親ディレクトリを作成し、種別に応じた形式で指定データまたは保持データを書き出す。

### `get_name() -> str` / `get_path() -> Path`

保存先のファイル名または完全パスを返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppConfig.FILE_TYPE_*` | シリアライズ形式の分岐。 |
| `yaml` / `json` / `toml` | 各形式の読み書き。 |
| `Loggerx` | パス構築・出力ログ。 |

## 設計上の注意

コンストラクタが `file_name_array.pop(0)` で呼び出し元のリストを破壊する。`get_value` は `store` が辞書様であることを暗黙に要求する。未知形式は読み込み時に行配列、書き込み時に `str(data)` となり、厳密な往復性はない。
