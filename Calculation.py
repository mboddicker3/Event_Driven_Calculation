'''
Program 3) Calculation 
 - This program will receive data on the topics "/random_numbers" and "/calculation/setup"
 - The program will use the input from "Calculation Setup" to tell it whether to perform addition("+") or subtraction("-")
 - The program will use the random number data to calculate either the addition or subtraction of "num1" and "num2"
 - Once the calcualtion is complete, the program will publish the result on topic "/calculated/add" for "+" or "/calculated/subtract" for "-"
 - example message {"type":"calculation","setup":"+","result":43.3453}
'''

from mqtt_basic import MqttClient
from random import random
import json
import sys

from random_num_client import RandomNumberClient
sys.path.append('..')


class Calculate(MqttClient):

    def __init__(self, ip, port, uid):
        super().__init__(ip, port, uid)
        self.subscribe('/random_numbers')
        self.subscribe('/calculation/setup')
        self.pubTopic = ''  # we decide what topic to publish to when we receive a message
        self.calcDict:dict[str, str] = {}

    def on_message(self, client, userdata, msg):
        data: dict = json.loads(msg.payload.decode('utf-8'))
        if (data['type'] == 'random_number'):#if we receive message with random numbers, save them in calcDict as num1 and num2
            self.calcDict['num1'] = data['num1']
            self.calcDict['num2'] = data['num2']
        #else if we receive message with setup, save it in calcDict as the operator
        elif (data['type'] == 'setup'):
            self.calcDict['setup'] = data['setup']

        #check to see if we have both pieces of information needed to make the calculation
        if(calcDict['num1'] != None and calcDict['num2'] != None and calcDict['setup'] != None):
            self.publishCalculation(self.calcDict)
            
        

    def publishCalculation(self, data):
        result: int = 0
        if (data['setup']) == '+':
            result = (data['num1']) + (data['num2'])
        elif (data['setup']) == '-':
            result = (data['num1']) - (data['num2'])

        calcinfo = {
            'setup': data['operation'],
            'result': result
        }

        self.publish(self.pubTopic, json.dumps(calcinfo).encode('utf-8'))
        # print(calcinfo) for debugging


if __name__ == "__main__":
    # need to change

    client = RandomNumberClient("127.0.0.1", 1883, '')
    client.start()
