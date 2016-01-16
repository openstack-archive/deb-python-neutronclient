# Copyright 2015 Huawei Technologies India Pvt. Ltd.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import sys

from mox3 import mox

from neutronclient.common import exceptions
from neutronclient.neutron.v2_0 import address_scope
from neutronclient.tests.unit import test_cli20


class CLITestV20AddressScopeJSON(test_cli20.CLITestV20Base):

    non_admin_status_resources = ['address_scope']

    def setUp(self):
        super(CLITestV20AddressScopeJSON, self).setUp(plurals={'tags': 'tag'})

    def test_create_address_scope_with_minimum_option(self):
        # Create address_scope: foo-address-scope with minimum option.
        resource = 'address_scope'
        cmd = address_scope.CreateAddressScope(
            test_cli20.MyApp(sys.stdout), None)
        name = 'foo-address-scope'
        myid = 'myid'
        args = [name]
        position_names = ['name']
        position_values = [name]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values)

    def test_create_address_scope_with_all_option(self):
        # Create address_scope: foo-address-scope with all options.
        resource = 'address_scope'
        cmd = address_scope.CreateAddressScope(
            test_cli20.MyApp(sys.stdout), None)
        name = 'foo-address-scope'
        myid = 'myid'
        args = [name, '--shared']
        position_names = ['name', 'shared']
        position_values = [name, True]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values)

    def test_create_address_scope_with_unicode(self):
        # Create address_scope: u'\u7f51\u7edc'.
        resource = 'address_scope'
        cmd = address_scope.CreateAddressScope(
            test_cli20.MyApp(sys.stdout), None)
        name = u'\u7f51\u7edc'
        myid = 'myid'
        args = [name]
        position_names = ['name']
        position_values = [name]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values)

    def test_update_address_scope_exception(self):
        # Update address_scope (Negative) : myid.
        resource = 'address_scope'
        cmd = address_scope.UpdateAddressScope(
            test_cli20.MyApp(sys.stdout), None)
        self.assertRaises(exceptions.CommandError, self._test_update_resource,
                          resource, cmd, 'myid', ['myid'], {})

    def test_update_address_scope(self):
        # Update address_scope: myid --name newname-address-scope.
        resource = 'address_scope'
        cmd = address_scope.UpdateAddressScope(
            test_cli20.MyApp(sys.stdout), None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'newname-address-scope'],
                                   {'name': 'newname-address-scope'}
                                   )

    def test_list_address_scope(self):
        # address_scope-list.
        resources = "address_scopes"
        cmd = address_scope.ListAddressScope(test_cli20.MyApp(sys.stdout),
                                             None)
        self._test_list_resources(resources, cmd, True)

    def test_list_address_scope_pagination(self):
        # address_scope-list.
        cmd = address_scope.ListAddressScope(test_cli20.MyApp(sys.stdout),
                                             None)
        self.mox.StubOutWithMock(address_scope.ListAddressScope,
                                 "extend_list")
        address_scope.ListAddressScope.extend_list(mox.IsA(list),
                                                   mox.IgnoreArg())
        self._test_list_resources_with_pagination("address_scopes",
                                                  cmd)
        self.mox.VerifyAll()
        self.mox.UnsetStubs()

    def test_list_address_scope_sort(self):
        # sorted list:
        # address_scope-list --sort-key name --sort-key id --sort-key asc
        # --sort-key desc
        resources = "address_scopes"
        cmd = address_scope.ListAddressScope(test_cli20.MyApp(sys.stdout),
                                             None)
        self._test_list_resources(resources, cmd,
                                  sort_key=["name", "id"],
                                  sort_dir=["asc", "desc"])

    def test_list_address_scope_limit(self):
        # size (1000) limited list: address_scope-list -P.
        resources = "address_scopes"
        cmd = address_scope.ListAddressScope(test_cli20.MyApp(sys.stdout),
                                             None)
        self._test_list_resources(resources, cmd, page_size=1000)

    def test_show_address_scope(self):
        # Show address_scope: --fields id --fields name myid.
        resource = 'address_scope'
        cmd = address_scope.ShowAddressScope(
            test_cli20.MyApp(sys.stdout), None)
        args = ['--fields', 'id', '--fields', 'name', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id, args,
                                 ['id', 'name'])

    def test_delete_address_scope(self):
        # Delete address_scope: address_scope_id.
        resource = 'address_scope'
        cmd = address_scope.DeleteAddressScope(
            test_cli20.MyApp(sys.stdout), None)
        myid = 'myid'
        args = [myid]
        self._test_delete_resource(resource, cmd, myid, args)
