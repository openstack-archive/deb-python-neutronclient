# Copyright 2013 Mirantis Inc.
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


class ListMember(neutronV20.ListCommand):
    """List members that belong to a given tenant."""

    resource = 'member'
    list_columns = [
        'id', 'address', 'protocol_port', 'weight', 'admin_state_up', 'status'
    ]
    pagination_support = True
    sorting_support = True


class ShowMember(neutronV20.ShowCommand):
    """Show information of a given member."""

    resource = 'member'
    allow_names = False


class CreateMember(neutronV20.CreateCommand):
    """Create a member."""

    resource = 'member'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false.'))
        parser.add_argument(
            '--weight',
            help=_('Weight of pool member in the pool (default:1, [0..256]).'))
        parser.add_argument(
            '--address',
            required=True,
            help=_('IP address of the pool member on the pool network.'))
        parser.add_argument(
            '--protocol-port',
            required=True,
            help=_('Port on which the pool member listens for requests or '
                   'connections.'))
        parser.add_argument(
            'pool_id', metavar='POOL',
            help=_('Pool ID or name this vip belongs to.'))

    def args2body(self, parsed_args):
        _pool_id = neutronV20.find_resourceid_by_name_or_id(
            self.get_client(), 'pool', parsed_args.pool_id)
        body = {'pool_id': _pool_id,
                'admin_state_up': parsed_args.admin_state}
        neutronV20.update_dict(
            parsed_args,
            body,
            ['address', 'protocol_port', 'weight', 'tenant_id']
        )
        return {self.resource: body}


class UpdateMember(neutronV20.UpdateCommand):
    """Update a given member."""

    resource = 'member'


class DeleteMember(neutronV20.DeleteCommand):
    """Delete a given member."""

    resource = 'member'
