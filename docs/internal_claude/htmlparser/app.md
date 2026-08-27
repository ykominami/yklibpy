# App — 内部仕様書

## モジュール

`yklibpy.htmlparser.app`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `links_list` | `list[Any]` | 未使用（将来用のスロット） |
| `links_assoc` | `dict[str, dict[str, Any]]` | `run` 実行後に結果が蓄積される連想配列 |
| `info` | `dict[str, Any]` | 未使用（将来用のスロット） |
| `append_count` | `int` | 集計用カウンタ（現時点では更新されない） |
| `no_append_count` | `int` | 集計用カウンタ（現時点では更新されない） |

## `create_scraper` の実装詳細

- 基底実装は常に `None` を返す
- サブクラスで `mode` と `sequence` に応じた `Scraper` サブクラスのインスタンスを返すようにオーバーライドする

## `loop` の処理フロー

```
for file in files:
    scraper = create_scraper(mode, sequence)  → None なら skip
    assoc = scraper.get_links_assoc_from_html(file)
    if assoc: assoc.update(...)
```

- `create_scraper` が `None` を返したファイルはスキップ（`continue`）
- `extracted_links_assoc` が空でない場合のみ `assoc.update(extracted_links_assoc)` でマージ

## `run` の処理フロー

1. `env.get_files()` でファイル一覧と `env.sequence` を取得
2. `env.mode()` でスクレイパーモード文字列を取得
3. `loop(path_array, mode, sequence)` を呼んで結果辞書を得る
4. `self.links_assoc.update(assoc)` で内部状態に蓄積する

## 依存関係

- `pathlib.Path`, `typing`（標準ライブラリ）
- `yklibpy.common.env.Env`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.htmlparser.scraper.Scraper`
