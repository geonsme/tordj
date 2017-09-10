# -*- coding:utf-8 -*-


from .base import Command

class RunGrpc(Command):

    Description = "run tornado server with options"

    def validate_ip(self, val):
        import socket
        try:
            ip, port = val.split(":")
            socket.inet_aton(ip)
            return ip, int(port)
        except Exception:
            raise self.UsageError("%s is invalid" % val)

    def add_arguments(self, parser):
        group = parser.add_argument_group('RunGrpcserver Options')
        group.add_argument("-i", dest="interface",
            help="listen interface, default is [::]",
            type=str,  default="[::]")
        group.add_argument("-p", dest="port",
            help="listen port, default is 50051",
            type=int,  default=50051)
        group.add_argument("--workers", 
            help="count of workers process, default is 10",
            type=int,  default=10)

    def run(self, *args, **kwargs):

        from tordj.grpcio.server import run_grpc
        from tordj.loader import ApplicationLoader
        ApplicationLoader().load()
        run_grpc(**kwargs)
