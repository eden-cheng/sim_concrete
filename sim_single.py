import openpyxl
import time

import relation
import output
import reprocess
import total 
import debugYaml
import excel
import para_recommend

range_ws_name = 'para_range_lib'
case_ws_name = 'case_lib'
recommend_ws_name = 'para_recommend_lib'

class Sim():
    def __init__(self, feature, excel_path, version_value):
    #id列的行关系，自动化解析
        self.feature = feature
        self.excel_path = excel_path
        self.version_value = version_value
        self.yaml_path = './output_debug/' + feature + '_relation_firstCol_' + version_value + '.yaml'
        self.wb = openpyxl.load_workbook(excel_path)
        self.range_ws = self.wb[range_ws_name]


    ######################### 将实车参数表中的内容提取到yaml ########################
    def sim_func(self):
        print("@@@@@@@@@@@@@@ start parser %s @@@@@@@@@@@" % self.feature)

        p_obj = para_recommend.Recommend(self.feature, self.wb, self.range_ws, case_ws_name, recommend_ws_name, range_ws_name, self.version_value)
        p_obj.func()

    ############################ 准备：行列关系 ###################################
        """
        1）对参数库做的case_id列做行号解析，并提取只保留三级case_id
        2）手动维护参数库中para部分的列号，并对para部分做了odd 和 excution 的区分
        3）手动维护参数库中几个典型列的列号
        """
        r_obj = relation.Relation(self.feature, self.excel_path, self.yaml_path, range_ws_name)
        r_obj.func()

    ########################### 正文：解析仿真case ###################################
        start_simple = time.time()

        output_obj = output.Output(self.feature, self.range_ws, self.excel_path, self.yaml_path, range_ws_name)

        output_obj.func()

        #后处理，替换tv_init_speed，替换summary
        reprocess_obj = reprocess.Reprocess(self.feature, output_obj.ex_sim_case, self.wb, self.range_ws, self.excel_path, self.yaml_path, range_ws_name)
        reprocess_obj.func()

        stop_simple = time.time()

        print('不写入yaml耗时： %.3f s\n' % (stop_simple - start_simple))

    ########################### 后续：统计，生成yaml和excel ###################################

        # 统计数量
        total_obj = total.Total(output_obj.ex_sim_case, output_obj.para_tag_dic)
        total_obj.func_print()

        # 写入yaml并统计耗时
        yaml_obj = debugYaml.DebugYaml(self.feature, self.version_value)
        yaml_obj.func(output_obj.para_origin_dic, output_obj.para_tag_dic, output_obj.ex_sim_case)

        ######################### 写进excel并统计耗时 ########################

        excel_obj = excel.Excel(self.feature, output_obj.all_tag_arr, output_obj.all_para_dic, 
                                output_obj.ex_sim_case, output_obj.ex_sim_case_single, self.version_value)
        excel_obj.func()

        print("################ finish parser %s ##############" % self.feature)