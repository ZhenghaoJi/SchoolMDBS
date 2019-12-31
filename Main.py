import pymysql
from tkinter import *
from tkinter import ttk
import tkinter as tk

database = pymysql.connect('localhost', 'root', 'dingding741', 'test1')


class Startpage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统')
        self.window.geometry('800x600')
        Label(self.window, text='选课系统', width=50, height=3, font=28).pack(pady=100)
        Button(self.window, text='For Students in FDU', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: Stupage(self.window)).pack()
        Button(self.window, text='For Teachers in FDU', fg='white', activebackground='red', activeforeground='white',
               bg='gray', width=30, height=3, font=24, command=lambda: Teacherpage(self.window)).pack()
        Button(self.window, text='Visitor', font=24, fg='white', activebackground='red', bg='gray', width=30, height=3,
               command=lambda: Vistorpage(self.window)).pack()
        Button(self.window, text='For Admin', font=24, fg='white', activebackground='red', bg='gray', width=30,
               height=3, command=lambda: Adminpage(self.window)).pack()
        Label(self.window, text='Author', width=50, height=3, font=28).pack()
        self.window.mainloop()


class Adminpage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统-管理员界面')
        self.window.geometry('800x600')
        Label(self.window, text='管理员登陆', font=24).pack(pady=100)
        Label(self.window, text='管理员登陆账号', font=18).pack()
        self.admin_id = StringVar()
        Entry(self.window, textvariable=self.admin_id).pack()
        Label(self.window, text='管理员登陆密码', font=18).pack()
        self.admin_pw = StringVar()
        Entry(self.window, textvariable=self.admin_pw).pack()
        Button(self.window, text='Sign in', font=24, command=lambda: self.login_admin()).pack()

        Button(self.window, text='ReStart', fg='white', activebackground='red', bg='gray',
               command=lambda: Startpage(self.window)).pack(pady=100)

        self.window.mainloop()

    def login_admin2(self):
        # 假的登陆函数
        AdminManage(self.window, ad_id=self.admin_id)

    def login_admin(self):
        # back to adminpage or go to admin manage page
        cursor = database.cursor()
        sql = "select * from admin_login where adminid='%s'and adminpw='%s'" % (self.admin_id.get(),
                                                                                self.admin_pw.get())

        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            if (results == None):
                print("Wrong password or not exists the id.")
                cursor.close()
                Adminpage(self.window)
            else:
                print("Welcome!")
                cursor.close()
                AdminManage(self.window, ad_id=self.admin_id)
        except:
            print("Something wrong happened.")
            cursor.close()
            Adminpage(self.window)


class AdminManage:
    # we have signed in.
    def __init__(self, parent_window, ad_id):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统-管理员操作界面')
        self.window.geometry('800x600')
        Label(self.window, text='管理员可执行操作', font=24).pack(pady=100)
        Button(self.window, text='学生管理', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: admin_stu(self.window, ad_id)).pack()
        Button(self.window, text='教师管理', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: admin_tea(self.window, ad_id)).pack()
        Button(self.window, text='成绩登陆', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: admin_score(self.window, ad_id)).pack()
        # backpage
        Button(self.window, text='ReStart', fg='white', activebackground='red', bg='gray',
               command=lambda: Startpage(self.window)).pack()
        self.window.mainloop()


class admin_stu:
    def __init__(self, parent_window, ad_id):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title('选课系统-管理员操作界面-学生管理')

        # Here Create buttons and entries
        Label(self.window, text='学号').pack()
        self.msg1 = StringVar()
        Entry(self.window, textvariable=self.msg1).pack()
        Label(self.window, text='姓名').pack()
        self.msg2 = StringVar()
        Entry(self.window, textvariable=self.msg2).pack()
        Label(self.window, text='性别').pack()
        self.msg3 = StringVar()
        Entry(self.window, textvariable=self.msg3).pack()
        Label(self.window, text='籍贯').pack()
        self.msg4 = StringVar()
        Entry(self.window, textvariable=self.msg4).pack()
        Button(self.window, text='增加', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_stu_add()).pack()
        Button(self.window, text='删除', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_stu_del()).pack()
        Button(self.window, text='查询', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_stu_search()).pack()
        self.dataTreeview = ttk.Treeview(self.window, show='headings',
                                         column=('1', '2', '3', '4'))
        self.dataTreeview.column('1', anchor="center")
        self.dataTreeview.column('2', anchor="center")
        self.dataTreeview.column('3', anchor="center")
        self.dataTreeview.column('4', anchor="center")
        self.dataTreeview.heading('1', text='学号')
        self.dataTreeview.heading('2', text='姓名')
        self.dataTreeview.heading('3', text='性别')
        self.dataTreeview.heading('4', text='籍贯')
        self.dataTreeview.pack()
        Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
               command=lambda: AdminManage(self.window, ad_id=ad_id)).pack()

    def admin_stu_add(self):
        cur = database.cursor()
        sql = "INSERT INTO stu_inf VALUE('%s','%s','%s','%s')" % (
            self.msg1.get(), self.msg2.get(), self.msg3.get(), self.msg4.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
            result = cur.fetchall()
        except:
            database.rollback()
        cur.close()

    def admin_stu_del(self):
        cur = database.cursor()
        sql = "DELETE FROM stu_inf WHERE stuid = '%s'" % (self.msg1.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
        except:
            database.rollback()
        cur.close()

    def admin_stu_search(self):
        x = self.dataTreeview.get_children()
        for item in x:
            self.dataTreeview.delete(item)
        # connect the db here
        cur = database.cursor()
        sql = "SELECT * FROM stu_inf "
        cur.execute(sql)
        lst = cur.fetchall()
        for item in lst:
            self.dataTreeview.insert("", 1, text="line1", values=item)
        cur.close()


class admin_tea:
    def __init__(self, parent_window, ad_id):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title('选课系统-管理员操作界面-教师管理')
        # Here Create buttons and entries
        Label(self.window, text='教师号').pack()
        self.msg1 = StringVar()
        Entry(self.window, textvariable=self.msg1).pack()
        Label(self.window, text='姓名').pack()
        self.msg2 = StringVar()
        Entry(self.window, textvariable=self.msg2).pack()
        Label(self.window, text='性别').pack()
        self.msg3 = StringVar()
        Entry(self.window, textvariable=self.msg3).pack()
        Label(self.window, text='院系').pack()
        self.msg4 = StringVar()
        Entry(self.window, textvariable=self.msg4).pack()
        Button(self.window, text='增加', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_tea_add()).pack()
        Button(self.window, text='删除', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_tea_del()).pack()
        Button(self.window, text='查询', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_tea_search()).pack()
        self.dataTreeview = ttk.Treeview(self.window, show='headings',
                                         column=('1', '2', '3', '4'))
        self.dataTreeview.column('1', anchor="center")
        self.dataTreeview.column('2', anchor="center")
        self.dataTreeview.column('3', anchor="center")
        self.dataTreeview.column('4', anchor="center")
        self.dataTreeview.heading('1', text='教师号')
        self.dataTreeview.heading('2', text='姓名')
        self.dataTreeview.heading('3', text='性别')
        self.dataTreeview.heading('4', text='院系')
        self.dataTreeview.pack()
        Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
               command=lambda: AdminManage(self.window, ad_id=ad_id)).pack()

    def admin_tea_add(self):
        cur = database.cursor()
        sql = "INSERT INTO tea_inf VALUE('%s','%s','%s','%s')" % (
            self.msg1.get(), self.msg2.get(), self.msg3.get(), self.msg4.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
            result = cur.fetchall()
        except:
            database.rollback()
        cur.close()

    def admin_tea_del(self):
        cur = database.cursor()
        sql = "DELETE FROM tea_inf WHERE teaid = '%s'" % (self.msg1.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
        except:
            database.rollback()
        cur.close()

    def admin_tea_search(self):
        x = self.dataTreeview.get_children()
        for item in x:
            self.dataTreeview.delete(item)
        # connect the db here
        cur = database.cursor()
        sql = "SELECT * FROM tea_inf "
        cur.execute(sql)
        lst = cur.fetchall()
        for item in lst:
            self.dataTreeview.insert("", 1, text="line1", values=item)
        cur.close()


class admin_score:
    def __init__(self, parent_window, ad_id):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title('选课系统-管理员操作界面-成绩登陆')
        # Here Create buttons and entries
        Label(self.window, text='学号').pack()
        self.msg1 = StringVar()
        Entry(self.window, textvariable=self.msg1).pack()
        Label(self.window, text='课程号').pack()
        self.msg2 = StringVar()
        Entry(self.window, textvariable=self.msg2).pack()
        Label(self.window, text='成绩').pack()
        self.msg3 = StringVar()
        Entry(self.window, textvariable=self.msg3).pack()
        Button(self.window, text='增加成绩', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_score_add()).pack()
        Button(self.window, text='修改成绩', fg='white', activebackground='red', bg='gray',
               command=lambda: self.admin_score_mod()).pack()
        Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
               command=lambda: AdminManage(self.window, ad_id=ad_id)).pack(pady=100)

    def admin_score_add(self):
        cur = database.cursor()
        sql = "INSERT INTO sc VALUE('%s','%s','%s')" % (self.msg2.get(), self.msg1.get(), self.msg3.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
        except:
            database.rollback()
        cur.close()

    def admin_score_mod(self):
        cur = database.cursor()
        sql = "UPDATE sc set grade='%s' WHERE stuid='%s' and classid='%s' " % (
            self.msg3.get(), self.msg1.get(), self.msg2.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
        except:
            database.rollback()
        cur.close()


class Stupage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统-学生界面')
        self.window.geometry('800x600')
        Label(self.window, text='学生登陆', font=24).pack(pady=100)
        Label(self.window, text='学号', font=18).pack()
        self.stu_id = StringVar()
        Entry(self.window, textvariable=self.stu_id).pack()
        Label(self.window, text='密码', font=18).pack()
        self.stu_pw = StringVar()
        Entry(self.window, textvariable=self.stu_pw).pack()
        Button(self.window, text='Sign in', font=24, command=lambda: self.login_admin()).pack()

        Button(self.window, text='ReStart', fg='white', activebackground='red', bg='gray',
               command=lambda: Startpage(self.window)).pack(pady=100)

        self.window.mainloop()

    def login_admin2(self):
        # 假的登陆函数
        StuManage(self.window, stu_id=self.stu_id)

    def login_admin(self):
        # back to adminpage or go to admin manage page

        cursor = database.cursor()
        sql = "select * from stu_login where stuid='%s'and stupw='%s'" % (self.stu_id.get(),
                                                                          self.stu_pw.get())
        print(sql)

        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            if (results == None):
                print("Wrong password or not exists the id.")
                cursor.close()
                Stupage(self.window)
            else:
                print("Welcome!")
                cursor.close()
                StuManage(self.window, stu_id=self.stu_id)
        except:
            print("Something wrong happened.")
            cursor.close()
            Stupage(self.window)


class StuManage:
    # we have signed in.
    def __init__(self, parent_window, stu_id):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统-学生操作界面')
        self.window.geometry('800x600')
        Label(self.window, text='学生可执行操作', font=24).pack(pady=100)
        Button(self.window, text='查询课表', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: stu_consult(self.window, stu_id)).pack()
        Button(self.window, text='查询分数', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: stu_score(self.window, stu_id)).pack()
        # backpage
        Button(self.window, text='ReStart', fg='white', activebackground='red', bg='gray',
               command=lambda: Startpage(self.window)).pack()
        self.window.mainloop()


class stu_consult:
    def __init__(self, parent_window, stu_id):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title('选课系统-学生操作界面-课程查询')
        self.stu_id = stu_id
        # Here Create buttons and entries
        Label(self.window, text='课程号').pack()
        self.msg1 = StringVar()
        Entry(self.window, textvariable=self.msg1).pack()
        Button(self.window, text='增加', fg='white', activebackground='red', bg='gray',
               command=lambda: self.stu_add()).pack()
        Button(self.window, text='删除', fg='white', activebackground='red', bg='gray',
               command=lambda: self.stu_del()).pack()
        Button(self.window, text='查询已选课程', fg='white', activebackground='red', bg='gray',
               command=lambda: self.stu_search()).pack()
        self.dataTreeview = ttk.Treeview(self.window, show='headings',
                                         column=('1', '2', '3', '4'))
        self.dataTreeview.column('1', anchor="center")
        self.dataTreeview.column('2', anchor="center")
        self.dataTreeview.column('3', anchor="center")
        self.dataTreeview.column('4', anchor="center")
        self.dataTreeview.heading('1', text='课程号')
        self.dataTreeview.heading('2', text='课程名')
        self.dataTreeview.heading('3', text='授课老师')
        self.dataTreeview.heading('4', text='考试时间')
        self.dataTreeview.pack()
        Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
               command=lambda: StuManage(self.window, stu_id)).pack()

    def stu_add(self):
        cur = database.cursor()
        sql = "INSERT INTO sc VALUES('%s','%s','')" % (self.msg1.get(), self.stu_id.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
            result = cur.fetchall()
        except:
            database.rollback()
        cur.close()

    def stu_del(self):
        cur = database.cursor()
        sql = "DELETE FROM sc WHERE classid='%s' and stuid = '%s'" % (self.msg1.get(), self.stu_id.get())
        print(sql)
        try:
            cur.execute(sql)
            database.commit()
        except:
            database.rollback()
        cur.close()

    def stu_search(self):
        x = self.dataTreeview.get_children()
        for item in x:
            self.dataTreeview.delete(item)
        # connect the db here
        cur = database.cursor()
        sql = "SELECT sc.classid,class_inf.classname,tea_inf.teaname,class_inf.examtime FROM sc,class_inf,tea_inf where class_inf.teaid=tea_inf.teaid and class_inf.classid=sc.classid and sc.stuid = '%s'" % (
            self.stu_id.get())
        print(sql)
        cur.execute(sql)
        lst = cur.fetchall()
        for item in lst:
            self.dataTreeview.insert("", 1, text="line1", values=item)
        cur.close()

class stu_score:
    def __init__(self, parent_window, stu_id):
        parent_window.destroy()
        self.stu_id = stu_id
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title('选课系统-学生操作界面-成绩查询')
        # Here Create buttons and entries
        self.dataTreeview = ttk.Treeview(self.window, show='headings',
                                         column=('1', '2', '3'))
        self.dataTreeview.column('1', anchor="center")
        self.dataTreeview.column('2', anchor="center")
        self.dataTreeview.column('3', anchor="center")
        self.dataTreeview.heading('1', text='课程号')
        self.dataTreeview.heading('2', text='课程名')
        self.dataTreeview.heading('3', text='成绩')
        self.dataTreeview.pack()

        Button(self.window, text='查询成绩', fg='white', activebackground='red', bg='gray',
               command=lambda: self.stu_score()).pack()
        Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
               command=lambda: StuManage(self.window, stu_id)).pack()

    def stu_score(self):
        x = self.dataTreeview.get_children()
        for item in x:
            self.dataTreeview.delete(item)
        # connect the db here
        cur = database.cursor()
        sql = "select sc.classid,class_inf.classname,sc.grade from sc,class_inf where class_inf.classid=sc.classid and sc.stuid = '%s'" % (self.stu_id.get())
        cur.execute(sql)
        lst = cur.fetchall()
        for item in lst:
            self.dataTreeview.insert("", 1, text="line1", values=item)
        cur.close()


class Teacherpage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统-教师界面')
        self.window.geometry('800x600')
        Label(self.window, text='教师登陆', font=24).pack(pady=100)
        Label(self.window, text='教师登陆账号', font=18).pack()
        self.admin_id = Entry(self.window).pack()
        Label(self.window, text='教师登陆密码', font=18).pack()
        self.admin_pw = Entry(self.window).pack()
        Button(self.window, text='Sign in', font=24, command=lambda: self.login_admin2()).pack()

        Button(self.window, text='ReStart', fg='white', activebackground='red', bg='gray',
               command=lambda: Startpage(self.window)).pack(pady=100)

        self.window.mainloop()

    def login_admin2(self):
        # 假的登陆函数
        TeaManage(self.window, tea_id=self.admin_id)

    def login_admin(self):
        # back to adminpage or go to admin manage page
        db = pymysql.connect('localhost', 'root', '', charset='utf8', port=3306)
        cursor = db.cursor()
        sql = "select * from admin_login where stuid='%s'and stupw='%s'" % (self.admin_id.get(),
                                                                            self.admin_pw.get())

        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            if (results == None):
                print("Wrong password or not exists the id.")
                db.close()
                Teacherpage(self.window)
            else:
                print("Welcome!")
                db.close()
                TeaManage(self.window, ad_id=self.admin_id)
        except:
            print("Something wrong happened.")
            db.close()
            Teacherpage(self.window)


class TeaManage:
    # we have signed in.
    def __init__(self, parent_window, tea_id):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统-教师操作界面')
        self.window.geometry('800x600')
        Label(self.window, text='教师可执行操作', font=24).pack(pady=100)
        Button(self.window, text='查询课程信息', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: self.stu_consult()).pack()
        Button(self.window, text='增加课程', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: self.stu_add()).pack()
        Button(self.window, text='取消授课', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: self.stu_score()).pack()
        # backpage
        Button(self.window, text='ReStart', fg='white', activebackground='red', bg='gray',
               command=lambda: Startpage(self.window)).pack()
        self.window.mainloop()

        def stu_consult(self):
            Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
                   command=lambda: AdminManage(self.window, ad_id=ad_id)).pack(pady=100)

        def stu_add(self):
            Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
                   command=lambda: AdminManage(self.window, ad_id=ad_id)).pack(pady=100)

        def stu_score(self):
            Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
                   command=lambda: AdminManage(self.window, ad_id=ad_id)).pack(pady=100)


class Vistorpage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('选课系统-游客界面')
        self.window.geometry('800x600')
        Label(self.window, text='Welcome to FDU!', font=24).pack(pady=100)
        Button(self.window, text='查询课表', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: self.stu_consult()).pack()
        Button(self.window, text='查询教授', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: self.stu_add()).pack()
        Button(self.window, text='查询院系', fg='white', activebackground='red', bg='gray', width=30,
               height=3, font=24, command=lambda: self.stu_score()).pack()

        Button(self.window, text='ReStart', fg='white', activebackground='red', bg='gray',
               command=lambda: Startpage(self.window)).pack()

        self.window.mainloop()

        def stu_consult(self):
            Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
                   command=lambda: AdminManage(self.window, ad_id=ad_id)).pack(pady=100)

        def stu_add(self):
            Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
                   command=lambda: AdminManage(self.window, ad_id=ad_id)).pack(pady=100)

        def stu_score(self):
            Button(self.window, text='ReManagePage', fg='white', activebackground='red', bg='gray',
                   command=lambda: AdminManage(self.window, ad_id=ad_id)).pack(pady=100)


if __name__ == '__main__':
    window = tk.Tk()
    Startpage(window)
