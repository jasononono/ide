import subprocess
import sys
from importlib import util

fileName = "requirement.txt"

def dependency_check():
    try:
        with open(fileName, 'r') as f:
            dependencies = f.read().split('\n')

        print("----- running dependency check...")
        for i in dependencies:
            if util.find_spec(i) is None:
                print(f"----- package '{i}' not found. Installing...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", i])
        print("----- dependency check completed.")

    except FileNotFoundError:
        print(f"----- '{fileName}' not found. Skipping dependency check...")