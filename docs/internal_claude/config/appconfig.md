# AppConfig — 内部仕様書

## モジュール

`yklibpy.config.appconfig`

## 定数群

### ファイル種別定数

| 定数名 | 値 |
|--------|----|
| `FILE_TYPE_YAML` | `"YAML"` |
| `FILE_TYPE_JSON` | `"JSON"` |
| `FILE_TYPE_TOML` | `"TOML"` |

### 種別（kind）定数

| 定数名 | 値 |
|--------|----|
| `KIND_CONFIG` | `"config"` |
| `KIND_DB` | `"db"` |
| `KIND_FETCH` | `"fetch"` |

### ベース名定数

| 定数名 | 値 |
|--------|----|
| `BASE_NAME_CONFIG` | `"config"` |
| `BASE_NAME_DB` | `"db"` |
| `BASE_NAME_FETCH` | `"fetch"` |

### 辞書キー定数

`PATH`, `FILE_TYPE`, `EXT_NAME`, `VALUE`, `DATE`

## クラス変数の実装詳細

### `file_type_dict`

```python
{ "YAML": ".yml", "JSON": ".json", "TOML": ".toml" }
```

### `file_type_reverse_dict`

`Util.swap_dict(file_type_dict)` で生成する逆引き辞書：`{ ".yml": "YAML", ".json": "JSON", ".toml": "TOML" }`

### `file_synonym_dict`

`.yaml` を `.yml` に正規化するためのエイリアス辞書。`get_file_type` 内で適用される。

### `directory_assoc`

```python
{ "config": {}, "db": {} }
```
サブクラスで拡張するためのエントリだけを用意した空辞書。

### `file_assoc`

```python
{
  "config": {
    "config": { FILE_TYPE: "YAML", EXT_NAME: "", PATH: {}, VALUE: {} }
  },
  "db": {
    "db":    { FILE_TYPE: "YAML", EXT_NAME: "", PATH: {}, VALUE: {} },
    "fetch": { FILE_TYPE: "YAML", EXT_NAME: "", PATH: {}, VALUE: {} },
  }
}
```
`AppStore.set_ext_name` により `EXT_NAME` が起動時に補完される。`PATH` / `VALUE` は `AppStore.prepare_*` / `load_file_*` で動的に埋まる。

## `get_file_type` の実装詳細

1. `os.path.splitext(file_path)` で拡張子を取得し小文字化
2. `file_synonym_dict` で正規化（`.yaml` → `.yml`）
3. `file_type_reverse_dict` でファイル種別名を返す。未知拡張子は `None`

## 継承の想定

`directory_assoc` / `file_assoc` はサブクラスで上書きして拡張することを意図している。

## 依存関係

- `os`（標準ライブラリ）
- `yklibpy.common.util.Util`（`swap_dict` のみ）
