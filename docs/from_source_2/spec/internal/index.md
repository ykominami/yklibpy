# 内部仕様書 — インデックス

`src/yklibpy/**/*.py` から生成したクラス別内部仕様書の一覧。

| ファイル | クラス | 概要 |
|---------|--------|------|
| [cli/__init__.md](cli/__init__.md) | —（モジュール） | CLI 基盤の公開 API と疎通確認用エントリポイントを提供する。 |
| [cli/cli.md](cli/cli.md) | `Cli` | argparse によるサブコマンド定義と解析結果を管理する。 |
| [command/__init__.md](command/__init__.md) | —（モジュール） | コマンド関連クラスを再公開する。 |
| [command/command.md](command/command.md) | `Command` | 外部プロセス実行と実行回数制御を提供する。 |
| [command/command_gh_user.md](command/command_gh_user.md) | `CommandGhUser` | GitHub CLI の認証ユーザー名を取得する。 |
| [command/fetchcount.md](command/fetchcount.md) | `FetchCount` | 取得履歴 DB から実行回数を選択する。 |
| [common/__init__.md](common/__init__.md) | —（モジュール） | 共通クラスと疎通確認関数を公開する。 |
| [common/env.md](common/env.md) | `Env` | YAML 設定から処理対象ファイル群を解決する。 |
| [common/info.md](common/info.md) | `Info` | HTML 解析処理のコンテキストを保持する。 |
| [common/loggerx.md](common/loggerx.md) | `Loggerx` | 名前別ロガーをキャッシュして共通ログ出力を提供する。 |
| [common/opresult.md](common/opresult.md) | `OpResult` | 成功値または失敗情報を保持する汎用結果型である。 |
| [common/result.md](common/result.md) | `Result` | URL 検証結果を保持する `Util` の入れ子クラスである。 |
| [common/safedict.md](common/safedict.md) | `SafeDict` | 未定義キーをプレースホルダーのまま返す辞書である。 |
| [common/timex.md](common/timex.md) | `Timex` | 日本標準時を ISO 8601 文字列で返す。 |
| [common/unique_list.md](common/unique_list.md) | `UniqueList` | 重複を除きながら追加順を保持する。 |
| [common/util.md](common/util.md) | `Util` | 文字列、URL、パス、DOM 等の汎用操作を集約する。 |
| [common/util_json.md](common/util_json.md) | `UtilJson` | JSON を Python オブジェクトへ変換する。 |
| [common/util_module.md](common/util_module.md) | —（モジュール） | `util.py` の共有型定義を記載する。 |
| [common/util_yaml.md](common/util_yaml.md) | `UtilYaml` | YAML の読み書きとコンストラクター登録を提供する。 |
| [config/__init__.md](config/__init__.md) | —（モジュール） | `AppConfig` と疎通確認関数を公開する。 |
| [config/appconfig.md](config/appconfig.md) | `AppConfig` | アプリ共通のファイル種別と設定構造を定義する。 |
| [db/__init__.md](db/__init__.md) | —（モジュール） | ストレージ関連クラスと CLI 関数を公開する。 |
| [db/appstore.md](db/appstore.md) | `AppStore` | 保存先解決とストレージ入出力を統括する。 |
| [db/db_base.md](db/db_base.md) | `DbBase` | 辞書ベース DB の基底状態を保持する。 |
| [db/db_yaml.md](db/db_yaml.md) | `DbYaml` | YAML と辞書を相互変換する簡易 DB である。 |
| [db/storex.md](db/storex.md) | `Storex` | ファイル種別別のデータ入出力を切り替える。 |
| [htmlparser/__init__.md](htmlparser/__init__.md) | —（モジュール） | HTML パーサーの主要クラスを公開する。 |
| [htmlparser/app.md](htmlparser/app.md) | `App` | HTML ファイル群のスクレイピングを統括する。 |
| [htmlparser/configprepare.md](htmlparser/configprepare.md) | `ConfigPrepare` | HTML パーサー設定へのアクセスを提供する。 |
| [htmlparser/htmlop.md](htmlparser/htmlop.md) | `HtmlOp` | DOM 探索とアンカー情報変換を提供する。 |
| [htmlparser/misc/__init__.md](htmlparser/misc/__init__.md) | —（モジュール） | HTML タグ補助クラス群を再公開する。 |
| [htmlparser/misc/anchortaginfo.md](htmlparser/misc/anchortaginfo.md) | `AnchorTagInfo` | アンカーと周辺 DOM ノードをまとめる。 |
| [htmlparser/misc/anchortagx.md](htmlparser/misc/anchortagx.md) | `AnchorTagx` | アンカー固有情報を持つタグラッパーである。 |
| [htmlparser/misc/priceinfo.md](htmlparser/misc/priceinfo.md) | `PriceInfo` | 旧価格と現在価格のタグ情報を保持する。 |
| [htmlparser/misc/tagx.md](htmlparser/misc/tagx.md) | `Tagx` | BeautifulSoup 要素をログ向けにラップする。 |
| [htmlparser/preparex.md](htmlparser/preparex.md) | `Preparex` | 設定に基づいてディレクトリとファイル群を準備する。 |
| [htmlparser/progress.md](htmlparser/progress.md) | `Progress` | 進捗表示値と辞書表現を保持する。 |
| [htmlparser/scraper.md](htmlparser/scraper.md) | `Scraper` | HTML を解析してリンク辞書を構築する基底クラスである。 |
| [tomlop/__init__.md](tomlop/__init__.md) | —（モジュール） | TOML/YAML 操作 API と CLI 関数を公開する。 |
| [tomlop/fileitem.md](tomlop/fileitem.md) | `FileItem` | 単一ファイルのパス、種別、ストレージを束ねる。 |
| [tomlop/tomlop.md](tomlop/tomlop.md) | `Tomlop` | TOML/YAML 変換、辞書比較、補完を提供する。 |
