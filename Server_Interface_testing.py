# -*- coding: utf-8 -*-
import unittest                                                                                  #支持Python单元测试模块
import urllib.parse                                                                              #这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                                                            #这里urllib.request要精确到子模块,否则会报错
import csv                                                                                       #支持csv自动化导表
import sys                                                                                       #用来打log
import time                                                                                      #获取时间戳
import hashlib                                                                                   #MD5加密

'''
获取服务器接口测试，用于运营后台，接收获取应用服务器的申请，返回申请的结果
'''
class test_server_interface(unittest.TestCase):
    url = 'http://wwwapi.15166.com/server?action=listAll&'                                        #所要访问的url,一个测试类对应一个url
    
    def setUp(self):                                                                             #文件/数据库/网络服务初始化工作
        pass

    def tearDown(self):                                                                          #销毁工作
        pass

    def test_server_interface_cases(self):                                                       #执行测试功能的函数
        with open('csv/server_interface_data.csv') as csvfile:                                   #打开csv文件流
            reader = csv.DictReader(csvfile)                                                     #创建文件流对象
            server_interface_num=0                                                               #计算一共跑了多少条测试数据
            for row in reader:                                                                   #这里的row对应csv表里的一行数据,第一行数据自动作为字段名,第二行数据开始作为测试实例
                server_interface_num+=1                                                         
                with self.subTest(row=row):                                                      #row=i,会报错row is not defined,必须用row=row(这里用的是subTest功能)
                    print("正在为'获取服务器接口模块'执行第 %d 条测试数据"% server_interface_num)#每跑一条数据,显示一次当前进度
                       
                    info = {'appid': row['appid'], 'channel': row['channel'], 'time':'', 'sign':''} #csv里的每一行测试实例，这里不用过滤空值，空值可以作为测试用例，引发异常
                    info['time'] =str(int(time.time()));                                         #赋值字典time
                 
                    strmd5 = info['appid']+info['time']+row['appkey'];                          
                    info['sign'] = hashlib.md5(strmd5.encode(encoding='UTF8')).hexdigest()
                   
                   # print(info);                                                                 #请求时发送的参数字典
 
                    url_values = urllib.parse.urlencode(info);                                   #将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码  
                    full_url = test_server_interface.url+url_values;
                    
                   # print(full_url);                                                             #get方法最终请求的URL
    
                    response = urllib.request.urlopen(full_url).read(); 
                    
                   # print(response);                                                             #服务器响应的字符串消息
  
                    response_dict = eval(response); 
                  
                    print(response_dict);                                                        #转换成字典后的消息
                    
                    self.assertEqual(response_dict['code'], eval(row['code']))                   #获取服务器接口模块---您看到此信息,代表当行测试数据未通过---  
        
        print("----------------------------------------------------------------------------------------------------------------------")
        print(response_dict['data']);
        print("----------------------------------------------------------------------------------------------------------------------")


'''
unittest.main(),固定格式,用于默认调用unittest模块
'''

if __name__ == '__main__':
    log_file = 'log/log_%s.txt'%time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime())             #定义log路径及文件名
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()
