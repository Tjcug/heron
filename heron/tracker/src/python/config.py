# Copyright 2016 Twitter. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml

from heron.statemgrs.src.python.config import Config as StateMgrConfig

STATEMGRS_KEY = "statemgrs"
VIZ_URL_FORMAT_KEY = "viz.url.format"

class Config:
  """
  Responsible for reading the yaml config file and
  exposing various tracker configs.
  """

  def __init__(self, conf_file):
    self.configs = None
    self.statemgr_config = StateMgrConfig()
    self.viz_url_format = None

    self.parse_config_file(conf_file)

  def parse_config_file(self, conf_file):
    expanded_conf_file_path = os.path.expanduser(conf_file)
    assert os.path.lexists(expanded_conf_file_path), "Config file does not exists: %s" % (conf_file)

    # Read the configuration file
    with open(expanded_conf_file_path, 'r') as f:
      self.configs = yaml.load(f)

    self.load_configs()

  def load_configs(self):
    self.statemgr_config.set_state_locations(self.configs[STATEMGRS_KEY])
    self.viz_url_format = self.validated_viz_url_format(self.configs[VIZ_URL_FORMAT_KEY])

  def validated_viz_url_format(self, viz_url_format):
    # We try to create a string by substituting all known
    # parameters. If an unknown parameter is present, an error
    # will be thrown
    valid_parameters = {
      "cluster": "dummy",
      "environ": "dummy",
      "jobname": "dummy",
      "role": "dummy",
      "submission_user": "dummy",
    }
    dummy_formatted_viz_url = viz_url_format.format(**valid_parameters)

    # No error is thrown, so the format is valid.
    return viz_url_format

  def get_formatted_viz_url(self, execution_state):
    """
    @param execution_state: The python dict representing JSON execution_state
    @return Formatted viz url
    """

    # We can directly use the whole execution state dict to format the viz_url
    return self.viz_url_format.format(**execution_state)