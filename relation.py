import openpyxl
import tool
import re

class Relation():
    def __init__(self, feature, excel_path, yaml_path, ws_name):
        
        #仿真参数库中para部分的列关系，若表更有变动，需手动维护
        self. para_col_dic = {
                                'odd_roadGeo': 8, 'odd_illumination': 9, 'odd_weather': 10, 
                                'hv_init': 11, 'hv_action1': 12, 'hv_action2': 13, 'hv_action3': 14, 
                                'tv1_init': 15, 'tv1_action1': 16, 'tv1_action2': 17, 'tv1_action3': 18, 'tv1_action4': 19, 
                                'tv2_init': 20, 'tv2_action1': 21, 'tv2_action2': 22, 'tv2_action3': 23, 'tv2_action4': 24,
                                'oddChange_action1':25, 'oddChange_action2':26, 'oddChange_action3':27, 'oddChange_action4':28
                                }

        #仿真参数库中几个常用行列的行列关系，若表更有变动，需手动维护
        self.allPara_row_num = 5    #参数全集行的行关系
        self.blankFlag_col_num = 6    #通过第6列判断这条case是否需要被参数化，如果有内容需要，反之不需要
        self.summary_col_num = 3    #summary列的列关系
        self.repalce_col_num = 4    #replace列的列关系
        self.rm_col_num = 5    #rm列的列关系
        self.tagFixed_col_dic = {'basic':6, 'reserve':7}    #固定tag的列关系
        # self.tagAuto_col_dic = {'odd':8, 'reserve':9}       #活动tag的列关系
        self.wb_case_lib = 'case_lib'
        self.case_id_col = 'A'

        self.feature = feature
        self.case_row_dic = {}
        self.para_odd_arr = []
        self.para_excution_arr = []
        self.t_obj = tool.Tool()
        self.excel_path = excel_path
        self.yaml_path = yaml_path
        self.ws_name = ws_name

    def func(self):
        #生成case_id的行关系，并生成  sim_cc\yaml_folder\relation_firstCol.yaml
        self.parser(self.excel_path, self.ws_name, 'A', self.yaml_path)
        
        #对行关系yaml做过滤，只保留三级标题
        temp_dic  = self.t_obj.yaml_manage(self.yaml_path)
        for id, row_num in temp_dic.items():
            if id: id_split = id.split("_")
            if id_split[0] == self.feature and len(id_split) == 3:
                self.case_row_dic[id] = row_num
        
        #将参数库中的标题 self. para_col_dic 分为 odd 和 excution 两部分到 self.para_odd_arr 和 self.para_excution_arr
        self.classify()

    def parser(self, excel_path, ws_name, position, yaml_name):
        """将参数表中的id列的行关系解析成yaml"""
        wb = openpyxl.load_workbook(excel_path)
        ws = wb[ws_name]
        relation_dic = {}
        position_col_row = ws[position]
        #因为参数表中的id列是通过excel映射生成的，所以需要做转化
        relation_dic = self.func_parser(position_col_row, wb)
        self.t_obj.output_yaml(relation_dic, yaml_name)

    def func_parser(self, func_arr, wb):
        ws_case = wb[self.wb_case_lib]
        relation_case = {}
        for cell in ws_case[self.case_id_col][:200]:
            relation_case[cell.value] = cell.row
        parser_col_row = {} 
        for cell in func_arr:
            if cell.value:
                cell_num = re.findall(r"\d+", cell.value)
                if cell_num:
                    for id, row in relation_case.items():
                        if int(cell_num[-1]) == row:
                            parser_col_row[id] = cell.row
        return parser_col_row
                
    def classify(self):
        for para in self.para_col_dic:
            para_split = para.split("_")
            if para_split[0] == 'odd':
                self.para_odd_arr.append(para)
            else:
                self.para_excution_arr.append(para)
        # print(self.para_odd_arr)
        # print(self.para_excution_arr)