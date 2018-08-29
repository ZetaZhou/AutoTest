#-*- coding:utf-8 -*-
import unittest
import sys
import logging.config

from selenium import webdriver
from itertools import cycle

from myutils.CommonConfig import CommonConfig
from myutils.TestReport import TestReport
from myutils.TestCaseInfo import TestCaseInfo

from Page.LoginPage import LoginPage
from Page.MainPage import MainPage


class Test_TC_Cbmd(unittest.TestCase):

    '''
        打开浏览器
        定义全局变量
    '''
    HOST = sys.argv[2].strip('-')
    driver = webdriver.Firefox()
    driver.set_window_size(1400, 900)
    # self.driver.maximize_window()

    # seq = count(1)

    def setUp(self):

        ''' 初始化testcase 信息'''
        name = repr(next(seq)).split('.')[1].strip('<>')
        self.testCaseInfo = TestCaseInfo(id=sys.argv[1].strip('-'), name= name,  owner='ZetaZhou')
        self.testCaseInfo.starttime = CommonConfig.getCurrentTime()

        ''' 初始化testreport '''
        self.testResult = TestReport()

        # ''' 初始化日志句柄'''


    def test_login(self):

        try:
            login = LoginPage(self.driver)
            login.open(self.HOST)
            # print(login.getTitle())

            login.Sendusername("zj")
            login.Sendpassword("admin123")
            login.Sendchecksum()
            login.ClickLogin()

            if not login.CheckLoginState() :
                self.test_login()

            try:
                assert (1==2)

            except Exception as e:
                self.testCaseInfo.errorinfo = " test_login Assert Error"
                loggerdetail.warning(("Error msg: {}".format(self.testCaseInfo.errorinfo)))
                assert False, self.testCaseInfo.errorinfo

            else:
                self.testCaseInfo.result = "Pass"

        except AssertionError:
            pass

        except Exception as e:
            self.testCaseInfo.errorinfo = e
            loggerdetail.warning(("Error msg: {}".format(e)))
            assert False

        else:
            self.testCaseInfo.result = "Pass"

    def test_cbmd(self):

        try:
            mainpage = MainPage(self.driver)
            mainpage.Printcancel()

        except Exception as e:
            self.testCaseInfo.errorinfo = e
            loggerdetail.warning("Error msg: {}".format(e))
            assert False

        else:
            self.testCaseInfo.result = "Pass"

    def tearDown(self):
        self.testCaseInfo.endtime = CommonConfig.getCurrentTime()
        self.testCaseInfo.secondsDuration = CommonConfig.timeDiff(self.testCaseInfo.starttime, self.testCaseInfo.endtime)
        self.testResult.WriteHTML(self.testCaseInfo)

if __name__ == '__main__':
    logging.config.fileConfig(CommonConfig().config_dir + "logger.conf")
    loggerdetail= logging.getLogger("detail")

    run =  Test_TC_Cbmd()
    suite = unittest.TestSuite()

    tests = [Test_TC_Cbmd("test_login"), Test_TC_Cbmd("test_cbmd")]
    suite.addTests(tests)
    seq = cycle(tests)

    runner = unittest.TextTestRunner(verbosity=2)           #日志等级为详细
    runner.run(suite)

    # EmailUtils.send_report()
    Test_TC_Cbmd.driver.quit()


