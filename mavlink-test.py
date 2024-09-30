from pymavlink import mavutil
import math


# connection = mavutil.mavlink_connection('udp:localhost:14550')
connection = mavutil.mavlink_connection('com18')

connection.wait_heartbeat()
print("Соединение с дроном установлено")

# Функция для запроса потока данных ATTITUDE
def request_attitude_data():
    connection.mav.request_data_stream_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        10, #Частота в герцах
        1
    )

def get_attitude():
    msg = connection.recv_match(type='ATTITUDE', blocking=True)
    
    if msg:
        roll = msg.roll * (180 / math.pi)
        pitch = msg.pitch * (180 / math.pi)
        yaw = msg.yaw * (180 / math.pi)

        print(f"roll: {roll:.2f}°, pitch: {pitch:.2f}°, yaw: {yaw:.2f}°")
        
        return roll, pitch, yaw
    else:
        print("Не удалось получить данные ATTITUDE")
        return None

if __name__ == "__main__":
    try:
        request_attitude_data()

        while True:
            roll, pitch, yaw = get_attitude()
            
    except KeyboardInterrupt:
        print("Программа остановлена пользователем")
