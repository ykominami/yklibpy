# ConfigPrepare — 外部仕様書

## 概要

`yklibpy.htmlparser.configprepare.ConfigPrepare`

HTML パーサ関連設定の辞書アクセスを簡略化する薄いラッパー。
`Preparex` のコンストラクタが設定辞書から特定キーを読み取る際に使用する。

## コンストラクタ

```python
ConfigPrepare(parent_file_path: Path, assoc: dict[str, Any])
```

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parent_file_path` | `Path` | 親設定ファイルの位置（参照用） |
| `assoc` | `dict[str, Any]` | 設定辞書 |

## パブリック API

| メソッド | 返す値 |
|----------|--------|
| `get(key)` | 指定キーに対応する設定値 |
| `get_command()` | `assoc["command"]` — コマンド設定ブロック全体 |
| `get_command_dir()` | `assoc["command"]["dir"]` — コマンドファイルの配置ディレクトリ |
| `get_category_config_file_extname()` | `assoc["category-config-file-extname"]` — カテゴリ設定ファイルの拡張子 |
| `get_utility_category()` | `assoc["utility-category"]` — ユーティリティカテゴリ一覧 |

**Raises**: `KeyError` — 期待するキーが `assoc` に存在しない場合。

## 期待する設定辞書の構造

```yaml
command:
  dir: bat1
category-config-file-extname: .yaml
utility-category:
  - foo
  - bar
```

## 依存関係

なし
