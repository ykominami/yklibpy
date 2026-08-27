# 外部仕様書 — インデックス

`docs/from_source/spec/internal/` のクラス別内部仕様書と `src/yklibpy/` の現行実装を基に生成した、クラス別外部仕様書の一覧。

定義ドキュメント（`docs/projects/def_ot_terms.md`・`docs/projects/def_of_file_and_dir.md`）は本書作成時点で空のため、全仕様書の記述は「現行実装の挙動」に基づく（各仕様書の「未確定事項」参照）。

## common

| ファイル | 対象クラス | 概要 |
|---------|-----------|------|
| [env.md](common/env.md) | `Env` | YAML 設定からスクレイピング対象の基準パス・パターン・対象ファイルを解決する |
| [info.md](common/info.md) | `Info` | 解析済み HTML と件数カウンタを保持するデータコンテナ |
| [safedict.md](common/safedict.md) | `SafeDict` | 未定義キーをプレースホルダ文字列で返す辞書 |
| [timex.md](common/timex.md) | `Timex` | JST 基準の現在時刻を ISO 8601 文字列で返す |
| [util_json.md](common/util_json.md) | `UtilJson` | JSON の読み込み（ファイル/文字列）補助 |
| [util_yaml.md](common/util_yaml.md) | `UtilYaml` | YAML の読み書きとカスタムタグ無害化 |
| [loggerx.md](common/loggerx.md) | `Loggerx` | ロガー生成とログレベル管理の集約 |
| [util.md](common/util.md) | `Util` | 文字列・パス・エンコーディング・TSV・URL の汎用ユーティリティ群 |
| [opresult.md](common/opresult.md) | `OpResult` | 操作の成否と例外情報を保持するイミュータブルな結果型 |

## htmlparser

| ファイル | 対象クラス | 概要 |
|---------|-----------|------|
| [app.md](htmlparser/app.md) | `App` | HTML ファイル群からリンク情報を集約する実行クラス（スクレイパー選択は未実装スタブ） |
| [configprepare.md](htmlparser/configprepare.md) | `ConfigPrepare` | HTML パーサ関連設定の辞書アクセサ |
| [htmlop.md](htmlparser/htmlop.md) | `HtmlOp` | BeautifulSoup 要素からアンカー情報を取り出す補助 |
| [preparex.md](htmlparser/preparex.md) | `Preparex` | 関連ディレクトリの作成と対象ファイル名の列挙 |
| [progress.md](htmlparser/progress.md) | `Progress` | ARIA 進捗属性値のデータコンテナ |
| [scraper.md](htmlparser/scraper.md) | `Scraper` | HTML からリンク連想配列を構築するスクレイパー基底クラス |
| [anchortaginfo.md](htmlparser/misc/anchortaginfo.md) | `AnchorTagInfo` | アンカー要素と周辺ノード情報のコンテナ |
| [anchortagx.md](htmlparser/misc/anchortagx.md) | `AnchorTagx` | アンカーの `href` と表示テキストを扱うラッパー |
| [priceinfo.md](htmlparser/misc/priceinfo.md) | `PriceInfo` | 旧価格・現在価格の表示文字列コンテナ |
| [tagx.md](htmlparser/misc/tagx.md) | `Tagx` | BeautifulSoup 要素の表示用情報ラッパー |

## db

| ファイル | 対象クラス | 概要 |
|---------|-----------|------|
| [db_base.md](db/db_base.md) | `DbBase` | 辞書ベースストレージの基底クラス |
| [storex.md](db/storex.md) | `Storex` | ファイル種別（YAML/JSON/TOML/テキスト）に応じた読み書きの抽象化 |
| [db_yaml.md](db/db_yaml.md) | `DbYaml` | YAML ファイルを背後ストアとする簡易 DB |
| [appstore.md](db/appstore.md) | `AppStore` | OS 規約に従った設定/DB ファイルの保存先解決と入出力の統括 |

## cli

| ファイル | 対象クラス | 概要 |
|---------|-----------|------|
| [cli.md](cli/cli.md) | `Cli` | `argparse.ArgumentParser` の薄いラッパー |

## command

| ファイル | 対象クラス | 概要 |
|---------|-----------|------|
| [command.md](command/command.md) | `Command` | 外部コマンド実行と取得回数（実行世代）管理の基底クラス |
| [command_gh_user.md](command/command_gh_user.md) | `CommandGhUser` | GitHub CLI からログインユーザー名を取得する |
| [fetchcount.md](command/fetchcount.md) | `FetchCount` | 取得済みデータの世代番号を管理する |

## config

| ファイル | 対象クラス | 概要 |
|---------|-----------|------|
| [appconfig.md](config/appconfig.md) | `AppConfig` | ファイル種別定数と設定/DB ファイル関連付けの初期定義 |

## tomlop

| ファイル | 対象クラス | 概要 |
|---------|-----------|------|
| [fileitem.md](tomlop/fileitem.md) | `FileItem` | ファイルパスとストレージラッパーを束ねる薄いラッパー |
| [tomlop.md](tomlop/tomlop.md) | `Tomlop` | TOML/YAML の比較・変換・差分出力（CLI エントリポイント `yklibpy-tomlop-zmain`/`yklibpy-toml2yaml`/`yklibpy-yaml2toml` 付き） |

---

## 読み方

- 本ライブラリはユーティリティライブラリであり、大半の対象は CLI を持たないライブラリクラスである。各仕様書は「公開インタフェース」「制約（現行実装の挙動）」「エラー処理・終了コード」を中心に構成している。
- CLI エントリポイントを持つのは [tomlop.md](tomlop/tomlop.md)（変換系 3 コマンド）と、[db_yaml.md](db/db_yaml.md) の関連エントリポイント `yklibpy-db-yaml` のみ。各モジュールの疎通確認用エントリポイント（`yklibpy-<module>-xmain`/`-ymain`）はメッセージを出力するだけのため、個別の仕様書は設けていない。
- 保存先解決の全体像は [appstore.md](db/appstore.md) → [storex.md](db/storex.md) → [appconfig.md](config/appconfig.md) の順に読むと分かりやすい。取得世代管理は [command.md](command/command.md) と [fetchcount.md](command/fetchcount.md) が対になっている（採番時に DB へ書き戻すかどうかが異なる）。
- 未完成・未使用の実装（[app.md](htmlparser/app.md) のスクレイパー選択、[tomlop.md](tomlop/tomlop.md) の差分出力と YAML→TOML 変換、[progress.md](htmlparser/progress.md) 等）は、各仕様書の「制約（現行実装の挙動）」に明記している。
