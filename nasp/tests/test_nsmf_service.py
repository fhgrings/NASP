import pytest
import subprocess
from unittest.mock import patch, mock_open, MagicMock
from src.services.helm_deployments import NsmfService

@pytest.fixture
def service():
    return NsmfService()

@patch("builtins.open", new_callable=mock_open, read_data="[]")
@patch("json.dump")
def test_add_to_db(mock_json_dump, mock_open_file, service):
    data =     {
        "name": "Test",
        "description": {
            "N3GPP Support": False,
            "Slice Attributes": {
                "Accuracy": 1e-07,
                "DN": 1,
                "MMTel": True,
                "Maximum number of PDU sessions": 1000,
                "Maximum number of UEs": 100000,
                "N3GPP Support": True,
                "SSC": 1,
                "SSQ": {
                    "Guaranteed Flow Bit Rate - Downlink": 100000,
                    "Guaranteed Flow Bit Rate - Uplink": 100000,
                    "Max Flow Bit Rate - Downlink": 100000,
                    "Max Flow Bit Rate - Uplink": 100000,
                    "Maximum Data Burts Volume": 0.001,
                    "Maximum Packet Loss Rate": 100000,
                    "Packet Delay Budget": 0.00012,
                    "Packet Error Rate": 1e-07,
                    "Priority Level": 1
                },
                "Shared": False,
                "Supported Data Network": "internet",
                "Supported device velocity": 10,
                "Synchronicity": "Between BS and UE",
                "UE density": 10000,
                "availability": 1,
                "exposed": True,
                "shared": True
            },
            "resource_description": {
                "core": {
                    "nfs": [
                        {
                            "config": {
                                "plmnSupportList": [
                                    {
                                        "plmnId": {
                                            "mcc": 208,
                                            "mnc": 93
                                        },
                                        "snssaiList": [
                                            {
                                                "sd": 4227,
                                                "sst": 1
                                            },
                                            {
                                                "sd": 112233,
                                                "sst": 1
                                            }
                                        ]
                                    }
                                ],
                                "supportDnnList": [
                                    "internet"
                                ]
                            },
                            "name": "amf",
                            "node": [
                                "new_york"
                            ]
                        },
                        {
                            "name": "nrf"
                        },
                        {
                            "name": "ausf"
                        },
                        {
                            "name": "nssf"
                        },
                        {
                            "name": "pcf"
                        },
                        {
                            "name": "udm"
                        },
                        {
                            "name": "udr"
                        },
                        {
                            "name": "smf"
                        },
                        {
                            "name": "upf"
                        }
                    ]
                },
                "ran": {
                    "nfs": [
                        {
                            "config": {
                                "amfConfigs": [
                                    {
                                        "address": "127.0.0.1",
                                        "port": 38412
                                    }
                                ],
                                "gtpIp": "127.0.0.1",
                                "idLength": 32,
                                "ignoreStreamIds": True,
                                "linkIp": "127.0.0.1",
                                "mcc": "208",
                                "mnc": "93",
                                "nci": "0x000000010",
                                "ngapIp": "127.0.0.1",
                                "slices": [
                                    {
                                        "sd": 66051,
                                        "sst": 1
                                    }
                                ],
                                "tac": 1
                            },
                            "name": "ueransim",
                            "node": [],
                            "replicas": 2,
                            "type": "gnb"
                        }
                    ]
                },
                "tn": {
                    "routes": [
                        {
                            "name": "backhaul"
                        }
                    ]
                }
            },
            "resources": "custom",
            "type": "custom"
        },
        "S_NSSAI": "1274447"
    },
    service.add_to_db(data, "nsi")
    mock_open_file.assert_called_with("../data/db/nsi.json",'w', encoding="utf-8")
    mock_json_dump.assert_called()

@patch("requests.post")
def test_post_data_success(mock_post, service):
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status = MagicMock()
    service.post_data({"key": "value"}, "https://google.com")
    mock_post.assert_called_once_with("https://google.com", json={"key": "value"})

@patch("subprocess.check_output")
def test_create_ns_success(mock_subprocess, service):
    mock_subprocess.return_value = b"Namespace created"
    result = service.create_ns("test-ns")
    assert result == "Namespace created"
    mock_subprocess.assert_called_once_with("kubectl create ns test-ns", shell=True, stderr=subprocess.STDOUT)

@patch("time.sleep")
@patch("subprocess.check_output")
def test_delete_ns_success(mock_subprocess, _, service):
    with patch("builtins.open", mock_open(read_data='[{"S_NSSAI": "test-nssai"}]')):
        service.delete_ns()
        mock_subprocess.assert_called_once_with(
            'nohup kubectl delete ns ns-test-nssai > /dev/null 2>&1 &',
            shell=True,
            stderr=subprocess.STDOUT,
        )

@patch("builtins.open", new_callable=mock_open, read_data="[]")
@patch("json.load", side_effect=[[], []])
@patch("json.dump")
def test_add_nsi(mock_json_dump, mock_json_load, mock_open_file, service):
    nsi = {"name": "test-nsi"}
    service.add_nsi(nsi)
    mock_open_file.assert_called_with("../data/db/nsi.json", "w", encoding="utf-8")
    # mock_json_dump.assert_called_once()

@patch("requests.post")
@patch("time.sleep")
def test_deploy_onos_intents(mock_sleep, mock_post, service):
    mock_post.return_value.status_code = 201
    intents = [
        [("device1", "1"), ("device2", "2")],
        [("device3", "3"), ("device4", "4")],
    ]
    service.deploy_onos_intents(intents)
    assert mock_post.call_count == len(intents)

@patch("subprocess.check_output")
@patch("os.makedirs")
def test_create_helm_tmp(mock_makedirs, mock_subprocess, service):
    mock_subprocess.return_value = b"Copied successfully"
    result = service.create_helm_tmp("../path/to/helm")
    assert result == "Copied successfully"
    mock_subprocess.assert_called_once_with(
        "cp -r ../path/to/helm /tmp/helm-nasp-temp/",
        shell=True,
        stderr=subprocess.STDOUT,
    )

@patch("builtins.open", new_callable=mock_open, read_data='[{"id": "test_id"}]')
@patch("json.load")
def test_get_nst(mock_json_load, mock_open_file, service):
    mock_json_load.return_value = [{"id": "test_id", "name": "test"}]
    result = service.get_nst("test_id")
    assert result == {"id": "test_id", "name": "test"}

@patch("builtins.open", new_callable=mock_open, read_data="[]")
def test_get_all_nst(mock_open_file, service):
    result = service.get_all_nst(None)
    assert result == []
    mock_open_file.assert_called_once_with("../data/db/nst.json", "r", encoding="utf-8")
