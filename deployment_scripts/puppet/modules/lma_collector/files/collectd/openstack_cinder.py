#!/usr/bin/python
# Copyright 2015 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Collectd plugin for getting statistics from Cinder
import collectd

import collectd_openstack as openstack

PLUGIN_NAME = 'cinder'
INTERVAL = openstack.INTERVAL


class CinderStatsPlugin(openstack.CollectdPlugin):
    """ Class to report the statistics on Cinder objects.

        number of volumes broken down by state
        total size of volumes usable and in error state
    """

    def __init__(self, *args, **kwargs):
        super(CinderStatsPlugin, self).__init__(*args, **kwargs)
        self.plugin = PLUGIN_NAME
        self.interval = INTERVAL

    def itermetrics(self):

        volumes_details = self.get_objects_details('cinder', 'volumes')

        def groupby(d):
            return d.get('status', 'unknown').lower()

        def count_size_bytes(d):
            return d.get('size', 0) * 10 ** 9

        status = self.count_objects_group_by(volumes_details,
                                             group_by_func=groupby)
        for s, nb in status.iteritems():
            yield {
                'plugin_instance': 'volumes',
                'type_instance': s,
                'values': nb
            }

        sizes = self.count_objects_group_by(volumes_details,
                                            group_by_func=groupby,
                                            count_func=count_size_bytes)
        for n, size in sizes.iteritems():
            yield {
                'plugin_instance': 'volumes_size',
                'type_instance': n,
                'values': size
            }

        snaps_details = self.get_objects_details('cinder', 'snapshots')
        status_snaps = self.count_objects_group_by(snaps_details,
                                                   group_by_func=groupby)
        for s, nb in status_snaps.iteritems():
            yield {
                'plugin_instance': 'snapshots',
                'type_instance': s,
                'values': nb
            }

        sizes = self.count_objects_group_by(snaps_details,
                                            group_by_func=groupby,
                                            count_func=count_size_bytes)
        for n, size in sizes.iteritems():
            yield {
                'plugin_instance': 'snapshots_size',
                'type_instance': n,
                'values': size
            }


plugin = CinderStatsPlugin(collectd, PLUGIN_NAME)


def config_callback(conf):
    plugin.config_callback(conf)


def notification_callback(notification):
    plugin.notification_callback(notification)


def read_callback():
    plugin.conditional_read_callback()

collectd.register_config(config_callback)
collectd.register_notification(notification_callback)
collectd.register_read(read_callback, INTERVAL)
