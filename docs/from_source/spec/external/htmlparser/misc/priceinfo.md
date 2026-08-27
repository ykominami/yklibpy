# 外部仕様書 — `priceinfo`

**対象クラス**: `yklibpy.htmlparser.misc.priceinfo.PriceInfo`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

旧価格と現在価格の表示文字列をまとめて保持するコンテナ。各値はタグラッパー（`tagx` 参照）経由で保持し、補助文字列として取り出す。

## 2. 公開インタフェース

### 生成

```python
PriceInfo(price_old: Tagx | None, price_real: Tagx | None)
```

### メソッド

| メソッド | 説明 |
|---------|------|
| `get_price_old() -> str \| None` | 旧価格文字列を返す。`price_old` が `None` なら `None` |
| `get_price_real() -> str \| None` | 現在価格文字列を返す。`price_real` が `None` なら `None` |

## 3. 前提条件

価格文字列はタグラッパーの補助文字列（`set_option()` で設定した値）から取り出すため、取得前に利用側で値を設定しておく必要がある（未設定の場合は空文字が返る）。

## 4. エラー処理・終了コード

例外を送出する経路は無い。ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 価格情報コンテナ | `yklibpy.htmlparser.misc.priceinfo.PriceInfo` |
| 価格文字列の保持元 | `yklibpy.htmlparser.misc.tagx.Tagx`（`set_option`/`get_option`） |
