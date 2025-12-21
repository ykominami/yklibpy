import toml
# import tomllib  # 3.11以上の場合
import sys
import yaml
import json
import os
from pathlib import Path
from .util import Util

class FileItem:
    def __init__(self, file):
        self.file_file = file
        self.file_path = Path(file)
        self.file_type = self.get_file_type(file) if file else None

    def get_file_type(self, file_path):
        """
        引数で指定されたファイルのパスから拡張子を取り出し、大文字小文字の区別なく、
        ファイルの種別を文字列で返す。
        
        Args:
            file_path: ファイルパス
        
        Returns:
            "YAML": .yaml, .yml の場合
            "JSON": .json の場合
            "TOML": .toml の場合
            "TEXT": .txt の場合
            "OTHER": 上記以外の場合
            None: file_path が None の場合
        """
        if file_path is None:
            return None
        _, ext = os.path.splitext(file_path)
        ext_lower = ext.lower()
        
        if ext_lower in ['.yaml', '.yml']:
            return "YAML"
        elif ext_lower == '.json':
            return "JSON"
        elif ext_lower == '.toml':
            return "TOML"
        elif ext_lower == '.txt':
            return "TEXT"
        else:
            return "OTHER"

class Tomlop:
    def __init__(self):
        pass

    def setup(self, ref_file, config_file):
        self.ref_file_item = FileItem(ref_file)
        self.config_file_item = FileItem(ref_file)
        self.data = None

    def compare_dict(self, dict1, dict2):
        """
        引数1と引数2のキーとキーに対応する値が完全に一致しているかを判定する。
        値が連想配列の場合は再帰的に処理する。
        
        Args:
            dict1: 比較元の入れ子の連想配列（辞書）
            dict2: 比較先の入れ子の連想配列（辞書）
        
        Returns:
            True: 引数1と引数2のキーとキーに対応する値が完全に一致している場合
            False: 引数1と引数2のキーとキーに対応する値がどれか一つでも一致しない場合
        """
        # キーの集合が一致しない場合はFalse
        if set(dict1.keys()) != set(dict2.keys()):
            return False
        
        # 各キーと値のペアを比較
        for key in dict1.keys():
            value1 = dict1[key]
            value2 = dict2[key]
            
            # 両方とも辞書の場合は再帰的に比較
            if isinstance(value1, dict) and isinstance(value2, dict):
                if not self.compare_dict(value1, value2):
                    return False
            # 値が一致しない場合はFalse
            elif value1 != value2:
                return False
        
        return True

    def merge_dict(self, dict1, dict2):
        """
        引数2の連想配列のキーが引数1に存在しない場合、そのキーと値を引数1に追加する。
        値が連想配列の場合は再帰的に処理する。
        
        Args:
            dict1: 比較元の入れ子の連想配列（辞書）
            dict2: 比較先の入れ子の連想配列（辞書）
        
        Returns:
            dict1: マージ後の辞書（引数1を直接変更）
        """
        for key, value in dict2.items():
            if key not in dict1:
                # キーが存在しない場合は追加
                dict1[key] = value
            elif isinstance(dict1[key], dict) and isinstance(value, dict):
                # 両方とも辞書の場合は再帰的に処理
                self.merge_dict(dict1[key], value)
        return dict1

    def diff_dict(self, dict1, dict2):
        """
        比較元と比較先の入れ子の連想配列の差分を文字列として返す。
        値が連想配列の場合は再帰的に処理する。
        
        Args:
            dict1: 比較元の入れ子の連想配列（辞書）
            dict2: 比較先の入れ子の連想配列（辞書）
        
        Returns:
            差分がない場合: 空文字列
            差分がある場合: 差分の状態を示す見出し行と、差分の内容を示す行からなる文字列
        """
        result_lines = []
        
        # すべてのキーを収集
        all_keys = set(dict1.keys()) | set(dict2.keys())
        
        # 各キーについて差分をチェック
        for key in sorted(all_keys):
            if key not in dict2:
                # 比較元のキーのみが存在する場合
                result_lines.append("# 比較元のキーのみ存在")
                result_lines.append(key)
                value_str = self._format_value(dict1[key])
                result_lines.append(f"  {value_str}")
            elif key not in dict1:
                # 比較先のキーのみが存在する場合
                result_lines.append("# 比較先のキーのみ存在")
                result_lines.append(key)
                value_str = self._format_value(dict2[key])
                result_lines.append(f"  {value_str}")
            else:
                # 両方にキーが存在する場合
                value1 = dict1[key]
                value2 = dict2[key]
                
                # 両方とも辞書の場合は再帰的に処理
                if isinstance(value1, dict) and isinstance(value2, dict):
                    nested_diff = self.diff_dict(value1, value2)
                    if nested_diff:
                        result_lines.append(f"# 値が異なる")
                        result_lines.append(key)
                        result_lines.append("## 比較元の値")
                        value_str1 = self._format_value(value1)
                        result_lines.append(f"  {value_str1}")
                        result_lines.append("## 比較先の値")
                        value_str2 = self._format_value(value2)
                        result_lines.append(f"  {value_str2}")
                elif value1 != value2:
                    # 値が異なる場合
                    result_lines.append("# 値が異なる")
                    result_lines.append(key)
                    result_lines.append("## 比較元の値")
                    value_str1 = self._format_value(value1)
                    result_lines.append(f"  {value_str1}")
                    result_lines.append("## 比較先の値")
                    value_str2 = self._format_value(value2)
                    result_lines.append(f"  {value_str2}")
        
        return "\n".join(result_lines) if result_lines else ""

    def _format_value(self, value):
        """
        値を文字列としてフォーマットする。
        辞書の場合は見やすい形式で表示する。
        """
        if isinstance(value, dict):
            # 辞書の場合は見やすい形式で表示
            items = []
            for k, v in value.items():
                if isinstance(v, dict):
                    items.append(f"{k}: {{...}}")
                else:
                    items.append(f"{k}: {v}")
            return "{" + ", ".join(items) + "}"
        else:
            return str(value)

    def read_toml_external(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                print(f'file_path = {file_path}')
                try:
                    self.data = toml.load(f)
                except Exception as e:
                    print(f"エラー: {e}")
                    return None
                # print(f'data={self.data}')
                # print(f'self.data["project"]={self.data["project"]}')
                print(f'self.data["project"]["authors"]={self.data["project"]["authors"]}')
                return self.data
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
            return None

    def write_toml_external(self, file_path, data):
        """
        tomlを用いて、引数で渡された連想配列を、引数で指定されたパスに、TOML形式ファイル出力する。
        
        Args:
            file_path: TOML形式ファイルへのパス
            data: 連想配列（辞書）
        
        Returns:
            True: 書き込み成功
            False: 書き込み失敗
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                toml.dump(data, f)
            return True
        except Exception as e:
            print(f"ファイルの書き込みに失敗しました: {file_path}")
            print(f"エラー: {e}")
            return False

    def load_toml(self,ref_file):
        print(f"ref_file={ref_file}")
        ref = None
        if ref_file:
            ref = self.read_toml_external(ref_file)
        if ref is not None:
            print(ref.keys())
            print("--------------------------------")
        return ref

    def load_file(self, file_path):
        file_item = FileItem(file_path)
        file_type = file_item.get_file_type(file_path)
        if file_type == "TOML":
            return self.load_toml(file_path)
        elif file_type == "YAML":
            return self.load_yaml(file_path)
        elif file_type == "JSON":
            return self.load_json(file_path)
        else:
            return None

    def exec(self):
        ref = self.load_file(self.ref_file_item.file_path)
        config = self.load_file(self.config_file_item.file_path)

        new_config = self.merge_dict(config, ref)
        result = self.compare_dict(new_config, ref)
        print(f"# result={result}")
        print(f'# new_config={new_config}')
        diff_result = self.diff_dict(new_config, ref)
        print(f"# diff")
        print(f'diff_result={diff_result}')
        self.write_toml_external("new_pyproject.toml", new_config)

    def store_yaml(self, file_path, data):
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)

    def load_yaml(self, file_path):
        """
        YAMLファイルを読み込んで辞書として返す。
        
        Args:
            file_path: YAMLファイルへのパス
        
        Returns:
            読み込んだデータ（辞書）、失敗時はNone
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
            return None
        except Exception as e:
            print(f"YAMLファイルの読み込みに失敗しました: {file_path}")
            print(f"エラー: {e}")
            return None

    def load_json(self, file_path):
        """
        JSONファイルを読み込んで辞書として返す。
        
        Args:
            file_path: JSONファイルへのパス
        
        Returns:
            読み込んだデータ（辞書）、失敗時はNone
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
            return None
        except Exception as e:
            print(f"JSONファイルの読み込みに失敗しました: {file_path}")
            print(f"エラー: {e}")
            return None

    # @classmethod
    def main(self):
        ref_file = None
        ref_file = sys.argv[1] if len(sys.argv) > 1 else None
        config_file = sys.argv[2] if len(sys.argv) > 2 else "pyproject.toml"
        if ref_file is not None:
            self.setup(ref_file, config_file)
            self.exec()
            new_file_path = self.ref_file_item.file_path.with_suffix(".yaml")
            self.store_yaml(new_file_path, self.data)

    def toml2yaml(self):
        ref_file = None
        src_file = sys.argv[1] if len(sys.argv) > 1 else None
        if src_file is not None:
            self.setup(src_file, None)
            new_file_path = self.ref_file_item.file_path.with_suffix(".yaml")
            self.read_toml_external(self.ref_file_item.file_path)
            # print(f"self.data={self.data}")
            output_path = Path("a.yaml")
            Util.save_yaml(self.data, output_path)
            # self.store_yaml(new_file_path, self.data)

    def yaml2toml(self):
        input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
        data = Util.load_yaml(input_path)
        print(f"data={data}")
        new_file_path = input_path.with_suffix(".toml")
        print(f"new_file_path={new_file_path}")
        # self.write_toml_external(new_file_path, data)
        # print(f"input_path={input_path}")
        '''
        ref_file = None
        src_file = sys.argv[1] if len(sys.argv) > 1 else None
        if src_file is not None:
            self.setup(src_file, None)
            new_file_path = self.ref_file_item.file_path.with_suffix(".yaml")
            self.read_toml_external(self.ref_file_item.file_path)
            self.store_yaml(new_file_path, self.data)
        '''

def zmain():
    tomlop = Tomlop()
    tomlop.main()

def toml2yaml():
    tomlop = Tomlop()
    tomlop.toml2yaml()

def yaml2toml():
    tomlop = Tomlop()
    tomlop.yaml2toml()

if __name__ == "__main__":
    tomlop = Tomlop()
    tomlop.main()
    
# 使用例
# new_config は exec() 内で定義されているため、ここでは使用できない
# tomlop.store_yaml("new_pyproject.yaml", new_config)

# データの取り出し
# print(f"ツール名: {config['title']}")
# print(f"対象フォルダ: {config['settings']['target_dir']}")
# print(f"出力先: {config['settings']['output_file']}")