import xlrd                                                        #导入xlrd模块
import xlwt
from xlutils.copy import copy
import pandas as pd

class ExcelData(object):
    def __init__(self,data_path,sheetname='Sheet1'):
        self.data_path = data_path                                 # excle表格路径，需传入绝对路径
        self.sheetname = sheetname                                 # excle表格内sheet名
        # self.data = xlrd.open_workbook(self.data_path)             # 打开excel表格
        # self.table = self.data.sheet_by_name(self.sheetname)       # 切换到相应sheet
        # self.keys = self.table.row_values(0)                       # 第一行作为key值
        # self.rowNum = self.table.nrows                             # 获取表格行数
        # self.colNum = self.table.ncols                             # 获取表格列数
        # print(self.rowNum)
        # print(self.colNum)

    def read_excel(self):
        self.data = xlrd.open_workbook(self.data_path)             # 打开excel表格
        self.table = self.data.sheet_by_name(self.sheetname)       # 切换到相应sheet
        self.keys = self.table.row_values(0)                       # 第一行作为key值
        self.rowNum = self.table.nrows                             # 获取表格行数
        self.colNum = self.table.ncols                             # 获取表格列数

        if self.rowNum<2:
            print("excle内数据行数小于2")
        else:
            L = []                                                 #列表L存放取出的数据
            for i in range(1,self.rowNum):                         #从第二行（数据行）开始取数据
                sheet_data = {}                                    #定义一个字典用来存放对应数据
                for j in range(self.colNum):                       #j对应列值
                    sheet_data[self.keys[j]] = self.table.row_values(i)[j]    #把第i行第j列的值取出赋给第j列的键值，构成字典
                L.append(sheet_data)                               #一行值取完之后（一个字典），追加到L列表中
            #print(type(L))
            return L

    def read_excel_last_row(self):
        self.data = xlrd.open_workbook(self.data_path)             # 打开excel表格
        self.table = self.data.sheet_by_name(self.sheetname)       # 切换到相应sheet
        self.keys = self.table.row_values(0)                       # 第一行作为key值
        self.rowNum = self.table.nrows                             # 获取表格行数
        self.colNum = self.table.ncols                             # 获取表格列数

        if self.rowNum<2:
            print("excle内数据行数小于2")
        else: 
            i = self.rowNum - 1                                              #列表L存放取出的数据
            sheet_data = {}                                    #定义一个字典用来存放对应数据
            for j in range(self.colNum):                       #j对应列值
                sheet_data[self.keys[j]] = self.table.row_values(i)[j]    #把第i行第j列的值取出赋给第j列的键值，构成字典                             #一行值取完之后（一个字典），追加到L列表中
            #print(type(L))
            return sheet_data

    def write_excel(self, data):
        lis=data
        listkeys = lis[0].keys()  # 找到所有的键值
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet(self.sheetname)
        number = 0
 
        for key in list(listkeys):  # 键值需要强制转换成list类型
            sheet.write(0, number, key)
            number = number + 1
 
        x = 1
        for one_dict in lis:  # 遍历列表中所有的字典
            y = 0
            for key in list(listkeys):  # 找到所有键值对应的数据
                sheet.write(x, y, one_dict[key])  # 存入
                # if (key == 'url'):
                #     sheet.write(x, y, ('=HYPERLINK("%s","%s")' % one_dict[key], one_dict[key]))  # 存入
                # else:
                #     sheet.write(x, y, one_dict[key])  # 存入
                y = y + 1
            x = x + 1
 
        wbk.save(self.data_path[:-3]+'xls')#保存文件

    def write_excel_xls_append(self, data):
        workbook = xlrd.open_workbook(self.data_path)  # 打开工作簿
        worksheet = workbook.sheet_by_name(self.sheetname)  # 获取工作簿中所有表格中的的第一个表格

        keys = worksheet.row_values(0)                       # 第一行作为key值
        cols = worksheet.col_values(0) # 获取第一列内容

        rows = worksheet.nrows  # 获取表格中已存在的数据的行数
        if (rows < 2):
            print("excle内数据行数小于2")
            return 
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        # new_worksheet = new_workbook.sheet_by_name(self.sheetname)  # 获取转化后工作簿中的第一个表格

        # 如果当天日期的值重复插入，用最新的值替换前面的值
        if (cols[-1] == data['日期']):
            x = rows - 1
        else:
            x = rows

        y = 0
        for key in list(keys):  # 找到所有键值对应的数据
            new_worksheet.write(x, y, data[key])  # 存入
            y = y + 1
        # for i in range(0, index):
        #     for j in range(0, len(value[i])):
        #         new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
        new_workbook.save(self.data_path)  # 保存工作簿
        # print("xls格式表格【追加】写入数据成功！")

    def get_column_data(self, column_name):
        workbook = xlrd.open_workbook(self.data_path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        cols = worksheet.col_values(0) # 获取第一列内容
        print(cols)


if __name__ == '__main__':
    data_path = "D:\\pythonData\\000001.xls"  #文件的绝对路径
    get_data = ExcelData(data_path)                       #定义get_data对象, sheet名称默认Sheet1
    # print(get_data.read_excel())
    get_data.get_column_data('日期')
