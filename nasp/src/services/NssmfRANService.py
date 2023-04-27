import os
import logging
import json

class NssmfRANService():
    """Nssmf Ran Class"""
    def alloc_nssi(self, request):
        """"Alloc NSSI RAN"""
        try:
            NSSAI = request.json['NSSAI']
            print(NSSAI)

            out = os.popen("pwd").read()
            print(out)
            commands = [
                "DIR='../helm_charts/ran/rantester'",
                f"cp -r $DIR {NSSAI['sd']}-ran",
                f'grep -rl "sst: 1" {NSSAI["sd"]}-ran | xargs sed -i "s/sst: 1/sst: {NSSAI["sst"]}/g"',
                f'grep -rl "sd: 112233" {NSSAI["sd"]}-ran | xargs sed -i "s/sd: 112233/sd: {NSSAI["sd"]}/g"',
                f"helm install {NSSAI['sd']}-ran {NSSAI['sd']}-ran -n free5gc"
                ]
            out = os.popen(";".join(commands))
            # print(";".join(commands))
            return ""
        except Exception as exception:
            logging.error(exception)
            return f"Bad Request - {exception}", 400

    def get_all_nssi(self, request):
        """Get All NSSI"""
        try:
            # deployed_list = os.popen("sudo helm list --filter 'core' -A").read()
            output = os.popen("helm list -A").read()
            print(output.split("\n")[1:])
            deployed_list = output.split("\n")[1:]
            return [obj.split("\t")[0] for obj in deployed_list]
        except Exception as exception:
            return f"Bad Request {exception}", 400
    
    def get_all_nsst(self, request):
        """Get All NSST"""
        try:
            data = open("../data/db/nsst_ran.json", encoding="utf-8")
            return json.load(data)
        except Exception as exception:
            return f"Bad Request {exception}", 400

    def add_nsst(self, request):
        """Get All NSSTs Core"""
        try:
            data = open("../data/db/nsst_ran.json", encoding="utf-8")
            nsst_list = json.load(data)
            data.close()
            nsst_list.append({
                "domain": "RAN",
                "name": "Ran Tester",
                "description": "Virtual RAN Tester",
                "id": "1",
                "status": "Ready",
                "is_shared": False,
                "path": "../helm_charts/ran/rantester'"
            })
            f = open("../data/db/nsst_ran.json", "w", encoding="utf-8")
            print(type(nsst_list[0]))
            f.write(json.dumps(nsst_list))
            f.close()
            return json.load(data)
        except Exception as exception:
            return f"Bad Request - {exception}", 400
