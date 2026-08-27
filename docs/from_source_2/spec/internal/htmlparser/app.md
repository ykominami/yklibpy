# App — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/app.py`  
**継承**: なし

## 概要

環境設定から HTML ファイル群を取得し、ファイルごとのスクレイパー生成とリンク情報の集約を統括する。実際のスクレイパー選択は `create_scraper` の拡張実装へ委譲する。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `links_list` | `list[Any]` | リンク情報のリスト。現行クラス内では未使用。 |
| `links_assoc` | `dict[str, dict[str, Any]]` | キー別に集約したリンク情報。 |
| `info` | `dict[str, Any]` | 補助情報の格納領域。現行クラス内では未使用。 |
| `append_count` | `int` | 追加件数。現行クラス内では更新されない。 |
| `no_append_count` | `int` | 非追加件数。現行クラス内では更新されない。 |

---

## メソッド

### `__init__() -> None`

リンク集計用のコンテナと件数カウンターを空の状態で初期化する。

### `create_scraper(mode: str, sequence: int) -> Scraper | None`

モードに対応するスクレイパーを生成する拡張ポイント。基底実装は未対応ログを出力して常に `None` を返す。

**Args**: `mode` は処理モード、`sequence` は抽出結果へ付与する系列番号。  
**Returns**: 基底実装では `None`。

### `loop(files: List[Path], mode: str, sequence: int) -> dict[str, dict[str, Any]]`

対象ファイルを順に処理し、抽出されたリンク辞書を一つに結合する。

処理フロー:

1. 各ファイルについて `create_scraper` を呼び出す。
2. スクレイパーを生成できた場合、HTML からリンク辞書を抽出する。
3. 空でない抽出結果を `dict.update` で集約辞書へ反映する。
4. 集約結果を返す。

**Args**: `files` は処理対象 HTML、`mode` はスクレイパー種別、`sequence` は系列番号。  
**Returns**: 集約済みリンク辞書。

### `run(env: Env) -> None`

`Env` からファイル、系列番号、モードを取得し、`loop` の結果を保持中のリンク辞書へ統合する。

処理フロー:

1. `env.get_files()` と `env.sequence` から処理条件を得る。
2. `env.mode()` からモードを得て `loop` を実行する。
3. 戻り値を `links_assoc` へ反映する。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Env` | ファイル一覧、系列番号、処理モードを供給する。 |
| `Scraper` | HTML からリンク情報を抽出する。 |
| `Loggerx` | 処理状況と未対応モードを記録する。 |

## 設計上の注意

基底実装の `create_scraper` は常に `None` のため、サブクラス等で差し替えない限り `run` は結果を追加しない。重複キーは後から処理したファイルの値で上書きされる。
