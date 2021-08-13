from ruamel import yaml
import os

yaml_path_file = "file_path.yaml"

class Parser():
    def yaml_manage(self, file_path):
        """载入yaml配置文件，并存为字典格式"""
        with open (file_path, encoding = 'utf-8') as file_obj:
            content = file_obj.read()
            # print(content)
            yaml_dic = yaml.load(content, Loader=yaml.Loader)
            return yaml_dic

    def yaml_path(self):
        """获取file_ptah.yaml中的文件路径"""
        return self.yaml_manage(yaml_path_file)

    def yaml_generate(self, content, file_path, name):
        """生成yaml文件,content可以是字典，也可以是列表"""
        isExists = os.path.exists(file_path)
        if not isExists:
            os.makedirs(file_path)
        file_name = file_path + name
        with open(file_name, 'w', encoding='utf-8') as f:
            yaml.dump(content, f, Dumper=yaml.RoundTripDumper)

    def charact_value(self, odd):
        """将yaml中的多组特征值文件路径，提取出成参数字典"""
        #实例化 Yaml_manage 类，并从yaml中提取出实车测试特征值文件的路径构成字典
        #键是实车测试对象，比如noload, payload
        #值是特征值文件的路径
        path = self.yaml_path()['parser_file']
        yaml_s = self.yaml_manage(path)[odd]
        #分别将实车测试特征值文件中的内容提取出来，形成一个庞大的特征值字典。
        #键是实车测试的对象， 比如noload, payload
        #值是特征值
        dic = {}
        for key, value in yaml_s.items():
            dic[key] = self.yaml_manage(value)
        return dic