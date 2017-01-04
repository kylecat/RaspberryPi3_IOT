# -*- coding: utf-8 -*-
"""
    * 多線程(threading)由 urls.py 啟動
    * MQTT 收到資料之後轉存到
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from MQTT.models import EnvironmentData, CarbonDioxideData, ParticleMatterData, ParticleNumberData, Sensor
import json
import time


# 運行狀態
state = True

#MQTT 連線設定
host = '192.168.0.21'  # 設定用'' 文字用""
topic = 'IAQ/MonitoringData'  # 之後要拆成控制用topic, 資料用topic, 測試用topic
client_id ='NB'  # 放設備ID


def on_message(client, userdata, message):
    rMessage = message.payload.decode()  #原本是byte格式，要解碼成str
    rTopic = message.topic
    rQos = message.qos
    print(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    if len(rMessage) > 30:
        print("Received len :{}".format(len(rMessage)))
        save2DB(rMessage)
    else:
        print("Received message :{}".format(rMessage))
        print("Received len :{}".format(len(rMessage)))
        print("Received topic :{}".format(rTopic))
        print("Received QoS :{}".format(rQos))
    print("======================================")


def MQTT_sub():
    print("< MQTT Subscriber start at MQTT Topic: {}>>".format(topic))
    try:
        client = mqtt.Client(client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
        client.connect(host, 1883, 60)
        client.subscribe(topic, qos=2)
        client.on_message = on_message
        client.loop_forever()
    except Exception as err:
        print(err)


def MQTT_pub():
    while True:
        send = input("input the massage: ")
        publish.single(topic, payload=send, qos=0, hostname=host)
        time.sleep(30)


def save2DB(message):
    try:
        ddict = json.loads(message)
        # print(ddict.keys())
        addSensor = add_sensor(ddict["ID"], ddict["Sensor_DHT"], ddict["Sensor_CO2"], ddict["Sensor_PM"])

        EnvironmentData.objects.create(sensor_id=addSensor,
                                       date=ddict["Date"], time=ddict["Time"],
                                       temperature=ddict["Temperature"], humidity=ddict['Humidity'],
                                       HeatIndex=ddict["HeatIndex"])
        CarbonDioxideData.objects.create(sensor_id=addSensor, date=ddict["Date"], time=ddict["Time"],
                                         concentration=ddict["CO2_ppm"])
        ParticleMatterData.objects.create(sensor_id=addSensor, date=ddict["Date"], time=ddict["Time"],
                                          pm010_TSI=ddict["pm010_TSI"], pm025_TSI=ddict["pm025_TSI"],
                                          pm100_TSI=ddict["pm100_TSI"], pm010_ATM=ddict["pm010_ATM"],
                                          pm025_ATM=ddict["pm025_ATM"], pm100_ATM=ddict["pm100_ATM"])
        ParticleNumberData.objects.create(sensor_id=addSensor, date=ddict["Date"], time=ddict["Time"],
                                          Diameter_003=ddict["D03_count"], Diameter_005=ddict["D05_count"],
                                          Diameter_010=ddict["D10_count"], Diameter_025=ddict["D25_count"],
                                          Diameter_050=ddict["D50_count"], Diameter_100=ddict["D100_count"])

        # print(Sensor.objects.all())
    except Exception as err:
        print(err)
        pass


# 因為 Sensor.sensor_id是設定成 ForeignKey 所以在其他資料寫入的時候要同時進行設定
def add_sensor(ID, Env, CO2, PM):
    add = Sensor.objects.get_or_create(sensor_id=ID, SensorEnv=Env, SensorCO2=CO2, SensorPM=PM, online=True)[0]
    return add

# Start execution here!
if __name__ == '__main__':
    print("<<  Starting MQTT Subscriber script...  >>")
    MQTT_sub()
