from kmk.keys import make_argumented_key
from kmk.modules.holdtap import ActivationType, HoldTap, HoldTapKeyMeta
from kmk.modules.layers import LayerKeyMeta
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


    def process_key(self, keyboard, current_key, is_pressed, int_coord):
        '''Release os key after interrupting non-os keyup, or reset timeout and
        stack multiple os keys.'''
        send_buffer = False

        for key, state in self.key_states.items():
            if key == current_key:
                continue

            if (isinstance(current_key.meta, OneShotKeyMeta)) or (
                isinstance(current_key.meta, LayerKeyMeta)
            ):
                keyboard.cancel_timeout(state.timeout_key)
                if key.meta.tap_time is None:
                    tap_time = self.tap_time
                else:
                    tap_time = key.meta.tap_time 
                state.timeout_key = keyboard.set_timeout(
                    tap_time,
                    lambda k=key: self.on_tap_time_expired(k, keyboard, True),
                )
                continue

        if send_buffer:
            self.key_buffer.append((int_coord, current_key, is_pressed))
            current_key = None

        self.send_key_buffer(keyboard)

        return current_key

    def osk_pressed(self, key, keyboard, *args, **kwargs):
        '''Register HoldTap mechanism and activate os key.'''
        keyboard.active_layers.clear()
        keyboard.active_layers.insert(0, 1)

        if debug.enabled:
            debug('Reach pressed')
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

        if state.activated == ActivationType.PRESSED:
            state.activated = ActivationType.RELEASED
        else:
            self.ht_released(key, keyboard, *args, **kwargs)

        return keyboard
