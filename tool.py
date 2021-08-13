from ruamel import yaml
import openpyxl

class Tool():
    #生成yaml
    def output_yaml(self, arr_case, file_name):
        with open(file_name, 'w+', encoding='utf-8') as f:
            yaml.dump(arr_case, f, Dumper=yaml.RoundTripDumper)

    #提取yaml
    def yaml_manage(self, file_path):
        """载入yaml配置文件，并存为字典格式"""
        with open (file_path, encoding = 'utf-8') as file_obj:
            content = file_obj.read()
            yaml_dic = yaml.load(content, Loader=yaml.Loader)
            return yaml_dic

    #创建新表格
    def wb_new(self):
        wb = openpyxl.Workbook()
        ws_default = wb.active
        wb.remove(ws_default)   #移除默认的表单，方便后面创建新的表单
        return wb

    #提取表格行列
    def ex_relation(self, ws):
        ex_temp_dic = {}
        row_title = ws['1']
        for i in row_title:
            ex_temp_dic[i.value] = i.column
        return ex_temp_dic