#实现对参数库的自动化解析
from veh_tool import yaml_parser
import shutil
import os

"""
取自实车解析工具
"""

relation = "./veh_tool/relation.yaml"
path_row = "./output_relation/"    
path_test = "./yaml_para"

file_CC = 'veh_tool/CC_rec_odd.yaml'
file_ILC = 'veh_tool/ILC_rec_odd.yaml'
file_odd = 'veh_tool/odd&module_rec_odd.yaml'

class Parser():
    def __init__(self, ws, name):
        self.ws = ws
        self.name = name
        self.y_obj = yaml_parser.Parser()
        self.file_row = path_row + name +'_recommend_row.yaml'
        self.dic01 = {}
        self.dic02 = {}
        self.file = file_CC   #默认采用CC的
        if name == 'CC': self.file = file_CC
        if name == 'ILC': self.file = file_ILC
        if name.split("&")[0] == 'odd': self.file = file_odd

    def extract_odd(self):
        odd_dic = self.y_obj.yaml_manage(self.file)
        arr = []
        for name, num in odd_dic.items():
            temp = name.split("_")
            cnt = len(temp[-1])
            arr.append(name[:-cnt-1])
        return arr

    def para_group_to_yaml(self):
        shutil.rmtree(path_test)
        os.mkdir(path_test)
        self.dic = {}
        odd_arr = self.extract_odd()
        # print(odd_arr)
        for i in odd_arr:
            self.combin(i)
        # str1 = "noload_none"
        # str2 = "noload_sedan"
        # str3 = "noload_truck"
        # self.combin(str1)
        # self.combin(str2)
        # self.combin(str3)
        key01 = self.name + "_values"
        self.dic01[key01] = self.dic02
        # print(self.dic01)
        self.dic02 = {}
        # print(self.dic)

    def combin(self, string):
        return self.para_to_yaml(self.action(string), self.odd(string), string)

    def action(self, string):
        # temp = self.y_obj.yaml_manage(relation)['lib_para']
        temp = self.y_obj.yaml_manage(self.file)
        return temp[string + '_action']

    def odd(self, string):
        # temp = self.y_obj.yaml_manage(relation)['lib_para']
        temp = self.y_obj.yaml_manage(self.file)
        return temp[string + '_odd']

    def para_to_yaml(self, action, odd, string):
        result = {}
        temp = {}
        dic = self.y_obj.yaml_manage(self.file_row)
        for id_1st in dic:
            temp = dic[id_1st]
            for id_2nd in temp:
                row_num = temp[id_2nd]
                dic_g = {}
                j = 0
                for i in range(5):
                    cell_action = self.ws.cell(row = row_num, column = action).value
                    cell_odd = self.ws.cell(row = row_num, column = odd).value
                    row_num += 1
                    #将字符串转化为字典格式
                    dic_action = self.func(cell_action)
                    dic_odd = self.func(cell_odd)
                    #如果action或odd任一不为空
                    if dic_action or dic_odd:
                        j += 1
                        dic_g['group'+str(j)] = self.arrange_para(dic_action, dic_odd)
                if dic_g:
                    result[id_2nd] = dic_g
        # print(result)
        if result:
            file_path =  path_test + "/"
            file_name = string + ".yaml"
            self.y_obj.yaml_generate(result, file_path, file_name)
            #
            key02 = string
            value = file_path + file_name
            self.dic02[key02] = value


    def arrange_para(slef, action, odd):
        temp = {}
        temp['para_action'] = action
        temp['para_odd'] = odd
        return temp

    #将下面形式转化成列表和字典嵌套格式
    #调用三面的三个方法
    # A:1;2;3;
    # B:1;2;
    # C:0;1;2;3;4;
    def func(self, string):
        if not string:    #空白
            return
        arr01 = self.func_arr_01(string)
        dic = {}
        for i in arr01:
            for key,value in self.func_dic(i).items():
                arr = self.func_arr_02(value)
                dic[key] = arr
        return dic

    #将 A：B 字符串转成字典结构
    def func_dic(self, string):
        key = ''
        temp = ''
        dic = {} 
        for i in string:
            if i == ":" or i == "：":
                key = temp
                temp = ''
                continue
            temp += i
        dic[key] = temp
        return dic

    # 将下面形式字符串转换成列表结构
    # a
    # b
    # c
    def func_arr_01(self, string):
        arr = []
        str = ""
        k = 0
        for i in string:
            k += 1
            if i == "\n":
                # print(str)
                arr.append(str)
                str = ""
                continue
            str += i
            if k == len(string):
                arr.append(str)
                break
        return arr

    #将a;b;c;转换成列表结构
    def func_arr_02(self, string):
        arr = []
        temp = ''
        for i in string:
            if i == ';' or i == '；':
                arr.append(temp)
                temp = ''
                continue
            temp += i
        return arr