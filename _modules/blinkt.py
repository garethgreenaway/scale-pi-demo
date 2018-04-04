# -*- coding: utf-8 -*-
'''
Module for controlling the Blinkt LED matrix

.. versionadded:: Fluorine

:maintainer:    Gareth J. Greenaway <gareth@saltstack.com>
:maturity:      new
:depends:       sense_hat Python module

'''

from __future__ import absolute_import, unicode_literals, print_function

import colorsys
import logging
import time

try:
    import blinkt
    has_blinkt = True
except (ImportError, NameError):
    has_blinkt = False
log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load the module if Blinkt is available
    '''
    if has_blinkt:
        return True
    else:
        return False, "The blinkt excecution module can not be loaded."


def one_rgb(pixel, r, g, b, timeout=None):
    '''
    Only load the module if Blinkt is available
    '''
    try:
        res = __salt__['event.fire']({'mode': 'one_rgb',
                                      'kwargs': {'pixel': pixel,
                                                 'r': r,
                                                 'g': g,
                                                 'b': b,
                                                 'timeout': timeout}},
                                     '/salt/minion/blinkt')
    except KeyError:         
        # Effectively a no-op, since we can't really return without an event system
        ret = {}             
        ret['comment'] = 'Event module not available.'
        ret['result'] = True 
        return ret     

def range_rgb(start, end, r, g, b, timeout=None):
    '''
    Only load the module if Blinkt is available
    '''
    try:
        res = __salt__['event.fire']({'mode': 'range_rgb',
                                      'kwargs': {'start_pixel': start,
                                                 'end_pixel': end,
                                                 'r': r,
                                                 'g': g,
                                                 'b': b,
                                                 'timeout': timeout}},
                                     '/salt/minion/blinkt')
    except KeyError:         
        # Effectively a no-op, since we can't really return without an event system
        ret = {}             
        ret['comment'] = 'Event module not available.'
        ret['result'] = True 
        return ret     

def rgb(r, g, b, timeout=None):
    '''
    Only load the module if Blinkt is available
    '''
    ret = {}             
    try:
        res = __salt__['event.fire']({'mode': 'all_rgb',
                                      'kwargs': {'r': r,
                                                 'g': g,
                                                 'b': b,
                                                 'timeout': timeout}},
                                     '/salt/minion/blinkt')
        ret['comment'] = res
    except KeyError:         
        # Effectively a no-op, since we can't really return without an event system
        ret['comment'] = 'Event module not available.'
        ret['result'] = True 
    return ret     

def clear(**kwargs):
    '''
    Only load the module if Blinkt is available
    '''
    try:
        res = __salt__['event.fire']({'mode': 'clear', 'kwargs': kwargs}, '/salt/minion/blinkt')
    except KeyError:         
        # Effectively a no-op, since we can't really return without an event system
        ret = {}             
        ret['comment'] = 'Event module not available.'
        ret['result'] = True 
        return ret     

def random_blink_colors(timeout=None):
    '''
    Only load the module if Blinkt is available
    '''
    try:
        res = __salt__['event.fire']({'mode': 'random_blink_colors',
                                      'kwargs': {'timeout': timeout}},
                                     '/salt/minion/blinkt')
    except KeyError:         
        # Effectively a no-op, since we can't really return without an event system
        ret = {}             
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
        return ret

def rainbow(timeout=None):
    '''
    Only load the module if Blinkt is available
    '''
    try:
        res = __salt__['event.fire']({'mode': 'rainbow',
                                      'kwargs': {'timeout': timeout}},
                                     '/salt/minion/blinkt')
    except KeyError:         
        # Effectively a no-op, since we can't really return without an event system
        ret = {}             
        ret['comment'] = 'Event module not available.'
        ret['result'] = True
        return ret
