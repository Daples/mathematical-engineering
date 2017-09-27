import subprocess
import platform
import os


class HandlerFiles:

    cross = "├"
    pipe = "│"
    line = "─"
    h_cross = "└"

    def __init__(self, name):
        self.system = platform.system()
        self.name = name
        if self.system == "Linux" or self.system == "Darwin":
            process = subprocess.Popen('tree -hDua / > ' + name, stdout=subprocess.PIPE, shell=True)
            process.communicate()[0].strip()

        self.file = open(name)
        self.list = []


    def read_file(self):
        i = 0
        dir = "/"
        for line in self.file:
            if i == 0:
                continue
