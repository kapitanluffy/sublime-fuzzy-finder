import subprocess
from .Terminal import FastFuzzyFinder


def run_command(command: str, directory: str, output, input):
    try:
        cmd = "rg --column --no-heading --smart-case %s ./" % command
        FastFuzzyFinder.process = subprocess.Popen(
            cmd,
            shell=True,
            text=True,
            cwd=directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            encoding='utf-8',
            bufsize=1,
            universal_newlines=True
        )

        while True:
            for line in FastFuzzyFinder.process.stdout:  # type: ignore
                output.put([line, 'ok'])

            return_code = FastFuzzyFinder.process.poll()

            if return_code is not None:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
