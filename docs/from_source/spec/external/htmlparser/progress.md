# 外部仕様書 — `progress`

**対象クラス**: `yklibpy.htmlparser.progress.Progress`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

HTML の ARIA 進捗属性（`aria-valuemin`/`aria-valuemax`/`aria-valuenow` 等）由来の値をまとめて保持し、辞書へ変換するデータコンテナ。

## 2. 公開インタフェース

### 生成

```python
Progress(meter_str: str, valuemin: str, valuemax: str, valuenow: str)
```

生成時に比較用文字列 `meter`（`"{valuemin}-{valuemax}-{valuenow}"` 形式）も組み立てる。

### `to_dict() -> Dict[str, str]`

保持している進捗情報を辞書へ変換する（`meter_str`/`valuemin`/`valuemax`/`valuenow`/`meter` の 5 キー）。

## 3. 制約（現行実装の挙動）

ライブラリ内に本クラスを生成している箇所は無く、現状はどこからも呼び出されていない（利用側アプリケーション向けに提供されるコンテナ）。

## 4. エラー処理・終了コード

例外を送出する経路は無い。ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 進捗値コンテナ | `yklibpy.htmlparser.progress.Progress` |
