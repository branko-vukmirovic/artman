# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import os
import unittest

import mock

from artman.tasks.publish import local
from artman.utils.logger import logger


class LocalStagingTests(unittest.TestCase):
    @mock.patch.object(local.LocalStagingTask, 'exec_command')
    def test_execute(self, exec_command):
        # Run the task.
        task = local.LocalStagingTask()
        task.execute(
            gapic_code_dir=os.path.expanduser('~/foo/bar'),
            git_repo={
                'gapic_subpath': 'pubsub',
                'location': 'api-client-staging.git',
            },
            local_paths={'api_client_staging': '/path/to/acs'},
            output_dir='/path/to/output',
        )

        # Ensure we executed the commands we expect.
        assert exec_command.call_count == 4
        _, rm_cmd, _ = exec_command.mock_calls[0]
        assert rm_cmd[0] == ['rm', '-rf', '/path/to/acs/pubsub']
        _, cp_cmd, _ = exec_command.mock_calls[1]
        assert cp_cmd[0] == ['cp', '-rf', os.path.expanduser('~/foo/bar'),
            '/path/to/acs/pubsub',
        ]
        _, rm_cmd_2, _ = exec_command.mock_calls[2]
        assert rm_cmd_2[0] == ['rm', '-rf', os.path.expanduser('~/foo/bar')]
        _, rm_cmd_3, _ = exec_command.mock_calls[3]
        assert rm_cmd_3[0] == ['rm', '-rf', '/path/to/output']

    @mock.patch.object(local.LocalStagingTask, 'exec_command')
    def test_execute_output_dir_parent_of_gapic_dest(self, exec_command):
        # Run the task.
        task = local.LocalStagingTask()
        task.execute(
            gapic_code_dir=os.path.expanduser('~/foo/bar'),
            git_repo={
                'gapic_subpath': 'pubsub',
                'location': 'api-client-staging.git',
            },
            local_paths={'api_client_staging': '/path/to/acs'},
            output_dir='/path/to',
        )

        # Ensure we executed the commands we expect.
        assert exec_command.call_count == 3
        _, rm_cmd, _ = exec_command.mock_calls[0]
        assert rm_cmd[0] == ['rm', '-rf', '/path/to/acs/pubsub']
        _, cp_cmd, _ = exec_command.mock_calls[1]
        assert cp_cmd[0] == ['cp', '-rf', os.path.expanduser('~/foo/bar'),
            '/path/to/acs/pubsub',
        ]
        _, rm_cmd_2, _ = exec_command.mock_calls[2]
        assert rm_cmd_2[0] == ['rm', '-rf', os.path.expanduser('~/foo/bar')]
