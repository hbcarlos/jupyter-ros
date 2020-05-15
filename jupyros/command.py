import time
import subprocess
from threading import Thread
from multiprocessing import Pipe

class Command(Thread):
    
    def __init__(self, cmd, output):
        Thread.__init__(self)
        self.cmd = cmd
        self.proc = None
        self.output = output
        
        self.parentPipe, self.childPipe = Pipe(False)
        
    def run(self):
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=self.childPipe, stderr=subprocess.STDOUT)
        
        cont = 0
        while self.parentPipe.poll(100) == None :
            cont += 1
            self.output.value = "Running: {}".format(cont)
            time.sleep(0.1)
        
        self.output.value = self.parentPipe.recv()
    
    def play(self):
        if self.proc != None and self.proc.poll() == None :
            print("resume")
            self.proc.stdin.write(b' \n')
            print("running")
        
        else :
            print("finished")
            print("reset")
            self.proc = None
        
    def pause(self):
        if self.proc != None and self.proc.poll() == None :
            print("pause")
            self.proc.stdin.write(b' \n')
            print("running")
        
        else :
            print("finished")
            print("reset")
            self.proc = None
    
    def step(self):
        if self.proc != None and self.proc.poll() == None :
            print("next")
            self.proc.stdin.write(b's\n')
            print("running")
            
        else :
            print("finished")
            print("reset")
            self.proc = None
        
    def stop(self):
        if self.proc != None and self.proc.poll() == None :
            print("Terminating")
            self.proc.terminate()
            print("Terminated")
        
        else :
            print("finished")
            print("reset")
            self.proc = None