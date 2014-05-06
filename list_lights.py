#!/usr/bin/env python3
import lifx

lights = lifx.get_lights()

for light in lights:
    print(light)