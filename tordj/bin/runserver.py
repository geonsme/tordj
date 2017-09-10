# -*- coding:utf-8 -*-


from .base import Command

class RunServer(Command):

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
        group = parser.add_argument_group('Runserver Options')
        group.add_argument("interface", 
            help="listen interface, format is ip:port. default is 0.0.0.0:8000",
            type=self.validate_ip,  default="0.0.0.0:8000")
        group.add_argument("--autoreload", type=bool, default=False,
            help="auto reload service when code changed. default is `False`")

    def run(self, *args, **kwargs):

        from tordj.http import App
        ip, port = kwargs.get("interface", ("0.0.0.0", 8000))
        self.logger.info( "Tornado Application starts on port: %s" % port)
        application = App()
        application.listen(port, ip)
        application.start()