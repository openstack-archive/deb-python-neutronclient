# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Nicira Inc.
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

import logging

from neutronclient.neutron import v2_0 as neutronV20
from neutronclient.openstack.common.gettextutils import _


class ListQoSQueue(neutronV20.ListCommand):
    """List queues that belong to a given tenant."""

    resource = 'qos_queue'
    log = logging.getLogger(__name__ + '.ListQoSQueue')
    list_columns = ['id', 'name', 'min', 'max',
                    'qos_marking', 'dscp', 'default']


class ShowQoSQueue(neutronV20.ShowCommand):
    """Show information of a given queue."""

    resource = 'qos_queue'
    log = logging.getLogger(__name__ + '.ShowQoSQueue')
    allow_names = True


class CreateQoSQueue(neutronV20.CreateCommand):
    """Create a queue."""

    resource = 'qos_queue'
    log = logging.getLogger(__name__ + '.CreateQoSQueue')

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name', metavar='NAME',
            help=_('Name of queue'))
        parser.add_argument(
            '--min',
            help=_('min-rate')),
        parser.add_argument(
            '--max',
            help=_('max-rate')),
        parser.add_argument(
            '--qos-marking',
            help=_('QOS marking untrusted/trusted')),
        parser.add_argument(
            '--default',
            default=False,
            help=_('If true all ports created with be the size of this queue'
                   ' if queue is not specified')),
        parser.add_argument(
            '--dscp',
            help=_('Differentiated Services Code Point')),

    def args2body(self, parsed_args):
        params = {'name': parsed_args.name,
                  'default': parsed_args.default}
        if parsed_args.min:
            params['min'] = parsed_args.min
        if parsed_args.max:
            params['max'] = parsed_args.max
        if parsed_args.qos_marking:
            params['qos_marking'] = parsed_args.qos_marking
        if parsed_args.dscp:
            params['dscp'] = parsed_args.dscp
        if parsed_args.tenant_id:
            params['tenant_id'] = parsed_args.tenant_id
        return {'qos_queue': params}


class DeleteQoSQueue(neutronV20.DeleteCommand):
    """Delete a given queue."""

    log = logging.getLogger(__name__ + '.DeleteQoSQueue')
    resource = 'qos_queue'
    allow_names = True
