import sqlite3
from time import sleep

from PIL import Image, ImageEnhance
from splinter.browser import Browser  #引入splinter的borwser对象
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def executeSQL(*args):
    conn = sqlite3.connect("Info.acr")
    cursor = conn.cursor()
    if args.__len__()==2:
        re = cursor.execute(args[0], args[1])
        re=re.fetchall()
    elif args.__len__()==1:
        re=cursor.execute(args[0])
        re=re.fetchall()
    else:
        re=False
    conn.commit()
    cursor.close()
    conn.close()

    return re

class AutomaticClassRobbing:

    __doc__ = "正在启动黑龙江大学选课自动抢课系统（模拟人工点击）......"

    def __init__(self):
        print(self.__doc__)
        self.getStudengtInfo()#获取用户的登录信息
        self.getClassList()#获取用户需要抢的课

        self.URL_Index="http://xsxk.hlju.edu.cn/xsxk/"#选课网站首页
        self.URL_ClassIndex="http://xsxk.hlju.edu.cn/xsxk/xkjs.xk"#选课的课程页面

        self.executable_path = "C:/chromedriver.exe"#浏览器驱动
        self.driver_name ='chrome'#浏览器名称

        print("初始化成功")

    def getStudengtInfo(self):  # 获取信息
        sql = "select valuse from setting where name='studentID'"
        self.StudentID = self.crypt(executeSQL(sql)[0][0])

        sql = 'select valuse from setting where name="password"'
        self.Password = self.crypt(executeSQL(sql)[0][0])

    def crypt(self, source):  # 加密解密
        self.key = "AutomaticClassRobbing"
        from itertools import cycle
        result = ''
        temp = cycle(self.key)
        for ch in source:
            result = result + chr(ord(ch) ^ ord(next(temp)))
        return result

    def getClassList(self):
        self.ClassIDs = []

        sql = "select * from ClassList"
        re = executeSQL(sql)
        for i in re:
            self.ClassIDs.append(str(i[0]))

    # def getClassList(self):
    #
    #     __doc__="正在获取用户需要的课......"
    #
    #     def delString(mes):  #
    #
    #         __doc__ = "格式化字符串"
    #
    #         if mes[-1] == '\n':
    #             return mes[:-1]
    #         else:
    #             return mes
    #
    #     def addID(mes):
    #         if mes not in self.ClassIDs:
    #             self.ClassIDs.add(mes)

        # print(__doc__)
        # self.ClassIDs = set()
        # file = open("ClassIDList.acr", "r")
        # for i in file.readlines():
        #     addID(delString(i))
        # file.close()

    # def getStudengtInfo(self):
    #
    #     __doc__="正在获取用户信息......"
    #
    #     def delString(mes):#
    #
    #         __doc__="格式化字符串"
    #
    #         if mes[-1] == '\n':
    #             return mes[:-1]
    #         else:
    #             return mes

        # print(__doc__)
        # file = open("setting.ini", "r")#读取用户数据
        # message = file.readline()
        # if message[:9] == "StudentID":
        #     StudentID = message[10:]
        #     message = file.readline()
        #     Password = message[9:]
        # else:
        #     Password = message[9:]
        #     message = file.readline()
        #     StudentID = message[10:-1]
        # self.StudentID=delString(StudentID)#学号
        # self.Password=delString(Password)#密码
        # file.close()

    def login(self):

        __doc__="正在准备登陆......"
        print(__doc__)
        self.driver.get(self.URL_Index)
        self.driver.find_element_by_id("xkgl").click()
        self.driver.find_element_by_id("username").send_keys(self.StudentID)
        self.driver.find_element_by_id("password").send_keys(self.Password)
        print("等待用户输入验证码......")
        while True:
            if self.driver.current_url != self.URL_Index:
                break

        # self.driver.find_by_xpath('//select[@id="ticketType_1"]/option[@value="1"]')._element.click()

        # self.driver.get_screenshot_as_file('./image1.jpg')  # 比较好理解
        # im = Image.open('./image1.jpg',"RGb")
        # box = (100, 100, 200, 200)  # 设置要裁剪的区域
        # region = im.crop(box)  # 此时，region是一个新的图像对象。
        # # region.show()#显示的话就会被占用，所以要注释掉
        # region.save("./image_code.jpg")
        # im = Image.open("./image_code.jpg")
        # imgry = im.convert('L')  # 图像加强，二值化
        # sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
        # sharp_img = sharpness.enhance(2.0)
        # sharp_img.save("./image_code.jpg")

    def start(self):

        __doc__="正在进入选课页面......"
        print(__doc__)

        self.driver.find_element_by_class_name("current").click()#选课中心
        js="comeToXkzx(this);"
        self.driver.execute_script(js)
        print("wite")

        self.driver.switch_to_frame("main")
        self.driver.execute_script("comeInQxgxk(this);")#全校公共选课

        self.driver.switch_to_frame("qxgxkFrame")

        count=0
        for ClassID in self.ClassIDs:
            count+=1
            print("正在选择第{}门课程......".format(count))
            self.driver.find_element_by_id("qKcxx").clear()
            self.driver.find_element_by_id("qKcxx").send_keys(ClassID[1:8])
            js="queryXkJxb();"
            self.driver.execute_script(js)#查询课程

            js="xkOper('2018-2019-"+ClassID+"')"#选课的js请求
            # print(js)
            count_try=0
            while True:
                count_try+=1
                print("正在进行第{}门课的第{}次尝试......".format(count,count_try))
                self.driver.execute_script(js)

                alert =self.driver.switch_to_alert()
                print(alert.text)
                # sleep(2)
                # alert.dismiss()#取消
                alert.accept()
                try:
                    #sleep(1)
                    alert = self.driver.switch_to_alert()
                    print(alert.text)
                    if alert.text=="选课成功！":
                        break
                    alert.accept()
                    sleep(1)
                except:
                    #sleep(5)
                    pass

    def main(self):
        print("准备开始选课......")
        print("正在打开浏览器......")
        self.driver = webdriver.Chrome()  # 打开浏览器
        self.driver.set_window_size(1200, 800)
        print("正在进入选课网站......")
        self.login()
        self.start()

if __name__ == '__main__':
    print("正在启动，请稍后......")
    a=AutomaticClassRobbing()
    a.main()
