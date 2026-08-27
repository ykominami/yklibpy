# UtilYaml — 内部仕様書

## モジュール

`yklibpy.common.util_yaml`

## クラス変数

| 変数名 | 型 | 初期値 | 役割 |
|--------|----|--------|------|
| `_constructors_registered` | `bool` | `False` | カスタムタグ登録を一度だけ実行するためのフラグ |

## プライベートメソッド

### `_register_constructors(tags: list[str]) -> None`

- `_constructors_registered` が `False` のときのみ登録処理を行う
- `tags` リストに `"tag:yaml.org,2002:python/object"` を必ず追記する（引数リストを破壊的に変更）
- `yaml.add_constructor(tag, ignore_python_object_tag, yaml.SafeLoader)` で `SafeLoader` に登録する
- 登録後 `_constructors_registered = True` にセットする

### `ignore_python_object_tag(loader, node) -> Any`

- `MappingNode` → `construct_mapping(deep=True)`
- `SequenceNode` → `construct_sequence(deep=True)`
- それ以外 → `construct_scalar`
- 未知の Python オブジェクトタグを例外にせず安全な Python 値へ変換するフォールバック

## `load_yaml` の実装詳細

- `yaml.load(f, Loader=yaml.FullLoader)` で読み込む（`SafeLoader` ではなく `FullLoader`）
- 戻り値が `None`（空ファイル）の場合は `{}` を返す

## `save_yaml` の実装詳細

- `yaml.dump(assoc, default_flow_style=False, allow_unicode=True, sort_keys=False)` で文字列化
- `output_path` が指定された場合のみファイルへ書き込む
- 戻り値は常に YAML 文字列（ファイル保存の有無に関わらず）

## `safe_load` の実装詳細

- `yaml.load(f, Loader=yaml.SafeLoader)` の薄いラッパー
- カスタムタグ登録は行わないため、未知タグは例外になる

## 依存関係

- `yaml`（PyYAML）
- `yklibpy.common.loggerx.Loggerx`
