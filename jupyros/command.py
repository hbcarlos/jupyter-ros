import time
import subprocess
from threading import Thread

class Command(Thread):
    
    def __init__(self, cmd, output):
        Thread.__init__(self)
        self.cmd = cmd
        self.proc = None
        self.output = output
        
    def run(self):
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, shell=True)
        self.output.value = "Inicialized"
        
        self.proc.wait()
        self.output.value = "Finished"
    
    def play(self):
        if self.proc != None and self.proc.poll() == None :
            self.proc.stdin.write(b' \n')
            self.output.value = "Running"
        
    def pause(self):
        if self.proc != None and self.proc.poll() == None :
            self.proc.stdin.write(b' \n')
            self.output.value = "Paused"
    
    def step(self):
        if self.proc != None and self.proc.poll() == None :
            self.proc.stdin.write(b's\n')
            self.output.value = "Next"
        
    def stop(self):
        if self.proc != None and self.proc.poll() == None :
            self.proc.terminate()
            self.output.value = "Finished"