# AppConfig — 内部仕様書

**ファイル**: `src/yklibpy/config/appconfig.py`  
**継承**: なし

## 概要

アプリケーション全体で共有するファイル種別、設定用途、関連付け辞書の既定構造を定義し、拡張子から内部ファイル種別を解決します。

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `FILE_TYPE_YAML`, `FILE_TYPE_JSON`, `FILE_TYPE_TOML` | `YAML`, `JSON`, `TOML` | 対応するファイル種別名です。 |
| `DIR_TYPE` | `DIRECTORY` | ディレクトリ種別名です。 |
| `KIND_CONFIG`, `KIND_DB`, `KIND_FETCH` | `config`, `db`, `fetch` | 設定用途の識別子です。 |
| `BASE_NAME_CONFIG`, `BASE_NAME_DB`, `BASE_NAME_FETCH` | `config`, `db`, `fetch` | 基本ファイル名です。 |
| `PATH`, `FILE_TYPE`, `EXT_NAME`, `VALUE`, `DATE` | 各同名小文字文字列 | 関連付け辞書のキーです。 |
| `file_type_dict` | `dict[str, str]` | ファイル種別名から標準拡張子への対応です。 |
| `file_type_reverse_dict` | `dict[str, str]` | 標準拡張子からファイル種別名への逆引きです。 |
| `file_synonym_dict` | `{'.yaml': '.yml'}` | 同義拡張子を標準化します。 |
| `directory_assoc` | `dict[str, dict[str, dict[str, Any]]]` | 継承先が拡張するディレクトリ設定の初期領域です。 |
| `file_assoc` | `dict[str, dict[str, dict[str, Any]]]` | config、db、fetch ファイルの既定メタデータです。 |
| `fetch_item` | `{DATE: ''}` | fetch 項目の既定構造です。 |

## メソッド

### `get_file_type(file_path: str | None) -> str | None` (classmethod)

パスの拡張子を正規化し、対応する内部ファイル種別名を返します。

処理フロー:

1. `None` なら `None` を返します。
2. 拡張子を小文字化し、同義拡張子を標準拡張子へ置換します。
3. 逆引き辞書から種別名を取得し、未対応なら `None` を返します。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `os.path.splitext` | パスから拡張子を分離します。 |
| `Util.swap_dict` | 種別辞書の逆引きをクラス定義時に生成します。 |

## 設計上の注意

関連付け辞書は可変なクラス変数であり、継承クラスや呼び出し側の変更が全利用箇所へ共有されます。
