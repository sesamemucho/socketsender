import argparse
import sys

from socketsender import sender


class SOCSCli:
    def __init__(self, args):
        self.args = args
        parser = argparse.ArgumentParser(description="Send IP packets.")
        parser.add_argument(
            "config",
            type=argparse.FileType("r"),
            help="YAML config file for SOCSender.",
        )
        self.cli_args = parser.parse_args(args[1:])

    def run(self):
        sender.SOCSender().run(self.cli_args.config)


def run():
    SOCSCli(sys.argv).run()
