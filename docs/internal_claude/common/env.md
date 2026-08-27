# Env — 内部仕様書

## モジュール

`yklibpy.common.env`

## インスタンス変数

| 変数名 | 型 | 初期値 | 役割 |
|--------|----|--------|------|
| `sequence` | `int` | `-1` | `get_files` 実行後にディレクトリ名（数字）から設定される世代番号 |
| `base_path` | `Path` | `Path(".")` | スクレイピング対象の探索起点 |
| `pattern` | `str \| None` | `None` | `set_pattern` で選択されたキー名 |
| `config` | `dict[str, Any]` | `{}` | `pattern` に対応する設定ブロック |
| `assoc` | `dict[str, Any]` | `{}` | YAML 設定ファイル全体を保持する辞書 |

## `__init__` の処理フロー

1. 各変数をデフォルト値で初期化
2. `config_path` が `None` でなければ YAML を `FullLoader` で読み込み `assoc` へ格納
3. `assoc["base_path"]` を `list[str]` としてキャスト後 `make_path` でパスを組み立て `base_path` へ設定

## `make_path` の実装詳細

```python
top_dir = path_array.pop(0)          # 先頭要素を取り出してルートドライブ等にする
top_path = Path(top_dir)
base_path = top_path / Path(*path_array)  # 残り要素をアンパックして結合
```

**副作用**: `pop(0)` で元のリストを破壊する。

## `set_pattern` の処理フロー

1. `self.pattern = pattern` を保存
2. `pattern` が `assoc` に存在しなければ `None` を返す
3. 存在すれば `self.config = self.assoc[pattern]` を設定して `config` を返す

## `get_files` の処理フロー

1. `self.config` が空なら `self.sequence = -1` をセットして空リストを返す
2. `config["dir"]` を `list[str]` としてキャストし `base_path / dir_path` を組み立てる
3. `dir_path.stem` を `int` 変換して `self.sequence` へ代入
4. `config["kind"] == "file"` なら `config["files"]` の各要素を dir_path 配下のパスとして返す
5. それ以外なら `dir_path.iterdir()` でファイル一覧を `sorted` して返す

## Loggerx 呼び出し

`get_files` 内で複数の `Loggerx.error` が呼ばれているが、これはデバッグ目的の痕跡であり異常系ではない（ログレベルが `error` であっても処理は継続する）。

## 依存関係

- `pathlib.Path`
- `yaml`（`FullLoader` で読み込み）
- `yklibpy.common.loggerx.Loggerx`
