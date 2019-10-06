import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_thanos_executable(host):
    f = host.file('/opt/thanos/current/thanos')

    assert f.exists


def test_thanos_bucket_config(host):
    f = host.file('/etc/thanos/bucket_config.yaml')

    assert f.exists


def test_sidecar(host):
    f = host.file('/etc/systemd/system/thanos-sidecar.service')

    assert f.exists


def test_query(host):
    f = host.file('/etc/systemd/system/thanos-query.service')

    assert f.exists


def test_store(host):
    f = host.file('/etc/systemd/system/thanos-store.service')

    assert f.exists


def test_compactor(host):
    f = host.file('/etc/systemd/system/thanos-compactor.service')

    assert f.exists
