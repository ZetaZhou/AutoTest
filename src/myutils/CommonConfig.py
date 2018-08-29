from datetime import datetime

#change time to str

class CommonConfig():

    def __init__(self):
        self.today = datetime.now().strftime('%Y_%m_%d')
        self.testcase_dir = '.\\testcase\\'
        self.config_dir = '.\\config\\'
        self.result_dir = '.\\result\\'

    @staticmethod
    def getCurrentTime():
        format = "%a %b %d %H:%M:%S %Y"
        return datetime.now().strftime(format)

    @staticmethod
    def timeDiff(starttime,endtime):
        format = "%a %b %d %H:%M:%S %Y"
        return datetime.strptime(endtime,format) - datetime.strptime(starttime,format)


