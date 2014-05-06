#!/usr/bin/env python3
import queue
import bottle as btl
import threading
import lifx

BROADCAST_ADDR = b'\00\00\00\00\00\00'
q = queue.Queue()

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
        params = map(cnvt, [hue, saturation, brightness])
        command = LifxColourCommand(params)
        q.put(command)
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


class LifxCommand(object):    

    def run_action(self):
        print("I worked!")
    
    
class LifxColourCommand(LifxCommand):
    
    def __init__(self, params):
        self.params = params
    
    def run_action(self):
        all_colour(*self.params)
        print("Color set")

def worker():
    while True:
        item = q.get() #blocking call        
        # TODO try twice/check confirmation?
        try:
            item.run_action()            
        except Exception as e:
            msg = "Error: {}".format(e)
            print(msg)         


# TODO some try/catch to ensure the commands got executed..
# TODO create a lock to ensure that only one instance works on the bulbs..
# TODO move power command to the queue too
if __name__ == "__main__":
    
    num_worker_threads = 1
    for i in range(num_worker_threads):
         t = threading.Thread(target=worker)
         t.daemon = True
         t.start()
        
    btl.run(server='cherrypy', host='0.0.0.0', port=8888)





