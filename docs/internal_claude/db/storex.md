# Storex — 内部仕様書

## モジュール

`yklibpy.db.storex`

## クラス変数

| 変数名 | 型 | 初期値 | 役割 |
|--------|----|--------|------|
| `_file_type_dict` | `dict[str, str]` | `{}` | 拡張子解決に使うファイル種別辞書（`set_file_type_dict` で設定） |

## `__init__` の処理フロー

1. `file_name_array.pop(0)` で先頭要素をルートパスとして取り出す（**引数リストを破壊的に変更する**）
2. 残りの要素を順に `/` で結合して `self.file_path` を構築する
3. `data` が `None` の場合は `{}` を `self.store` にセット

## `load` の処理フロー

- `self.file_path.exists()` が `False` なら何もせず現在の `store` を返す
- ファイル種別に応じて読み込み方法を切り替える:
  - `YAML` → `yaml.safe_load(f) or {}`
  - `JSON` → `json.load(f)`
  - `TOML` → `toml.load(f)`
  - それ以外 → `{"_lines": f.readlines()}`

## `output` の処理フロー

1. `self.file_path.parent.mkdir(parents=True, exist_ok=True)` で親ディレクトリを自動生成
2. ファイル種別に応じて書き込み方法を切り替える:
   - `YAML` → `yaml.dump(data, f, allow_unicode=True)`
   - `JSON` → `json.dump(data, f, ensure_ascii=False, indent=2)`
   - `TOML` → `toml.dump(data, f)`
   - それ以外 → `f.write(str(data))`
3. `data` 引数が `None` の場合は `self.store` を書き出す

## `get_ext_name` の実装詳細

- `cls._file_type_dict[file_type]` を直接参照するため、キーが存在しない場合は `KeyError`

## 依存関係

- `json`, `pathlib.Path`（標準ライブラリ）
- `yaml`（PyYAML）
- `toml`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.config.appconfig.AppConfig`
