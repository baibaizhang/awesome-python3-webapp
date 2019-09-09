import xlrd                                                        #导入xlrd模块
import xlwt

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
                y = y + 1
            x = x + 1
 
        wbk.save(self.data_path[:-3]+'xls')#保存文件


if __name__ == '__main__':
    data_path = "D:\\pythonData\\股票数据\\科创板Data20190909.xls"  #文件的绝对路径
    get_data = ExcelData(data_path)                       #定义get_data对象, sheet名称默认Sheet1
    print(get_data.read_excel())