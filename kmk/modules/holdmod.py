from kmk.keys import make_argumented_key
from kmk.modules.holdtap import ActivationType, HoldTap, HoldTapKeyMeta
from kmk.utils import Debug

debug = Debug(__name__)


class OneShotKeyMeta(HoldTapKeyMeta):
    def __init__(self, kc, tap_time=None):
        super().__init__(tap=kc, hold=kc, prefer_hold=False, tap_time=tap_time)


class HoldMod(HoldTap):
    tap_time = 3000

    def __init__(self):
        super().__init__(True)
        make_argumented_key(
            validator=OneShotKeyMeta,
            names=('HM', 'HOLDMOD'),
            on_press=self.osk_pressed,
            on_release=self.osk_released,
        )

    def osk_pressed(self, key, keyboard, *args, **kwargs):
        '''Register HoldTap mechanism and activate os key.'''
        keyboard.active_layers.clear()
        keyboard.active_layers.insert(0, 1)

        if debug.enabled:
            debug('osk_pressed hold mod')

        self.ht_pressed(key, keyboard, *args, **kwargs)
        self.ht_activate_tap(key, keyboard, *args, **kwargs)
        self.send_key_buffer(keyboard)

        return keyboard

    def osk_released(self, key, keyboard, *args, **kwargs):
        '''On keyup, mark os key as released or handle HoldTap.'''
        try:
            state = self.key_states[key]
        except KeyError:
            if debug.enabled:
                debug(f'OneShot.osk_released: no such key {key}')
            return keyboard

        if debug.enabled:
            debug('osk_released hold mod')

        if state.activated == ActivationType.PRESSED:
            state.activated = ActivationType.RELEASED
        else:
            self.ht_released(key, keyboard, *args, **kwargs)

        return keyboard
