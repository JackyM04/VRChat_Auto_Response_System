import yaml
import os
import sys
import random
import argparse
import pyOSC3
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
class main:
    
    def load_configFile(self):
        configAdd = f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/config.yml"
        configOpen = open(configAdd, 'r', encoding='utf-8')
        configRead = configOpen.read()
        self.configFile = yaml.load(configRead, Loader=yaml.SafeLoader)
        
        return self.configFile

    def read_parameter(self):
        self.type_parameter = []
        self.ran_num_parameter = []
        self.parameters_dict = {}
        self.parameters = list(dict.keys(self.configFile))
        self.len_parameters = len(self.parameters)
        for i in range(0, self.len_parameters):
            self.type_parameter.append(0)
            self.ran_num_parameter.append(0)
            self.parameters_dict[self.parameters[i]] = i
        
        
        return self.parameters, self.len_parameters, self.type_parameter,self.ran_num_parameter,self.parameters_dict

    def read_read_sen(self):
        self.sen = list(dict.values(self.configFile))
        return self.sen

    def server_start(self):
        #启动OSCserver 
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
            default="127.0.0.1", help="The ip to listen on")
        parser.add_argument("--port",
            type=int, default=9001, help="The port to listen on")
        args = parser.parse_args()
        self.server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
        #启动OSclient
        parser_c = argparse.ArgumentParser()
        parser_c.add_argument("--ip", default="127.0.0.1",
            help="The ip of the OSC server")
        parser_c.add_argument("--port", type=int, default=9000,
            help="The port the OSC server is listening on")
        args_c = parser_c.parse_args()
        self.client = udp_client.SimpleUDPClient(args_c.ip, args_c.port)
        
        return self.server, self.client

    def count_sen(self):
        self.len_sen_sin = []
        for i in range(0, self.len_parameters):
            self.len_sen_sin.append(len(self.sen[i]))
            sen_sin = self.sen[i]
            print(self.parameters[i],":")
            for iin in range(0, self.len_sen_sin[i]):
                if sen_sin[iin] != None:
                    print("sentence {} correct".format(iin+1))
                else:
                    print("ERROR sentence {} in {} cannot be empty, please cheak the config file.".format(iin+1,self.parameters[i]))
        print("Serving on {}".format(self.server.server_address))
        return self.len_sen_sin

    def send_sen_bool(self,num_p,data,Ran_num):
        parameters = self.parameters[num_p]
        sen_list = self.sen[num_p]
        len_sen_sin = len(sen_list)
        if "/avatar/parameters/{}".format(parameters) in str(data):
            k = str(data).split(",")
            l = k[1]
            if "T" in str(l):
                outPut_sen = sen_list[Ran_num-1]
                self.client.send_message("/chatbox/input", [outPut_sen, True])
                print('prameter({})exported sentence[{}]'.format(parameters,outPut_sen))
                #产生不相等的随机数
                
        return None
    
    def ball(self):
        sen_sin = self.sen[0]
        if sen_sin[0] == "Who is Jacky?":
            print("Jacky is the smartest man in the world!!!")
            
            self.client.send_message("/chatbox/input", ["Jacky is the smartest man in the world!!!", True])
        else:
            pass

    def send_sen_inflo(self,num_p,data,Ran_num):
        parameters = self.parameters[num_p]
        sen_list = self.sen[num_p]
        len_sen_sin = len(sen_list)
        if "/avatar/parameters/{}".format(parameters) in str(data):
            dec = pyOSC3.decodeOSC(data)
            
            if dec[2] != 0.00:
                outPut_sen = sen_list[Ran_num-1]
                self.client.send_message("/chatbox/input", [outPut_sen, True])
                print('prameter({})exported sentence[{}]'.format(parameters,outPut_sen))
                #产生不相等的随机数          
                
        return None
    def receive_to_bin(self,time_set):
        time_now = 0
        time_start = time.time()
        while time_now < time_set:
            data, client_addr = self.server.socket.recvfrom(self.server.max_packet_size)
            time_now = time.time() - time_start

    def send_main(self):
        while True:    
            data, client_addr = self.server.socket.recvfrom(self.server.max_packet_size)
            if any(word in str(data) for word in self.parameters):
            #for word in self.parameters_dict:
                #if word in str(data):
                    #i = self.parameters_dict[word]
            
                for i in range(0,self.len_parameters):
                    
                    if self.parameters[i] in str(data):        
                        
                        
                        if self.type_parameter[i] == 0:
                            try:
                                self.send_sen_inflo(i,data,self.ran_num_parameter[i])
                                old_Ran_num = self.ran_num_parameter[i]
                        
                                while old_Ran_num == self.ran_num_parameter[i] and self.len_sen_sin[i]!= 1:
                                    self.ran_num_parameter[i] = random.randrange(1, self.len_sen_sin[i]+1)
                                self.receive_to_bin(2)
                                
                            except:
                                self.type_parameter[i] = 1
                                self.send_sen_bool(i,data,self.ran_num_parameter[i])
                        if self.type_parameter[i] == 1:
                            self.send_sen_bool(i,data,self.ran_num_parameter[i])
                            old_Ran_num = self.ran_num_parameter[i]
                            while old_Ran_num == self.ran_num_parameter[i] and self.len_sen_sin[i]!= 1:
                                self.ran_num_parameter[i] = random.randrange(1, self.len_sen_sin[i]+1)
                            time.sleep(2)
    
    def start(self):
        self.load_configFile()
        self.read_parameter()
        self.read_read_sen()
        self.server_start()
        self.count_sen()
        self.ball()
        self.send_main()

mm = main()
mm.start()