import time
import subprocess
from threading import Thread
#from multiprocessing import Process, Pipe

class Command(Thread):
    
    def __init__(self, cmd):
        Thread.__init__(self)
        self.cmd = cmd
        self.proc = None
        
    def run(self):
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(self.proc.stdout.read())
    
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
            
        print("reset")
        self.proc = None
    

command = ['rosbag', 'play', 'bags/pallet.bag']
th = Command(command)
th.start()

time.sleep(3)
th.pause()

time.sleep(3)
th.step()

time.sleep(3)
th.step()

time.sleep(3)
th.play()
    
#th.join()