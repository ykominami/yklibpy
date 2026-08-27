# util — 内部仕様書

**ファイル**: `src/yklibpy/common/util.py`

## 概要

`Util` とその入れ子クラスが共用する型定義を保持するモジュールです。各クラスの詳細は `util.md`、`unique_list.md`、`result.md` を参照してください。

## モジュールレベル定数・型

| 変数名 | 値/型 | 用途 |
|--------|-------|------|
| `TargetType` | `Literal["file", "dir", "both"]` | パス探索結果の種別指定です。 |
| `T` | `TypeVar("T")` | `UniqueList` の要素型です。 |

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Path`, `csv`, `StringIO` | ファイル探索と TSV 入出力に使用します。 |
| `chardet`, `locale` | 文字コード検出とデコードに使用します。 |
| `BeautifulSoup.Tag` | DOM の共通親探索に使用します。 |
| `Loggerx`, `UtilYaml` | ログ記録と YAML 比較処理に使用します。 |

## 設計上の注意

ソースには過去の動的クラス公開案が文字列リテラルとして残っており、実行されません。
