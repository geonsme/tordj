# tordj

a django style wrapper for tornado web framework. grpc service integrated(**Support python2 only**)

## Features

- Django style, which including but not limited to

    1. lazy settings mechanism
    2. Multiple applications support
    3. Middleware support
    4. Extensible sub command mechanism

- Session support

- Jinja2 template engine integrated

- (Asynchronous)[gRpc](https://github.com/grpc/grpc) service integrated

## Dependencies

- tornado

- jinja2(optional)

- redis(optional)

- grpcio(optional)

all the dependecies can be installed through `pip`

## Install

you can install this package using pip(depend on git cmd tool)

```shell
pip install git+https://github.com/wcsjtu/tordj.git
```

or download source code, then

```shell
cd .
python setup.py install
```

## Usage

TODO