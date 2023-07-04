import os
import logging
import json

class NssmfRANService():
    """Nssmf Ran Class"""
    def alloc_nssi(self, request):
        """"Alloc NSSI RAN"""
        try:
            NSSAI = request.json['S-NSSAI']
            name = request.json['name']
            path = ""
            data = open("../data/db/nsst_ran.json", encoding="utf-8")
            for i in json.load(data):
                if i.get("name") == name:
                    path = i.get("path")
            name = f"{NSSAI['sd']}-{name.lower()}"
            print(NSSAI)
            out = os.popen("pwd").read()
            print(out)
            print(f'Testing - {name}')
            commands = [
                f"DIR='{path}'",
                f"cp -r $DIR {name}",
                f'grep -rl "sst: 1" {name} | xargs sed -i "s/sst: 1/sst: {NSSAI["sst"]}/g"',
                f'grep -rl "sd: 112233" {name} | xargs sed -i "s/sd: 112233/sd: {NSSAI["sd"]}/g"',
                f"helm install {name} {name} -n 1274401-demo"
                ]
            out = os.popen(";".join(commands))
            # print(";".join(commands))
            return "OK"
        except Exception as exception:
            logging.error(str(exception))
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
            try:
                return json.load(data)
            except Exception as exception:
                print(str(exception))
                return []
        except Exception as exception:
            return f"Bad Request {exception}", 400

    def add_nsst(self, request):
        """Get All NSSTs Core"""
        print(request)
        try:
            data = open("../data/db/nsst_ran.json", encoding="utf-8")
            try:
                nsst_list = json.load(data)
            except Exception as exception:
                print(str(exception))
                nsst_list = []
                
            nsst_list.append({
                "domain": request.json.get("domain"),
                "name": request.json.get("name"),
                "description": request.json.get("description"),
                "id": "1",
                "status": "Ready",
                "is_shared": True,
                "path": "../helm_charts/core/free5gc"
            })
            f = open("../data/db/nsst_ran.json", "w", encoding="utf-8")
            print(type(nsst_list[0]))
            f.write(json.dumps(nsst_list))
            f.close()
            return data
        except Exception as exception:
            return f"Bad Request - {exception}", 400
