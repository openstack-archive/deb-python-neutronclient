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

import argparse
import logging

from neutronclient.neutron import v2_0 as neutronV20
from neutronclient.openstack.common.gettextutils import _


class ListFloatingIP(neutronV20.ListCommand):
    """List floating ips that belong to a given tenant."""

    resource = 'floatingip'
    log = logging.getLogger(__name__ + '.ListFloatingIP')
    list_columns = ['id', 'fixed_ip_address', 'floating_ip_address',
                    'port_id']
    pagination_support = True
    sorting_support = True


class ShowFloatingIP(neutronV20.ShowCommand):
    """Show information of a given floating ip."""

    resource = 'floatingip'
    log = logging.getLogger(__name__ + '.ShowFloatingIP')
    allow_names = False


class CreateFloatingIP(neutronV20.CreateCommand):
    """Create a floating ip for a given tenant."""

    resource = 'floatingip'
    log = logging.getLogger(__name__ + '.CreateFloatingIP')

    def add_known_arguments(self, parser):
        parser.add_argument(
            'floating_network_id', metavar='FLOATING_NETWORK',
            help=_('Network name or id to allocate floating IP from'))
        parser.add_argument(
            '--port-id',
            help=_('ID of the port to be associated with the floatingip'))
        parser.add_argument(
            '--port_id',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--fixed-ip-address',
            help=_('IP address on the port (only required if port has multiple'
                   'IPs)'))
        parser.add_argument(
            '--fixed_ip_address',
            help=argparse.SUPPRESS)

    def args2body(self, parsed_args):
        _network_id = neutronV20.find_resourceid_by_name_or_id(
            self.get_client(), 'network', parsed_args.floating_network_id)
        body = {self.resource: {'floating_network_id': _network_id}}
        if parsed_args.port_id:
            body[self.resource].update({'port_id': parsed_args.port_id})
        if parsed_args.tenant_id:
            body[self.resource].update({'tenant_id': parsed_args.tenant_id})
        if parsed_args.fixed_ip_address:
            body[self.resource].update({'fixed_ip_address':
                                        parsed_args.fixed_ip_address})
        return body


class DeleteFloatingIP(neutronV20.DeleteCommand):
    """Delete a given floating ip."""

    log = logging.getLogger(__name__ + '.DeleteFloatingIP')
    resource = 'floatingip'
    allow_names = False


class AssociateFloatingIP(neutronV20.NeutronCommand):
    """Create a mapping between a floating ip and a fixed ip."""

    api = 'network'
    log = logging.getLogger(__name__ + '.AssociateFloatingIP')
    resource = 'floatingip'

    def get_parser(self, prog_name):
        parser = super(AssociateFloatingIP, self).get_parser(prog_name)
        parser.add_argument(
            'floatingip_id', metavar='FLOATINGIP_ID',
            help=_('ID of the floating IP to associate'))
        parser.add_argument(
            'port_id', metavar='PORT',
            help=_('ID or name of the port to be associated with the '
                   'floatingip'))
        parser.add_argument(
            '--fixed-ip-address',
            help=_('IP address on the port (only required if port has multiple'
                   'IPs)'))
        parser.add_argument(
            '--fixed_ip_address',
            help=argparse.SUPPRESS)
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format
        update_dict = {}
        if parsed_args.port_id:
            update_dict['port_id'] = parsed_args.port_id
        if parsed_args.fixed_ip_address:
            update_dict['fixed_ip_address'] = parsed_args.fixed_ip_address
        neutron_client.update_floatingip(parsed_args.floatingip_id,
                                         {'floatingip': update_dict})
        print >>self.app.stdout, (
            _('Associated floatingip %s') % parsed_args.floatingip_id)


class DisassociateFloatingIP(neutronV20.NeutronCommand):
    """Remove a mapping from a floating ip to a fixed ip.
    """

    api = 'network'
    log = logging.getLogger(__name__ + '.DisassociateFloatingIP')
    resource = 'floatingip'

    def get_parser(self, prog_name):
        parser = super(DisassociateFloatingIP, self).get_parser(prog_name)
        parser.add_argument(
            'floatingip_id', metavar='FLOATINGIP_ID',
            help=_('ID of the floating IP to associate'))
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format
        neutron_client.update_floatingip(parsed_args.floatingip_id,
                                         {'floatingip': {'port_id': None}})
        print >>self.app.stdout, (
            _('Disassociated floatingip %s') % parsed_args.floatingip_id)
