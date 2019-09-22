

from ExcelData import ExcelData


def generate_list_by_code_list(list_path, base_list_path= 'D:\\PythonData\\stock\\list\\hs_a_board.xls'):
    excel_read = ExcelData(list_path)
    stock_list = excel_read.read_excel()
    excel_read = ExcelData(base_list_path)
    base_list = excel_read.read_excel()

    L = []

    for stock in stock_list:
        code = stock['code']
        is_match = False
        for base in base_list:
            if code == base['code']:
                is_match = True
                if '备注' in stock:
                    base['备注'] = stock['备注']
                L.append(base)
                break
        if not is_match:
            print(code + ' is not exist')

    excel_write = ExcelData(list_path)
    excel_write.write_excel(L)

def generate_list_by_name_list(list_path, base_list_path= 'D:\\PythonData\\stock\\list\\hs_a_board.xls'):
    excel_read = ExcelData(list_path)
    stock_list = excel_read.read_excel()
    excel_read = ExcelData(base_list_path)
    base_list = excel_read.read_excel()

    L = []

    for stock in stock_list:
        name = stock['名称']
        is_match = False
        for base in base_list:
            if name == base['名称']:
                is_match = True
                if '备注' in stock:
                    base['备注'] = stock['备注']
                L.append(base)
                break
        if not is_match:
            print(name + ' is not exist')

    excel_write = ExcelData(list_path)
    excel_write.write_excel(L)

def main():
    # generate_list_by_code_list('D:\\PythonData\\stock\\list\\huawei5G.xls')
    # generate_list_by_code_list('D:\\PythonData\\stock\\list\\trace.xls')
    # generate_list_by_code_list('D:\\PythonData\\stock\\list\\performance_up.xls')
    generate_list_by_code_list('D:\\PythonData\\stock\\list\\science_chip.xls')
    # generate_list_by_name_list('D:\\PythonData\\stock\\list\\top_list.xls')

if __name__ == '__main__':
    main()
	