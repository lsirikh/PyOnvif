import json

class JsonClass():
    def __init__(self) -> None:
        print("JsonClass was created")
        
        
    def readConfig(self):
        self.file_path = "./setup.ini"

        # 기존 json 파일 읽어오기
        with open(self.file_path, 'r') as file:
            self.readData = json.load(file)

        return self.readData
