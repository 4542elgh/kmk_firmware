# Status LEDs

Indicate which layer you are on with single led.
Layer color will be defined using RGB values

_Most of the code come from Neopixel and statusled.py_.

## Enabling the extension

To enable the extension you need to define a list of LED lights.

```python
from kmk.extensions.statusled_neopixel import statusLED
import board

statusLED = statusLED(breath_mode = True, colors=(
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255)
))
keyboard.extensions.append(statusLED)
```

## Configuration

All of these values can be set by default for when the keyboard boots.

```python
statusLED = statusLED(
    brightness=0.01,
    breath_mode = False, 
    colors = None
    )
```

The brightness values are in percentages.
