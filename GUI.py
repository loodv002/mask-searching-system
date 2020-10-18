import tkinter as tk
import requests
from tkinter import ttk
from tkinter import scrolledtext

win = tk.Tk()

win.title('MASK GUI')

win.geometry('800x400')

temp = tk.Frame(win)

maskURL = 'https://data.nhi.gov.tw/resource/mask/maskdata.csv'
ID = []#'2332120011'
fullNum = ['０','１','２','３','４','５','６','７','８','９']

#ID text

class Button(object):
    def __init__(self, frame, text, bg, width, height, row, column, cmd):
        self.button = tk.Button(frame, text = text, fg = 'white')
        
        self.button.config(bg = bg)
        self.button.config(width = width, height = height)
        self.button.config(command = cmd)
        self.button.grid(row = row, column = column)

class listButton(object):
    def __init__(self, frame, text, bg, width, height, row, column, index, BTNtype):
        self.button = tk.Button(frame, text = text, fg = 'white')
        
        self.button.config(bg = bg)
        self.button.config(width = width, height = height)
        
        if BTNtype == 0:
            self.button.config(command = self.delID)
        elif BTNtype == 1:
            self.button.config(command = self.addID)
            
        self.button.grid(row = row, column = column)
        
        self.index = index
        self.frame = frame

    def delID(self):
        ID.pop(self.index)
        self.frame.destroy()
        show()

    def addID(self):
        if searchTemp[self.index] not in ID:
            ID.append(searchTemp[self.index])

class Label(object):
    def __init__(self, frame, text, row, column, rowspan, columnspan):
        self.label = tk.Label(frame, text = text)
        
        self.label.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)

class Combobox(object):
    def __init__(self, frame, value, row, column):
        self.combobox = ttk.Combobox(frame, values = value, state = 'readonly')

        self.combobox.grid(row = row, column = column)

class Entry(object):
    def __init__(self, frame, row, column, columnspan):
        self.entry = tk.Entry(frame)
        
        self.entry.grid(row = row, column = column, columnspan = columnspan)

class show(object):
    def __init__(self):
        self.frame = tk.Frame(win)
        
        self.showBTN = Button(self.frame, '顯示資料', 'blue', 10, 3, 0, 0, None)
        self.searchBTN = Button(self.frame, '搜尋藥局', 'skyblue', 10, 3, 0, 1, self.search)
        self.updateBTN = Button(self.frame, '更新資料', 'skyblue', 10, 3, 0, 2, self.update)
        
        self.frame.pack()

        self.showData()

    def showData(self):
        if len(ID) == 0:
            Label(self.frame, '請至\"搜尋藥局\"添加資料', 1, 0, 1, 3)
        
        for i in range(len(ID)):
            for j in range(len(data)):
                if ID[i] == data[j][0]:
                    Label(self.frame, data[j][1] + ' ' + data[j][2] + ' ' + data[j][3] + ' 成人:' + data[j][4] + ' 兒童:' + data[j][5], i + 1, 0, 1, 3)
                    break
                
                if j == len(data) - 1:
                    Label(self.frame, data[i][0] + ' 離線', i + 1, 0, 1, 3)

            listButton(self.frame, '刪除', 'green', 3, 1, i + 1, 4, i, 0)

    def search(self):
        self.frame.destroy()
        search()

    def update(self):
        self.frame.destroy()
        update()

class search(object):
    def __init__(self):
        self.frame = tk.Frame(win)
        
        self.showBTN = Button(self.frame, '顯示資料', 'skyblue', 10, 3, 0, 0, self.show)
        self.searchBTN = Button(self.frame, '搜尋藥局', 'blue', 10, 3, 0, 1, None)
        self.updateBTN = Button(self.frame, '更新資料', 'skyblue', 10, 3, 0, 2, self.update)

        self.searchType = Combobox(self.frame, ['用藥局名稱查找', '用藥局電話查找', '用藥局地址查找'], 1, 0)
        self.searchType.combobox.current(0)

        self.enterEntry = Entry(self.frame, 1, 1, 3)
        
        self.enterBTN = Button(self.frame, '搜尋', 'gray', 3, 1, 1, 4, self.gainData)

        self.frame.pack()

    def gainData(self):
        self.ST = self.searchType.combobox.current()
        self.E = self.enterEntry.entry.get()

        if self.E != '':
            self.reload()
    
    def searchData(self, ST, E):
        global searchTemp
        searchTemp = []
        self.ST = ST
        self.E = E

        
        if self.ST == 0:
            name = self.E

            for i in range(len(data)):
                if similar(name, data[i][1]):
                    searchTemp.append(data[i][0])
            
        elif self.ST == 1:
            num = self.E
            num = num.replace('(', '')
            num = num.replace(')', '')
            num = num.replace('-', '')
            num = num.replace(' ', '')

            for i in range(len(data)):
                temp = data[i][3]
                temp = temp.replace('(', '')
                temp = temp.replace(')', '')

                if num in temp:
                    searchTemp.append(data[i][0])
                
        else:
            address = self.E
            
            for i in range(len(address)):
                if address[i].isdigit():
                    address = address[:i] + fullNum[int(address[i])] + address[i + 1:]

            for i in range(len(data)):
                if similar(address, data[i][2]):
                    searchTemp.append(data[i][0])

        if len(searchTemp) == 0:
            Label(self.frame, '查無結果', 2, 0, 1, 3)
        else:
            self.pageCombobox = Combobox(self.frame, ['第' + str(i) + '頁' for i in range(1, (len(searchTemp) - 1) // 10 + 2)], 2, 0)
            self.pageCombobox.combobox.current(0)
            self.pageBTN = Button(self.frame, 'go', 'gray', 3, 1, 2, 1, self.showPage)
            self.pageFrame = tk.Frame(self.frame, width = 860, height = 300)
            
            self.showPage()
    
    def showPage(self):
        self.pageFrame.destroy()
        
        self.pageFrame = tk.Frame(self.frame, width = 860, height = 300)

        for i in range(self.pageCombobox.combobox.current() * 10, self.pageCombobox.combobox.current() * 10 + 10):
            if i < len(searchTemp):
                for j in range(len(data)):
                    if data[j][0] == searchTemp[i]:
                        Label(self.pageFrame, data[j][1] + ' ' + data[j][2] + ' ' + data[j][3], i % 10, 0, 1, 3)

                        listButton(self.pageFrame, '加入主頁', 'green', 6, 1, i % 10, 4, i, 1)

        self.pageFrame.grid(row = 3, column = 0, columnspan = 4)

                        
        
    def show(self):
        self.frame.destroy()
        show()

    def update(self):
        self.frame.destroy()
        update()

    def reload(self):
        self.frame.destroy()
        search().searchData(self.ST, self.E)

class update(object):
    def __init__(self):
        self.frame = tk.Frame(win)
        
        self.frame.pack()
            
        updateOperation()

        self.reload()

    def show(self):
        self.frame.destroy()
        show()

    def search(self):
        self.frame.destroy()
        search()

    def reload(self):
        self.frame.destroy()
        
        self.frame = tk.Frame(win)
        
        self.showBTN = Button(self.frame, '顯示資料', 'skyblue', 10, 3, 0, 0, self.show)
        self.searchBTN = Button(self.frame, '搜尋藥局', 'skyblue', 10, 3, 0, 1, self.search)
        self.updateBTN = Button(self.frame, '更新資料', 'blue', 10, 3, 0, 2, None)
        completeTEXT = Label(self.frame, '更新成功', 1, 1, 1, 1)
        
        self.frame.pack()


def updateOperation():
    global data

    r = requests.get(maskURL)
    data = r.text.split('\n')[1:-1]

    for i in range(len(data)):
        data[i] = data[i].split(',')

def similar(a, b):
    count = 0

    for i in a:
        if i in b:
            count += 1

    if count / len(a) >= 0.85:
        return True
    return False


updateOperation()
show()

win.mainloop()
