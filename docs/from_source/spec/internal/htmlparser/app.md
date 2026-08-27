# App — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/app.py`
**継承**: なし

## 概要

`Env` から得た設定に基づき、対象 HTML ファイル群を走査してリンク情報を収集する実行クラス。サイト別 `Scraper` を生成するファクトリの土台となるが、本体（`create_scraper()`）は未対応モード用のスタブになっている。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `links_list` | `list[Any]` | （未使用気味の）リンク一覧。 |
| `links_assoc` | `dict[str, dict[str, Any]]` | 収集済みリンク連想配列。 |
| `info` | `dict[str, Any]` | （未使用気味の）処理途中の補助情報用の辞書（`__init__()` で初期化されるのみで参照・更新されない）。 |
| `append_count` | `int` | （未使用気味の）追加件数カウンタ。 |
| `no_append_count` | `int` | （未使用気味の）非追加件数カウンタ。 |

---

## メソッド

### `__init__() -> None`

リンク集計用の内部状態を初期化する。

### `create_scraper(mode: str, sequence: int) -> Scraper | None`

モードに対応するスクレイパーを生成する。現状は常に `None` を返すスタブ実装で、`Loggerx.debug` で未対応モードをログ出力するのみ。サイト別サブクラス（`Scraper` 継承クラス）を生成する分岐は未実装。

### `loop(files: List[Path], mode: str, sequence: int) -> dict[str, dict[str, Any]]`

対象ファイルを順に処理し、抽出したリンク情報をマージする。

```
処理フロー:
  1. 各ファイルについて create_scraper でスクレイパーを生成（None ならスキップ）
  2. scraper.get_links_assoc_from_html(file) で抽出結果を取得
  3. 抽出結果が空でなければ assoc へ update でマージ
  4. 全ファイル処理後、マージ済み assoc を返す
```

### `run(env: Env) -> None`

環境設定から対象ファイルを取得し、リンク情報を収集する。`env.get_files()` でファイル一覧、`env.mode()` でモード、`env.sequence` で連番を取得し、`loop(path_array, mode, sequence)` を呼び出して結果を `self.links_assoc` にマージする。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Env` | 実行環境設定（対象ファイル・モード）の取得元 |
| `Scraper` | 生成対象の抽出処理クラス（型のみ参照） |
| `Loggerx` | デバッグログ出力 |

---

## 設計上の注意

`create_scraper()` が常に `None` を返すため、`App` を単体で使う限りリンクは一切収集されない。実際のサイト別スクレイパー選択ロジックは呼び出し元アプリケーション側で `Scraper` を直接インスタンス化するか、`App` を継承・拡張して実装する必要がある。ドキュメント上の「モード文字列からスクレイパーを選ぶファクトリ」という役割は、このクラス単体では未完成の状態。
