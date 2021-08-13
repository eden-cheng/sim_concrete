from veh_tool import col_row_parser
from veh_tool import lib_para_parser
from veh_tool import yaml_parser
import os

class Recommend():
    def __init__(self, feature, wb, ws_range, ws_case_lib_name, ws_para_recommend_name, ws_para_range_name, version_value):
        self.feature = feature
        self.wb = wb
        self.ws_range = ws_range
        self.ws_case_lib_name = ws_case_lib_name
        self.ws_para_recommend_name = ws_para_recommend_name
        self.ws_para_range_name = ws_para_range_name
        self.version_value = version_value

    def func_split(self, para_list):
        dic = {}
        for para in para_list:
            temp = para.split(":")
            # print(temp)
            dic[temp[0]] = temp[1]
        return dic

    def func(self):
        #实例化各种类
        cr_obj = col_row_parser.Parser()
        #step1：获取场景库和参数库
        ws_case_lib = self.wb[self.ws_case_lib_name]
        ws_para_recommend =  self.wb[self.ws_para_recommend_name]
        ws_para_range =  self.wb[self.ws_para_range_name]

        #step2：对场景库和推荐参数库的行列关系做解析（必须先对case表做行列解析，再对para表做行列解析）
        cr_obj.func_case(ws_case_lib, self.feature)
        cr_obj.func_para_recommend(ws_para_recommend, self.feature)
        cr_obj.func_para_range(ws_para_range, self.feature)
        #step3: 参数库由excel转化为yaml（必须先对para表做行列解析，才能对para表做解析）
        obj = lib_para_parser.Parser(ws_para_recommend, self.feature)
        obj.para_group_to_yaml()

        #step3: 将多个yaml汇总成一个yaml
        para_gather_dic = {}
        y_obj = yaml_parser.Parser()
        para_yaml_path = './yaml_para/'
        for root, dirs, files in os.walk(para_yaml_path):
            for file in files:
                file_path = './yaml_para/' + file
                content = y_obj.yaml_manage(file_path).copy()
                para_gather_dic[file] = content
        # for key, value in para_gather_dic.items():
        #     print(key)
        #     print(value)

        #对行列关系yaml做整理
        case_row_temp = {}
        case_row_dic = y_obj.yaml_manage('./output_relation/'+self.feature+'_range_row.yaml')
        # print(case_row_dic)
        for case1_name, case2_dic in case_row_dic.items():
            for case2_name, row in case2_dic.items():
                case_row_temp[row] = case2_name
        # print(case_row_temp)

        #step4: 获取变量名替换关系
        replace_dic = {}
        replace_col = self.ws_range['D']
        for cell in replace_col:
            replace_dic[cell.row] = cell.value
        # print(replace_dic)
        replace_case_dic = {}
        for row, replace_value in replace_dic.items():
            if row in case_row_temp.keys():
                replace_case_dic[case_row_temp[row]] = replace_value
        # print(replace_case_dic)

        #step5: 变量名替换格式整理
        for case_name, replace_content in replace_case_dic.items():
            if replace_content:
                temp_list = replace_content.split('\n')
                # print(temp_list)
                temp_dic = self.func_split(temp_list)
                # print(temp_dic)
                replace_case_dic[case_name] = temp_dic.copy()
        # print(replace_case_dic)

        #step6: 做变量名替换
        for odd, para_odd_idc in para_gather_dic.items():
            for case_name, para_case_dic in para_odd_idc.items():
                # print(case_name)
                if not replace_case_dic[case_name]: break
                for group_name, para_group_dic in para_case_dic.items():
                    for action_or_odd, para_action_odd_dic in para_group_dic.items():
                        if action_or_odd == 'para_action':
                            for para_name, para_value in para_action_odd_dic.items():
                                for origin, para in replace_case_dic[case_name].items():
                                    if origin == para_name:                        
                                        para_action_odd_dic[para] = para_action_odd_dic.pop(origin)
        # print(para_gather_dic)
        y_obj.yaml_generate(para_gather_dic, './output_final/', self.feature + '_para_recommend_' + self.version_value +'.yaml')