# Copyright 2015 Huawei Technologies India Pvt. Ltd..
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

from neutronclient._i18n import _
from neutronclient.neutron import v2_0 as neutronV20


class ListAddressScope(neutronV20.ListCommand):
    """List address scopes that belong to a given tenant."""

    resource = 'address_scope'
    list_columns = ['id', 'name']
    pagination_support = True
    sorting_support = True


class ShowAddressScope(neutronV20.ShowCommand):
    """Show information about an address scope."""

    resource = 'address_scope'


class CreateAddressScope(neutronV20.CreateCommand):
    """Create an address scope for a given tenant."""

    resource = 'address_scope'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--shared',
            action='store_true',
            help=_('Set the address scope as shared.'))
        parser.add_argument(
            'name',
            help=_('Specify the name of the address scope.'))

    def args2body(self, parsed_args):
        body = {'name': parsed_args.name}
        if parsed_args.shared:
            body['shared'] = True
        neutronV20.update_dict(parsed_args, body, ['tenant_id'])
        return {self.resource: body}


class DeleteAddressScope(neutronV20.DeleteCommand):
    """Delete an address scope."""

    resource = 'address_scope'


class UpdateAddressScope(neutronV20.UpdateCommand):
    """Update an address scope."""

    resource = 'address_scope'

    def add_known_arguments(self, parser):
        parser.add_argument('--name',
                            help=_('Name of the address scope to update.'))

    def args2body(self, parsed_args):
        body = {}
        neutronV20.update_dict(parsed_args, body, ['name'])
        return {self.resource: body}
