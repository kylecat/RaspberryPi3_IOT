# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as  sub
import os
import json, time
import sqlite3

#MQTT 連線設定
host = '192.168.0.21'  # 設定用'' 文字用""
topic = 'IAQ/+'  # 之後要拆成控制用topic, 資料用topic, 測試用topic
client_id ='pi'  # 放設備ID

database = os.path.join(os.path.abspath('.')+"/db.sqlite3")

run = True

def MQTT_sub():
    print(">>MQTT Subscriber start<<")
    sub_simple = sub.simple(topics=topic, qos=0, hostname=host, port=1883, client_id=client_id)
    rTopic = sub_simple.topic
    rMessage = sub_simple.payload.decode()

    if len(rMessage) > 100 and rTopic == 'IAQ/MonitoringData':
        # print("len :{}".format(len(rMessage)))
        # print("type :{}".format(type(rMessage)))
        # print(rMessage)
        save2DB(rMessage)
    else:
        print("len :{}".format(len(rMessage)))
        print("topic :{}".format(rTopic))
        print("message :{}".format(rMessage))


def save2DB(message):
    try:
        ddict = json.loads(message)
        print(ddict.keys())

    except Exception as err:
        print("Message load to JSON fail ：{}".format(err))

    list_sensorID = listID()
    print(list_sensorID)

    if len(list_sensorID) == 0:
        columns = ("sensor_id", "SensorEnv", "SensorCO2", "SensorPM", "name", "location", "type", "online")
        data = (ddict["ID"], ddict["Sensor_DHT"], ddict["Sensor_CO2"], ddict["Sensor_PM"], "name", "location", "type", 1)
        insert_data(columns, data, "MQTT_sensor")
        sensor_id_index = 1

    elif ddict["ID"] in list_sensorID:
        sensor_id_index = list_sensorID.index(ddict["ID"]) + 1

    else:
        columns = ("sensor_id", "SensorEnv", "SensorCO2", "SensorPM")
        data = (ddict["ID"], ddict["Sensor_DHT"], ddict["Sensor_CO2"], ddict["Sensor_PM"])
        insert_data(columns, data, "MQTT_sensor")
        new_list = listID()
        sensor_id_index = new_list.index(ddict["ID"]) + 1

    env_colums = ("sensor_id_id", "name", "date", "time", "Temperature", "Humidity", "HeatIndex")
    env_data = (sensor_id_index, ddict["Sensor_DHT"], ddict["Date"], ddict["Time"], ddict["Temperature"],
                ddict['Humidity'], ddict["HeatIndex"])
    insert_data(env_colums, env_data, "MQTT_environmentdata")
    time.sleep(0.5)
    print("<< Temp Humidity insert done >>")

    co2_colums = ("sensor_id_id", "name", "date", "time", "concentration")
    co2_data = (sensor_id_index, ddict["Sensor_CO2"], ddict["Date"], ddict["Time"], ddict["CO2_ppm"])
    insert_data(co2_colums, co2_data, "MQTT_carbondioxidedata")
    time.sleep(0.5)
    print("<< CO2 concentration insert done >>")

    pmc_colums = ("sensor_id_id", "name", "date", "time", "pm010_TSI", "pm025_TSI", "pm100_TSI",
                  "pm010_ATM", "pm025_ATM", "pm100_ATM")
    pmc_data = (sensor_id_index, ddict["Sensor_PM"], ddict["Date"], ddict["Time"], ddict["pm010_TSI"], ddict['pm025_TSI'],
                ddict["pm100_TSI"], ddict["pm010_ATM"], ddict['pm025_ATM'], ddict["pm100_ATM"])
    insert_data(pmc_colums, pmc_data, "MQTT_particlematterdata")
    time.sleep(0.5)
    print("<< PM concentration insert done >>")

    pmc_colums = ("sensor_id_id", "name", "date", "time", "Diameter_003", "Diameter_005",
                  "Diameter_010", "Diameter_025", "Diameter_050", "Diameter_100")
    pmc_data = (sensor_id_index, ddict["Sensor_PM"], ddict["Date"], ddict["Time"], ddict["D03_count"], ddict['D05_count'],
                ddict["D10_count"], ddict["D25_count"], ddict['D50_count'], ddict["D100_count"])
    insert_data(pmc_colums, pmc_data, "MQTT_particlenumberdata")
    time.sleep(0.5)
    print("<< PM number insert done >>")


def listID():
    try:
        # open sqlite3
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        sqlcheck = "SELECT DISTINCT sensor_id from MQTT_sensor"
        cur.execute(sqlcheck)
        sensorID = cur.fetchone()
        print("Sensor ID list: {}".format(sensorID))
        conn.close()  # 關閉連線

        if sensorID == None:
            return []
        else:
            return sensorID

    except Exception as err:
        print("get ID list fail ：{}".format(err))

def insert_data(table_tuple, data_tuple , table):
    try:
        # open sqlite3
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        sqladd = "INSERT INTO  "+table+" %s VALUES %s" % (table_tuple, data_tuple)
        cur.execute(sqladd)
        conn.commit()  # 儲存
        time.sleep(0.5)
        conn.close()  # 關閉連線
    except Exception as err:
        print("{} data insert fail ：{}".format(table, err))

# 執行(放在最下面)
if __name__ == "__main__":
    while run:
        print("Topic: {}".format(topic))
        MQTT_sub()
