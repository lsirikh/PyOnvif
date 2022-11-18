import json

data = {
    "onvif" : {
        "ip_address": "192.168.1.119",
        "port" : 80,
        "id" : "admin",
        "password" : "sensorway1"
    },
    "rtsp" : {
        "ip_address": "192.168.1.119",
        "port" : 554,
        "id" : "admin",
        "password" : "sensorway1"
    }
}

file_path = "./setup.ini"

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent="\t")