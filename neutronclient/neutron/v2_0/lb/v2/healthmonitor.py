# Copyright 2013 Mirantis Inc.
# Copyright 2014 Blue Box Group, Inc.
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


class ListHealthMonitor(neutronV20.ListCommand):
    """LBaaS v2 List healthmonitors that belong to a given tenant."""

    resource = 'healthmonitor'
    shadow_resource = 'lbaas_healthmonitor'
    list_columns = ['id', 'name', 'type', 'admin_state_up']
    pagination_support = True
    sorting_support = True


class ShowHealthMonitor(neutronV20.ShowCommand):
    """LBaaS v2 Show information of a given healthmonitor."""

    resource = 'healthmonitor'
    shadow_resource = 'lbaas_healthmonitor'


class CreateHealthMonitor(neutronV20.CreateCommand):
    """LBaaS v2 Create a healthmonitor."""

    resource = 'healthmonitor'
    shadow_resource = 'lbaas_healthmonitor'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            help=_('Name of the health monitor to be created.'))
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false.'))
        parser.add_argument(
            '--expected-codes',
            help=_('The list of HTTP status codes expected in '
                   'response from the member to declare it healthy. This '
                   'attribute can contain one value, '
                   'or a list of values separated by comma, '
                   'or a range of values (e.g. "200-299"). If this attribute '
                   'is not specified, it defaults to "200".'))
        parser.add_argument(
            '--http-method',
            help=_('The HTTP method used for requests by the monitor of type '
                   'HTTP.'))
        parser.add_argument(
            '--url-path',
            help=_('The HTTP path used in the HTTP request used by the monitor'
                   ' to test a member health. This must be a string '
                   'beginning with a / (forward slash).'))
        parser.add_argument(
            '--delay',
            required=True,
            help=_('The time in seconds between sending probes to members.'))
        parser.add_argument(
            '--max-retries',
            required=True,
            help=_('Number of permissible connection failures before changing '
                   'the member status to INACTIVE. [1..10].'))
        parser.add_argument(
            '--timeout',
            required=True,
            help=_('Maximum number of seconds for a monitor to wait for a '
                   'connection to be established before it times out. The '
                   'value must be less than the delay value.'))
        parser.add_argument(
            '--type',
            required=True, choices=['PING', 'TCP', 'HTTP', 'HTTPS'],
            help=_('One of the predefined health monitor types.'))
        parser.add_argument(
            '--pool', required=True,
            help=_('ID or name of the pool that this healthmonitor will '
                   'monitor.'))

    def args2body(self, parsed_args):
        pool_id = neutronV20.find_resourceid_by_name_or_id(
            self.get_client(), 'pool', parsed_args.pool,
            cmd_resource='lbaas_pool')
        body = {'admin_state_up': parsed_args.admin_state,
                'delay': parsed_args.delay,
                'max_retries': parsed_args.max_retries,
                'timeout': parsed_args.timeout,
                'type': parsed_args.type,
                'pool_id': pool_id}
        neutronV20.update_dict(parsed_args, body,
                               ['expected_codes', 'http_method', 'url_path',
                                'tenant_id', 'name'])
        return {self.resource: body}


class UpdateHealthMonitor(neutronV20.UpdateCommand):
    """LBaaS v2 Update a given healthmonitor."""

    resource = 'healthmonitor'
    shadow_resource = 'lbaas_healthmonitor'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            help=_('Updated name of the health monitor.'))

    def args2body(self, parsed_args):
        body = {}
        neutronV20.update_dict(parsed_args, body, ['name'])
        return {self.resource: body}


class DeleteHealthMonitor(neutronV20.DeleteCommand):
    """LBaaS v2 Delete a given healthmonitor."""

    resource = 'healthmonitor'
    shadow_resource = 'lbaas_healthmonitor'
