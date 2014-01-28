# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#    (c) Copyright 2013 Hewlett-Packard Development Company, L.P.
#    All Rights Reserved.
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
# @author: Swaminathan Vasudevan, Hewlett-Packard.
#

import logging

from neutronclient.neutron import v2_0 as neutronv20
from neutronclient.openstack.common.gettextutils import _


class ListVPNService(neutronv20.ListCommand):
    """List VPNService configurations that belong to a given tenant."""

    resource = 'vpnservice'
    log = logging.getLogger(__name__ + '.ListVPNService')
    list_columns = [
        'id', 'name', 'router_id', 'status'
    ]
    _formatters = {}
    pagination_support = True
    sorting_support = True


class ShowVPNService(neutronv20.ShowCommand):
    """Show information of a given VPNService."""

    resource = 'vpnservice'
    log = logging.getLogger(__name__ + '.ShowVPNService')


class CreateVPNService(neutronv20.CreateCommand):
    """Create a VPNService."""
    resource = 'vpnservice'
    log = logging.getLogger(__name__ + '.CreateVPNService')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false'))
        parser.add_argument(
            '--name',
            help=_('Set a name for the vpnservice'))
        parser.add_argument(
            '--description',
            help=_('Set a description for the vpnservice'))
        parser.add_argument(
            'router', metavar='ROUTER',
            help=_('Router unique identifier for the vpnservice'))
        parser.add_argument(
            'subnet', metavar='SUBNET',
            help=_('Subnet unique identifier for the vpnservice deployment'))

    def args2body(self, parsed_args):
        _subnet_id = neutronv20.find_resourceid_by_name_or_id(
            self.get_client(), 'subnet',
            parsed_args.subnet)
        _router_id = neutronv20.find_resourceid_by_name_or_id(
            self.get_client(), 'router',
            parsed_args.router)

        body = {self.resource: {'subnet_id': _subnet_id,
                                'router_id': _router_id,
                                'admin_state_up': parsed_args.admin_state}, }
        neutronv20.update_dict(parsed_args, body[self.resource],
                               ['name', 'description',
                                'tenant_id'])

        return body


class UpdateVPNService(neutronv20.UpdateCommand):
    """Update a given VPNService."""

    resource = 'vpnservice'
    log = logging.getLogger(__name__ + '.UpdateVPNService')


class DeleteVPNService(neutronv20.DeleteCommand):
    """Delete a given VPNService."""

    resource = 'vpnservice'
    log = logging.getLogger(__name__ + '.DeleteVPNService')
