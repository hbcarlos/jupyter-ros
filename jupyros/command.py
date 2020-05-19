import subprocess
from threading import Thread

class Command(Thread):
    
    def __init__(self, cmd, output):
        Thread.__init__(self)
        self.cmd = cmd
        self.proc = None
        self.output = output
        
        print(self.cmd)
        
    def run(self):
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, shell=True)
        self.output.value = "Inicialized"
        
        self.proc.wait()
        self.output.value = "Finished"
    
    def play(self):
        print("play")
        if self.proc != None and self.proc.poll() == None :
            print("entra")
            self.proc.stdin.write(b' \n')
            self.proc.stdin.flush()
            self.output.value = "Running"
        
    def pause(self):
        if self.proc != None and self.proc.poll() == None :
            self.proc.stdin.write(b' \n')
            self.proc.stdin.flush()
            self.output.value = "Paused"
    
    def step(self):
        if self.proc != None and self.proc.poll() == None :
            self.proc.stdin.write(b's\n')
            self.proc.stdin.flush()
            self.output.value = "Next"
        
    def stop(self):
        if self.proc != None and self.proc.poll() == None :
            self.proc.terminate()
            self.output.value = "Finished"