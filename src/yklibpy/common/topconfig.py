import json
from pathlib import Path
from typing import List
from .util import Util
from .env import Env

class TopConfig:
  def __init__(self, config_file_path: Path):
    self.config_file_path = config_file_path
    self.config = Util.load_yaml(self.config_file_path)
    self.parent_path = self.config_file_path.parent

    self.assoc = Util.load_yaml(self.config_file_path)
    print(f"assoc={self.assoc}")
    self.main_config_file = self.assoc.get("config_file", None)
    self.main_config_file_path = self.parent_path / Path(self.main_config_file)
    print(f"main_config_file_path={self.main_config_file_path}")
    self.env = Env(self.main_config_file_path)
    self.patterns = self.assoc["patterns"] if "patterns" in self.assoc else ["Amazon-KU-1-file"]
    self.output_file = self.assoc["output_file"] if "output_file" in self.assoc else ["output_0.yaml"]
    self.output_file_path = self.parent_path / Path(self.output_file)
    self.input_file = self.assoc["input_file"] if "input_file" in self.assoc else None
    if self.input_file is not None:
      self.input_file_path = self.parent_path / Path(self.input_file)
    else:
      self.input_file_path = None

  def get_main_config_file_path(self) -> Path:
    return self.main_config_file_path

  def get_env(self) -> Env:
    return self.env

  def get_patterns(self) -> List[str]:
    return self.patterns  

  def get_output_file_path(self) -> Path:
    return self.output_file_path

  def get_output_file_name(self) -> str:
    return self.output_file

  def get_input_file_path(self) -> Path:
    return self.input_file_path

  def get_input_file_name(self) -> str:
    return self.input_file
