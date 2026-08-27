# 内部仕様書 — インデックス

`src/{common,htmlparser,db,cli,command,config,tomlop}/**/*.py` から生成したクラス別内部仕様書の一覧。

## common

| ファイル | クラス | 概要 |
|---------|--------|------|
| [env.md](common/env.md) | `Env` | YAML 設定からスクレイピング対象の基準パス・パターン・対象ファイルを組み立てる |
| [info.md](common/info.md) | `Info` | 解析済み HTML と処理件数を保持するデータコンテナ |
| [safedict.md](common/safedict.md) | `SafeDict` | 未定義キーをプレースホルダ文字列で返す辞書 |
| [timex.md](common/timex.md) | `Timex` | JST 基準の現在時刻を ISO 8601 文字列で返す |
| [util_json.md](common/util_json.md) | `UtilJson` | JSON の読み込み処理をまとめた補助クラス |
| [util_yaml.md](common/util_yaml.md) | `UtilYaml` | YAML の読み書きとカスタムタグ登録を補助する |
| [loggerx.md](common/loggerx.md) | `Loggerx` | ロガー生成とログレベル管理を集約する |
| [util.md](common/util.md) | `Util`（内部に `UniqueList`/`Result`） | 文字列処理・パス操作・表形式変換などの汎用ユーティリティ群 |
| [opresult.md](common/opresult.md) | `OpResult` | 操作の成否と失敗時の例外情報を保持するイミュータブルな結果型 |

## htmlparser

| ファイル | クラス | 概要 |
|---------|--------|------|
| [app.md](htmlparser/app.md) | `App` | HTML ファイル群からリンク情報を集約する実行クラス（`create_scraper()` は未実装スタブ） |
| [configprepare.md](htmlparser/configprepare.md) | `ConfigPrepare` | HTML パーサ関連設定の辞書アクセスを簡略化する |
| [htmlop.md](htmlparser/htmlop.md) | `HtmlOp` | BeautifulSoup 要素からアンカー情報を取り出す補助クラス |
| [anchortaginfo.md](htmlparser/misc/anchortaginfo.md) | `AnchorTagInfo` | アンカー要素と周辺ノードの情報をまとめて保持する |
| [anchortagx.md](htmlparser/misc/anchortagx.md) | `AnchorTagx` | アンカー要素の href と表示文字列を扱う `Tagx` 拡張 |
| [priceinfo.md](htmlparser/misc/priceinfo.md) | `PriceInfo` | 旧価格と現在価格の表示文字列をまとめて保持する |
| [tagx.md](htmlparser/misc/tagx.md) | `Tagx` | BeautifulSoup 要素から表示用情報を取り出して保持する |
| [preparex.md](htmlparser/preparex.md) | `Preparex` | 関連ディレクトリを準備し、対象ファイル名を列挙する |
| [progress.md](htmlparser/progress.md) | `Progress` | 進捗表示に必要な ARIA 由来の値をまとめて保持する |
| [scraper.md](htmlparser/scraper.md) | `Scraper` | HTML からリンク連想配列を構築するスクレイパー基底クラス |

## db

| ファイル | クラス | 概要 |
|---------|--------|------|
| [db_base.md](db/db_base.md) | `DbBase` | 辞書ベースのストレージ実装が共有する基底クラス |
| [storex.md](db/storex.md) | `Storex` | ファイル種別（YAML/JSON/TOML/プレーンテキスト）に応じた読み書きを抽象化する |
| [db_yaml.md](db/db_yaml.md) | `DbYaml` | YAML ファイルを背後ストアとして扱う簡易 DB 実装 |
| [appstore.md](db/appstore.md) | `AppStore` | OS 規約に従い設定ファイル・DB ファイル・ディレクトリの保存先を解決し入出力を統括する |

## cli

| ファイル | クラス | 概要 |
|---------|--------|------|
| [cli.md](cli/cli.md) | `Cli` | `argparse.ArgumentParser` を扱いやすく包む |

## command

| ファイル | クラス | 概要 |
|---------|--------|------|
| [command.md](command/command.md) | `Command` | 外部コマンド実行と取得回数（実行世代）の管理を提供する基底クラス |
| [command_gh_user.md](command/command_gh_user.md) | `CommandGhUser` | GitHub CLI からログインユーザー名を取得する |
| [fetchcount.md](command/fetchcount.md) | `FetchCount` | 取得済みデータの世代番号を管理する |

## config

| ファイル | クラス | 概要 |
|---------|--------|------|
| [appconfig.md](config/appconfig.md) | `AppConfig` | ファイル種別定数と設定/DB ファイル関連付けの初期定義を保持する |

## tomlop

| ファイル | クラス | 概要 |
|---------|--------|------|
| [fileitem.md](tomlop/fileitem.md) | `FileItem` | ファイルパスと `Storex` を束ねる薄いラッパー |
| [tomlop.md](tomlop/tomlop.md) | `Tomlop` | TOML と YAML の比較・変換・差分出力を扱う |

---

## 対象外ファイル

各モジュールの `__init__.py` は基本的に再エクスポートと疎通確認用の `xmain()`/`ymain()` のみで、独自クラスを定義していないため本仕様書の対象から除外した。ただし `db/__init__.py` のみ例外で、`xmain`/`ymain` に加えて `get_or_create_db`/`db_yaml_x`/`db_yaml`/`db_yaml_main` という実質的なロジックを持つモジュールレベル関数を定義している（クラスではないため対象からは同様に除外するが、未文書化のまま残る既知のギャップ）。
