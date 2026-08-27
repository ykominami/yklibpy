# AppConfig — 内部仕様書

**ファイル**: `src/yklibpy/config/appconfig.py`
**継承**: なし

## 概要

アプリ全体で共有する設定キー名・ファイル種別・拡張子対応表・ディレクトリ/ファイル関連付けの初期定義を保持する定数クラス。`AppStore`/`Storex`/`FileItem` など、ファイルアクセス系の全モジュールから参照される。継承して拡張することも想定されている。

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `FILE_TYPE_YAML` | `"YAML"` | YAML 種別識別子。 |
| `FILE_TYPE_JSON` | `"JSON"` | JSON 種別識別子。 |
| `FILE_TYPE_TOML` | `"TOML"` | TOML 種別識別子。 |
| `DIR_TYPE` | `"DIRECTORY"` | ディレクトリ種別識別子。 |
| `KIND_CONFIG` | `"config"` | 設定ファイル種別キー。 |
| `KIND_DB` | `"db"` | DB ファイル種別キー。 |
| `KIND_FETCH` | `"fetch"` | 取得履歴種別キー。 |
| `BASE_NAME_CONFIG` | `"config"` | 設定ファイルの既定ベース名。 |
| `BASE_NAME_DB` | `"db"` | DB ファイルの既定ベース名。 |
| `BASE_NAME_FETCH` | `"fetch"` | 取得履歴ファイルの既定ベース名。 |
| `PATH` | `"path"` | `file_assoc`/`directory_assoc` のパス格納キー名。 |
| `FILE_TYPE` | `"file_type"` | ファイル種別格納キー名。 |
| `EXT_NAME` | `"ext_name"` | 拡張子格納キー名。 |
| `VALUE` | `"value"` | 読み込み済みデータ格納キー名。 |
| `DATE` | `"date"` | 日時格納キー名。 |
| `file_type_dict` | `ClassVar[dict[str, str]]` | 種別 → 拡張子（`.yml`/`.json`/`.toml`）の対応表。 |
| `file_type_reverse_dict` | `ClassVar[dict[str, str]]` | `file_type_dict` を反転した拡張子 → 種別の対応表。 |
| `file_synonym_dict` | `ClassVar[dict[str, str]]` | 拡張子の別名解決表（`.yaml` → `.yml`）。 |
| `directory_assoc` | `ClassVar[dict[str, dict[str, dict[str, Any]]]]` | ディレクトリ関連付けの既定枠（`config`/`db` とも空辞書）。継承先で拡張する前提。 |
| `file_assoc` | `ClassVar[dict[str, dict[str, dict[str, Any]]]]` | ファイル関連付けの既定定義。トップレベルは `directory_assoc` と同じ `config`/`db` の 2 種別で、`config` 配下に `config` ベース名、`db` 配下に `db`/`fetch` の 2 ベース名がネストされた初期エントリを持つ。 |
| `fetch_item` | `ClassVar[dict[str, str]]` | 取得履歴の項目テンプレート（`date` キーのみ）。 |

---

## メソッド

### `get_file_type(file_path: str | None) -> str | None` (classmethod)

拡張子から内部で使うファイル種別名を返す。

```
処理フロー:
  1. file_path が None なら None を返す
  2. os.path.splitext で拡張子を取り出し小文字化
  3. file_synonym_dict による別名解決（.yaml → .yml 等）
  4. file_type_reverse_dict で種別名へ変換。見つからなければ None
```

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Util` | `swap_dict` による `file_type_reverse_dict` の生成 |

---

## 設計上の注意

`file_assoc`/`directory_assoc`/`file_type_dict` 等は `ClassVar` として定義されたミュータブルな辞書であり、`AppStore.__init__` はこれをそのまま受け取って（コピーせず）内部でミューテートする（`AppStore.set_ext_name` で `EXT_NAME` を書き込む等）。`AppConfig.file_assoc` を複数の `AppStore` インスタンス間で共有すると、片方の変更がもう片方に波及するおそれがある。呼び出し側で `copy.deepcopy` するなどの対策が必要な場合がある。
