from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import *
import sqlite3

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

class classinfo():
    __doc__ = "更新课程信息"

    def __init__(self):
        self.getInfo()
        self.StartStr=""
        for i in self.ClassIDs:
            self.StartStr=str(self.StartStr)+str(i)+str('\n')

    def getInfo(self):
        self.ClassIDs = []
        sql = "select * from ClassList"
        re = executeSQL(sql)
        for i in re:
            self.ClassIDs.append(i[0])

    def start(self):
        self.root=Tk()
        self.root.title="课程ID号管理"

        self.e1 = Text(self.root,width=25,height=30)
        self.e1.insert(INSERT,self.StartStr)
        # self.e1.insert(END)
        self.e1.grid(row=0, column=0, sticky=N)

        bl = Button(self.root, text="修改", command=self.change)
        bl.grid(row=1, column=0, stick=N)
        self.root.mainloop()


        self.root.mainloop()

    def change(self):
        s1=str(self.e1.get(1.0,END))
        s1= s1.split("\n")
        # s1.remove("")
        for i in s1:
            print(i.__len__())
            if i.__len__()<13:
                s1.remove(i)
        print(s1)
        executeSQL("delete from ClassList")
        sql='insert into "ClassList" values (?)'
        for i in s1:
            try:
                para=(i,)
                executeSQL(sql,para)
            except:
                pass
        a = tkinter.messagebox.showinfo(title="更新结果", message="更新完成！")



class userinfo():
     __doc__ = "更改用户们密码"
     def __init__(self):
         self.getInfo()
         pass

     def getInfo(self):#获取信息
         sql="select valuse from setting where name='studentID'"
         self.Student=self.crypt(executeSQL(sql)[0][0])

         sql='select valuse from setting where name="password"'
         self.Password=self.crypt(executeSQL(sql)[0][0])

     def crypt(self,source):#加密解密
         self.key="AutomaticClassRobbing"
         from itertools import cycle
         result = ''
         temp = cycle(self.key)
         for ch in source:
             result = result + chr(ord(ch) ^ ord(next(temp)))
         return result

     def start(self):#初始化窗口
         self.root = Tk()
         self.root.title="用户登录信息数据"

         for j in range(8):
             for i in range(9):
                 l = Label(self.root, text="          ")
                 l.grid(row=j, column=i, sticky=W)
         l = Label(self.root, text="user:")
         l.grid(row=2, column=3, sticky=W)


         self.e1 = Entry(self.root)
         self.e1.insert(END,self.Student)
         self.e1.grid(row=2, column=4, sticky=E)

         l = Label(self.root, text="pwd:")
         l.grid(row=3, column=3, sticky=W)

         self.e2 = Entry(self.root)
         self.e2.insert(END,self.Password)
         self.e2.grid(row=3, column=4, sticky=E)

         bl = Button(self.root, text="修改", command=self.change)
         bl.grid(row=5, column=4, stick=N)
         self.root.mainloop()

     def change(self):#修改信息
         Student=self.e1.get()
         Password=self.e2.get()


         if Student.__len__()!=8 or Password.__len__()==0:
             a = tkinter.messagebox.showerror(title="更新结果", message="请输入正确值！")

         else:
             sql='update setting set valuse=(?) where name="studentID"'
             para=(self.crypt(Student),)
             executeSQL(sql,para)

             sql = 'update setting set valuse=(?) where name="password"'
             para = (self.crypt(Password),)
             executeSQL(sql, para)

             a = tkinter.messagebox.showinfo(title="更新结果",message="更新完成！")
             self.root.destroy()

def StartUserinfo():
    temp=userinfo()
    temp.start()

def Startclassinfo():
    temp=classinfo()
    temp.start()
    pass

root=Tk()
root.title="黑龙江大学抢课数据管理平台"


for j in range(6):
    for i in range(9):
        l = Label(root, text="          ")
        l.grid(row=j, column=i, sticky=W)

b_userinfo=Button(root,text="修改用户登录信息",command=StartUserinfo)
b_userinfo.grid(row=2,column=4,stick=N)

b_classiinfo=Button(root,text="修改需要修改的课程",command=Startclassinfo)
b_classiinfo.grid(row=3,column=4,stick=N)


root.mainloop()
