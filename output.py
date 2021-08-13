import solution
import relation

class Output():
    def __init__(self, feature, ws, excel_path, yaml_path, ws_name):
        self.para_origin_dic = {}   #每行case的原始形式
        self.ex_sim_case = {}       #每行case的展开
        self.all_para_dic = {}      #参数全集
        self.para_tag_dic = {}      #参数加tag全集
        self.ex_sim_case_single = {}    #每行case的展开，但是只留一个
        self.all_tag_arr = []       #tag全集，含固定tag和自动生成tag

        self.ws = ws
        self.r_obj = relation.Relation(feature, excel_path, yaml_path, ws_name)
        self.r_obj.func()
        self.s_obj = solution.Solution(feature, ws, excel_path, yaml_path, ws_name)

    def func(self):
        #提取tag全集所在行，也就是第5行，其中tag的部分，输出到字典 self.all_tag_arr
        self.func_allTag()
        #提取参数全集所在行，也就是第5行，其中para的部分，输出到字典 self.all_para_dic
        self.func_allPara()
        #提取参数全集所在行，也就是第5行，其中para和tag的部分，输出到字典 self.para_tag_dic
        self.func_Para_Tag()
        #提取每一条case的tag和para，输出到字典 self.para_origin_dic
        for i in self.r_obj.case_row_dic.keys():
            # print('@@@@@@@ postion1: ', i)
            self.para_origin_dic[i] = self.func_para_origin(i)
        #对每一条case的扩展，输出到字典 self.ex_sim_case
        for i in self.r_obj.case_row_dic.keys():
            # print('@@@@@@@ postion2: ', i)
            case_para_arr = self.s_obj.func_gather(i)
            # print(i)
            # print(case_para_arr)
            self.ex_sim_case[i] = case_para_arr
        #对每一条case的扩展后的默认参数行，此处用第一组参数作为默认行，输出到字典 self.ex_sim_case_single
        for case_id, value_group in self.ex_sim_case.items():
            # print(case_id)
            # print(value_group)
            if value_group:
                self.ex_sim_case_single[case_id] = value_group[0]
                # print(value_group[0])

        # 因为取消auto_tag后，下面两行都不需要了
        # self.func_tag_auto()
        # self.func_get_tag()

    def func_allPara(self):
        """
        提取参数全集
        也就是para_range_lib中第5行中para的部分，不含tag的部分
        输出：将提取的内容整理到 self.all_para_dic 字典中
        """
        # self.all_para_dic = {}
        for odd_name in self.r_obj.para_col_dic:
            # print(self.r_obj.allPara_row_num)
            # print(self.r_obj.para_col_dic[odd_name])
            # print(odd_name)
            cell_odd = self.ws.cell(row=self.r_obj.allPara_row_num, column=self.r_obj.para_col_dic[odd_name]).value
            # print(cell_odd)
            arr = cell_odd.split('\n')
            for line in arr:
                temp = line.split(";")
                name = 'para_' + odd_name + "_" + temp[0]
                self.s_obj.para_ex(self.all_para_dic, name, temp)

    def func_allTag(self):
        """
        提取tag全集
        也就是para_range_lib中第5行中para的部分，不含para的部分
        输出：将提取的内容整理到 self.all_tag_arr 列表中
        """
        for tag_fixed_name in self.r_obj.tagFixed_col_dic:
            cell_odd = self.ws.cell(row=self.r_obj.allPara_row_num, column=self.r_obj.tagFixed_col_dic[tag_fixed_name]).value
            if not cell_odd: continue
            arr = cell_odd.split('\n')
            for line in arr:
                temp = line.split(";")
                if temp[0] == 'reserve': continue
                name = 'tag_fixed_' + tag_fixed_name + "_" + temp[0]
                self.s_obj.para_ex(self.para_tag_dic, name, temp)
        for key, value in self.para_tag_dic.items():
            self.all_tag_arr.append(key)
        # print(self.all_tag_arr)

    def func_Para_Tag(self):
        """
        提取参数全集和tag全集
        也就是para_range_lib中第5行中para 和 tag的部分
        输出：将提取的内容整理到 self.para_tag_dic 字典中
        备注：auto_tag被取消了
        """
        # for tag_fixed_name in self.r_obj.tagFixed_col_dic:
        #     cell_odd = self.ws.cell(row=self.r_obj.allPara_row_num, column=self.r_obj.tagFixed_col_dic[tag_fixed_name]).value
        #     if not cell_odd: continue
        #     arr = cell_odd.split('\n')
        #     for line in arr:
        #         temp = line.split(";")
        #         name = 'tag_fixed_' + tag_fixed_name + "_" + temp[0]
        #         self.s_obj.para_ex(self.para_tag_dic, name, temp)
        # for tag_auto_name in self.r_obj.tagAuto_col_dic:
        #     cell_odd = self.ws.cell(row=self.r_obj.allPara_row_num, column=self.r_obj.tagAuto_col_dic[tag_auto_name]).value
        #     if not cell_odd: continue
        #     arr = cell_odd.split('\n')
        #     for line in arr:
        #         temp = line.split(";")
        #         name = 'tag_auto_' + tag_auto_name + "_" + temp[0]
        #         self.s_obj.para_ex(self.para_tag_dic, name, temp)
        for para_name in self.r_obj.para_col_dic:
            cell_odd = self.ws.cell(row=self.r_obj.allPara_row_num, column=self.r_obj.para_col_dic[para_name]).value
            if not cell_odd: continue
            arr = cell_odd.split('\n')
            for line in arr:
                temp = line.split(";")
                name = 'para_' + para_name + "_" + temp[0]
                self.s_obj.para_ex(self.para_tag_dic, name, temp)
        # print(self.para_tag_dic)

    def func_para_origin(self, row_name):
        """
        提取第 row_name 行的 tag 和 para
        只提取了变量名吗？提取变量的内容吗？（看样子好像没有）
        输出：每行的tag和para的每个单元格加入列表，最后输出列表arr
        """
        arr = []
        for tag_name in self.r_obj.tagFixed_col_dic:
            cell_content = self.ws.cell(row=self.r_obj.case_row_dic[row_name], column=self.r_obj.tagFixed_col_dic[tag_name]).value
            if not cell_content: continue
            line = cell_content.split('\n')
            for i in line:
                temp = i.split(';')
                temp[0] = 'tag_fixed_' +tag_name + "_" + temp[0]
                arr.append(temp)
        # for tag_name in self.r_obj.tagAuto_col_dic:
        #     cell_content = self.ws.cell(row=self.r_obj.case_row_dic[row_name], column=self.r_obj.tagAuto_col_dic[tag_name]).value
        #     if not cell_content: continue
        #     line = cell_content.split('\n')
        #     for i in line:
        #         temp = i.split(';')
        #         temp[0] = 'tag_auto_' + tag_name + "_" + temp[0]
        #         arr.append(temp)
        for odd_name in self.r_obj.para_col_dic:
            cell_content = self.ws.cell(row=self.r_obj.case_row_dic[row_name], column=self.r_obj.para_col_dic[odd_name]).value
            if not cell_content: continue
            line = cell_content.split('\n')
            for i in line:
                temp = i.split(';')
                temp[0] = 'para_' + odd_name + "_" + temp[0]
                arr.append(temp)
        return arr  
        
    def func_tag_auto(self):
        ######################## 后处理之tag_auto ########################
        for case_id, value_group in self.ex_sim_case.items():
            if not value_group: continue
            for value_sub in value_group:
                illu_value = ''
                weather_value = ''
                area_value = ''
                roadGeo_value = ''
                tvNum_value = 0
                tvType_value = 'none'

                for key in value_sub:
                    # print(key)
                    temp = key.split('_')
                    if len(temp) == 1: continue
                    if temp[2] == 'illumination':
                        illu_value = temp[-1]
                        # print(illu_value)
                    if temp[2] == 'weather':
                        weather_value = temp[-1]
                        # print(weather_value)
                    if temp[2] == 'area':
                        area_value = temp[-1]
                        # print(area_value)
                    # if temp[2] == 'load':
                    #     area_value = temp[-1]
                    #     # print(area_value)
                    if temp[2] == 'roadGeo':
                        if temp[-1][-1] == 'l':
                            roadGeo_value = temp[-1][-4:].lower()
                        elif temp[-1][-1] == 'e':
                            roadGeo_value = temp[-1][-5:].lower()
                        else:
                            roadGeo_value = temp[-1]
                        # print(roadGeo_value)

                key_arr = []
                for key in value_sub:
                    # print(key)
                    temp = key.split('_')
                    key_arr.append(temp[0])
                #判断目标车
                if 'tv2' in key_arr:
                    tvNum_value = 2
                    tvType_value = 'mutiple'
                    # print(tvNum_value)
                if  'tv1' in key_arr and 'tv2' not in key_arr:
                    tvNum_value = 1
                    tvType_value = value_sub['tv1_init_type']
                    # print(tvType_value)

                value_sub['tag_auto_odd_illumination'] = illu_value
                value_sub['tag_auto_odd_weather'] = weather_value
                value_sub['tag_auto_odd_area'] = area_value
                value_sub['tag_auto_odd_roadGeo'] = roadGeo_value
                value_sub['tag_auto_odd_tvNum'] = tvNum_value
                value_sub['tag_auto_odd_tvType'] = tvType_value
                value_sub['tag_auto_reserve'] = ''

    def func_get_tag(self):
        ######################## 后处理之提取tag ########################
        for case_id, value_group in self.ex_sim_case.items():
            if not value_group: continue
            for value_sub in value_group:
                for key, value in value_sub.items():
                    temp = key.split("_")
                    if temp[0] == 'tag':
                        # print(key)
                        self.all_tag_arr.append(key)
                break
            break
        # print(self.all_tag_arr)

