import yaml
import os
import sys
import random
from pythonosc import dispatcher as dp
from pythonosc import osc_server
from pythonosc import udp_client


def load_configFile():
    configAdd = f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/config_try.yml"
    configOpen = open(configAdd, 'r', encoding='utf-8')
    configRead = configOpen.read()
    configFile = yaml.load(configRead, Loader=yaml.SafeLoader)

    return configFile

#回调函数
class Osc_processer:
    
    def __init__(self, avater_parameters: str, sentences_list: list):
        self.avater_parameters = avater_parameters
        self.sentences_list = sentences_list

    def print_handler(self, address, *args):
        print(address, args)
        return self.osc_sencer(args[0], type(args))


    def osc_receiver(self):
        dispatcher = dp.Dispatcher()
        dispatcher.map("/avatar/parameters/" + self.avater_parameters, self.print_handler)
    
    def osc_sencer(self, parameter_value, value_type):
        if value_type == bool:
            pass
        if value_type == float:
            pass
        if value_type == int:
            pass



def ser():
    dispatcher = dp.Dispatcher()
    dispatcher.map("/avatar/parameters/", print_handler)

    server = osc_server.ThreadingOSCUDPServer(("localhost", 9001), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ ==  "__main__":
    

