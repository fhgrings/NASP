import os
import json

class NssmfCoreService():
    """Nssmf Core Class"""
    def alloc_nssi(self, request):
        """"Alloc NSSI Core"""
        try:
            NSSAI = request.json['S-NSSAI']
            commands = [
                "DIR='../helm_charts/core/free5gc'",
                f"cp -r $DIR {NSSAI['sd']}-core",
                f'grep -rl "sst: 1" {NSSAI["sd"]}-core | xargs sed -i "s/sst: 1/sst: {NSSAI["sst"]}/g"',
                f'grep -rl "sd: 112233" {NSSAI["sd"]}-core | xargs sed -i "s/sd: 112233/sd: {NSSAI["sd"]}/g"',
                f"helm install {NSSAI['sd']}-core {NSSAI['sd']}-core -n free5gc"
                ]
            out = os.popen(";".join(commands))
            # print(";".join(commands))
            return "OK"
        except Exception:
            return "Bad Request", 400

    def get_all_nssi(self, request):
        """Get All NSSI CORE"""
        try:
            # deployed_list = os.popen("sudo helm list --filter 'core' -A").read()
            output = os.popen("helm list -A").read()
            print(output.split("\n")[1:])
            deployed_list = output.split("\n")[1:]
            return [obj.split("\t")[0] for obj in deployed_list]
        except Exception:
            return "Bad Request", 400

    def get_all_nsst(self, request):
        """Get All NSSTs Core"""
        try:
            data = open("../data/db/nsst_core.json", encoding="utf-8")
            return json.load(data)
        except Exception:
            return "Bad Request", 400
    
    def add_nsst(self, request):
        """Get All NSSTs Core"""
        try:
            data = open("../data/db/nsst_core.json", encoding="utf-8")
            nsst_list = json.load(data)
            data.close()
            nsst_list.append({
                "domain": "Core",
                "name": "Full Core",
                "description": "Complete 5G core environment",
                "id": "1",
                "status": "Ready",
                "is_shared": False,
                "path": "../helm_charts/core/free5gc"
            })
            f = open("../data/db/nsst_core.json", "w", encoding="utf-8")
            print(type(nsst_list[0]))
            f.write(json.dumps(nsst_list))
            f.close()
            return json.load(data)
        except Exception as exception:
            return f"Bad Request - {exception}", 400

        