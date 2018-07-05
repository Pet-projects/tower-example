# Copyright 2012, Dag Wieers <dag@wieers.com>
# Copyright 2016, Toshio Kuratomi <tkuratomi@ansible.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)

import os

__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    ''' Print statements during execution '''

    TRANSFERS_FILES = False
    VALID_ARGS = frozenset(('msg', 'x'))

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        for arg in self._task.args:
            if arg not in self.VALID_ARGS:
                return {"failed": True, "msg": "'%s' is not a valid option in debug" % arg}

        # Call super to initialise the parent class variables and run some checks
        result = super(ActionModule, self).run(tmp, task_vars)

        # Read the files
        path_to_file = os.path.join(os.path.dirname(__file__), "my_debug_files", "custom_message.txt")
        message_from_file = open(path_to_file, 'r').read()
        message_data = message_from_file + self._task.args['msg']

        # Copy to remote
        super(ActionModule, self)._transfer_data("/tmp/mydata.txt", message_data)

        # Set as response
        if 'msg' in self._task.args:
            result['msg'] = message_data

        # force flag to make debug output module always verbose
        result['_ansible_verbose_always'] = True

        return result
