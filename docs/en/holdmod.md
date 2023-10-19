# Hold Mod Keycodes

Hold Mod enable you to have modifier key that keep staying pressed
for a certain time. If the timeout expires and the sticky key wasn't
released, it is handled as a regular key hold.

## Enable OneShot Keys

```python
from kmk.modules.holdmod import HoldMod
holdmod_handler = HoldMod()
# optional: set a custom tap timeout in ms (default: 1000ms)
# holdmod_handler.tap_time = 1500
keyboard.modules.append(holdmod_handler)
```

## Keycodes

|Keycode          | Aliases      |Description                       |
|-----------------|--------------|----------------------------------|
|`KC.HM(KC.ANY)`  | `KC.HOLDMOD` |make a sticky version of `KC.ANY` |

`KC.HOLDMOD` accepts any valid key code as argument, including modifiers and KMK
internal keys like momentary layer shifts.

## Custom Hold Mod Behavior

The full Hold Mod signature is as follows:

```python
KC.HM(
    KC.TAP, # the sticky keycode
    tap_time=None # length of the tap timeout in milliseconds
    )
```