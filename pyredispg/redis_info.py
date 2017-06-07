import os
from collections import OrderedDict

import sys


class RedisInfo(object):
    def get_server_info(self):
        return OrderedDict([
            ('redis_version', '3.2.8'),
            ('redis_git_sha1', '00000000'),
            ('redis_git_dirty', 0),
            ('redis_build_id', 'b533f811ec736a0c'),
            ('redis_mode', 'standalone'),
            ('os', 'Darwin 16.6.0 x86_64'),
            ('arch_bits', 64),
            ('multiplexing_api', 'kqueue'),
            ('gcc_version', '4.2.1'),
            ('process_id', 97572),
            ('run_id', '3b0d94deafc30c3ecf2ba3b7fe00db216050d3a8'),
            ('tcp_port', 6379),
            ('uptime_in_seconds', 16463),
            ('uptime_in_days', 0),
            ('hz', 10),
            ('lru_clock', 3630551),
            ('executable', os.path.abspath(sys.argv[0])),
            ('config_file', '')
        ])

    def get_client_info(self):
        return OrderedDict([
            ('connected_clients', '1'),
            ('client_longest_output_list', '0'),
            ('client_biggest_input_buf', '0'),
            ('blocked_clients', '0')
        ])

    def get_memory_info(self):
        return OrderedDict([
            ('used_memory', '1011632'),
            ('used_memory_human', '987.92K'),
            ('used_memory_rss', '1003520'),
            ('used_memory_rss_human', '980.00K'),
            ('used_memory_peak', '1011712'),
            ('used_memory_peak_human', '988.00K'),
            ('total_system_memory', '17179869184'),
            ('total_system_memory_human', '16.00G'),
            ('used_memory_lua', '37888'),
            ('used_memory_lua_human', '37.00K'),
            ('maxmemory', '0'),
            ('maxmemory_human', '0B'),
            ('maxmemory_policy', 'noeviction'),
            ('mem_fragmentation_ratio', '0.99'),
            ('mem_allocator', 'libc')
        ])

    def get_persistence_info(self):
        return OrderedDict([
            ('loading', '0'),
            ('rdb_changes_since_last_save', '1'),
            ('rdb_bgsave_in_progress', '0'),
            ('rdb_last_save_time', '1496801818'),
            ('rdb_last_bgsave_status', 'ok'),
            ('rdb_last_bgsave_time_sec', '0'),
            ('rdb_current_bgsave_time_sec', '-1'),
            ('aof_enabled', '0'),
            ('aof_rewrite_in_progress', '0'),
            ('aof_rewrite_scheduled', '0'),
            ('aof_last_rewrite_time_sec', '-1'),
            ('aof_current_rewrite_time_sec', '-1'),
            ('aof_last_bgrewrite_status', 'ok'),
            ('aof_last_write_status', 'ok')
        ])

    def get_stats_info(self):
        return OrderedDict([
            ('total_connections_received', '3'),
            ('total_commands_processed', '20'),
            ('instantaneous_ops_per_sec', '0'),
            ('total_net_input_bytes', '514'),
            ('total_net_output_bytes', '18083046'),
            ('instantaneous_input_kbps', '0.01'),
            ('instantaneous_output_kbps', '0.02'),
            ('rejected_connections', '0'),
            ('sync_full', '0'),
            ('sync_partial_ok', '0'),
            ('sync_partial_err', '0'),
            ('expired_keys', '0'),
            ('evicted_keys', '0'),
            ('keyspace_hits', '3'),
            ('keyspace_misses', '0'),
            ('pubsub_channels', '0'),
            ('pubsub_patterns', '0'),
            ('latest_fork_usec', '1311'),
            ('migrate_cached_sockets', '0')
        ])

    def get_replication_info(self):
        return OrderedDict([
            ('role', 'master'),
            ('connected_slaves', '0'),
            ('master_repl_offset', '0'),
            ('repl_backlog_active', '0'),
            ('repl_backlog_size', '1048576'),
            ('repl_backlog_first_byte_offset', '0'),
            ('repl_backlog_histlen', '0')
        ])

    def get_cpu_info(self):
        return OrderedDict([
            ('used_cpu_sys', '6.55'),
            ('used_cpu_user', '3.14'),
            ('used_cpu_sys_children', '0.01'),
            ('used_cpu_user_children', '0.00')
        ])

    def get_cluster_info(self):
        return OrderedDict([
            ('cluster_enabled', 0)
        ])

    def get_keyspace_info(self):
        return OrderedDict([
            ('db0', 'keys = 15, expires = 0, avg_ttl = 0')
        ])

    def get_info(self):
        return OrderedDict([
            ('Server', self.get_server_info()),
            ('Client', self.get_client_info()),
            ('Memory', self.get_memory_info()),
            ('Persistence', self.get_persistence_info()),
            ('Stats', self.get_stats_info()),
            ('Replication', self.get_replication_info()),
            ('CPU', self.get_cpu_info()),
            ('Cluster', self.get_cluster_info()),
            ('Keyspace', self.get_keyspace_info())
        ])
