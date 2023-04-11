from pyhelm.chartbuilder import ChartBuilder

chart = ChartBuilder({"name": "nginx-ingress", "source": {"type": "directory", "location": "./helm_charts/free5gc"}})