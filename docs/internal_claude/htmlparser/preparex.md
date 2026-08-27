# Preparex — 内部仕様書

## モジュール

`yklibpy.htmlparser.preparex`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `parts` | `Any` | `config.get_utility_category()` で取得したカテゴリ一覧 |
| `top_path` | `Path` | 探索の起点ディレクトリ |
| `bat1_path` | `Path` | コマンド出力ディレクトリ（`top_path / command_dir`） |
| `htmlparser_path` | `Path` | HTML パーサ出力ディレクトリ（`top_path / category`） |

## `__init__` の処理フロー

1. `ConfigPrepare(Path(config_parent_dir), assoc)` で設定ラッパーを生成
2. `bat1_path` / `htmlparser_path` を決定し `mkdir(parents=True, exist_ok=True)` で作成
3. `file_extname` を取得し正規表現 `re.compile(re.escape(file_extname) + "$")` を組み立てる
4. `Util.find_paths(top_path, "*", "file")` で全ファイルを列挙し、拡張子が一致するものを `UniqueList` へ追加

### ファイル名分解ロジック

```
stem.split("-") → [left, right]  (size == 2 のとき)
```

`left` を `ul.append(left)` で UniqueList へ追加する。`right` はログ出力のみで使わない。

## `list_files_containing` の実装詳細

- `target_path.iterdir()` で直下のファイルのみを列挙
- `search_string in file_path.name` で部分一致フィルタリング

## `list_utility_files` の実装詳細

- `Util.list_files(name, self.parts, suffix)` を呼んで `"{name}-{part}{suffix}"` 形式の文字列リストを返す

## 依存関係

- `re`, `pathlib.Path`, `typing`（標準ライブラリ）
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
- `yklibpy.htmlparser.configprepare.ConfigPrepare`
