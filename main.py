
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ua = UserAgent()
all_link = []
page = 0
user_agent = ua.random
unique = set()
options = Options()
options.add_argument(f'User-agent={user_agent}')

# получаем все блоки с классом 'media-body' и текст из него.Попутно использую Try для стабильности программы
with webdriver.Chrome(options=options) as browser:
    while page < 199:
        try:
            browser.get(f'https://www.allsamsungringtones.com/?cp_443={page}')
            WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'media-body')))
            if EC.alert_is_present()(browser):
                alert = browser.switch_to.alert
                alert.dismiss()
            for x in browser.find_elements(By.CLASS_NAME,"media-body"):
                try:
                    elem = x.find_element(By.CLASS_NAME, 'package-title').find_element(By.TAG_NAME,'a').get_attribute('href')
                    # получаю размер файла и фильтрую по нему
                    size_elem = x.text.split(' ')[-2]
                    if float(size_elem) >800:
                        all_link.append(elem)
                except Exception as b:
                    # print(b)
                    pass
            page += 1
        except Exception as e:
            # print(e)
            pass
    # прохожу по ссылкам полученым и скачиваю файлы
    for link in all_link:
        if link not in unique:
            unique.add(link)
            browser.get(link)
            WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'wpdm-download-link.btn.btn-primary')))
            browser.find_element(By.CLASS_NAME, 'wpdm-download-link.btn.btn-primary').click()





