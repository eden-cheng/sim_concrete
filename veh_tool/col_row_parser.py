from veh_tool import yaml_parser
from veh_tool import excel_parser
relation = "./veh_tool/relation.yaml"

class Parser:
    def __init__(self):
        y_obj = yaml_parser.Parser()
        self.content = y_obj.yaml_manage(relation)
        self.dic = {}

    def func_case(self, ws_lib, feature):
        case_first_col = (self.content['lib_case_first'])['id_column']
        case_first_row = (self.content['lib_case_first'])['title_row']
        e_obj = excel_parser.Parser(ws_lib, feature, 'lib', case_first_col, case_first_row)
        e_obj.combine()
        self.dic[feature + '_lib_relation'] = e_obj.dic
        # print(e_obj.dic)
        # for key, value in e_obj.dic.items():
        #     self.dic[key] = value
        # print(e_obj.dic)

    def func_para_recommend(self, ws_para, feature):
        case_first_col = (self.content['lib_para_recommend_first'])['id_column']
        case_first_row = (self.content['lib_para_recommend_first'])['title_row']
        e_obj = excel_parser.Parser(ws_para, feature, 'recommend', case_first_col, case_first_row)
        e_obj.combine()
        self.dic[feature + '_recommend_relation'] = e_obj.dic
        # for key, value in e_obj.dic.items():
        #     self.dic[key] = value
        # print(e_obj.dic)

    def func_para_range(self, ws_para, feature):
        case_first_col = (self.content['lib_para_range_first'])['id_column']
        case_first_row = (self.content['lib_para_range_first'])['title_row']
        e_obj = excel_parser.Parser(ws_para, feature, 'range', case_first_col, case_first_row)
        e_obj.combine()
        self.dic[feature + '_range_relation'] = e_obj.dic
        # for key, value in e_obj.dic.items():
        #     self.dic[key] = value
        # print(e_obj.dic)