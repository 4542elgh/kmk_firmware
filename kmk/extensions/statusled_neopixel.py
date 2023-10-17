# Use this extension for showing layer status with single leds, this is tested on XIAO RP2040
# Author: Evan Liu
# Last Modified: 10/17/2023

import board
import neopixel

from kmk.extensions import Extension

class statusLED(Extension):
    def __init__(self, brightness=0.01, breath_mode = False, colors = None):
        self.led = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.brightness = brightness
        self.colors = colors
        self.breath_mode = breath_mode
        self.breath_brightness_delta = 0.00001
        self.breath_mode_inc_dec = 'desc'

    # This is contineously scanned, LED will change once the scan detect a new layer is active
    def _layer_indicator(self, layer_active, *args, **kwargs):
        for (index, rgb) in enumerate(self.colors):
            if layer_active == index:
                self.led[0] = rgb
        
        if self.breath_mode:
            if self.brightness >= 0.02:
                self.breath_mode_inc_dec = 'desc'
            elif self.brightness <= 0:
                self.breath_mode_inc_dec = 'inc'

            if self.breath_mode_inc_dec == 'desc':
                self.brightness -= self.breath_brightness_delta
            else:
                self.brightness += self.breath_brightness_delta
            
        self.led.brightness = self.brightness

    def __repr__(self):
        return f'SLED({self._to_dict()})'

    def _to_dict(self):
        return {
            'brightness': self.brightness,
            'colors': self.colors,
        }

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        # This could cycle LED lights for user
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        self._layer_indicator(sandbox.active_layers[0])
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        self.set_brightness(0)
        return

    def on_powersave_disable(self, sandbox):
        self.set_brightness(self.brightness)
        return

    def set_brightness(self, percent):
        self.led.brightness = percent
