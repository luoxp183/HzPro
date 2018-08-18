from django.test import TestCase

import log_
import logging

# Create your tests here.
class TestLogger(TestCase):
    def testLog(self):
        self.assertEqual('1', '1')
        logging.info('测试 1=1 成功！', extra={'username': 'disen'})

    def testErrorLog(self):
        try:
            self.assertEqual('1', '2')
            logging.info('测试 1=2 成功！', extra={'username': 'disen'})
        except:
            logging.error('测试 1=2 失败！', extra={'username': 'disen'})

    def testDjangoLog(self):
        self.assertIn(1, [1, 2, 3])
        logging.getLogger('mdjango').info('1 在 [1,2,3]列表中 测试成功！')  # 获取settings中配置的日志记录器