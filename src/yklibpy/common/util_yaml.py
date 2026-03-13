from pathlib import Path
from typing import Any, Optional

import yaml

from yklibpy.common.loggerx import Loggerx


class UtilYaml:
    """YAML の読み書きとカスタムタグ登録を補助する。"""

    _constructors_registered = False

    @classmethod
    def ignore_python_object_tag(cls, loader: Any, node: Any) -> Any:
        """未知の Python オブジェクトタグを安全な値へ変換する。"""
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node, deep=True)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node, deep=True)
        else:
            return loader.construct_scalar(node)

    @classmethod
    def _register_constructors(cls, tags: list[str]) -> None:
        """指定タグを `SafeLoader` で読めるように登録する。"""
        Loggerx.debug(f"1 UtilYaml._register_constructors: {tags}", __name__)
        if not cls._constructors_registered:
            Loggerx.debug(f"2 UtilYaml._register_constructors: {tags}", __name__)
            tags.append("tag:yaml.org,2002:python/object")
            # カスタムタグのコンストラクタを登録
            for tag in tags:
                yaml.add_constructor(
                    tag,
                    cls.ignore_python_object_tag,
                    yaml.SafeLoader,
                )
                Loggerx.debug(f"3 UtilYaml._register_constructors: tag={tag}", __name__)
        cls._constructors_registered = True

    @classmethod
    def safe_load(cls, f: Any) -> Any:
        """`SafeLoader` を使って YAML を読み込む。"""
        return yaml.load(f, Loader=yaml.SafeLoader)

    @classmethod
    def load_yaml(cls, input_path: Path) -> dict[str, Any]:
        """YAML ファイルを辞書として読み込む。"""
        data = {}
        Loggerx.debug(f"1 UtilYaml.load_yaml: input_path={input_path}", __name__)
        with open(input_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        if data is None:
            data = {}
        return data

    @classmethod
    def save_yaml(
        cls, assoc: dict[Any, Any], output_path: Optional[Path] = None
    ) -> str:
        """辞書を YAML 文字列へ変換し、必要ならファイルへ保存する。"""
        yaml_str = yaml.dump(
            assoc, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

        if output_path is not None:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(yaml_str)

        return yaml_str
