import yaml
import os
import sys
from random import randint
import threading
from pythonosc import dispatcher as dp
from pythonosc import osc_server
from pythonosc import udp_client



#回调函数
class Osc_processer:
    
    def __init__(self, avater_parameters: str, sentences_list: list, client, dispatcher):
        self.avater_parameters = avater_parameters
        self.sentences_list = sentences_list
        self.client = client
        self.dispatcher = dispatcher
        self.ran_lasttime = None

    def print_handler(self, address, *args):
        return self.osc_sencer(args[0], type(args[0]))

    def osc_receiver_main(self):
        
        self.dispatcher.map("/avatar/parameters/" + self.avater_parameters, self.print_handler)
        
    
    def osc_sencer(self, parameter_value, value_type):
        if (value_type == bool and parameter_value == True):
            self.send_sen(self.sentences_list)
        if (value_type == float and parameter_value == 0):
            self.send_sen(self.sentences_list)
        if (value_type == int and parameter_value == 0):
            self.send_sen(self.sentences_list)
    
    def send_sen(self, sen_list):
        random_num = randint(0, len(sen_list) -1)
        if self.ran_lasttime == None:
            self.ran_lasttime = random_num
        elif self.ran_lasttime == random_num:
            self.send_sen(sen_list)
            return

        self.ran_lasttime = random_num
        self.client.send_message("/chatbox/input", [sen_list[random_num], True])
        print(sen_list[random_num])
        
    def get_name(self):
        return self.avater_parameters


def load_configFile():
    configAdd = f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/config_try.yml"
    configOpen = open(configAdd, 'r', encoding='utf-8')
    configRead = configOpen.read()
    configFile = yaml.load(configRead, Loader=yaml.SafeLoader)

    return configFile

def check_file(configFile):
    print(configFile)
    key_count = 0
    value_count = 0
    try:
        for key in configFile:
            key_count += 1
            for value in configFile[key]:
                value_count += 1
        
        print("---Totaly {} parameter and {} sentence loaded---".format(key_count, value_count))
        return True
    except:
        print("ERROR!! sentence cannot be empty, please cheak the config file.")
        return False
    
def send_main(configFile):
    processers = []
    processers_thread = []
    if not check_file(configFile):
        return
    client = udp_client.SimpleUDPClient("localhost", 9000)
    dispatcher = dp.Dispatcher()
    server = osc_server.ThreadingOSCUDPServer(("localhost", 9001), dispatcher)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print("Serving on ('127.0.0.1', 9001)")
    for key in configFile:
        processers.append(Osc_processer(key, configFile[key], client, dispatcher))
        

    for index in range(len(processers)):
        processers_thread.append(threading.Thread(target=processers[index].osc_receiver_main))
        processers_thread[index].start()
        
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Received exit request. Shutting down...")
        server.shutdown()


if __name__ ==  "__main__":
    send_main(load_configFile())
    

