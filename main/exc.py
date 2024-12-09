import time
import subprocess
import json

def execute_main():
    subprocess.run(["python", "main.py"])

def main():
    while True:
        execute_main()
        time.sleep(5)  # Wait for 5 minutes (300 seconds)

if __name__ == "__main__":
    main()
