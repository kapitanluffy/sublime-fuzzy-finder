import subprocess
import select
import sys
import threading
from typing import Generator, Literal
from .Terminal import Terminal

# read_fd, write_fd = os.pipe()
# python -c "print('hello!');x=input('Enter something: ');print(x)"
# python -c "print('hello!');x=input('Enter something: ');print('foo');print(x);"

STYLE = """
html {{
    border-left-style:solid;
    border-left-color:#111111;
    border-left-width:0.1px;
}}
"""

HTML = "<body><style>%s</style>{body}</body>" % STYLE


def output_sheet():
    print("output sheet thread!")
    while True:
        if Terminal.process.stdout is None:
            print("bb")
            continue

        line = Terminal.process.stdout.readline()

        if not line:
            print("no output lines")
            break

        if Terminal.sheet is None:
            print("sheet is gone")
            break

        # if output != "" and isinstance(output, int) is False:
        #     # output = output.replace(" ", sublime.html.entities.html5.get('nbsp'))
        #     # line = "<div style=\"margin-bottom:1rem;\">%s</div>" % sublime.html.escape(output)
        #     line = "<div style=\"margin-bottom:1rem;\">%s</div>" % output
        # elif output != "" and isinstance(output, int):
        #     line = "<div style=\"margin-bottom:1rem;\">Return Code: %s</div>" % output
        # else:
        #     line = "<div style=\"margin-bottom:1rem;\">&nbsp;</div>"

        print("> ", line)
        Terminal.thread_output.put([line, 'ok'])
        # content = HTML.format(body=' '.join(Terminal.output))
        # Terminal.sheet.set_contents(content)
    print("output sheet done!")


def append_sheet_content(output: str):
    line = "<div style=\"margin-bottom:1rem;\">%s</div>" % output
    Terminal.output.append(line)
    content = HTML.format(body=' '.join(Terminal.output))
    Terminal.sheet.set_contents(content)


def run_command(command: str, directory: str, output, input):
    try:
        # cmd = ["d:\\~\\bin\\ripgrep\\rg.exe", "--smart-case", "--column", "--no-heading", command]
        # cmd = "d:\\~\\bin\\ripgrep\\rg.exe plugin"
        # print("cwd", "cd \"%s\" && d:/~/bin/fzf.exe" % directory)

        cmd = "rg --column --no-heading --smart-case -e \"%s\" ./" % command
        Terminal.process = subprocess.Popen(
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
            for line in Terminal.process.stdout:  # type: ignore
                output.put([line, 'ok'])

            return_code = Terminal.process.poll()

            if return_code is not None:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
