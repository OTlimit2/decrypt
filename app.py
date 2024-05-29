import os
import socket
import xlrd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from vigenere_cipher import VigenereCipher
from key_repo import KeyRepo


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.init_vars()
        self.style_config()
        self.create_widgets()

    def init_vars(self):
        self.file_1 = tk.StringVar()
        self.file_1.set("")
        self.infile_1 = tk.StringVar()
        self.infile_1.set("./数据模板/国标点模板.xls")
        self.infile_2 = tk.StringVar()
        self.infile_2.set("./数据模板/土壤模板.xlsx")
        self.infile_3 = tk.StringVar()
        self.infile_3.set("")
        self.infile_4 = tk.StringVar()
        self.infile_4.set("")
        self.infile_5 = tk.StringVar()
        self.infile_5.set("")

        self.keyrepo = tk.StringVar()
        self.keyrepo.set("./keys_vigenere")
        self.outdir = tk.StringVar()
        self.outdir.set("./output")

    def style_config(self):
        style = ttk.Style()
        style.configure("P.TButton", relief="flat", padding=5,
                        background="#ccc", font=("Microsoft YaHei UI", 12))
        style.configure("H.TLabel", relief="flat",
                        font=("Microsoft YaHei UI Bold", 20))
        style.configure("P.TLabel", relief="flat",
                        font=("Microsoft YaHei UI Bold", 14))
        style.configure("C.TLabel", relief="flat",
                        font=("Microsoft YaHfei UI", 10))

    def create_widgets(self):

        # ROW 1
        self.header = ttk.Label(self, style="H.TLabel")
        self.header["text"] = "农产品产地土壤环境监测数据解码程序"  # 2019.07.05改动
        self.header.grid(row=0, columnspan=3, padx=10, pady=40)

        # ROW 2
        self.choose_infile_1_lbl = ttk.Label(self, style="P.TLabel")
        self.choose_infile_1_lbl["text"] = "采样信息:"  # 2019.07.05改动
        self.choose_infile_1_lbl.grid(row=1, pady=10, sticky='e')

        self.choose_infile_1_entry = ttk.Entry(self)
        self.choose_infile_1_entry["textvariable"] = self.infile_1
        self.choose_infile_1_entry["width"] = 30
        self.choose_infile_1_entry["font"] = ("Microsoft YaHei UI", 12)
        self.choose_infile_1_entry.grid(row=1, column=1, padx=20, pady=10)

        self.choose_infile_1_btn = ttk.Button(self, style="P.TButton")
        self.choose_infile_1_btn["text"] = "选择文件"
        self.choose_infile_1_btn["command"] = self.choose_infile_1
        self.choose_infile_1_btn.grid(row=1, column=2, padx=10)

        # ROW 3
        self.choose_infile_2_lbl = ttk.Label(self, style="P.TLabel")
        self.choose_infile_2_lbl["text"] = "土壤重金属检测结果:"         # 2020.07.05改动
        self.choose_infile_2_lbl.grid(row=2, pady=10, sticky='e')

        self.choose_infile_2_entry = ttk.Entry(self)
        self.choose_infile_2_entry["textvariable"] = self.infile_2
        self.choose_infile_2_entry["width"] = 30
        self.choose_infile_2_entry["font"] = ("Microsoft YaHei UI", 12)
        self.choose_infile_2_entry.grid(row=2, column=1, padx=20, pady=10)

        self.choose_infile_2_btn = ttk.Button(self, style="P.TButton")
        self.choose_infile_2_btn["text"] = "选择文件"
        self.choose_infile_2_btn["command"] = self.choose_infile_2
        self.choose_infile_2_btn.grid(row=2, column=2, padx=10)

        # ROW 4
        self.choose_infile_4_lbl = ttk.Label(self, style="P.TLabel")
        self.choose_infile_4_lbl["text"] = "土壤农药检测结果:"  # 2019.07.28改动
        self.choose_infile_4_lbl.grid(row=3, pady=10, sticky='e')

        self.choose_infile_4_entry = ttk.Entry(self)
        self.choose_infile_4_entry["textvariable"] = self.infile_4
        self.choose_infile_4_entry["width"] = 30
        self.choose_infile_4_entry["font"] = ("Microsoft YaHei UI", 12)
        self.choose_infile_4_entry.grid(row=3, column=1, padx=20, pady=10)

        self.choose_infile_4_btn = ttk.Button(self, style="P.TButton")
        self.choose_infile_4_btn["text"] = "选择文件"
        self.choose_infile_4_btn["command"] = self.choose_infile_4
        self.choose_infile_4_btn.grid(row=3, column=2, padx=10)
        
        # ROW 5
        self.choose_infile_5_lbl = ttk.Label(self, style="P.TLabel")
        self.choose_infile_5_lbl["text"] = "土壤理化检测结果:"  # 2019.07.28改动
        self.choose_infile_5_lbl.grid(row=4, pady=10, sticky='e')

        self.choose_infile_5_entry = ttk.Entry(self)
        self.choose_infile_5_entry["textvariable"] = self.infile_5
        self.choose_infile_5_entry["width"] = 30
        self.choose_infile_5_entry["font"] = ("Microsoft YaHei UI", 12)
        self.choose_infile_5_entry.grid(row=4, column=1, padx=20, pady=10)

        self.choose_infile_5_btn = ttk.Button(self, style="P.TButton")
        self.choose_infile_5_btn["text"] = "选择文件"
        self.choose_infile_5_btn["command"] = self.choose_infile_5
        self.choose_infile_5_btn.grid(row=4, column=2, padx=10)

        # ROW 6
        self.choose_infile_3_lbl = ttk.Label(self, style="P.TLabel")
        self.choose_infile_3_lbl["text"] = "农产品样品检测结果:"  # 2019.07.28改动
        self.choose_infile_3_lbl.grid(row=5, pady=10, sticky='e')

        self.choose_infile_3_entry = ttk.Entry(self)
        self.choose_infile_3_entry["textvariable"] = self.infile_3
        self.choose_infile_3_entry["width"] = 30
        self.choose_infile_3_entry["font"] = ("Microsoft YaHei UI", 12)
        self.choose_infile_3_entry.grid(row=5, column=1, padx=20, pady=10)

        self.choose_infile_3_btn = ttk.Button(self, style="P.TButton")
        self.choose_infile_3_btn["text"] = "选择文件"
        self.choose_infile_3_btn["command"] = self.choose_infile_3
        self.choose_infile_3_btn.grid(row=5, column=2, padx=10)

        # 空一行，便于区分
        self.choose_infile_3_lbl = ttk.Label(self, style="P.TLabel")
        self.choose_infile_3_lbl["text"] = "    "  # 2019.07.28改动
        self.choose_infile_3_lbl.grid(row=6, pady=1, sticky='e')
        
        # ROW 7
        self.choose_key_btn = ttk.Label(self, style="P.TLabel")
        self.choose_key_btn["text"] = "密钥库:"
        self.choose_key_btn.grid(row=7, pady=10, sticky='e')

        self.choose_key_entry = ttk.Entry(self)
        self.choose_key_entry["textvariable"] = self.keyrepo
        self.choose_key_entry["width"] = 30
        self.choose_key_entry["font"] = ("Microsoft YaHei UI", 12)
        self.choose_key_entry.grid(row=7, column=1, padx=20, pady=10)

        self.choose_keypath_btn = ttk.Button(self, style="P.TButton")
        self.choose_keypath_btn["text"] = "选择文件夹"
        self.choose_keypath_btn["command"] = self.choose_keyrepo
        self.choose_keypath_btn.grid(row=7, column=2, padx=10)

        # ROW 8
        self.choose_outdir_lbl = ttk.Label(self, style="P.TLabel")
        self.choose_outdir_lbl["text"] = "输出路径:"  # 2019.07.05改动
        self.choose_outdir_lbl.grid(row=8, pady=10, sticky='e')

        self.choose_outdir_entry = ttk.Entry(self)
        self.choose_outdir_entry["textvariable"] = self.outdir
        self.choose_outdir_entry["width"] = 30
        self.choose_outdir_entry["font"] = ("Microsoft YaHei UI", 12)
        self.choose_outdir_entry.grid(row=8, column=1, padx=20, pady=10)

        self.choose_outdir_btn = ttk.Button(self, style="P.TButton")
        self.choose_outdir_btn["text"] = "选择文件夹"
        self.choose_outdir_btn["command"] = self.choose_outdir
        self.choose_outdir_btn.grid(row=8, column=2, padx=10)

        # ROW 9
        self.keygen_btn = ttk.Button(self, style="P.TButton")
        self.keygen_btn["text"] = "生成密钥库"
        self.keygen_btn["command"] = self.keygen
        self.keygen_btn.grid(row=9, column=0, padx=10, pady=10)

        self.decrypt_btn = ttk.Button(self, style="P.TButton")
        self.decrypt_btn["text"] = "解码合并"
        self.decrypt_btn["command"] = self.decrypt
        self.decrypt_btn.grid(row=9, column=2, padx=10, pady=10)

        # ROW 10
        self.comment_lbl = ttk.Label(self, style="C.TLabel")
        self.comment_lbl["text"] = "· 生成的密钥库位于应用所在路径下的keys文件夹，若存在同名文件夹，请做好备份和删除\n"  \
                                   "· 若只合并部分文件，请正确选择对应文件\n" \
                                   "· 输出文件位于输出文件夹下，命名为 采样+所选择文件名称、合并_5"
        self.comment_lbl.grid(row=10, columnspan=2, sticky='s')

    def decrypt(self):
        flag = isNetOK()  # 2019.07.08改动，添加是否断网判断逻辑
        if flag == True:
            messagebox.showerror('错误', '请断网后运行！')
            return

        try:
            self._cipher = VigenereCipher()
            ifname1 = self.infile_1.get()
            ifname2 = self.infile_2.get()
            ifname3 = self.infile_3.get()
            ifname4 = self.infile_4.get()
            ifname5 = self.infile_5.get()

            if not ifname1:
                messagebox.showerror('错误', '采样信息不能为空')
                return
            if not ifname2 and not ifname3 and not ifname4 and not ifname5:
                messagebox.showerror('错误', '土壤或农产品信息不能全为空')
                return
            
            # 文件合并逻辑
            self._cipher.decrypt_merge_model(ifname1, ifname2, ifname3 , ifname4 , ifname5 , self.outdir.get())
            
        except Exception as e:
            messagebox.showerror('错误', str(e))
        else:
            messagebox.showinfo('消息', '解码成功!')

    def keygen(self):
        flag = isNetOK()  # 2019.07.08改动，添加是否断网判断逻辑
        if flag == True:
            messagebox.showerror('错误', '请断网后运行！')
            return

        try:
            if os.path.exists('./keys'):
                messagebox.showinfo('消息', '当前路径已存在keys文件夹，请删除后重试')
                return

            kr = KeyRepo('./keys')
            kr.clear()
            kr.gen_vigenere()
        except Exception as e:
            messagebox.showerror('错误', str(e))
        else:
            messagebox.showinfo('消息', '生成密钥库成功')


    def choose_infile_1(self):
        self.infile_1.set(filedialog.askopenfilename(initialdir='./'))

    # 土壤重金属文件匹配
    def choose_infile_2(self):
        str = filedialog.askopenfilename(initialdir='./')
        if headermatch(str, '有机质'):
            self.infile_2.set(str)
        else:
            messagebox.showerror('错误', '请选择土壤重金属文件')
            return

    # 农产品文件匹配
    def choose_infile_3(self):
        str = filedialog.askopenfilename(initialdir='./')
        if headermatch(str, '农产品Hg'):
            self.infile_3.set(str)
        else:
            messagebox.showerror('错误', '请选择农产品文件')
            return
    
    # 土壤农药文件匹配
    def choose_infile_4(self):
        str = filedialog.askopenfilename(initialdir='./')
        if headermatch(str, '三环唑'):
            self.infile_4.set(str)
        else:
            messagebox.showerror('错误', '请选择土壤农药文件')
            return
    
    # 土壤理化文件匹配
    def choose_infile_5(self):
        str = filedialog.askopenfilename(initialdir='./')
        if headermatch(str, '阳离子交换量'):
            self.infile_5.set(str)
        else:
            messagebox.showerror('错误', '请选择土壤理化文件')
            return

    def choose_keyrepo(self):
        self.keyrepo.set(filedialog.askdirectory(initialdir='./'))

    def choose_outdir(self):
        self.outdir.set(filedialog.askdirectory(initialdir='./'))


# 2019.07.08添加，判断是否连网
def isNetOK():
    s = socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(('www.baidu.com', 443))
        if status == 0:
            s.close()
            return True
        else:
            return False
    except:
        return False


# 2019.7.29日添加，字符串模糊匹配
def fuzzymatch(str, key):
    if not str:
        return True
    result = key in str
    return result


# 2019.9.3  读取Excel表头，并且匹配
def headermatch(str, key):
    if not str:
        return True
    table = xlrd.open_workbook(str).sheets()[0]
    header = table.row_values(0)[1:]  # 从1开始，省掉了“二次转码”一列
    return fuzzymatch(header, key)


root = tk.Tk()
flag = isNetOK()
if flag == True:
    root.withdraw()
    messagebox.showerror('错误', '请断网后运行！')
    os._exit()
else:
    root.title("农产品产地土壤环境监测数据解码程序")  # 2019.07.05改动
    root.geometry("850x650")
    app = Application(master=root)
    app.mainloop() 
