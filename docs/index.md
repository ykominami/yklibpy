# yklibpy 外部仕様書 — インデックス

本ディレクトリは `src/yklibpy` 配下の各クラスに対する外部仕様書をまとめる。

## common/

| クラス | ファイル | 概要 |
|--------|----------|------|
| `Loggerx` | [common/loggerx.md](common/loggerx.md) | ロガー生成とログレベル管理 |
| `Env` | [common/env.md](common/env.md) | YAML 設定ファイルからスクレイピング環境情報を組み立てる |
| `Info` | [common/info.md](common/info.md) | 解析済み HTML と処理件数を保持するデータ容器 |
| `Util` | [common/util.md](common/util.md) | 文字列処理・パス操作・表形式変換の汎用ユーティリティ |
| `UtilYaml` | [common/util_yaml.md](common/util_yaml.md) | YAML 読み書きとカスタムタグ登録の補助 |
| `UtilJson` | [common/util_json.md](common/util_json.md) | JSON 読み込みの補助 |
| `SafeDict` | [common/safedict.md](common/safedict.md) | 未定義キーをプレースホルダ文字列で返す辞書 |
| `Timex` | [common/timex.md](common/timex.md) | JST 基準の時刻取得 |

## cli/

| クラス | ファイル | 概要 |
|--------|----------|------|
| `Cli` | [cli/cli.md](cli/cli.md) | argparse ラッパー |

## command/

| クラス | ファイル | 概要 |
|--------|----------|------|
| `Command` | [command/command.md](command/command.md) | 外部コマンド実行と実行回数管理 |
| `CommandGhUser` | [command/command_gh_user.md](command/command_gh_user.md) | GitHub CLI からログインユーザー名を取得 |
| `FetchCount` | [command/fetchcount.md](command/fetchcount.md) | 取得済みデータの世代番号を管理 |

## config/

| クラス | ファイル | 概要 |
|--------|----------|------|
| `AppConfig` | [config/appconfig.md](config/appconfig.md) | アプリ全体で共有する設定キーとファイル種別定義 |

## db/

| クラス | ファイル | 概要 |
|--------|----------|------|
| `DbBase` | [db/db_base.md](db/db_base.md) | ストレージ実装の基底クラス |
| `DbYaml` | [db/db_yaml.md](db/db_yaml.md) | YAML ファイルを背後ストアとして扱う簡易 DB |
| `Storex` | [db/storex.md](db/storex.md) | ファイル種別に応じた読み書きを抽象化するストレージラッパー |
| `AppStore` | [db/appstore.md](db/appstore.md) | 設定ファイルと DB ファイルの保存先解決と入出力の統括 |

## htmlparser/

| クラス | ファイル | 概要 |
|--------|----------|------|
| `Scraper` | [htmlparser/scraper.md](htmlparser/scraper.md) | スクレイパー基底クラス |
| `App` | [htmlparser/app.md](htmlparser/app.md) | HTML ファイル群からリンク情報を集約する実行クラス |
| `HtmlOp` | [htmlparser/htmlop.md](htmlparser/htmlop.md) | BeautifulSoup 要素からアンカー情報を取り出す補助クラス |
| `Preparex` | [htmlparser/preparex.md](htmlparser/preparex.md) | 関連ディレクトリを準備しファイル名を列挙 |
| `ConfigPrepare` | [htmlparser/configprepare.md](htmlparser/configprepare.md) | HTML パーサ関連設定の辞書アクセスを簡略化 |
| `Progress` | [htmlparser/progress.md](htmlparser/progress.md) | 進捗表示に必要な値を保持 |
| `AnchorTagInfo` | [htmlparser/misc/anchortaginfo.md](htmlparser/misc/anchortaginfo.md) | アンカー要素と周辺ノード情報を保持 |
| `AnchorTagx` | [htmlparser/misc/anchortagx.md](htmlparser/misc/anchortagx.md) | アンカー要素の href と表示文字列を扱う Tagx 拡張 |
| `Tagx` | [htmlparser/misc/tagx.md](htmlparser/misc/tagx.md) | BeautifulSoup 要素から表示用情報を抜き出して保持 |
| `PriceInfo` | [htmlparser/misc/priceinfo.md](htmlparser/misc/priceinfo.md) | 旧価格と現在価格の表示文字列を保持 |

## tomlop/

| クラス | ファイル | 概要 |
|--------|----------|------|
| `Tomlop` | [tomlop/tomlop.md](tomlop/tomlop.md) | TOML と YAML の比較・変換・差分出力 |
| `FileItem` | [tomlop/fileitem.md](tomlop/fileitem.md) | ファイルパスと Storex を束ねる薄いラッパー |
