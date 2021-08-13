import tool
import time

class DebugYaml():
    def __init__(self, feature, version_value):
        self.t_obj = tool.Tool()
        self.feature = feature
        self.version_value = version_value
    
    def func(self, para_origin_dic, para_tag_dic, ex_sim_case):
        ex_sim_case_path = './output_debug/' + self.feature + '_ex_sim_' + self.version_value +'.yaml'
        all_para_path = './output_debug/para_complete_set_' + self.version_value +'.yaml'
        case_origin_path = './output_final/'+ self.feature +'_para_range_' + self.version_value +'.yaml'

        start_write = time.time()

        #打印excel中直接参数
        self.t_obj.output_yaml(para_origin_dic, case_origin_path)
        stop01_write = time.time()
        print('每个case的原始参数写入yaml耗时： %.3f s' % (stop01_write - start_write))

        #将参数全集写入
        self.t_obj.output_yaml(para_tag_dic, all_para_path)
        stop02_write = time.time()
        print('参数全集全展开写入yaml耗时： %.3f s' % (stop02_write - start_write))

        #将展开后的所有case写入
        # self.t_obj.output_yaml(ex_sim_case, ex_sim_case_path)  #注释掉，因为会影响运行的速度，调试用

        stop_write = time.time()
        print('全部写入yaml耗时： %.3f s' % (stop_write - start_write))