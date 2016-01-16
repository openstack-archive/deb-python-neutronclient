# Copyright 2012 OpenStack Foundation.
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

from __future__ import print_function

import argparse

from neutronclient._i18n import _
from neutronclient.neutron import v2_0 as neutronV20


class ListFloatingIP(neutronV20.ListCommand):
    """List floating IPs that belong to a given tenant."""

    resource = 'floatingip'
    list_columns = ['id', 'fixed_ip_address', 'floating_ip_address',
                    'port_id']
    pagination_support = True
    sorting_support = True


class ShowFloatingIP(neutronV20.ShowCommand):
    """Show information of a given floating IP."""

    resource = 'floatingip'
    allow_names = False


class CreateFloatingIP(neutronV20.CreateCommand):
    """Create a floating IP for a given tenant."""

    resource = 'floatingip'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'floating_network_id', metavar='FLOATING_NETWORK',
            help=_('Network name or ID to allocate floating IP from.'))
        parser.add_argument(
            '--port-id',
            help=_('ID of the port to be associated with the floating IP.'))
        parser.add_argument(
            '--port_id',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--fixed-ip-address',
            help=_('IP address on the port (only required if port has '
                   'multiple IPs).'))
        parser.add_argument(
            '--fixed_ip_address',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--floating-ip-address',
            help=_('IP address of the floating IP'))
        parser.add_argument(
            '--subnet',
            dest='subnet_id',
            help=_('Subnet ID on which you want to create the floating IP.'))

    def args2body(self, parsed_args):
        _network_id = neutronV20.find_resourceid_by_name_or_id(
            self.get_client(), 'network', parsed_args.floating_network_id)
        body = {'floating_network_id': _network_id}
        neutronV20.update_dict(parsed_args, body,
                               ['port_id', 'tenant_id',
                                'fixed_ip_address',
                                'floating_ip_address', 'subnet_id'])
        return {self.resource: body}


class DeleteFloatingIP(neutronV20.DeleteCommand):
    """Delete a given floating IP."""

    resource = 'floatingip'
    allow_names = False


class AssociateFloatingIP(neutronV20.NeutronCommand):
    """Create a mapping between a floating IP and a fixed IP."""

    api = 'network'
    resource = 'floatingip'

    def get_parser(self, prog_name):
        parser = super(AssociateFloatingIP, self).get_parser(prog_name)
        parser.add_argument(
            'floatingip_id', metavar='FLOATINGIP_ID',
            help=_('ID of the floating IP to associate.'))
        parser.add_argument(
            'port_id', metavar='PORT',
            help=_('ID or name of the port to be associated with the '
                   'floating IP.'))
        parser.add_argument(
            '--fixed-ip-address',
            help=_('IP address on the port (only required if port has '
                   'multiple IPs).'))
        parser.add_argument(
            '--fixed_ip_address',
            help=argparse.SUPPRESS)
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        update_dict = {}
        neutronV20.update_dict(parsed_args, update_dict,
                               ['port_id', 'fixed_ip_address'])
        neutron_client.update_floatingip(parsed_args.floatingip_id,
                                         {'floatingip': update_dict})
        print(_('Associated floating IP %s') % parsed_args.floatingip_id,
              file=self.app.stdout)


class DisassociateFloatingIP(neutronV20.NeutronCommand):
    """Remove a mapping from a floating IP to a fixed IP."""

    api = 'network'
    resource = 'floatingip'

    def get_parser(self, prog_name):
        parser = super(DisassociateFloatingIP, self).get_parser(prog_name)
        parser.add_argument(
            'floatingip_id', metavar='FLOATINGIP_ID',
            help=_('ID of the floating IP to disassociate.'))
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.update_floatingip(parsed_args.floatingip_id,
                                         {'floatingip': {'port_id': None}})
        print(_('Disassociated floating IP %s') % parsed_args.floatingip_id,
              file=self.app.stdout)
