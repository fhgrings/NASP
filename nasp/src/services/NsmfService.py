import os
import logging
import time
import json
import requests

class NsmfService():
    """Nsmf Service Class"""
    def allocNsi(self, request):
        try:
            logging.info("Selected NSI Template: %s", request.json['NsiTemplateId'])

            logging.info("Choosen S-NSSAI - SST:1 SD:123")
            logging.info("Selecting NSSI Core...")
            response = requests.get("http://127.0.0.1:5000/nsstCore", timeout=100)
            logging.info("NSST Core Selected - ID %s - Description: %s", response.json()[0]['id'], {response.json()[0]['description']})

            logging.info("Selecting NSSI RAN...")
            response = requests.get("http://127.0.0.1:5000/nsstRAN", timeout=100)
            logging.info("NSST RAN Selected - ID %s - Description: %s", response.json()[0]['id'], {response.json()[0]['description']})
            logging.info("Deploying NSI SST1SD123")

            url = "http://localhost:5000//allocNssiCore"
            payload = json.dumps({
                "S-NSSAI": {
                    "sst": "1",
                    "sd": "123"
                },
                "interfaces": [
                    {"name": "amf", "port": "38804", "protool": "SCTP"}
                ]
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.request("PUT", url, headers=headers, data=payload, timeout=100)
            
            time.sleep(3)
            url = "http://localhost:5000//allocNssiRAN"
            payload = json.dumps({
                "S-NSSAI": {
                    "sst": "1",
                    "sd": "24401"
                },
                "interfaces": [
                    {"name": "amf", "port": "38804", "protool": "SCTP"}
                ]
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.request("PUT", url, headers=headers, data=payload, timeout=100)

            return ""
        except Exception as exception:
            return f"Bad Request - {exception}", 400

    def getAllNsi(self, request):
        try:
            # deployed_list = os.popen("sudo helm list --filter 'core' -A").read()
            output = os.popen("helm list -A").read()
            print(output.split("\n")[1:])
            deployed_list = output.split("\n")[1:]
            return [obj.split("\t")[0] for obj in deployed_list]
        except Exception as exception:
            return f"Bad Request {exception}", 400

    def get_all_nst(self, request):
        """Get All NSTs"""
        try:
            data = open("../data/db/nst.json", "r", encoding="utf-8")
            nst_list = json.load(data)["nst_list"]
            return nst_list

        except Exception as exception:
            return f"Bad Request - {exception}", 400
