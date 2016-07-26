#qpy:kivy
from kivy.app import App

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.filechooser import FileChooserIconView

from kivy.graphics import Color, Rectangle

import socket

import SimpleHTTPServer
import SocketServer
import threading
import webbrowser
import platform
from socket import SOL_SOCKET,SO_REUSEADDR
import os

class Server(object):
    def __init__(self,port=8000):
        self.ip = self.ip()
        self.port = self.port()
        self.thread = None

        self.httpd = SocketServer.TCPServer((self.ip, self.port), SimpleHTTPServer.SimpleHTTPRequestHandler)
        self.httpd.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.run = False
        self.url = 'http://{0}:{1}'.format(self.ip, self.port)

    def start(self):
        print 'serving on', self.url
        self.run = True

        self.thread = threading.Thread(target = self._serve)
        self.thread.start()


    def _serve(self):
        while self.run:
            self.httpd.handle_request()

    def stop(self):
        self.run = False

    def start2run(self, event):
        if event.state == 'down':
            self.start()
        else:
            self.stop()

    def ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        return s.getsockname()[0]

    def port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in range(8000, 8080):
            if sock.connect_ex(('127.0.0.1', port)) != 0:
                return port

class Page1(BoxLayout):
    def __init__(self, **kwargs):
        super(Page1, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)


        self.server = Server()

        self.togglebutton = ToggleButton(
            text='start',
            on_press=self.update
        )

        self.label = Label(text='Press start to start server')

        self.add_widget(self.label)
        self.add_widget(self.togglebutton)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update(self, event):
        if event.state == 'down':
            self.server.start2run(event)
            self.label.text =  'Started on http://{0}:{1}'.format(self.server.ip, self.server.port)
            self.togglebutton.text = 'stop'
        else:
            self.label.text = 'Press start to start server'
            self.server.start2run(event)
            self.togglebutton.text = 'start'

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

class Page2(BoxLayout):
    def __init__(self, **kwargs):
        super(Page2, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)


        self.fciv = FileChooserIconView()

        self.button = Button(
            text='choose directory',
            on_release=self.choosedir
        )


        self.add_widget(self.fciv)
        self.add_widget(self.button)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def choosedir(self, event):
        os.chdir(self.fciv.path)

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

class PhoneServer(PageLayout):
    def __init__(self,**kwargs):
        super(PhoneServer, self).__init__(**kwargs)
        self.pathtoserver = '/'

        self.page1 = Page1(orientation='vertical')
        self.page2 = Page2(orientation='vertical')
        self.add_widget(self.page1)
        self.add_widget(self.page2)


class MyApp(App):
    def build(self):
        return PhoneServer()

if __name__ == "__main__":
    MyApp().run()
