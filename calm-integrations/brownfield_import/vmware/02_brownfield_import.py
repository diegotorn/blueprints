import os, sys, json, re, uuid, time
import logging, argparse
import requests
logging.basicConfig(
        filename='brownfield_import.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

linux_template_uuid = "50204284-5a62-9f9f-16c1-de61da074ee7"
windows_template_uuid = "5020b0fe-19fa-bbfe-0d94-844a9a4145d2"
headers = {'content-type': 'application/json', 'Accept': 'application/json'}

def help_parser():

    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to vCenter or ESXi')
    parser.add_argument('--pc',
                        required=True,
                        action='store',
                        help='vSphere service to connect to')
    parser.add_argument('--port',
                        type=int,
                        default=9440,
                        action='store',
                        help='Port to connect on')
    parser.add_argument('--user',
                        required=True,
                        action='store',
                        help='User name to use when connecting to pc')
    parser.add_argument('--password',
                        required=True,
                        action='store',
                        help='Password to use when connecting to pc')
    parser.add_argument('--project',
                        required=True,
                        action='store',
                        help='CALM project name')
    parser.add_argument('--account',
                        required=True,
                        action='store',
                        help='CALM VMware account name')
    parser.add_argument('--vm-info',
                        required=True,
                        action='store',
                        help='File path of esxi vm metadata csv')
    parser.add_argument('-n', '--parallel',
                        type=int,
                        default=5,
                        action='store',
                        help='Number of parallel executions')
    return parser


BP_SPEC = {
    "api_version": "3.0",
    "metadata": {
      "kind": "blueprint",
      "categories": {
          "TemplateType": "Vm"
      },
      "project_reference": {
        "kind": "project",
        "uuid": ""
      },
      "uuid": "67ff4eaf-f7e3-4563-b1da-f42de3113402"
    },
    "spec": {
      "resources": {
        "service_definition_list": [
          {
            "name": "Service1",
            "depends_on_list": [],
            "variable_list": [],
            "port_list": [],
            "action_list": [],
            "uuid": "37cc2dc9-da1b-1c2f-d3a7-20b7d5cf365f"
          }
        ],
        "credential_definition_list": [
        {
            "name": "TEST",
            "type": "PASSWORD",
            "username": "root",
            "secret": {
              "attrs": {
                "is_secret_modified": true
              },
              "value": "nutanix/4u"
            },
            "uuid": "2bb8197c-f11d-2026-ebaf-a7b3c5090d48"
          }
        ],
        "substrate_definition_list": [
          {
            "variable_list": [],
            "type": "VMWARE_VM",
            "os_type": "Linux",
            "action_list": [],
            "create_spec": {
              "type": "PROVISION_VMWARE_VM",
              "name": "vm1",
              "datastore": "",
              "host": "",
              "resources": {
                "guest_customization": {
                  "customization_type": "GUEST_OS_LINUX"
                },
                "account_uuid": "",
                "num_vcpus_per_socket": 0,
                "num_sockets": 0,
                "memory_size_mib": 0,
                "nic_list": []
              }
            },
            "name": "VMSubstrate",
            "readiness_probe": {
              "disable_readiness_probe": True
            },
            "editables": {
              "create_spec": {
                "resources": {
                  "nic_list": {},
                  "controller_list": {},
                  "template_nic_list": {},
                  "template_controller_list": {},
                  "template_disk_list": {}
                }
              }
            },
            "uuid": "61520e7a-67cc-e521-2853-fe249c92de18"
          }
        ],
        "client_attrs": {
        },
        "package_definition_list": [
          {
            "type": "DEB",
            "variable_list": [],
            "options": {
              "install_runbook": {
                "name": "92ca74bb_runbook",
                "variable_list": [],
                "main_task_local_reference": {
                  "kind": "app_task",
                  "uuid": "d43e8dc6-0fe3-18cf-426e-eab0f9ef8f3b"
                },
                "task_definition_list": [
                  {
                    "name": "fbaf0c95_dag",
                    "target_any_local_reference": {
                      "kind": "app_package",
                      "uuid": "139e0915-3bfd-f7dd-de96-68da22503290"
                    },
                    "variable_list": [],
                    "child_tasks_local_reference_list": [],
                    "type": "DAG",
                    "attrs": {
                      "edges": []
                    },
                    "uuid": "d43e8dc6-0fe3-18cf-426e-eab0f9ef8f3b"
                  }
                ],
                "uuid": "8299be1c-ff93-2246-cf7d-3a7a48c40927"
              },
              "uninstall_runbook": {
                "name": "104819f4_runbook",
                "variable_list": [],
                "main_task_local_reference": {
                  "kind": "app_task",
                  "uuid": "9b017f12-1253-cf9d-f889-894904bd9a7c"
                },
                "task_definition_list": [
                  {
                    "name": "04e26f0f_dag",
                    "target_any_local_reference": {
                      "kind": "app_package",
                      "uuid": "139e0915-3bfd-f7dd-de96-68da22503290"
                    },
                    "variable_list": [],
                    "child_tasks_local_reference_list": [
                      {
                        "kind": "app_task",
                        "uuid": "c1457c3e-83f0-561a-3454-b35d1e3f670e"
                      }
                    ],
                    "type": "DAG",
                    "attrs": {
                      "edges": []
                    },
                    "uuid": "9b017f12-1253-cf9d-f889-894904bd9a7c"
                  },
                  {
                    "name": "Task1",
                    "target_any_local_reference": {
                      "kind": "app_service",
                      "uuid": "37cc2dc9-da1b-1c2f-d3a7-20b7d5cf365f"
                    },
                    "variable_list": [],
                    "child_tasks_local_reference_list": [],
                    "type": "EXEC",
                    "attrs": {
                      "script_type": "static",
                      "script": "SPEC = {\n  \"spec\": {\n    \"args\": [],\n    \"default_target_reference\": None\n    }\n}\n\nheaders = {'content-type': 'application/json', 'Accept': 'application/json'}\n\ndef find_runbook(base_url, auth, runbook_name):\n    method = 'POST'\n    url = base_url + \"/runbooks/list\"\n    payload = {\"length\":20,\"offset\":0,\"filter\":\"name=={}\".format(runbook_name)}\n    runbook_uuid = None\n    resp = urlreq(\n        url,\n        verb=method,\n        params=json.dumps(payload),\n        headers=headers,\n        auth='BASIC',\n        user=auth[\"username\"],\n        passwd=auth[\"password\"],\n        verify=False\n    )\n    if resp.ok:\n        json_resp = json.loads(resp.content)\n        brownfield_instance_list = []\n        if json_resp['metadata']['total_matches'] > 0:\n            for runbook in json_resp[\"entities\"]:\n                if runbook[\"metadata\"][\"name\"] == runbook_name:\n                    runbook_uuid = runbook[\"metadata\"][\"uuid\"]\n        else:\n            print(\"Could not fetch runbook '{}'.\".format(runbook_name))\n            exit(1)\n        if runbook_uuid != None:\n            print(\"Runbook uuid for '{}' is '{}'.\".format(runbook_name, runbook_uuid))\n            return True, runbook_uuid\n        else:\n            print(\"Failed to fetch uuid for '{}'.\".format(runbook_name))\n            return False, runbook_uuid\n\n    else:\n        print(\"Request to fetch uuid '{}' failed.\".format(runbook_name))\n        print('Status code: {}'.format(resp.status_code))\n        print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))\n        exit(1)\n### --------------------------------------------------------------------------------- ###\n\ndef get_runbook(base_url, auth, runbook_uuid):\n    method = 'GET'\n    url = base_url + \"/runbooks/{}\".format(runbook_uuid)\n    runbook_get = None\n    resp = urlreq(\n        url,\n        verb=method,\n        headers=headers,\n        auth='BASIC',\n        user=auth[\"username\"],\n        passwd=auth[\"password\"],\n        verify=False\n    )\n    if resp.ok:\n        #print resp.content\n        runbook_get = json.loads(resp.content)\n        return runbook_get\n    else:\n        print(\"Failed to get runbook '{}'\".format(runbook_uuid))\n        print('Status code: {}'.format(resp.status_code))\n        print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))\n        exit(1)\n### --------------------------------------------------------------------------------- ###\n\ndef launch_runbook(base_url, auth, runbook_name, runbook_uuid, payload):\n    method = 'POST'\n    url = base_url + \"/runbooks/{}/run\".format(runbook_uuid)\n    payload = payload\n    resp = urlreq(\n        url,\n        verb=method,\n        params=json.dumps(payload),\n        headers=headers,\n        auth='BASIC',\n        user=auth[\"username\"],\n        passwd=auth[\"password\"],\n        verify=False\n    )\n    if resp.ok:\n        json_resp = json.loads(resp.content)\n        return json_resp\n    else:\n        print(\"Failed to launch_runbook '{}' uuid '{}'.\".format(runbook_name, runbook_uuid))\n        print('Status code: {}'.format(resp.status_code))\n        print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))\n        exit(1)\n### --------------------------------------------------------------------------------- ###\n\ndef check_runlog_status(base_url, auth, runlog_uuid):\n    method = 'GET'\n    url = base_url + \"/runbooks/runlogs/{}\".format(runlog_uuid)\n    resp = urlreq(\n        url,\n        verb=method,\n        headers=headers,\n        auth='BASIC',\n        user=auth[\"username\"],\n        passwd=auth[\"password\"],\n        verify=False\n    )\n    if resp.ok:\n        json_resp = json.loads(resp.content)\n        return json_resp\n    else:\n        print(\"Failed to get runlog '{}'.\".format(runlog_uuid))\n        print('Status code: {}'.format(resp.status_code))\n        print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))\n        exit(1)\n### --------------------------------------------------------------------------------- ###\n\npc_ip = \"10.44.19.140\"\npc_port = 9440\nbase_url = \"https://{}:{}/api/nutanix/v3\".format(pc_ip,str(pc_port))\nauth = { \"username\": \"admin\", \"password\": \"Nutanix.123\"}\nrunbook_name = \"EY-Day2Ops\"\nHOSTNAME = \"@@{calm_application_name}@@\"\nstatus, runbook_uuid = find_runbook(base_url, auth, runbook_name)\nif status == False:\n    print(\"Could not fetch uuid for '{}'.\".format(runbook_name))\n\nrunbook_get = get_runbook(base_url, auth, runbook_uuid)\n\n# -*- Building runbook spec.\nSPEC[\"spec\"][\"args\"] = runbook_get[\"spec\"][\"resources\"][\"runbook\"][\"variable_list\"]\nSPEC[\"spec\"][\"default_target_reference\"] = runbook_get[\"spec\"][\"resources\"][\"default_target_reference\"]\n\nSPEC[\"spec\"][\"args\"][0][\"value\"] = HOSTNAME\n\nprint(json.dumps(SPEC))\n\nlaunch_runlog = launch_runbook(base_url, auth, runbook_name, runbook_uuid, SPEC)\nrunlog_uuid = launch_runlog[\"status\"][\"runlog_uuid\"]\n\nstatus = False\nwhile(status == False):\n    runlog_output = check_runlog_status(base_url, auth, runlog_uuid)\n    if runlog_output[\"status\"][\"state\"] == 'SUCCESS':\n        status = True\n        print(\"Runbook '{}' runlog uuid '{}' is '{}'.\".format(runbook_name, runlog_uuid, runlog_output[\"status\"][\"state\"]))\n    elif runlog_output[\"status\"][\"state\"] == 'FAILURE':\n        status = True\n        print(\"Runbook '{}' runlog uuid '{}' has 'FAILED'.\".format(runbook_name, runlog_uuid))\n    else:\n        print(\"Runbook '{}' runlog uuid '{}' is in '{}' state.\".format(runbook_name, runlog_uuid, runlog_output[\"status\"][\"state\"]))\n    sleep(5)\n"
                    },
                    "uuid": "c1457c3e-83f0-561a-3454-b35d1e3f670e"
                  }
                ],
                "uuid": "c152b6d7-1577-3311-e366-4f18ddf2bc18"
              }
            },
            "service_local_reference_list": [
              {
                "kind": "app_service",
                "uuid": "37cc2dc9-da1b-1c2f-d3a7-20b7d5cf365f"
              }
            ],
            "name": "Package1",
            "uuid": "139e0915-3bfd-f7dd-de96-68da22503290"
          }
        ],
        "app_profile_list": [
          {
            "name": "VMware",
            "action_list": [],
            "variable_list": [],
            "deployment_create_list": [
              {
                "variable_list": [],
                "action_list": [],
                "min_replicas": "1",
                "name": "a7aadef7_deployment",
                "brownfield_instance_list": [
                  {
                    "instance_id": "",
                    "instance_name": "",
                    "address": [
                    ],
                    "platform_data": {}
                  }
                ],
                "max_replicas": "1",
                "substrate_local_reference": {
                  "kind": "app_substrate",
                  "uuid": "61520e7a-67cc-e521-2853-fe249c92de18"
                },
                "type": "BROWNFIELD",
                "package_local_reference_list": [
                  {
                    "kind": "app_package",
                    "uuid": "139e0915-3bfd-f7dd-de96-68da22503290"
                  }
                ],
                "uuid": "48a70045-d71a-4486-0d03-e15a871372b5"
              }
            ],
            "uuid": "bc40ba37-6e84-49af-1ad3-280a5c3c1af4"
          }
        ],
        "type": "BROWNFIELD"
      },
      "name": ""
    }
}

def create_open_file(file_name, file_operation):
    if not os.path.exists(file_name) and file_operation == "r":
        with open(file_name, 'w'): pass
    try:
        file = open(file_name, file_operation)
    except:
        logging.error("Failed to open file '{}' with operation '{}'.".format(file_name, file_operation))
        sys.exit(1)
    return file

### --------------------------------------------------------------------------------- ###
def get_vm_spec(vm_meta_info):
    vm_meta = vm_meta_info.split(',')
    address = [vm_meta[2]]
    vm_spec = {
        "instance_name": vm_meta[0],
        "instance_id": vm_meta[1],
        "address": address,
        "num_sockets": vm_meta[3],
        "num_vcpus_per_socket": vm_meta[4],
        "memory_size_mib": vm_meta[5],
        "guestFamily": vm_meta[6],
        "host_uuid": vm_meta[7],
        "datastore_location": vm_meta[8],
        "power_state": vm_meta[9]
    }
    return vm_spec

### --------------------------------------------------------------------------------- ###
def get_project_uuid(base_url, auth, project_name):
    method = 'POST'
    url = base_url + "/projects/list"
    resp = None
    payload = {
        "length":100,
        "offset":0,
        "filter":"name=={0}".format(project_name)
    }
    try:
        resp = requests.request(
            method,
            url,
            data=json.dumps(payload),
            headers=headers,
            auth=(auth["username"], auth["password"]),
            verify=False
        )
    except requests.exceptions.ConnectionError as e:
        logging.error("Failed to connect to PC: {}".format(e))
        sys.exit(1)
    finally:
        if resp.ok:
            json_resp = resp.json()
            if json_resp['metadata']['total_matches'] > 0:
                project = json_resp['entities'][0]
                project_uuid = project["metadata"]["uuid"]
                return project_uuid
            else:
                logging.error("Could not find project '{}'.".format(project_name))
                sys.exit(1)
        else:
            logging.error("Request failed")
            logging.error("Headers: {}".format(headers))
            logging.error('Status code: {}'.format(resp.status_code))
            logging.error('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            sys.exit(1)

### --------------------------------------------------------------------------------- ###
def get_vmware_account_uuid(base_url, auth, account_name):
    method = 'POST'
    url = base_url + "/accounts/list"
    payload = {
        "length":100,
        "offset":0,
        "filter":"name=={0};type==vmware".format(account_name)
    }
    try:
        resp = requests.request(
            method,
            url,
            data=json.dumps(payload),
            headers=headers,
            auth=(auth["username"], auth["password"]),
            verify=False
        )
    except requests.exceptions.ConnectionError as e:
        logging.error("Failed to connect to PC: {}".format(e))
        sys.exit(1)
    finally:
        if resp.ok:
            json_resp = resp.json()
            if json_resp['metadata']['total_matches'] > 0:
                account = json_resp['entities'][0]
                return account["metadata"]["uuid"]
            else:
                logging.error("Could not find account '{}'".format(account_name))
                sys.exit(1)
        else:
            logging.error("Request failed")
            logging.error("Headers: {}".format(headers))
            logging.error('Status code: {}'.format(resp.status_code))
            logging.error('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            sys.exit(1)

### --------------------------------------------------------------------------------- ###
def get_vmware_account_info(base_url, auth, account_uuid):
    method = 'GET'
    url = base_url + "/accounts/{}".format(account_uuid)
    try:
        resp = requests.request(
            method,
            url,
            headers=headers,
            auth=(auth["username"], auth["password"]),
            verify=False
        )
    except requests.exceptions.ConnectionError as e:
        logging.error("Failed to connect to PC: {}".format(e))
        sys.exit(1)
    finally:
        if resp.ok:
            json_resp = resp.json()
            if json_resp['status']['resources']["state"] != "VERIFIED":
                return False, "", ""
            else:
                return True, json_resp['status']['resources']["data"]["server"], json_resp['status']['resources']["data"]["datacenter"]
        else:
            logging.error("Request failed")
            logging.error("Headers: {}".format(headers))
            logging.error('Status code: {}'.format(resp.status_code))
            logging.error('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
            sys.exit(1)

### --------------------------------------------------------------------------------- ###
def get_single_vm_app_status(base_url, auth, application_uuid):
    method = 'GET'
    url = base_url + "/apps/{}".format(application_uuid)
    status = ""
    while True:
        try:
            resp = requests.request(
                method,
                url,
                headers=headers,
                auth=(auth["username"], auth["password"]),
                verify=False
            )
        except requests.exceptions.ConnectionError as e:
            logging.error("Failed to connect to PC: {}".format(e))
            return ""
        finally:
            if resp.ok:
                json_resp = resp.json()
                status = json_resp["status"]["state"]
                return status
            else:
                logging.error("Request failed")
                logging.error("Headers: {}".format(headers))
                logging.error('Status code: {}'.format(resp.status_code))
                logging.error('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
                return ""


def esxi_brownfield_import(spec, vm_spec, project_uuid, account_uuid):
    application_uuid = ""

    ### --------------------------------------------------------------------------------- ###
    def change_uuids(bp, context):
        if isinstance(bp, dict):
            for key, val in bp.items():
                if key == 'uuid':
                    old_uuid = val
                    if old_uuid in context:
                        bp[key] = context[old_uuid]
                    else:
                        new_uuid = str(uuid.uuid4())
                        context[old_uuid] = new_uuid
                        bp[key] = new_uuid
                else:
                    change_uuids(val, context)
        elif isinstance(bp, list):
            for item in bp:
                if isinstance(item, str):
                    try:
                        uuid.UUID(hex=str(item), version=4)
                    except Exception:
                        change_uuids(item, context)
                        continue
                    old_uuid = item
                    if old_uuid in context:
                        new_uuid = context[old_uuid]
                        bp[bp.index(item)] = new_uuid
                    else:
                        new_uuid = str(uuid.uuid4())
                        context[old_uuid] = new_uuid
                        bp[bp.index(item)] = new_uuid
                else:
                    change_uuids(item, context)
        return bp

    ### --------------------------------------------------------------------------------- ###
    def create_single_vm_bp(base_url, auth, payload):
        method = 'POST'
        url = base_url + "/blueprints"
        try:
            resp = requests.request(
                method,
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(auth["username"], auth["password"]),
                verify=False
            )
        except requests.exceptions.ConnectionError as e:
            logging.error("Failed to connect to PC: {}".format(e))
            return False, ""
        finally:
            if resp.ok:
                json_resp = resp.json()
                if json_resp["status"]["state"] != "ACTIVE":
                    logging.error("Blueprint state is not Active. It is : {}".format(json_resp["status"]["state"]))
                    return False, json_resp
                return True, json_resp
            else:
                logging.error("Request failed")
                logging.error("Headers: {}".format(headers))
                logging.error('Status code: {}'.format(resp.status_code))
                logging.error('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
                return False, ""

    ### --------------------------------------------------------------------------------- ###
    def launch_single_vm_bp(base_url, auth, blueprint_uuid, payload):
        method = 'POST'
        url = base_url + "/blueprints/{}/launch".format(blueprint_uuid)
        launch_request_uuid = ""
        try:
            resp = requests.request(
                method,
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(auth["username"], auth["password"]),
                verify=False
            )
        except requests.exceptions.ConnectionError as e:
            logging.error("ERROR: Failed to connect to PC: {}".format(e))
            return False, launch_request_uuid
        finally:
            if resp.ok:
                json_resp = resp.json()
                launch_request_uuid = json_resp["status"]["request_id"]
                return True, launch_request_uuid
            else:
                logging.error("Request failed")
                logging.error("Headers: {}".format(headers))
                logging.error('Status code: {}'.format(resp.status_code))
                logging.error('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
                return False, launch_request_uuid

    ### --------------------------------------------------------------------------------- ###
    def get_single_vm_app_uuid(base_url, auth, launch_request_uuid):
        method = 'GET'
        url = base_url + "/blueprints/{}/pending_launches/{}".format(blueprint_uuid,launch_request_uuid)
        application_uuid = ""
        while True:
            try:
                resp = requests.request(
                    method,
                    url,
                    headers=headers,
                    auth=(auth["username"], auth["password"]),
                    verify=False
                )
            except requests.exceptions.ConnectionError as e:
                logging.error("ERROR: Failed to connect to PC: {}".format(e))
                return False, application_uuid
            finally:
                if resp.ok:
                    json_resp = resp.json()
                    if json_resp["status"]["state"] == "failure":
                        return False, application_uuid
                    if json_resp["status"]["state"] == "success":
                        application_uuid = json_resp["status"]["application_uuid"]
                        return True, application_uuid
                else:
                    logging.error("Request failed")
                    logging.error("Headers: {}".format(headers))
                    logging.error('Status code: {}'.format(resp.status_code))
                    logging.error('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
                    return False, application_uuid

    ### --------------------------------------------------------------------------------- ###

    ### Update uuids, project ref, account ref, bp name, vm-info etc.
    updated_spec = change_uuids(spec, {})
    if vm_spec["guestFamily"] == "Linux":
        template_uuid = linux_template_uuid
    else:
        template_uuid = windows_template_uuid
    updated_spec["metadata"]["project_reference"]["uuid"] = project_uuid

    substrate = updated_spec["spec"]["resources"]["substrate_definition_list"][0]
    substrate["create_spec"]["name"] = vm_spec["instance_name"]
    substrate["create_spec"]["host"] = vm_spec["host_uuid"]
    substrate["create_spec"]["template"] = template_uuid
    substrate["create_spec"]["datastore"] = vm_spec["datastore_location"]
    substrate["create_spec"]["resources"]["account_uuid"] = account_uuid
    substrate["create_spec"]["resources"]["num_vcpus_per_socket"] = vm_spec["num_vcpus_per_socket"]
    substrate["create_spec"]["resources"]["num_sockets"] = vm_spec["num_sockets"]
    substrate["create_spec"]["resources"]["memory_size_mib"] = vm_spec["memory_size_mib"]
    substrate["create_spec"]["resources"]["power_state"] = vm_spec["power_state"]

    brownfield_instance = updated_spec["spec"]["resources"]["app_profile_list"][0]["deployment_create_list"][0]["brownfield_instance_list"][0]
    brownfield_instance["instance_name"] = vm_spec["instance_name"]
    brownfield_instance["instance_id"] = vm_spec["instance_id"]
    brownfield_instance["address"] = vm_spec["address"]
    brownfield_instance["power_state"] = vm_spec["power_state"]
    brownfield_instance["platform_data"] = {}

    updated_spec["spec"]["resources"]["substrate_definition_list"][0] = substrate
    updated_spec["spec"]["resources"]["app_profile_list"][0]["deployment_create_list"][0]["brownfield_instance_list"][0] = brownfield_instance
    updated_spec["spec"]["name"] = vm_spec["instance_name"].replace(" ", "_")

    ### Create a single vm bp
    create_status, resp = create_single_vm_bp(base_url, auth, updated_spec)
    if create_status != True:
        return False, resp

    ### Update single vm bp spec to launch
    del resp["status"]
    blueprint_uuid = resp["metadata"]["uuid"]

    app_uuid = resp["spec"]["resources"]["app_profile_list"][0]["uuid"]
    resp["spec"]["application_name"] =  resp["spec"]["name"]
    resp["spec"]["app_profile_reference"] = {
        "kind": "app_profile",
        "uuid": app_uuid
    }

    del resp["spec"]["name"]

    ### Launch a single vm bp
    launch_request_status, launch_request_uuid = launch_single_vm_bp(base_url, auth, blueprint_uuid, resp)
    if launch_request_status != True:
        return False, launch_request_uuid
    app_uuid_status, application_uuid = get_single_vm_app_uuid(base_url, auth, launch_request_uuid)
    if app_uuid_status != True:
        return False, application_uuid
    return True, application_uuid

if __name__ == "__main__":
    parser = help_parser().parse_args()
    pc_ip = parser.pc
    pc_port = parser.port
    base_url = "https://{}:{}/api/nutanix/v3".format(pc_ip,str(pc_port))
    auth = { "username": parser.user, "password": parser.password}
    project_name = parser.project
    account_name = parser.account
    file_path = parser.vm_info
    parallel_process = parser.parallel

    vm_input_list = []

    vm_input_content = create_open_file(file_path, "r")
    vm_input_list = vm_input_content.read().splitlines()[1:]

    vm_input_success_content = create_open_file("brownfield_import_success.csv", "r")
    vm_input_success_list = vm_input_success_content.read().splitlines()
    vm_input_success_content.close()

    vm_input_failed_content = create_open_file("brownfield_import_failed.csv", "r")
    vm_input_failed_list = vm_input_failed_content.read().splitlines()
    vm_input_failed_content.close()

    vm_output_success_content = create_open_file("brownfield_import_success.csv", "a+")
    vm_output_failed_content = create_open_file("brownfield_import_failed.csv", "a+")

    project_uuid = get_project_uuid(base_url, auth, project_name)
    account_uuid = get_vmware_account_uuid(base_url, auth, account_name)

    if project_uuid == "" or account_uuid == "":
        logging.error("Failed to get project or account details.")
        sys.exit(1)

    status, vcenter_ip, datacenter = get_vmware_account_info(base_url, auth, account_uuid)
    if status != True:
        logging.error("Failed to get VCenter details.")
        sys.exit(1)

    logging.info("Brownfield import process started.")
    logging.info("VCenter IP: '{}'.".format(vcenter_ip))
    logging.info("Datacenter: '{}'.".format(datacenter))

    total_matches = len(vm_input_list)
    count = 0

    while (count < total_matches):
        apps_ids = {}
        first_item = count
        last_item = first_item + parallel_process
        if total_matches < last_item:
            last_item = total_matches
        number_of_executions = last_item-first_item
        success_fail_apps = 0
        count += number_of_executions
        for vm_meta_info in vm_input_list[first_item:last_item]:
            vm_spec = get_vm_spec(vm_meta_info)
            if vm_meta_info in vm_input_success_list:
                logging.info("Application '{}' already imported.".format(vm_spec["instance_name"]))
                continue
            logging.info("Importing VM: '{}' ({})".format(vm_spec["instance_name"], vm_spec["address"][0]))
            launch_status, application_uuid = esxi_brownfield_import(BP_SPEC, vm_spec, project_uuid, account_uuid)
            if launch_status != True:
                logging.error("Import failed: {}.".format(vm_spec["instance_name"]))
                if vm_meta_info not in vm_input_failed_list:
                    vm_output_failed_content.write("{}\n".format(vm_meta_info))
                continue
            apps_ids[application_uuid] = { "name" : vm_spec["instance_name"], "state" : "provisioning", "ip" : vm_spec["address"][0], "csv": vm_meta_info}
        if len(apps_ids) < number_of_executions:
            number_of_executions = len(apps_ids)
        while True:
            for apps_id in apps_ids.keys():
                if apps_ids[apps_id]["state"] == 'provisioning':
                    status = get_single_vm_app_status(base_url, auth, apps_id)
                    logging.info("Checking application '{}' ({}) status.".format(apps_ids[apps_id]["name"], apps_ids[apps_id]["ip"]))
                    if status == 'running':
                        apps_ids[apps_id]["state"] = 'success'
                        logging.info("Application '{}' ({}) import successful.".format(apps_ids[apps_id]["name"], apps_ids[apps_id]["ip"]))
                        vm_output_success_content.write("{}\n".format(apps_ids[apps_id]["csv"]))
                        success_fail_apps += 1
                    elif status == "failed":
                        apps_ids[apps_id]["state"] = 'failed'
                        logging.error("Application '{}' ({}) import failed.".format(apps_ids[apps_id]["name"], apps_ids[apps_id]["ip"]))
                        if apps_ids[apps_id]["csv"] not in vm_input_failed_list:
                            vm_output_failed_content.write("{}\n".format(apps_ids[apps_id]["csv"]))
                        success_fail_apps += 1
                    elif status == "error":
                        apps_ids[apps_id]["state"] = 'error'
                        logging.error("Application '{}' ({}) import failed.".format(apps_ids[apps_id]["name"], apps_ids[apps_id]["ip"]))
                        if apps_ids[apps_id]["csv"] not in vm_input_failed_list:
                            vm_output_failed_content.write("{}\n".format(apps_ids[apps_id]["csv"]))
                        success_fail_apps += 1
            if success_fail_apps == number_of_executions:
                logging.info("Completed ({}/{}) applications.".format(count, total_matches))
                break
            time.sleep(10)
    logging.info("Completed brownfield import.")