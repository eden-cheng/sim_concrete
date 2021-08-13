class Total():
    def __init__(self, ex_case_dic, para_tag_dic):
        self.total = {}
        self.ex_case_dic = ex_case_dic
        self.para_tag_dic = para_tag_dic

    def func_total(self):
        for id, arr in self.ex_case_dic.items():
            if not arr: continue
            tag_num = 0
            self.total[id] = {'col_num':'', 'tag_num':'', 'para_num':'', 'case_num':''}
            self.total[id]['col_num'] = str(len(arr[-1])) 
            self.total[id]['case_num'] = str(len(arr)) 
            # tag数量
            for key, content in arr[-1].items():
                temp = key.split('_')
                if temp[0] == 'tag':
                    tag_num += 1
            # print(tag_num)
            self.total[id]['tag_num'] = tag_num
            self.total[id]['para_num'] = len(arr[-1]) - tag_num - 2

    def func_print(self):
        self.func_total()

        #输出每个case的统计
        print('case展开后统计：')
        # print(total)
        for key, value in self.total.items():
            print (key)
            print (value)

        #输出所有case的总数统计
        sum = 0
        for key, value in self.total.items():
            sum += int(value['case_num'])
        print('case展开后总数统计：')
        print(sum)
        
        print('参数全集数量统计：')
        print('%d\n' % (len(self.para_tag_dic)))
        