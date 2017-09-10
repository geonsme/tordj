# -*- coding: utf-8 -*-
import time

from tordj.conf import settings
from tordj.utils.module_loading import import_module, import_string

SERVICES = []

def load_services():
    services = settings.GRPC_SERVICES.keys()
    for service in services:
        import_module(service)
        


def run_grpc(**config):
    from concurrent import futures
    import grpc
    load_services()
    if not config:
        config = settings.GRPC_SERVER_CONFIG
    service_count = len(SERVICES)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=config["workers"]))
    module_list = []
    for register_func, cls_module in SERVICES:
        service_cls = import_string(cls_module)
        register_func(service_cls(), server)
        module_list.append(cls_module)
    server.add_insecure_port("%(interface)s:%(port)s" % config)
    server.start()
    print """start grpc server on %(interface)s:%(port)s with %(workers)s workers\nit contains services below:\n""" % config
    print ("    %s\n"*service_count) % tuple(module_list)
    try:
        while True:
            time.sleep(-1)
    except KeyboardInterrupt:
        server.stop(0)


