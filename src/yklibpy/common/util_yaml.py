from pathlib import Path
from typing import Any, Optional

import yaml

from yklibpy.common.loggerx import Loggerx


class UtilYaml:
    _constructors_registered = False

    @classmethod
    def ignore_python_object_tag(cls, loader, node):
        """カスタムタグを辞書として読み込む"""
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node, deep=True)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node, deep=True)
        else:
            return loader.construct_scalar(node)

    @classmethod
    def _register_constructors(cls, tags: list[str]):
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
    def safe_load(cls, f):
        return yaml.load(f, Loader=yaml.SafeLoader)

    @classmethod
    def load_yaml(cls, input_path: Path) -> dict[str, Any]:
        """Load a YAML file and return it as a dictionary.

        Args:
            input_path (Path): Path to the YAML file.

        Returns:
            dict: Parsed YAML content.
        """
        data = {}
        Loggerx._debug(f"1 UtilYaml.load_yaml: input_path={input_path}", __name__)
        with open(input_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        if data is None:
            data = {}
        return data

    @classmethod
    def save_yaml(
        cls, assoc: dict[Any, Any], output_path: Optional[Path] = None
    ) -> str:
        """Serialize a dictionary to YAML and optionally save it to disk.

        Args:
            assoc (dict): Data to dump.
            output_path (Path | None): Destination path. When ``None`` the YAML
                string is merely returned.

        Returns:
            str: YAML representation of ``assoc``.
        """
        yaml_str = yaml.dump(
            assoc, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

        if output_path is not None:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(yaml_str)

        return yaml_str
