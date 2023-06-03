import paho.mqtt.client as mqtt  #import the client1
import time
import random
import sqlite3
global click
global button_click
button_click = 1
def get_status_door_by_number(doorNumber):
    c.execute("SELECT * FROM doorsTable WHERE doorNumber=:doorNumber", {'doorNumber': doorNumber})
    return c.fetchone()

def update_door(doorNumber, lock):
    with conn:
        c.execute("""UPDATE doorsTable SET lock = :lock WHERE doorNumber =:doorNumber""",{'doorNumber':doorNumber, 'lock':lock})

def get_status_window_by_number(windowNumber):
    c2.execute("SELECT * FROM windowsTable WHERE windowNumber=:windowNumber", {'windowNumber': windowNumber})
    return c2.fetchone()

def update_window(windowNumber, lock):
    with conn2:
        c2.execute("""UPDATE windowsTable SET lock = :lock WHERE windowNumber =:windowNumber""",{'windowNumber':windowNumber, 'lock':lock})

# broker list
brokers=["iot.eclipse.org","broker.hivemq.com",\
         "test.mosquitto.org"]

broker=brokers[1]


def on_log(client, userdata, level, buf):
        print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
def on_message(client,userdata,msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message received: ",m_decode)
        msg_parse(m_decode)

def msg_parse(m_decode):
        print(m_decode) 
        global button_click
        global click
        subString="Temperature:" 
        if subString in m_decode:    
            rez=float(m_decode.split('Temperature: ')[1].split(' Humidity:')[0])
            print(rez) 
            if rez >= 25 :
                client.publish(pub_topic,"too hot The owner is stingy on the air conditioner  the system opens all the windows")
                conn2 = sqlite3.connect('windows.db')
                c2=conn2.cursor()
                for windowNumber in range(20):
                    c2.execute("""UPDATE windowsTable SET lock = :lock WHERE windowNumber =:windowNumber""",{'windowNumber':windowNumber+1, 'lock':'open'})
                    conn2.commit()
                time.sleep(3)
        elif "open" in m_decode:
            conn = sqlite3.connect('doors.db')
            c=conn.cursor()
            c.execute("""UPDATE doorsTable SET lock = :lock WHERE doorNumber =:doorNumber""",{'doorNumber':21, 'lock':'open'})
            conn.commit()
        elif "close" in m_decode:
            conn = sqlite3.connect('doors.db')
            c=conn.cursor()
            c.execute("""UPDATE doorsTable SET lock = :lock WHERE doorNumber =:doorNumber""",{'doorNumber':21, 'lock':'close'})
            conn.commit()
            
client = mqtt.Client("IOT_project", clean_session=True) # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message
print("Connecting to broker ",broker)
port=1883
client.connect(broker,port)     #connect to broker
pub_topic= 'Lock_Me'



conn = sqlite3.connect('doors.db')
conn2 = sqlite3.connect('windows.db')
c=conn.cursor()
c2=conn2.cursor()
for doorNumber in range(20):
    if (get_status_door_by_number(doorNumber+1)[1] == "open"):
        client.publish(pub_topic," There are open doors on floor " + str(doorNumber+1)+" The system will close the windows")
        update_door(doorNumber+1, 'close')
        time.sleep(1.5)
        client.publish(pub_topic," The system closed the doors")
    else:
        client.publish(pub_topic, "There are no open doors on the floor " + str(doorNumber+1))
    time.sleep(1.5)
for windowNumber in range(20):
    
    if (get_status_window_by_number(windowNumber+1)[1] == "open"):
        client.publish(pub_topic," There are open windows on floor " + str(windowNumber+1)+" The system will close the windows")
        update_window(windowNumber+1, 'close')
        time.sleep(1.5)
        client.publish(pub_topic," The system closed the windows")
    else:
        client.publish(pub_topic, "There are no open windows on the floor " + str(windowNumber+1))

    time.sleep(1.5)
client.publish(pub_topic, "The scan is finished all the doors and windows are colse ")
client.loop_start()
client.subscribe("Lock_Me")
time.sleep(300)
client.loop_stop()

client.disconnect() # disconnect
print("End publish_client run script")






