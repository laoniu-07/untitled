from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
import re,time,random
# 引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
File_Path=r'C:\Users\Administrator\Desktop\mm.txt'
compile1=re.compile('100.00%')
compile2=re.compile('已完成：')
compile3=re.compile(r'[\r\n]+')
compile_ksxx=re.compile('开始学习')
compile_jxxx=re.compile('继续学习')
url="http://www.fsa.gov.cn/zxHome/index.html"
def open_file(file):
    with open(file,'r') as f:
        data=f.read()
    return data
class Study(Thread):
    def __init__(self,data,addr=url):
        Thread.__init__(self)
        self.data=data
        self.url=addr
        self.flag=1
        self.driver=None
        self.wait=None
        self.main_handle=None
    def waiting(self):
        self.driver.implicitly_wait(10)
    def login(self):
        time.sleep(random.uniform(1, 3))
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(4)
        self.driver.get(self.url)
        print('填充id,pw：', self.data)
        self.driver.find_element_by_id('wlxy_username').send_keys(self.data[0])
        self.driver.find_element_by_id('wlxy_password').send_keys(self.data[1])

        self.driver.find_element_by_id('checkCode').click()
        text = self.driver.find_element_by_id('checkCode').text
        print('填充验证码：', text)
        self.driver.find_element_by_id('wlxy_code').send_keys(text)
        self.driver.find_element_by_class_name('btn_index_login').click()
        self.waiting()
        self.main_handle = self.driver.current_window_handle
    def check_ndbx(self):
        print(self.data[0],'check ndbxk')
        self.driver.find_element_by_class_name('ndbxk').click()
        self.waiting()
        elements = self.driver.find_elements_by_class_name('index_dt')
        n = 0
        for i in elements:
            if compile_ksxx.search(i.text) or compile_jxxx.search(i.text):
                n += 1
        if n == 0:
            self.flag = 0
            print(self.data[0],'年度必修已经学完....')
        else:
            print(self.data[0],'年度必修。。。。')
    def chose_xxk_or_bxk(self):
        if self.flag:
            try:
                self.driver.find_element_by_class_name('ndbxk').click()
            except NoSuchElementException:
                self.driver.find_element_by_class_name('ndbxk cur').click()
            print(self.data[0],'click ndbxk')
        else:
            self.driver.switch_to.window(self.main_handle)
            self.driver.refresh()
            self.waiting()
            try:
                self.driver.find_element_by_class_name('xxk').click()
            except NoSuchElementException:
                self.driver.find_element_by_class_name('xxk cur').click()
            print(self.data[0], 'click xxk')
        time.sleep(1)
    def start_learn(self):
        try:
            self.waiting()
            self.driver.find_element_by_link_text('继续学习').click()
        except NoSuchElementException:
            self.waiting()
            self.driver.find_element_by_link_text('开始学习').click()

    def switch_handle(self):
        time.sleep(3)
        all_handles = self.driver.window_handles
        print(self.data[0],'handles:', all_handles)
        for handle in all_handles:
            if handle != self.main_handle:
                self.driver.switch_to.window(handle)
        try:
            self.driver.find_element_by_link_text('点这里').click()
            print(self.data[0],'路过点这里')
        except NoSuchElementException:
            print(self.data[0],'continue')
     #系列课程里的选择
    def chose_kcml(self):
        self.waiting()
        print(self.data[0],'find kcml ')
        elements = self.driver.find_elements_by_id('kcml')
        for i in elements:
            s = compile3.split(i.text)
            print(self.data[0],'list:', s)
            for n in s:
                is_over = compile1.search(n)
                is_link = compile2.search(n)
                if is_link:
                    if not is_over:
                        try:
                            print('正在播放：',str(n))
                            p=self.wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, str(n[:-10]))))
                            self.driver.execute_script("arguments[0].click();", p)
                            p.click()
                            p.click()
                        except  Exception as e :
                            print('......',e)
                        break
    def play(self):
        self.waiting()
        data = self.driver.find_element_by_id('playBtn').get_attribute('title')
        print(data)
        p = self.driver.find_element_by_id('playBtn')
        try:
            self.driver.execute_script("arguments[0].click();", p)
            p = self.wait.until(EC.element_to_be_clickable((By.ID, 'playBtn')))
            p.click()
        except Exception:
            p.click()
        count = random.randint(10,20)
        for i in range(count):
            print('%d,还剩:%d分钟' % (count, (count - i)))
            time.sleep(60)
        print('close', self.driver.current_window_handle)
        self.driver.close()

    def run(self):
        self.login()
        self.check_ndbx()
        #必修课是否有学完 flag=0 表示必修课已经都学完了
        while 1:
            self.chose_xxk_or_bxk()
            self.start_learn()
            self.switch_handle()
            self.chose_kcml()
            self.play()
            self.driver.switch_to.window(self.main_handle)
            self.driver.refresh()
            self.waiting()
            self.chose_xxk_or_bxk()
if __name__=='__main__':

    # 打开文件
    users=open_file(File_Path)
    #多线程
    threads=[]
    for i in re.split(r'[\r\n]+',users):
        if i:
            user=re.split(r'[\s]+',i)
            if '#'in i:
                continue
            print('user:', user)
            t=Study(user,)
            threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print('all process end...........')
