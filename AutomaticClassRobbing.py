from time import sleep

from PIL import Image, ImageEnhance
from splinter.browser import Browser  #引入splinter的borwser对象
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AutomaticClassRobbing:

    __doc__ = "黑龙江大学选课自动抢课（模拟人工点击）"

    def __init__(self):
        self.StudentID="20154471"
        self.Password="900514"

        self.URL_Index="http://xsxk.hlju.edu.cn/xsxk/"#选课网站首页
        self.URL_ClassIndex="http://xsxk.hlju.edu.cn/xsxk/xkjs.xk"#选课的课程页面

        self.executable_path = "C:/chromedriver.exe"#浏览器驱动
        self.driver_name ='chrome'#浏览器名称


    def login(self):
        print("登录")
        self.driver.get(self.URL_Index)
        self.driver.find_element_by_id("xkgl").click()
        self.driver.find_element_by_id("username").send_keys(self.StudentID)
        self.driver.find_element_by_id("password").send_keys(self.Password)


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
        print("进入选课页面")
        # self.driver.get(self.URL_ClassIndex)
        self.driver.find_element_by_class_name("current").click()#选课中心
        js="comeToXkzx(this);"
        self.driver.execute_script(js)
        print("wite")

        self.driver.switch_to_frame("main")
        self.driver.execute_script("comeInQxgxk(this);")#全校公共选课
        # self.driver.find_element_by_id("qxgxkLink").click()

        self.driver.switch_to_frame("qxgxkFrame")
        self.driver.find_element_by_id("qKcxx").clear()
        self.driver.find_element_by_id("qKcxx").send_keys(self.ClassID[:11])
        # sleep(5)
        # count=0
        # while True:
        #     try:
        #         self.driver.find_element_by_id("qKcxx").clear()
        #         self.driver.find_element_by_id("qKcxx").send_keys(self.ClassID)
        #         self.driver.find_element_by_id("qGlct").click()#过滤冲突
        #         self.driver.find_element_by_id("qGlym").click()#过滤已满
        #         break
        #     except:
        #         count+=1
        #         sleep(1)
        #         print("Try again")
        #         if count==10:
        #             break
        # # self.driver.find_element_by_text("查询").click()
        js="queryXkJxb();"
        self.driver.execute_script(js)

        js="xkOper('2018-2019-"+self.ClassID+"')"
        print(js)
        while True:
            self.driver.execute_script(js)

            alert =self.driver.switch_to_alert()
            print(alert.text)
            # sleep(2)
            # alert.dismiss()#取消
            alert.accept()
            try:
                sleep(2)
                alert = self.driver.switch_to_alert()
                print(alert.text)

                if alert.text=="选课成功！":
                    break
                alert.accept()
                sleep(1)
            except:
                sleep(5)
                pass



    def main(self,ClassID):
        self.driver = webdriver.Chrome()  # 打开浏览器
        self.driver.set_window_size(1200, 800)
        self.login()
        self.ClassID=ClassID
        self.start()

if __name__ == '__main__':
    a=AutomaticClassRobbing()
    a.main("1151200201201")