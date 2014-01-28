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
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import sys

from neutronclient.neutron.v2_0 import subnet
from neutronclient.tests.unit import test_cli20


class CLITestV20SubnetJSON(test_cli20.CLITestV20Base):
    def setUp(self):
        super(CLITestV20SubnetJSON, self).setUp(plurals={'tags': 'tag'})

    def test_create_subnet(self):
        """Create subnet: --gateway gateway netid cidr."""
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'cidrvalue'
        gateway = 'gatewayvalue'
        args = ['--gateway', gateway, netid, cidr]
        position_names = ['ip_version', 'network_id', 'cidr', 'gateway_ip']
        position_values = [4, netid, cidr, gateway]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values)

    def test_create_subnet_with_no_gateway(self):
        """Create subnet: --no-gateway netid cidr."""
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'cidrvalue'
        args = ['--no-gateway', netid, cidr]
        position_names = ['ip_version', 'network_id', 'cidr', 'gateway_ip']
        position_values = [4, netid, cidr, None]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values)

    def test_create_subnet_with_bad_gateway_option(self):
        """Create sbunet: --no-gateway netid cidr."""
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'cidrvalue'
        gateway = 'gatewayvalue'
        args = ['--gateway', gateway, '--no-gateway', netid, cidr]
        position_names = ['ip_version', 'network_id', 'cidr', 'gateway_ip']
        position_values = [4, netid, cidr, None]
        try:
            self._test_create_resource(resource, cmd, name, myid, args,
                                       position_names, position_values)
        except Exception:
            return
        self.fail('No exception for bad gateway option')

    def test_create_subnet_tenant(self):
        """Create subnet: --tenant_id tenantid netid cidr."""
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid', netid, cidr]
        position_names = ['ip_version', 'network_id', 'cidr']
        position_values = [4, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_tags(self):
        """Create subnet: netid cidr --tags a b."""
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = [netid, cidr, '--tags', 'a', 'b']
        position_names = ['ip_version', 'network_id', 'cidr']
        position_values = [4, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tags=['a', 'b'])

    def test_create_subnet_allocation_pool(self):
        """Create subnet: --tenant_id tenantid <allocation_pool> netid cidr.
        The <allocation_pool> is --allocation_pool start=1.1.1.10,end=1.1.1.20
        """
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--allocation_pool', 'start=1.1.1.10,end=1.1.1.20',
                netid, cidr]
        position_names = ['ip_version', 'allocation_pools', 'network_id',
                          'cidr']
        pool = [{'start': '1.1.1.10', 'end': '1.1.1.20'}]
        position_values = [4, pool, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_allocation_pools(self):
        """Create subnet: --tenant-id tenantid <pools> netid cidr.
        The <pools> are --allocation_pool start=1.1.1.10,end=1.1.1.20 and
        --allocation_pool start=1.1.1.30,end=1.1.1.40
        """
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--allocation_pool', 'start=1.1.1.10,end=1.1.1.20',
                '--allocation_pool', 'start=1.1.1.30,end=1.1.1.40',
                netid, cidr]
        position_names = ['ip_version', 'allocation_pools', 'network_id',
                          'cidr']
        pools = [{'start': '1.1.1.10', 'end': '1.1.1.20'},
                 {'start': '1.1.1.30', 'end': '1.1.1.40'}]
        position_values = [4, pools, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_host_route(self):
        """Create subnet: --tenant_id tenantid <host_route> netid cidr.
        The <host_route> is
        --host-route destination=172.16.1.0/24,nexthop=1.1.1.20
        """
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--host-route', 'destination=172.16.1.0/24,nexthop=1.1.1.20',
                netid, cidr]
        position_names = ['ip_version', 'host_routes', 'network_id',
                          'cidr']
        route = [{'destination': '172.16.1.0/24', 'nexthop': '1.1.1.20'}]
        position_values = [4, route, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_host_routes(self):
        """Create subnet: --tenant-id tenantid <host_routes> netid cidr.
        The <host_routes> are
        --host-route destination=172.16.1.0/24,nexthop=1.1.1.20 and
        --host-route destination=172.17.7.0/24,nexthop=1.1.1.40
        """
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--host-route', 'destination=172.16.1.0/24,nexthop=1.1.1.20',
                '--host-route', 'destination=172.17.7.0/24,nexthop=1.1.1.40',
                netid, cidr]
        position_names = ['ip_version', 'host_routes', 'network_id',
                          'cidr']
        routes = [{'destination': '172.16.1.0/24', 'nexthop': '1.1.1.20'},
                  {'destination': '172.17.7.0/24', 'nexthop': '1.1.1.40'}]
        position_values = [4, routes, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_dns_nameservers(self):
        """Create subnet: --tenant-id tenantid <dns-nameservers> netid cidr.
        The <dns-nameservers> are
        --dns-nameserver 1.1.1.20 and --dns-nameserver 1.1.1.40
        """
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--dns-nameserver', '1.1.1.20',
                '--dns-nameserver', '1.1.1.40',
                netid, cidr]
        position_names = ['ip_version', 'dns_nameservers', 'network_id',
                          'cidr']
        nameservers = ['1.1.1.20', '1.1.1.40']
        position_values = [4, nameservers, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_with_disable_dhcp(self):
        """Create subnet: --tenant-id tenantid --disable-dhcp netid cidr."""
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--disable-dhcp',
                netid, cidr]
        position_names = ['ip_version', 'enable_dhcp', 'network_id',
                          'cidr']
        position_values = [4, False, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_merge_single_plurar(self):
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--allocation-pool', 'start=1.1.1.10,end=1.1.1.20',
                netid, cidr,
                '--allocation-pools', 'list=true', 'type=dict',
                'start=1.1.1.30,end=1.1.1.40']
        position_names = ['ip_version', 'allocation_pools', 'network_id',
                          'cidr']
        pools = [{'start': '1.1.1.10', 'end': '1.1.1.20'},
                 {'start': '1.1.1.30', 'end': '1.1.1.40'}]
        position_values = [4, pools, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_merge_plurar(self):
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                netid, cidr,
                '--allocation-pools', 'list=true', 'type=dict',
                'start=1.1.1.30,end=1.1.1.40']
        position_names = ['ip_version', 'allocation_pools', 'network_id',
                          'cidr']
        pools = [{'start': '1.1.1.30', 'end': '1.1.1.40'}]
        position_values = [4, pools, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_create_subnet_merge_single_single(self):
        resource = 'subnet'
        cmd = subnet.CreateSubnet(test_cli20.MyApp(sys.stdout), None)
        name = 'myname'
        myid = 'myid'
        netid = 'netid'
        cidr = 'prefixvalue'
        args = ['--tenant_id', 'tenantid',
                '--allocation-pool', 'start=1.1.1.10,end=1.1.1.20',
                netid, cidr,
                '--allocation-pool',
                'start=1.1.1.30,end=1.1.1.40']
        position_names = ['ip_version', 'allocation_pools', 'network_id',
                          'cidr']
        pools = [{'start': '1.1.1.10', 'end': '1.1.1.20'},
                 {'start': '1.1.1.30', 'end': '1.1.1.40'}]
        position_values = [4, pools, netid, cidr]
        self._test_create_resource(resource, cmd, name, myid, args,
                                   position_names, position_values,
                                   tenant_id='tenantid')

    def test_list_subnets_detail(self):
        """List subnets: -D."""
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, True)

    def test_list_subnets_tags(self):
        """List subnets: -- --tags a b."""
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, tags=['a', 'b'])

    def test_list_subnets_known_option_after_unknown(self):
        """List subnets: -- --tags a b --request-format xml."""
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, tags=['a', 'b'])

    def test_list_subnets_detail_tags(self):
        """List subnets: -D -- --tags a b."""
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, detail=True, tags=['a', 'b'])

    def test_list_subnets_fields(self):
        """List subnets: --fields a --fields b -- --fields c d."""
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd,
                                  fields_1=['a', 'b'], fields_2=['c', 'd'])

    def test_list_subnets_pagination(self):
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources_with_pagination(resources, cmd)

    def test_list_subnets_sort(self):
        """List subnets: --sort-key name --sort-key id --sort-key asc
        --sort-key desc
        """
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd,
                                  sort_key=["name", "id"],
                                  sort_dir=["asc", "desc"])

    def test_list_subnets_limit(self):
        """List subnets: -P."""
        resources = "subnets"
        cmd = subnet.ListSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, page_size=1000)

    def test_update_subnet(self):
        """Update subnet: myid --name myname --tags a b."""
        resource = 'subnet'
        cmd = subnet.UpdateSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'myname',
                                    '--tags', 'a', 'b'],
                                   {'name': 'myname', 'tags': ['a', 'b'], }
                                   )

    def test_update_subnet_known_option_before_id(self):
        """Update subnet: --request-format json myid --name myname."""
        # --request-format xml is known option
        resource = 'subnet'
        cmd = subnet.UpdateSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['--request-format', 'json',
                                    'myid', '--name', 'myname'],
                                   {'name': 'myname', }
                                   )

    def test_update_subnet_known_option_after_id(self):
        """Update subnet: myid --name myname --request-format json."""
        # --request-format xml is known option
        resource = 'subnet'
        cmd = subnet.UpdateSubnet(test_cli20.MyApp(sys.stdout), None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'myname',
                                    '--request-format', 'json'],
                                   {'name': 'myname', }
                                   )

    def test_show_subnet(self):
        """Show subnet: --fields id --fields name myid."""
        resource = 'subnet'
        cmd = subnet.ShowSubnet(test_cli20.MyApp(sys.stdout), None)
        args = ['--fields', 'id', '--fields', 'name', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id,
                                 args, ['id', 'name'])

    def test_delete_subnet(self):
        """Delete subnet: subnetid."""
        resource = 'subnet'
        cmd = subnet.DeleteSubnet(test_cli20.MyApp(sys.stdout), None)
        myid = 'myid'
        args = [myid]
        self._test_delete_resource(resource, cmd, myid, args)


class CLITestV20SubnetXML(CLITestV20SubnetJSON):
    format = 'xml'
