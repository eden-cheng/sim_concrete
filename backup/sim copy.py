import openpyxl
import time
import os

import relation
import output
import reprocess
import total 
import debugYaml
import excel
import para_recommend

# excel_path = './input_excel/CC_TC_LIB_V2.5_20210706.xlsx'
# feature = 'CC'

# excel_path = './input_excel/OnOff_TC_LIB_V2.5_20210706.xlsx'
# feature = 'ONOFF'

# excel_path = './input_excel/Override_TC_LIB_V2.5_20210629.xlsx'
# feature = 'Override'

# excel_path = './input_excel/PD_TC_LIB_V2.5_20210702.xlsx'
# feature = 'PD'

# excel_path = './input_excel/PM_TC_LIB_V2.5_20210706.xlsx'
# feature = 'PM'

# excel_path = './input_excel/AD_ADAS_TC_LIB_V2.5_20210709.xlsx'
# feature = 'interaction'

# excel_path = './input_excel/DSR_TC_LIB_V2.5_20210709.xlsx'
# feature = 'DSR'

# excel_path = './input_excel/Cooling_TC_LIB_V2.5_20210709.xlsx'
# feature = 'AC'

# excel_path = './input_excel/Fallback vehicle test case.xlsx'
# feature = 'FB'

# excel_path = './input_excel/HMI vehicle test case.xlsx'
# feature = 'HMI'

# excel_path = './input_excel/Sensor_wash.xlsx'
# feature = 'SW'

# excel_path = './input_excel/ILC_TC_LIB_V2.5_20210709.xlsx'
# feature = 'ILC'

version = 'v2.5'

range_ws_name = 'para_range_lib'
case_ws_name = 'case_lib'
recommend_ws_name = 'para_recommend_lib'

        

#id列的行关系，自动化解析
yaml_path = './yaml_folder/' + feature + '_relation_firstCol' + '.yaml'
wb = openpyxl.load_workbook(excel_path)
range_ws = wb[range_ws_name]

######################### 将实车参数表中的内容提取到yaml ########################

p_obj = para_recommend.Recommend(feature, wb, range_ws, case_ws_name, recommend_ws_name, range_ws_name)
p_obj.func()

# def func_split(para_list):
#     dic = {}
#     for para in para_list:
#         temp = para.split(":")
#         dic[temp[0]] = temp[1]
#     return dic

# #实例化各种类
# cr_obj = col_row_parser.Parser()
# #step1：获取场景库和参数库
# ws_case_lib = wb[case_ws_name]
# ws_para_recommend =  wb[para_ws_name]
# ws_para_range =  wb[ws_name]

# #step2：对场景库和推荐参数库的行列关系做解析（必须先对case表做行列解析，再对para表做行列解析）
# cr_obj.func_case(ws_case_lib, feature)
# cr_obj.func_para_recommend(ws_para_recommend, feature)
# cr_obj.func_para_range(ws_para_range, feature)
# #step3: 参数库由excel转化为yaml（必须先对para表做行列解析，才能对para表做解析）
# obj = lib_para_parser.Parser(ws_para_recommend, feature)
# obj.para_group_to_yaml()

# #step3: 将多个yaml汇总成一个yaml
# para_gather_dic = {}
# y_obj = yaml_parser.Parser()
# para_yaml_path = './yaml_para/'
# for root, dirs, files in os.walk(para_yaml_path):
#     for file in files:
#         file_path = './yaml_para/' + file
#         content = y_obj.yaml_manage(file_path).copy()
#         para_gather_dic[file] = content
# # for key, value in para_gather_dic.items():
# #     print(key)
# #     print(value)

# #对行列关系yaml做整理
# case_row_temp = {}
# case_row_dic = y_obj.yaml_manage('parser_result/'+feature+'_range_row.yaml')
# # print(case_row_dic)
# for case1_name, case2_dic in case_row_dic.items():
#     for case2_name, row in case2_dic.items():
#         case_row_temp[row] = case2_name
# # print(case_row_temp)

# #step4: 获取变量名替换关系
# replace_dic = {}
# replace_col = ws['D']
# for cell in replace_col:
#     replace_dic[cell.row] = cell.value
# # print(replace_dic)
# replace_case_dic = {}
# for row, replace_value in replace_dic.items():
#     if row in case_row_temp.keys():
#         replace_case_dic[case_row_temp[row]] = replace_value
# # print(replace_case_dic)

# #step5: 变量名替换格式整理
# for case_name, replace_content in replace_case_dic.items():
#     if replace_content:
#         temp_list = replace_content.split('\n')
#         # print(temp_list)
#         temp_dic = func_split(temp_list)
#         # print(temp_dic)
#         replace_case_dic[case_name] = temp_dic.copy()
# # print(replace_case_dic)

# #step6: 做变量名替换
# for odd, para_odd_idc in para_gather_dic.items():
#     for case_name, para_case_dic in para_odd_idc.items():
#         if not replace_case_dic[case_name]: break
#         for group_name, para_group_dic in para_case_dic.items():
#             for action_or_odd, para_action_odd_dic in para_group_dic.items():
#                 if action_or_odd == 'para_action':
#                     for para_name, para_value in para_action_odd_dic.items():
#                         for origin, para in replace_case_dic[case_name].items():
#                             if origin == para_name:                        
#                                 para_action_odd_dic[para] = para_action_odd_dic.pop(origin)
# # print(para_gather_dic)
# y_obj.yaml_generate(para_gather_dic, './yaml_folder/', 'para_recommend.yaml')

############################ 准备：行列关系 ###################################
"""
1）对参数库做的case_id列做行号解析，并提取只保留三级case_id
2）手动维护参数库中para部分的列号，并对para部分做了odd 和 excution 的区分
3）手动维护参数库中几个典型列的列号
"""
r_obj = relation.Relation(feature, excel_path, yaml_path, range_ws_name)
r_obj.func()
# r_obj.func('./yaml_folder/relation_firstCol_ilc.yaml')
# print(r_obj.case_row_dic) 
# print(r_obj.para_col_dic)
# print(r_obj.allPara_row_num)
# print(r_obj.summary_col_num)
# print(r_obj.repalce_col_num)
# print(r_obj.tagFixed_col_dic)
# print(r_obj.tagAuto_col_dic)
# print(r_obj.para_odd_arr)
# print(r_obj.para_excution_arr)

########################### 正文：解析仿真case ###################################
start_simple = time.time()

output_obj = output.Output(feature, range_ws, excel_path, yaml_path, range_ws_name)

output_obj.func()
# print(output_obj.all_para_dic)    #参数全集
# print(output_obj.para_tag_dic)    #参数和tag全集
# print(output_obj.para_origin_dic) #每条case的原始参数
# print(output_obj.ex_sim_case)     #每条case的展开
# print(output_obj.ex_sim_case_single)   #每条case的展开，但是只保留一条
# print(output_obj.all_tag_arr)     #tag全集
# for key, value in output_obj.para_origin_dic.items():
#     print(key)
#     print(value)
# print(output_obj.ex_sim_case['CC_3_1'])
# for key, value in output_obj.ex_sim_case.items():
#     print(key)
#     print(value)
# for key, value in output_obj.ex_sim_case_single.items():
#     print(key)
#     print(value)

#后处理，替换tv_init_speed，替换summary
reprocess_obj = reprocess.Reprocess(feature, output_obj.ex_sim_case, wb, range_ws, excel_path, yaml_path, range_ws_name)
reprocess_obj.func()

stop_simple = time.time()

print('不写入yaml耗时： %.3f s\n' % (stop_simple - start_simple))

########################### 后续：统计，生成yaml和excel ###################################

# 统计数量
total_obj = total.Total(output_obj.ex_sim_case, output_obj.para_tag_dic)
total_obj.func_print()

# 写入yaml并统计耗时
yaml_obj = debugYaml.DebugYaml(feature, version)
yaml_obj.func(output_obj.para_origin_dic, output_obj.para_tag_dic, output_obj.ex_sim_case)

######################### 写进excel并统计耗时 ########################

excel_obj = excel.Excel(feature, output_obj.all_tag_arr, output_obj.all_para_dic, 
                        output_obj.ex_sim_case, output_obj.ex_sim_case_single, version)
excel_obj.func()

