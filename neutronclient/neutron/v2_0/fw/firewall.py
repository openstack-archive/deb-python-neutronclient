# Copyright 2013 Big Switch Networks
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
# @author: KC Wang, Big Switch Networks
#

import argparse
import logging

from neutronclient.neutron import v2_0 as neutronv20
from neutronclient.openstack.common.gettextutils import _


class ListFirewall(neutronv20.ListCommand):
    """List firewalls that belong to a given tenant."""

    resource = 'firewall'
    log = logging.getLogger(__name__ + '.ListFirewall')
    list_columns = ['id', 'name', 'firewall_policy_id']
    _formatters = {}
    pagination_support = True
    sorting_support = True


class ShowFirewall(neutronv20.ShowCommand):
    """Show information of a given firewall."""

    resource = 'firewall'
    log = logging.getLogger(__name__ + '.ShowFirewall')


class CreateFirewall(neutronv20.CreateCommand):
    """Create a firewall."""

    resource = 'firewall'
    log = logging.getLogger(__name__ + '.CreateFirewall')

    def add_known_arguments(self, parser):
        parser.add_argument(
            'firewall_policy_id', metavar='POLICY',
            help=_('Firewall policy id'))
        parser.add_argument(
            '--name',
            help=_('Name for the firewall'))
        parser.add_argument(
            '--description',
            help=_('Description for the firewall rule'))
        parser.add_argument(
            '--shared',
            action='store_true',
            help=_('Set shared to True (default False)'),
            default=argparse.SUPPRESS)
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state',
            action='store_false',
            help=_('Set admin state up to false'))

    def args2body(self, parsed_args):
        _policy_id = neutronv20.find_resourceid_by_name_or_id(
            self.get_client(), 'firewall_policy',
            parsed_args.firewall_policy_id)
        body = {
            self.resource: {
                'firewall_policy_id': _policy_id,
                'admin_state_up': parsed_args.admin_state, }, }
        neutronv20.update_dict(parsed_args, body[self.resource],
                               ['name', 'description', 'shared',
                                'tenant_id'])
        return body


class UpdateFirewall(neutronv20.UpdateCommand):
    """Update a given firewall."""

    resource = 'firewall'
    log = logging.getLogger(__name__ + '.UpdateFirewall')


class DeleteFirewall(neutronv20.DeleteCommand):
    """Delete a given firewall."""

    resource = 'firewall'
    log = logging.getLogger(__name__ + '.DeleteFirewall')
