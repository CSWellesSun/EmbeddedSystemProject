import requests
import configparser

configParser = configparser.ConfigParser()
configParser.read("config.ini")


class ChatgptCaller:
    def __init__(self):
        self.url = configParser.get("CHATGPT", "url")
        self.head = {"Content-type": "application/json; charset=unicode"}

    def __call__(self, str):
        data = {"msg": str}
        print(self.url)
        response = requests.post(url=self.url, json=data, headers=self.head)
        return response.text


class ChatgptSession:
    def __init__(self):
        self.chatgptcaller = ChatgptCaller()

    def run(self):
        print("欢迎使用本系统的聊天功能,Ctrl+C结束通话")
        try:
            while True:
                question = input("input question:")
                print(self.chatgptcaller(question))
        except KeyboardInterrupt:
            print("\n结束会话,欢迎下次使用")
        except Exception as e:
            print(e)
            print("会话异常中断,请联系管理人员修理,对于给您带来的不便,我们深感抱歉")


if __name__ == "__main__":
    session = ChatgptSession()
    session.run()
