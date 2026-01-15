import yaml


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
        if not cls._constructors_registered:
          tags.append("tag:yaml.org,2002:python/object")
          # カスタムタグのコンストラクタを登録
          for tag in tags:
            yaml.add_constructor(
                tag,
                cls.ignore_python_object_tag,
                yaml.SafeLoader,
            )
        cls._constructors_registered = True

    @classmethod
    def safe_load(cls, f):
        return yaml.load(f, Loader=yaml.SafeLoader)
