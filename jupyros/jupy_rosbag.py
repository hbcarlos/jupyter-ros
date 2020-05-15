import rosbag

import subprocess
from command import Command
from datetime import datetime
import ipywidgets as widgets
from IPython.display import HTML


class RosBag():

    def __init__(self, file):
        self.bag = rosbag.Bag(file, mode='r', allow_unindexed=True)
        self.types, self.topics = self.bag.get_type_and_topic_info()
        self.messages = self.bag.read_messages()

        self.cmd = None
        self.proc = None
        self.output = None
    
    def _repr_mimebundle_(self, include=None, exclude=None):
        path = self.bag.filename
        version = float(self.bag.version) / 100
        start = datetime.utcfromtimestamp( self.bag.get_start_time() )
        end = datetime.utcfromtimestamp( self.bag.get_end_time() )
        duration = end - start
        size = str(round(self.bag.size / 1048576.0, 2)) + " MB"
        messages = self.bag.get_message_count()
        compression = self.bag.compression
        
        types = "<table>"
        for k,v in self.types.items():
            types += "<tr><td>{}</td><td>{}</td></tr>".format(k, v)
        types += "</table>"

        topics = "<table><tr><th>Topic</th><th>Message type</th><th>Message count</th><th>Connections</th><th>Frequency</th></tr>"
        for k,v in self.topics.items():
            topics += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(k, v[0], v[1], v[2], v[3])
        topics += "</table>"

        return {
            "text/html":
                "<div>Path: {}</div>\
                <div>Version: {}</div>\
                <div>Duration: {}</div>\
                <div>Start: {}</div>\
                <div>End: {}</div>\
                <div>Size: {}</div>\
                <div>Messages: {}</div>\
                <div>Compresion: {}</div>\
                <div>Types: {}</div>\
                <div>Topics: {}</div>"
                .format(path, version, duration, start, end, size, messages, compression,types, topics),

            "text/plain": "somthing"
        }

    def show_types(self):
        txt = "<h5>Types:</h5>\n<table>"

        for k,v in self.types.items():
            txt += "\n\t<tr><td>{}</td><td>{}</td></tr>".format(k, v)
        
        txt += "\n</table>"
        
        return HTML(data=txt)

    def show_topics(self):
        txt = "<h5>Topics:</h5>\n<table>"
        txt += "\n\t<tr><th>Topic</th><th>Message type</th><th>Message count</th><th>Connections</th><th>Frequency</th></tr>"

        for k,v in self.topics.items():
            txt += "\n\t<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(k, v[0], v[1], v[2], v[3])
        
        txt += "\n</table>"
        
        return HTML(data=txt)
    
    def playUI(self):
        btn_play = widgets.Button(description="Play", icon='play')
        btn_pause = widgets.Button(description="Pause", icon='pause', disabled=True)
        btn_step = widgets.Button(description="Step", icon='step-forward')
        btn_stop = widgets.Button(description="Stop", icon='stop', disabled=True)  
        
        #btn_play.disabled = True
        #btn_pause.disabled = False
        #btn_step.disabled = True
        #btn_stop.disabled = True
        
        command = ['rosbag', 'play', '--pause', 'bags/pallet.bag']
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE) #, stdout=self.childPipe, stderr=subprocess.STDOUT)
            
        def btn_play_on_click(arg):
            print("play")
            btn_play.disabled = True
            btn_pause.disabled = False
            btn_step.disabled = True
            btn_stop.disabled = False
            
            #self.cmd.play()
            if self.proc != None and self.proc.poll() == None :
                print("resume")
                self.proc.stdin.write(b' \n')
                print("running")

            else :
                print("finished")
                print("reset")
                self.proc = None
        
        def btn_pause_on_click(arg):
            print("pause")
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = False
            
            #self.cmd.pause()
            if self.proc != None and self.proc.poll() == None :
                print("pause")
                self.proc.stdin.write(b' \n')
                print("running")

            else :
                print("finished")
                print("reset")
                self.proc = None
        
        def btn_step_on_click(arg):
            print("step")
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = False
            
            #self.cmd.step()
            if self.proc != None and self.proc.poll() == None :
                print("next")
                self.proc.stdin.write(b's\n')
                print("running")

            else :
                print("finished")
                print("reset")
                self.proc = None
        
        def btn_stop_on_click(arg):
            print("stop")
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = True
            
            #self.cmd.stop()
            if self.proc != None and self.proc.poll() == None :
                print("Terminating")
                self.proc.terminate()
                print("Terminated")

            print("reset")
            self.proc = None

        btn_play.on_click(btn_play_on_click)
        btn_pause.on_click(btn_pause_on_click)
        btn_step.on_click(btn_step_on_click)
        btn_stop.on_click(btn_stop_on_click)
        
        btns = widgets.HBox([btn_play, btn_pause, btn_step, btn_stop])
        self.output = widgets.widgets.Textarea()
        return widgets.VBox([btns, self.output])
    
    def ui(self):
        btn_play = widgets.Button(description="Play", icon='play')
        btn_pause = widgets.Button(description="Pause", icon='pause', disabled=True)
        btn_step = widgets.Button(description="Step", icon='step-forward')
        btn_stop = widgets.Button(description="Stop", icon='stop', disabled=True)  
        
        #btn_play.disabled = True
        #btn_pause.disabled = False
        #btn_step.disabled = True
        #btn_stop.disabled = True
            
        def btn_play_on_click(arg):
            print("play")
            btn_play.disabled = True
            btn_pause.disabled = False
            btn_step.disabled = True
            btn_stop.disabled = False
            
            self.cmd.play()
        
        def btn_pause_on_click(arg):
            print("pause")
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = False
            
            self.cmd.pause()
        
        def btn_step_on_click(arg):
            print("step")
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = False
            
            self.cmd.step()
        
        def btn_stop_on_click(arg):
            print("stop")
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = True
            
            self.cmd.stop()

        btn_play.on_click(btn_play_on_click)
        btn_pause.on_click(btn_pause_on_click)
        btn_step.on_click(btn_step_on_click)
        btn_stop.on_click(btn_stop_on_click)
        
        btns = widgets.HBox([btn_play, btn_pause, btn_step, btn_stop])
        self.output = widgets.widgets.Textarea()
        return widgets.VBox([btns, self.output])
        
    def play(self):
        command = ['rosbag', 'play', '--pause', 'bags/pallet.bag']
        self.cmd = Command(command, self.output)
        self.cmd.start()
        self.cmd.join()