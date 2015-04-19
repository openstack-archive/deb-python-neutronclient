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

import re

from tempest_lib import exceptions

from neutronclient.tests.functional import base


class SimpleReadOnlyNeutronClientTest(base.ClientTestBase):

    """This is a first pass at a simple read only python-neutronclient test.
    This only exercises client commands that are read only.

    This should test commands:
    * as a regular user
    * as a admin user
    * with and without optional parameters
    * initially just check return codes, and later test command outputs

    """

    def test_admin_fake_action(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.neutron,
                          'this-does-neutron-exist')

    # NOTE(mestery): Commands in order listed in 'neutron help'

    # Optional arguments:

    def test_neutron_fake_action(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.neutron,
                          'this-does-not-exist')

    def test_neutron_net_list(self):
        net_list = self.parser.listing(self.neutron('net-list'))
        self.assertTableStruct(net_list, ['id', 'name', 'subnets'])

    def test_neutron_ext_list(self):
        ext = self.parser.listing(self.neutron('ext-list'))
        self.assertTableStruct(ext, ['alias', 'name'])

    def test_neutron_dhcp_agent_list_hosting_net(self):
        self.neutron('dhcp-agent-list-hosting-net',
                     params='private')

    def test_neutron_agent_list(self):
        agents = self.parser.listing(self.neutron('agent-list'))
        field_names = ['id', 'agent_type', 'host', 'alive', 'admin_state_up']
        self.assertTableStruct(agents, field_names)

    def test_neutron_floatingip_list(self):
        self.neutron('floatingip-list')

    def test_neutron_meter_label_list(self):
        self.neutron('meter-label-list')

    def test_neutron_meter_label_rule_list(self):
        self.neutron('meter-label-rule-list')

    def _test_neutron_lbaas_command(self, command):
        try:
            self.neutron(command)
        except exceptions.CommandFailed as e:
            if '404 Not Found' not in e.stderr:
                self.fail('%s: Unexpected failure.' % command)

    def test_neutron_lb_healthmonitor_list(self):
        self._test_neutron_lbaas_command('lb-healthmonitor-list')

    def test_neutron_lb_member_list(self):
        self._test_neutron_lbaas_command('lb-member-list')

    def test_neutron_lb_pool_list(self):
        self._test_neutron_lbaas_command('lb-pool-list')

    def test_neutron_lb_vip_list(self):
        self._test_neutron_lbaas_command('lb-vip-list')

    def test_neutron_net_external_list(self):
        net_ext_list = self.parser.listing(self.neutron('net-external-list'))
        self.assertTableStruct(net_ext_list, ['id', 'name', 'subnets'])

    def test_neutron_port_list(self):
        port_list = self.parser.listing(self.neutron('port-list'))
        self.assertTableStruct(port_list, ['id', 'name', 'mac_address',
                                           'fixed_ips'])

    def test_neutron_quota_list(self):
        self.neutron('quota-list')

    def test_neutron_router_list(self):
        router_list = self.parser.listing(self.neutron('router-list'))
        self.assertTableStruct(router_list, ['id', 'name',
                                             'external_gateway_info'])

    def test_neutron_security_group_list(self):
        security_grp = self.parser.listing(self.neutron('security-group-list'))
        self.assertTableStruct(security_grp, ['id', 'name',
                                              'security_group_rules'])

    def test_neutron_security_group_rule_list(self):
        security_grp = self.parser.listing(self.neutron
                                           ('security-group-rule-list'))
        self.assertTableStruct(security_grp, ['id', 'security_group',
                                              'direction', 'ethertype',
                                              'protocol/port', 'remote'])

    def test_neutron_subnet_list(self):
        subnet_list = self.parser.listing(self.neutron('subnet-list'))
        self.assertTableStruct(subnet_list, ['id', 'name', 'cidr',
                                             'allocation_pools'])

    def test_neutron_vpn_ikepolicy_list(self):
        ikepolicy = self.parser.listing(self.neutron('vpn-ikepolicy-list'))
        self.assertTableStruct(ikepolicy, ['id', 'name',
                                           'auth_algorithm',
                                           'encryption_algorithm',
                                           'ike_version', 'pfs'])

    def test_neutron_vpn_ipsecpolicy_list(self):
        ipsecpolicy = self.parser.listing(self.neutron('vpn-ipsecpolicy-list'))
        self.assertTableStruct(ipsecpolicy, ['id', 'name',
                                             'auth_algorithm',
                                             'encryption_algorithm',
                                             'pfs'])

    def test_neutron_vpn_service_list(self):
        vpn_list = self.parser.listing(self.neutron('vpn-service-list'))
        self.assertTableStruct(vpn_list, ['id', 'name',
                                          'router_id', 'status'])

    def test_neutron_ipsec_site_connection_list(self):
        ipsec_site = self.parser.listing(self.neutron
                                         ('ipsec-site-connection-list'))
        self.assertTableStruct(ipsec_site, ['id', 'name',
                                            'peer_address',
                                            'peer_cidrs',
                                            'route_mode',
                                            'auth_mode', 'status'])

    def test_neutron_firewall_list(self):
        firewall_list = self.parser.listing(self.neutron
                                            ('firewall-list'))
        self.assertTableStruct(firewall_list, ['id', 'name',
                                               'firewall_policy_id'])

    def test_neutron_firewall_policy_list(self):
        firewall_policy = self.parser.listing(self.neutron
                                              ('firewall-policy-list'))
        self.assertTableStruct(firewall_policy, ['id', 'name',
                                                 'firewall_rules'])

    def test_neutron_firewall_rule_list(self):
        firewall_rule = self.parser.listing(self.neutron
                                            ('firewall-rule-list'))
        self.assertTableStruct(firewall_rule, ['id', 'name',
                                               'firewall_policy_id',
                                               'summary', 'enabled'])

    def test_neutron_help(self):
        help_text = self.neutron('help')
        lines = help_text.split('\n')
        self.assertFirstLineStartsWith(lines, 'usage: neutron')

        commands = []
        cmds_start = lines.index('Commands for API v2.0:')
        command_pattern = re.compile('^ {2}([a-z0-9\-\_]+)')
        for line in lines[cmds_start:]:
            match = command_pattern.match(line)
            if match:
                commands.append(match.group(1))
        commands = set(commands)
        wanted_commands = set(('net-create', 'subnet-list', 'port-delete',
                               'router-show', 'agent-update', 'help'))
        self.assertFalse(wanted_commands - commands)

    # Optional arguments:

    def test_neutron_version(self):
        self.neutron('', flags='--version')

    def test_neutron_debug_net_list(self):
        self.neutron('net-list', flags='--debug')

    def test_neutron_quiet_net_list(self):
        self.neutron('net-list', flags='--quiet')
