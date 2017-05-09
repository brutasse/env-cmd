import os
import sys


def split_lines(f):
    return [
        l.strip().split('=', 1) for l in f.readlines()
        if not l.startswith('#') and l.strip()
    ]


def read_environ(config_name, default_config_path, default_environ=None):
    if default_environ is None:
        default_environ = {}

    def func():
        config_path = os.getenv(config_name, default_config_path)

        environ = {}
        environ.update(default_environ)
        with open(config_path) as f:
            environ.update({k: v.strip("\"' ") for k, v in split_lines(f)})

        extra_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        path = os.getenv('PATH', '')
        path_items = list(filter(None, [extra_path] + path.split(':')))
        normalized_path = []
        for item in path_items:
            if item not in normalized_path:
                normalized_path.append(item)
        environ['PATH'] = ":".join(normalized_path)
        return environ
    return func


def main(read_environ):
    def func():
        if len(sys.argv) == 1 or sys.argv[1].startswith('-'):
            _, name = sys.argv[0].rsplit(os.sep, 1)
            raise SystemExit("Usage: {} <subcommand> [OPTIONS]".format(name))

        os.execvpe(sys.argv[1], sys.argv[1:], read_environ())
    return func
