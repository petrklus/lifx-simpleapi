#!/usr/bin/env python3

import lifx

# first step is to always ensure all bulbs are on (we do not switch them off, we just set brightness to 0 if we do not want any light)
lifx.set_power(lifx.BCAST, True)



def light_set_colour(light, hue, saturation, brightness):    
    hue =           int(hue)
    saturation =    int(saturation)
    brightness =    int(brightness)

    # pre-scale hue, TODO integrate into checks..
    hue = hue / 355 * 100

    if hue > 100 or saturation > 100 or brightness > 100 \
      or hue < 0 or saturation < 0   or brightness < 0:
        raise Exception("Only accepting percentages between 0 and 100")

    scaling_coef = 65535/100
    cnvt = lambda val: int(val * scaling_coef)
    
    # set colour
    params = map(cnvt, [hue, saturation, brightness])
    
    paramsTest = list(params) + [3500, 50]
    print(paramsTest)
    light.set_color(*paramsTest)
    



if __name__ == "__main__":
    
    import sys
    lights = lifx.get_lights()
    
    packets = sys.argv[1].split(".")
    
    control_lights = {}
    for packet in packets:
        print(packet)
        try:
            light_addr, hue, saturation, brightness = packet.split(",")
            control_lights[light_addr] = hue, saturation, brightness
        except ValueError:
            print("Invalid packet: {}".format(packet))
    
    print(light_addr)
    for light in lights:
        cur_addr = light.get_addr()
        if cur_addr in control_lights.keys():            
            light_set_colour(light, *control_lights[cur_addr])
    
    
"""

office:         d073d500072c
living room:    d073d5010fe5
./colour_setter.py d073d500072c 355 100 100
./colour_setter.py d073d5010fe5 355 100 0

"""