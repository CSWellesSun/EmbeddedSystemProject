import datetime
from face_recog import FaceRecoginition
from chatgpt import ChatgptSession
import sqlite3
import os
from model import FaceModel


class SystemManager:
    def __init__(self, rknn_file):
        self.face_recog = FaceRecoginition(rknn_file)
        self.funccall = [
            self.register,
            self.logquery,
            self.userinfoquery,
            self.face_reg,
            self.quit,
        ]
        self.funcdesc = ["用户注册", "日志查询", "用户信息查询", "人脸识别", "退出应用"]
        self.chatgpt = ChatgptSession()
        self.conn = sqlite3.connect("log.db")
        self.db = self.conn.cursor()
        self.db.execute(
            "create table if not exists log(id int primary key,user text,name text,time datatime,event text)"
        )
        self.conn.commit()

    def getchoose(self):
        while True:
            for i, desc in enumerate(self.funcdesc):
                print("%s:%d" % (desc, i))
            try:
                choose = int(input("选择功能:"))
                if choose >= 0 and choose < len(self.funcdesc):
                    return choose
                else:
                    print("请输入1-4之间的选项")
            except:
                print("请输入数字选项")

    def menu(self):
        while True:
            choose = self.getchoose()
            self.funccall[choose]()

    def register(self):
        self.face_recog.register()

    def logquery(self):
        self.db.execute("SELECT * FROM log")
        rows = self.db.fetchall()
        for row in rows:
            print(row)
        input("回车退出")

    def userinfoquery(self):
        foldernames = os.listdir("user")
        for foldername in foldernames:
            filename = "user/" + foldername + "/info.txt"
            print(foldername)
            with open(filename, "rt") as f:
                print("name:", f.readline().strip())
                print("age:", f.readline().strip())
        input("回车退出")

    def addlog(self, index, username, event):
        self.db.execute("select IFNULL(MAX(id),0)+1 from log")
        id = self.db.fetchone()[0]
        if id is not None:
            id = int(id)
        now = datetime.datetime.now()
        self.db.execute(
            "insert into log values(%s,'%s','%s','%s-%s-%s %s:%s:%s','%s')"
            % (
                id,
                index,
                username,
                now.year,
                now.month,
                now.day,
                now.hour,
                now.minute,
                now.second,
                event,
            )
        )
        self.conn.commit()

    def face_reg(self):
        try:
            while True:
                index = self.face_recog.recognite()
                with open("user/%s/info.txt" % index, "rt") as f:
                    username = f.readline().strip()
                print("欢迎用户%s" % username)

                self.addlog(index, username, "usechatgpt")
                self.chatgpt.run()
                self.addlog(index, username, "endchatgpt")
        except KeyboardInterrupt:
            print("人脸检测结束")
        except Exception as e:
            print("发生故障,请联系管理人员修复")
            raise e

    def quit(self):
        exit(0)


if __name__ == "__main__":
    system = SystemManager("resnet.rknn")
    # system.face_recog.camera.setfoldername("test_faces")
    system.menu()
