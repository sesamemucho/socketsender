import argparse
import sys

from udpsender import sender


class UDPSCli:
    def __init__(self, args):
        self.args = args
        parser = argparse.ArgumentParser(description="Send UDP packets.")
        parser.add_argument(
            "config",
            type=argparse.FileType("r"),
            help="YAML config file for UDPSender.",
        )
        self.cli_args = parser.parse_args(args[1:])

    def run(self):
        sender.UDPSender().run(self.cli_args.config)


def run():
    UDPSCli(sys.argv).run()
