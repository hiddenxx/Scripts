import argparse
import subprocess

parser = argparse.ArgumentParser(description="Changing MAC Address of the system.")
parser.add_argument("-n", help=("Name of the interface"), dest="input", type=str, required=True)
args = parser.parse_args()

subprocess.call(["sudo", "ifconfig", args, "down"])
subprocess.call(["sudo", "ifconfig", args, "hw", "ether", "00:11:22:33:44:55"])
subprocess.call(["sudo", "ifconfig", args, "up"])
