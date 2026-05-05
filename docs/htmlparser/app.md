# App — 外部仕様書

## 概要

`yklibpy.htmlparser.app.App`

複数の HTML ファイルを処理してリンク情報を集約する実行クラス。
`create_scraper` をオーバーライドすることで、モードに応じたスクレイパーを差し替えられるファクトリ兼オーケストレータ。

## コンストラクタ

```python
App()
```

リンク集計用の内部状態を空で初期化する。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `links_list` | `list[Any]` | 収集したリンク情報のリスト |
| `links_assoc` | `dict[str, dict[str, Any]]` | 収集したリンクの連想配列（URL をキー） |
| `info` | `dict[str, Any]` | 処理済み情報のキャッシュ |
| `append_count` | `int` | 追加件数 |
| `no_append_count` | `int` | 追加スキップ件数 |

## パブリック API

### `create_scraper(mode: str, sequence: int) -> Scraper | None`

**サブクラスで実装する拡張ポイント。** 基底クラスは常に `None` を返す。
モード文字列に対応する `Scraper` のサブクラスを生成して返す。
未対応のモードの場合は `None` を返し、そのファイルの処理をスキップする。

### `loop(files: List[Path], mode: str, sequence: int) -> dict[str, dict[str, Any]]`

ファイルリストを順に処理し、`create_scraper` でスクレイパーを生成しながらリンク情報を結合して返す。
スクレイパーが `None` の場合や抽出結果が空の場合はスキップする。

### `run(env: Env) -> None`

`Env` から対象ファイルとシーケンス番号・モードを取得し、`loop` を実行して `links_assoc` に蓄積する。

## スクレイパーファクトリパターン

```python
class MyApp(App):
    def create_scraper(self, mode: str, sequence: int) -> Scraper | None:
        if mode == "udemy":
            return UdemyScraper(sequence)
        return None
```

## 依存関係

- `yklibpy.common.env.Env`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.htmlparser.scraper.Scraper`
