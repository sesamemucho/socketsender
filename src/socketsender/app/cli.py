import argparse
import importlib.util
import sys
from pathlib import Path

from socketsender import sender


class SOCSCli:
    def __init__(self, args):
        self.args = args
        parser = argparse.ArgumentParser(description="Send IP packets.")
        parser.add_argument(
            "-m",
            "--module",
            action="store",
            help="Specifies a module.class to use with a 'source' parameter",
        )
        parser.add_argument(
            "config",
            type=argparse.FileType("r"),
            help="YAML config file for SOCSender.",
        )
        self.cli_args = parser.parse_args(args[1:])

    def run(self):
        if self.cli_args.module:
            path = Path(self.cli_args.module)
            if not path.exists():
                print(f'Can\'t find module file "{path}"', file=sys.stderr)
                sys.exit(3)

            module_name = path.stem
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Optional; only necessary if you want to be able to import the module
            # by name later.
            sys.modules[module_name] = module

        sender.SOCSender().run(self.cli_args.config)


def run():
    SOCSCli(sys.argv).run()
