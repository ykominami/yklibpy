# FileItem — 内部仕様書

## モジュール

`yklibpy.tomlop.fileitem`

## クラスメソッド

### `setup(file_type_dict)`

- `Storex.set_file_type_dict(file_type_dict)` を呼んでクラス変数 `_file_type_dict` を設定する
- デフォルトは `AppConfig.file_type_dict`（`{"YAML": ".yml", "JSON": ".json", "TOML": ".toml"}`）

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `file_path` | `Path` | 確定したファイルの絶対・相対パス |
| `file_type` | `str` | `AppConfig.get_file_type` で判定した種別 (`"YAML"` 等) |
| `storex` | `Storex` | パスとデータを管理するストレージラッパー |

## `__init__` の処理フロー

```
if isinstance(file, list):
    filex = file.pop(0)          # 先頭を取り出し（リストを破壊的に変更）
    self.file_path = Path(filex)
    if isinstance(filex, str):   # 文字列なら先頭のみ
        pass
    else:                        # Path なら残り要素を結合
        for file_name in file:
            self.file_path = self.file_path / Path(file_name)
else:
    self.file_path = Path(file)
```

- `AppConfig.get_file_type(str(self.file_path))` で拡張子から種別を判定
- 未対応拡張子なら `ValueError` を送出
- `Storex(self.file_type, [self.file_path], data)` を生成（`Storex.__init__` が `pop(0)` するためリストで包む）

## 委譲メソッド

| メソッド | 委譲先 |
|----------|--------|
| `set_data(data)` | `storex.set_data(data)` |
| `output(data)` | `storex.output(data)` |
| `get_name()` | `storex.get_name()` |
| `get_path()` | `storex.get_path()` |

## `with_suffix` の実装詳細

- `self.file_path.with_suffix(suffix)` を返す
- `Storex` の拡張子変更ではなく、`Path` レベルの操作のみ

## 依存関係

- `pathlib.Path`, `typing`（標準ライブラリ）
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.storex.Storex`
