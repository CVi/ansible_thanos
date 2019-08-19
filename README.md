Thanos
======

Deploy [Thanos](https://thanos.io/) Prometheus extension using ansible.

Requirements
------------

This role does not deploy Prometheus. Installing prometheus must be installed
by another role.

This role should work on every linux system with an amd64 or arm64 CPU and
systemd. If tar and bzip2 are not available in the package manager under
those names, this role will fail.

For testing purposes all systemd-invocations are skipped if systemd is not
the init daemon on, the system is not systemd, but it will still create the
systemd service unit. If you want to use this role on an operatingsystem 
without systemd be aware of this limitation.

Role Variables
--------------

### Generic variables ###

| Name                 | Default Value  | Description                         |
| -------------------- | -------------- | ----------------------------------- |
| thanos_version       | 0.6.0          | Version of thanos to install        |
| thanos_user          | prometheus     | User thanos is run as, defaults to prometheus to play well as sidecar |
| thanos_group         | prometheus     | Group thanos is run as, defaults to prometheus to play well as sidecar |
| thanos_bucket_config | (empty string) | The contents of the objstore config-file as a string |



### Thanos services ###
| Name                 | Default Value | Description                          |
| -------------------- | ------------- | ------------------------------------ |
| thanos_sidecar       | no            | Install sidecar service on this host |
| thanos_query         | no            | Install query service on this host   |
| thanos_store         | no            | Install store service on this host   |
| thanos_compactor     | no            | Install compactor service on this host |
| thanos_remove_unused | yes           | Uninstall and/or remove all serivices that are not set to be installed on this host.|

### Paths ###
| Name           | Default Value | Description                                |
| --------------------- | ------------- | ----------------------------------- |
| thanos_root_dir       | /opt/thanos   | Thanos installation root path       |
| thanos_config_dir     | /etc/thanos   | Thanos config path                  |
| thanos_tsdb_dir       | /var/lib/prometheus | Prometheus tsdb path          |
| thanos_data_dir       | /var/lib/thanos   | Thanos (temp-)data directory    |
| thanos_sidecar_pid_path | /var/run/thanos-sidecar.pid | PID file for sidecar demon |
| thanos_query_pid_path | /var/run/thanos-query.pid | PID file for query demon |
| thanos_store_pid_path | /var/run/thanos-store.pid | PID file for store demon |
| thanos_compactor_pid_path | /var/run/thanos-compactor.pid | PID file for compactor demon |
| thanos_dist_dir       | {{ thanos_root_dir }}/dist | Dist directory for Thanos |
| thanos_bin_dir        | {{ thanos_root_dir }}/current | Current release directory for Thanos (linked from dist) |


### Network Addresses ###
| Name           | Default Value | Description                                |
| -------------- | ------------- | ------------------------------------------ |
| thanos_sidecar_web_listen_port | 19191 | Prometheus-compatible listen port for sidecar service |
| thanos_sidecar_web_listen_address | 0.0.0.0:{{ thanos_sidecar_web_listen_port }} | Bind address for sidecar service |
| thanos_query_web_listen_port | 19192 | Prometheus-compatible listen port for query service |
| thanos_query_web_listen_address | 0.0.0.0:{{ thanos_query_web_listen_port }} | Bind address for query service |
| thanos_store_web_listen_port | 19193 | Prometheus-compatible listen port for store service |
| thanos_store_web_listen_address | 0.0.0.0:{{ thanos_store_web_listen_port }} |  Bind address for query service |
| thanos_compactor_web_listen_port | 19194 | Prometheus-compatible listen port for compactor service |
| thanos_compactor_web_listen_address | 0.0.0.0:{{ thanos_compactor_web_listen_port }} | Bind address for compactor service |
| thanos_sidecar_grpc_listen_port | 19181 | GRPC port for sidecar service |
| thanos_sidecar_grpc_listen_address | 0.0.0.0:{{ thanos_sidecar_grpc_listen_port }} | Bind address for GRPC on sidecar service |
| thanos_query_grpc_listen_port | 19182 | GRPC port for query service |
| thanos_query_grpc_listen_address | 0.0.0.0:{{ thanos_query_grpc_listen_port }} | Bind address for GRPC on query service |
| thanos_store_grpc_listen_port | 19183 | GRPC port for store service |
| thanos_store_grpc_listen_address | 0.0.0.0:{{ thanos_store_grpc_listen_port }}" | Bind address for GRPC on store service |

### Service parameters ###
| Name                       | Default Value          | Description           |
| -------------------------- | ---------------------- | --------------------- |
| thanos_web_prometheus_url  | http://localhost:9090/ | Address of local Prometheus (for sidecar) |
| thanos_query_stores        | (empty string)         | List of store flags to pass to querier |
| thanos_query_replica_label | replica                | Label that  distinguish replica set in HA configurations, for deduplication. |


### Service cli flags ###
| Name                   | Default Value | Description                        |
| ---------------------- | ------------- | ---------------------------------- |
| thanos_sidecar_flags   | -             | Command line flags passed to sidecar demon | 
| thanos_query_flags     | -             | Command line flags passed to query demon |
| thanos_store_flags     | -             | Command line flags passed to store demon |
| thanos_compactor_flags | -             | Command line flags passed to compactor demon |

### Internal variables ###
| Name                | Default Value | Description                           |
| ------------------- | ------------- | ------------------------------------- |
| thanos_platform     | -             | Platform section of thanos package name |
| thanos_release_name | -             | Name of thanos package                |
| thanos_download_fn  | -             | Filename of thanos package            |
| thanos_download_url | -             | url for release package               |


Example Playbooks
-----------------

The following playbook will install a sidecar service alongside any prometheus service.
Since it does not have any thanos_bucket_config, it will not enable long-term storage.

    - hosts: prometheus-servers
      roles:
        - role: cvi.thanos
          become: yes
          # Vars
          thanos_sidecar: yes

The following playbook will install a thanos query service and query from the sidecars
deployed above.

    - hosts: thanos-query
      roles:
        - role: cvi.thanos
          become: yes
          # Vars
          thanos_query: yes
          thanos_query_stores: >-
             {% for host in groups['prometheus-servers'] | sort %}
             --store {{ host }}:{{ hostvars[host]['thanos_sidecar_grpc_listen_port'] | default(19181) }}
             {% endfor %}


License
-------

MIT
