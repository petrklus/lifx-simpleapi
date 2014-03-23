#!/usr/bin/env python3

import bottle as btl
import lifx

BROADCAST_ADDR = b'\00\00\00\00\00\00'

@btl.route('/hello/<name>')
def index(name):
    return btl.template('<b>Hello {{name}}</b>!', name=name)


@btl.route('/all/on')
def all_lights_on():
    light_power(True)
    return "OK"

@btl.route('/all/off')
def all_lights_on():
    light_power(False)
    return "OK"



@btl.route('/all/color/<hue>/<saturation>/<brightness>')
def all_lights_color(hue, saturation, brightness):    
    try:
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
        all_colour(*map(cnvt, [hue, saturation, brightness]))
        print("Color set")
        return "OK"
        
    except Exception as e:
        msg = "Error: {}".format(e)
        print(msg)
        return msg


def light_power(power_state=False):    
    lifx.set_power(BROADCAST_ADDR, power_state)

def all_colour(hue, saturation, brightness):
    lights = lifx.get_lights()

    # hue, saturation, brightness, kelvin, fade_time)
    # [ 0x0000, 0x0000, 0xffff, 6500, 10000 ]
    paramsTest = [ hue, saturation, brightness, 3500, 50]
    print(paramsTest)
    lifx.set_color(*([BROADCAST_ADDR]+paramsTest))



# TODO some try/catch to ensure the commands got executed..
# TODO create a lock to ensure that only one instance works on the bulbs..
# 

if __name__ == "__main__":
    btl.run(server='cherrypy', host='0.0.0.0', port=8888)





