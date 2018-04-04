# -*- coding: utf-8 -*-
'''
Blinkt engine
'''

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals
import datetime
import colorsys
import logging
import random
import time

try:
    import blinkt
    has_blinkt = True
except (ImportError, NameError):
    has_blinkt = False

# Import salt libs
import salt.utils.event

log = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load the module if Blinkt is available
    '''
    if has_blinkt:
        return True
    else:
        return False

class BlinktEngine(object):

    def __init__(self):
        '''
        '''
        self.stop_time = None

    def run(self):
        '''
        '''
        if __opts__['__role'] == 'master':
            event_bus = salt.utils.event.get_master_event(
                    __opts__,
                    __opts__['sock_dir'],
                    listen=True)
        else:
            event_bus = salt.utils.event.get_event(
                'minion',
                transport=__opts__['transport'],
                opts=__opts__,
                sock_dir=__opts__['sock_dir'],
                listen=True)

        _kwags = {}
        mode = None
        while True:
            now = datetime.datetime.now()
            event = event_bus.get_event(full=True)
            if event:
                if 'tag' in event:
                    if event['tag'].startswith('/salt/minion/blinkt'):
                        mode = event['data'].get('mode', None)
                        _kwargs = event['data'].get('kwargs', {})
                        if _kwargs.get('timeout', None):
                            self.stop_time = now + datetime.timedelta(seconds=_kwargs.get('timeout'))

            if mode:
                func = getattr(self, mode, None)
                if func:
                    func(**_kwargs)
                    if self.stop_time:
                        if self.stop_time <= now:
                            mode = None
                            self.clear(**_kwargs)

    def random_blink_colors(self, **kwargs):
        '''
        '''
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.1)

        for i in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        blinkt.show()

    def rainbow(self, **kwargs):
        '''
        '''

        spacing = 360.0 / 16.0
        hue = 0

        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.1)

        hue = int(time.time() * 100) % 360
        for x in range(blinkt.NUM_PIXELS):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)
        blinkt.show()

    def one_rgb(self, **kwargs):
        '''
        '''
        pixel = kwargs.get('pixel')
        r = kwargs.get('r')
        g = kwargs.get('g')
        b = kwargs.get('b')
        blinkt.set_pixel(pixel, r, g, b)
        blinkt.show()

    def range_rgb(self, **kwargs):
        '''
        '''
        start_pixel = kwargs.get('start_pixel')
        end_pixel = kwargs.get('end_pixel')
        r = kwargs.get('r')
        g = kwargs.get('g')
        b = kwargs.get('b')
        for pixel in range(start_pixel, end_pixel + 1):
            blinkt.set_pixel(pixel, r, g, b)
            blinkt.show()

    def all_rgb(self, **kwargs):
        '''
        '''
        r = kwargs.get('r')
        g = kwargs.get('g')
        b = kwargs.get('b')
        blinkt.set_all(r, g, b)
        blinkt.show()

    def clear(self, **kwargs):
        '''
        '''
        if 'pixel' in kwargs:
            self.clear_one(kwargs['pixel'])
        elif 'start' in kwargs and 'end' in kwargs:
            self.clear_range(kwargs['start'], kwargs['end'])
        else:
            blinkt.set_all(0, 0, 0)
            blinkt.show()

    def clear_one(self, pixel):
        blinkt.set_pixel(pixel, 0, 0, 0)
        blinkt.show()

    def clear_range(self, start_pixel, end_pixel):
        for pixel in range(start_pixel, end_pixel + 1):
            blinkt.set_pixel(pixel, 0, 0, 0)
        blinkt.show()

def start(interval=1):
    '''
    Listen to events and write them to a log file
    '''
    client = BlinktEngine()
    client.run()
