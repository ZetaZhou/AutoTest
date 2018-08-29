#-*- coding:utf-8 -*-

'''
@ auther: ZetaZhou
'''

from myutils.CommonConfig import CommonConfig
from myutils.EmailUtils import *
from myutils.LogMethod import *

class RunTest(CommonConfig):

    def __init__(self):
        super().__init__()
        self.config = self.initconfig()
        initlogfile(self.config_dir, self.config['main_log'], 'main')
        initlogfile(self.config_dir, self.config['detail_log'], 'detail')

        logging.config.fileConfig(self.config_dir + "logger.conf")
        self.loggermain = logging.getLogger("main")

    def initconfig(self):
        '''
        初始化config文件, 把配置写入self.config字典中
        :return:
        '''
        config_dict = dict()
        with open(self.config_dir + 'config.txt', 'r') as file:
            configdatalist = file.readlines()
        if '[config]' in configdatalist[0]:
            for configdata in configdatalist:
                try:
                    config = configdata.split('=')
                    config_dict[config[0]] = config[1].strip('\n ')
                except:
                    pass
        # loggerAnalyze.info('[*] Config info: ' + str(config_dict))
        return config_dict

    def create_testcase(self):
        '''
        创建testcase列表文件, 文件存在返回true, 文件不存在创建并返回false
        :return:
        '''

        if  os.path.exists(self.config['testcase_file']):
            return True

        else:
            filehandler = open(self.config['testcase_file'], 'w+')
            for root, dirs, files in os.walk(self.testcase_dir):
                # print(root)  # 当前目录路径
                # print(dirs)  # 当前路径下所有子目录
                # print(files)  # 当前路径下所有非目录子文件
                while len(dirs) != 0:
                    for root, dirs, files in os.walk(root):
                        filehandler.write(root + '\n')
                        for file in files:
                            file_type = os.path.splitext(file)[1]
                            if file_type == '.py':
                                filehandler.write(file + '$\n')
            filehandler.close()
            self.loggermain.info('[*] Testcase create successful!')
            return False

    def generator_testcase(self):
        '''
        testcase生成器
        从testcase列表文件中, 读取testcase名字并返回
        :return:
        '''
        testcase_dir = dict()
        with open(self.config['testcase_file'] , 'r') as filehandler:
            caselist = filehandler.readlines()
            for case in caselist:
                if case.startswith('.'):
                    testcase_dir['url'] = case.strip('\n')
                if (not case.startswith('#')) and case.strip('\n').endswith('$'):
                    yield testcase_dir['url'] + '\\' + case.strip('\n$')

    def excute_testcase(self, testcase, caseseq):

        self.loggermain.info('[*] Testcase [ {} ] start !'.format(testcase))
        subprocess.call("python " + testcase + ' -%d -%s' %(caseseq, HOST), shell=True)
        self.loggermain.info('[*] Testcase [ {} ] finish !'.format(testcase))
        self.loggermain.info('')

    def rename_testcase(self):
        if os.path.exists('testcase_old.txt'):
            os.remove('testcase_old.txt')
            os.rename(self.config['testcase_file'], 'testcase_old.txt')
        else:
            os.rename(self.config['testcase_file'], 'testcase_old.txt')

    def send_mail(self):
        '''
        从result文件夹中找到当天的完成报告并发送
        :return:
        '''
        send_report(self.result_dir + '\TestResult_' + self.today + '.html')


if __name__ == '__main__':
    import subprocess
    import logging.config

    HOST = "http://sbrz.sinoecare.net:8000"

    mainloop = RunTest()                            # 初始化自动化框架
    mainloop.initconfig()

    runsign = mainloop.create_testcase()            # 获取testcase状态
    if runsign:
        caseseq = 1
        casegenerator = mainloop.generator_testcase()
        while True:
            try:
                mainloop.excute_testcase(next(casegenerator), caseseq)              # 执行用例
                caseseq += 1
            except StopIteration:
                break

        mainloop.send_mail()                        # 发送邮件

    else:
        exit()

