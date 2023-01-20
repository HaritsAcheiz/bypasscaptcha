from concurrent.futures.thread import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import requests
from bs4 import BeautifulSoup

def get_proxies():
    print("Collecting proxies...")
    with requests.Session() as s:
        response = s.get('https://www.us-proxy.org/')
    s.close()
    soup = BeautifulSoup(response.text, 'html.parser')
    list_data = soup.select('table.table.table-striped.table-bordered>tbody>tr')
    scraped_proxies = []
    blocked_cc = ['IR', 'RU']
    for i in list_data:
        ip = i.select_one('tr > td:nth-child(1)').text
        port = i.select_one('tr > td:nth-child(2)').text
        cc = i.select_one('tr > td:nth-child(3)').text
        if cc in blocked_cc:
            continue
        else:
            scraped_proxies.append(f'{ip}:{port}')
    print(f"{len(scraped_proxies)} proxies collected")
    return scraped_proxies

def cek_proxy(scraped_proxy):
    print(f'checking {scraped_proxy}...')
    formated_proxy = {
        "http": f"http://{scraped_proxy}",
        "https": f"http://{scraped_proxy}"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    try:
        with requests.Session() as session:
            response = session.get(url='https://www.instagram.com', proxies=formated_proxy, headers=headers,
                                   timeout=(7, 10), allow_redirects=False)
        if response.status_code == 200:
            print(f'{scraped_proxy} selected')
            result = scraped_proxy
        else:
            print(f"not working with status code: {response.status_code}")
            result = 'Not Working'
        response.close()
    except Exception as e:
        print(f"not working with {e}")
        result = 'Not Working'
    return result

def webdriver_setup(proxies=None):
    ip, port = proxies.split(sep=':')
    ff_opt = Options()
    ff_opt.add_argument('--no-sandbox')

    ff_opt.set_preference('network.proxy.type', 1)
    ff_opt.set_preference('network.proxy.socks', ip)
    ff_opt.set_preference('network.proxy.socks_port', int(port))
    ff_opt.set_preference('network.proxy.socks_version', 4)
    ff_opt.set_preference('network.proxy.socks_remote_dns', True)
    ff_opt.set_preference('network.proxy.http', ip)
    ff_opt.set_preference('network.proxy.http_port', int(port))
    ff_opt.set_preference('network.proxy.ssl', ip)
    ff_opt.set_preference('network.proxy.ssl_port', int(port))

    return webdriver.Firefox(options=ff_opt)

def login(url, login_email, password, proxies):
    user_input_loc = '/input[@name="username"]'
    user_input_loc2 = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input'
    pass_input_loc = '/input[@name="password"]'
    pass_input_loc2 = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input'
    not_now_button_loc = 'button._acan._acao._acas._aj1-'
    log_in_loc = 'button._acan._acap._acas._aj1-'

    driver = webdriver_setup(proxies=proxies[0])
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver,30)
    wait.until(ec.presence_of_element_located((By.XPATH, pass_input_loc2)))
    driver.find_element(By.XPATH, user_input_loc2).send_keys(login_email + Keys.TAB)
    driver.find_element(By.XPATH, pass_input_loc2).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, log_in_loc).click()
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, not_now_button_loc)))
    driver.find_element(By.CSS_SELECTOR, not_now_button_loc).click()

def search():
    pass

def extract():
    pass

def to_csv():
    pass


if __name__ == '__main__':
    scraped_proxies = get_proxies()
    print(scraped_proxies)
    with ThreadPoolExecutor() as executor:
        working_proxies = list(filter(lambda x: x != 'Not Working', executor.map(cek_proxy, scraped_proxies)))

    url = 'https://www.instagram.com'
    username = 'paypal4betterlife@gmail.com'
    password = 'P4yp4l48'
    login(url=url, login_email=username, password=password, proxies=working_proxies)