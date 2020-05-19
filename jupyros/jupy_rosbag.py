import rosbag
from datetime import datetime

import ipywidgets as widgets
import ipyvuetify as vue
from IPython.display import HTML

from .command import Command

class RosBag():

    def __init__(self, file):
        self.bag = rosbag.Bag(file, mode='r', allow_unindexed=True)
        self.types, self.topics = self.bag.get_type_and_topic_info()
        self.messages = self.bag.read_messages()
        
        self.cmd = None
    
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
    
    def __help__(self):
        txt = """<h5>Help:</h5>
                <table>
                <tr> <th>Option</th> <th>Description</th> </tr>
                <tr> <td>--clock</td> <td>publish the clock time</td></tr>
                <tr> <td>--loop</td> <td>loop playback</td></tr>
                <tr> <td>--keep-alive</td> <td>keep alive past end of bag (useful for publishing latched topics)</td></tr>
                <tr> <td>--wait-for-subscribers</td> <td>wait for at least one subscriber on each topic before publishing</td></tr>
                </table>"""
        
        return HTML(data=txt)

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
    
    def play(self):
        
        #labels = widgets.HBox([widgets.Label(value="Option"), widgets.Label(value="Topics")])
        #options = widgets.SelectMultiple(options=['--clock', '--loop', '--keep-alive', '--wait-for-subscribers'])
        #topics = widgets.SelectMultiple(options=self.topics.keys(), value=self.topics.keys())
        
        options = [ vue.Checkbox(label='--clock', value='--clock', v_model=None, class_='mx-0 px-0'),
                    vue.Checkbox(label='--loop', value='--loop', v_model=None, class_='mx-0 px-0'),
                    vue.Checkbox(label='--keep-alive', value='--keep-alive', v_model=None, class_='mx-0 px-0'),
                    vue.Checkbox(label='--wait-for-subscribers', value='--wait-for-subscribers', v_model=None, class_='mx-0 px-0') ]
        
        topics = [ vue.Checkbox(label=t, value=t, v_model=t, class_='mx-0 px-0') for t in self.topics.keys() ]
        
        config = vue.Html(tag='div', class_='d-flex flex-row', children=[
            vue.Html(tag='div', class_='d-flex flex-column', children=[
                vue.Html(tag='h3', children=['Options']),
                vue.Container(children=options)
            ]),
            
            vue.Html(tag='div', class_='d-flex flex-column', children=[
                vue.Html(tag='h3', children=['Topics']),
                vue.Container(children=topics)
            ]),
        ])
        
        #config = widgets.HBox([options, topics])
        
        #btn_init = widgets.Button(description="Initialize", button_style='warning')
        #btn_play = widgets.Button(description="Play", icon='play', button_style='success')
        #btn_pause = widgets.Button(description="Pause", icon='pause', disabled=True)
        #btn_step = widgets.Button(description="Step", icon='step-forward')
        #btn_stop = widgets.Button(description="Stop", icon='stop', button_style='danger', disabled=True)
        
        btn_init = vue.Btn(color='warning', children=['Initialize'], class_='mx-2')
        btn_play = vue.Btn(color='success', disabled=True, children=[vue.Icon(left=True, children=['play']), 'Play'], class_='mx-2')
        btn_pause = vue.Btn(color='primary', disabled=True, children=[vue.Icon(left=True, children=['pause']), 'Pause'], class_='mx-2')
        btn_step = vue.Btn(color='primary', disabled=True, children=[vue.Icon(left=True, children=['step-forward']), 'Step'], class_='mx-2')
        btn_stop = vue.Btn(color='error', disabled=True, children=[vue.Icon(left=True, children=['stop']), 'Stop'], class_='mx-2')
        
        #output = widgets.widgets.Text()
        output = vue.TextField(label='Output')
        
        def btn_init_on_click(widget, event, data):
            btn_init.disabled = True
            btn_play.disabled = False
            btn_pause.disabled = False
            btn_step.disabled = True
            btn_stop.disabled = False
            
            opt = [ o.value for o in options if o.v_model != None ]
            top = [ t.value for t in topics if t.v_model != None ]
            
            command = ' '.join(['rosbag', 'play', '--pause'] + list(opt) + ['--topics'] + [' '.join(top)] + ['--bags='+self.bag.filename])
            self.cmd = Command(command, output)
            self.cmd.start()
            
            
        def btn_play_on_click(widget, event, data):
            btn_init.disabled = True
            btn_play.disabled = True
            btn_pause.disabled = False
            btn_step.disabled = True
            btn_stop.disabled = False
            
            if self.cmd != None :
                print("cmd.play")
                self.cmd.play()
            else :
                output.value = "You should initialize the command."
        
        def btn_pause_on_click(widget, event, data):
            btn_init.disabled = True
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = False
            
            if self.cmd != None :
                self.cmd.pause()
            else :
                output.value = "You should initialize the command."
        
        def btn_step_on_click(widget, event, data):
            btn_init.disabled = True
            btn_play.disabled = False
            btn_pause.disabled = True
            btn_step.disabled = False
            btn_stop.disabled = False
            
            if self.cmd != None :
                self.cmd.step()
            else :
                output.value = "You should initialize the command."
        
        def btn_stop_on_click(widget, event, data):
            btn_init.disabled = False
            btn_play.disabled = True
            btn_pause.disabled = True
            btn_step.disabled = True
            btn_stop.disabled = True
            
            if self.cmd != None :
                self.cmd.stop()
            else :
                output.value = "You should initialize the command."

        #btn_init.on_click(btn_init_on_click)
        #btn_play.on_click(btn_play_on_click)
        #btn_pause.on_click(btn_pause_on_click)
        #btn_step.on_click(btn_step_on_click)
        #btn_stop.on_click(btn_stop_on_click)
        
        btn_init.on_event('click', btn_init_on_click)
        btn_play.on_event('click', btn_play_on_click)
        btn_pause.on_event('click', btn_pause_on_click)
        btn_step.on_event('click', btn_step_on_click)
        btn_stop.on_event('click', btn_stop_on_click)
        
        #btns = widgets.VBox([widgets.HBox([btn_init, btn_play, btn_pause, btn_step, btn_stop]), output])
        
        btns = vue.Html(tag='div', class_='d-flex flex-row', children=[btn_init, btn_play, btn_pause, btn_step, btn_stop])
        
        #display( widgets.VBox([labels, config, btns]) )
        display( vue.Container(children=[config, btns, output]) )