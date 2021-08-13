import tool
import time

class Excel():
    def __init__(self, feature, all_tag_arr, all_para_dic, ex_sim_case, ex_sim_case_single, version_value):
        self.tool_obj = tool.Tool()
        self.all_tag_arr = all_tag_arr
        self.all_para_dic = all_para_dic
        self.ex_sim_case = ex_sim_case
        self.ex_sim_case_single = ex_sim_case_single
        self.feature = feature
        self.version_value = version_value

    def func(self):
        start_excel = time.time()

        #填写完全展开后的参数
        wb_ex = self.tool_obj.wb_new()
        ws_ex = self.ws_new(wb_ex)
        relation_ex = self.tool_obj.ex_relation(ws_ex)

        row_title = ws_ex['1']
        row_arr =[]
        for i in row_title:
            row_arr.append(i.value)
        self.tool_obj.output_yaml(row_arr, './output_debug/outline_' + self.version_value + '.yaml')

        # k = 2
        # for case_id, value_group in self.ex_sim_case.items():
        #     # print("@@@@@@@@@@: ", case_id)
        #     if not value_group: continue
        #     for value_sub in value_group:
        #         #填充case_id
        #         ws_ex.cell(row = k, column = 1).value = case_id
        #         #填充内容
        #         for para_name, para_value in value_sub.items():
        #             # print(para_name)
        #             ws_ex.cell(row = k, column = relation_ex[para_name]).value = para_value
        #         k += 1
        # name01 = './output_debug/'+ self.feature+ '_sim_para_ex_' + self.version_value + ".xlsx"
        # wb_ex.save(name01)

        #生成展开case模板
        wb_single = self.tool_obj.wb_new()
        ws_single = self.ws_new(wb_single)
        relation_single = self.tool_obj.ex_relation(ws_single)

        k = 2
        for case_id, value_sub in self.ex_sim_case_single.items():
            #填充case_id
            ws_single.cell(row = k, column = 1).value = case_id
            #填充内容
            for para_name, para_value in value_sub.items():
                ws_single.cell(row = k, column = relation_single[para_name]).value = para_value
            k += 1
        name02 = './output_final/'+ self.feature+ '_sim_para_' + self.version_value + ".xlsx"
        wb_single.save(name02)

        stop_excel = time.time()
        print('写入excel耗时： %.3f s' % (stop_excel - start_excel))

    def ws_new(self, wb):
        #创建表格和表单
        ws_cc = wb.create_sheet('sim_vtd')

        #填写标题
        ##填写id和summary标题
        ws_cc.cell(row = 1, column = 1).value = 'id'
        ws_cc.cell(row = 1, column = 2).value = 'summary'
        ws_cc.cell(row = 1, column = 3).value = 'rm'
        ##填写tag标题
        k = 4
        for title in self.all_tag_arr:
            # print(title)
            ws_cc.cell(row = 1, column = k).value = title
            k += 1
        ##填写参数标题
        for title in self.all_para_dic:
            # print(title)
            ws_cc.cell(row = 1, column = k).value = title
            k += 1
        return ws_cc