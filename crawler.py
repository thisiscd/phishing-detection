import string
import time
import helium
import os
from selenium.common.exceptions import TimeoutException
from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def initialize_chrome_settings():
    '''
    initialize chrome settings
    '''
    options = webdriver.ChromeOptions()

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')  # ignore errors
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument("--headless") # FIXME: do not disable browser (have some issues: https://github.com/mherrmann/selenium-python-helium/issues/47)
    options.add_argument('--no-proxy-server')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")

    options.add_argument("--start-maximized")
    options.add_argument('--window-size=1920,1080')  # fix screenshot size
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    options.set_capability('unhandledPromptBehavior', 'dismiss')  # dismiss

    return options

def driver_loader():
    '''
    load chrome driver
    '''

    seleniumwire_options = {
        'seleniumwire_options': {
            'enable_console_log': True,
            'log_level': 'DEBUG',
        }
    }

    options = initialize_chrome_settings()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
    capabilities["unexpectedAlertBehaviour"] = "dismiss"  # handle alert
    capabilities["pageLoadStrategy"] = "eager"  # eager mode #FIXME: set eager mode, may load partial webpage

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver_path = 'E:\Project\Phishing Detection\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service, seleniumwire_options=seleniumwire_options)
    driver.set_page_load_timeout(60)  # set timeout to avoid wasting time
    driver.set_script_timeout(60)  # set timeout to avoid wasting time
    helium.set_driver(driver)
    return driver

def visit_url(driver, url):
    '''
    Visit a URL
    :param driver: chromedriver
    :param orig_url: URL to visit
    :param popup: click popup window or not
    :param sleep: need sleep time or not
    :return: load url successful or not
    '''
    try:
        driver.get(url)
        time.sleep(2)
        driver.switch_to.alert.dismiss()
        return True
    except TimeoutException as e:
        print(str(e))
        return False
    except Exception as e:
        print(str(e))
        print("no alert")
        return True
    
def make_valid_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename

if __name__ == '__main__':
    cwd = os.getcwd()
    datasets_path = os.path.join(cwd, "datasets")
    if not os.path.exists(datasets_path):
        os.mkdir(datasets_path)
        print("folder:" + datasets_path + " make success")
    else:
        print("folder:" + datasets_path + " exist")

    driver = driver_loader()
    print('Finish loading webdriver')

    url = 'https://www.baidu.com'
    folder = os.path.join(datasets_path, make_valid_filename(url))

    if not os.path.exists(folder):
        os.mkdir(folder)

        visit_success = visit_url(driver, url)
        if visit_success:
            shot_path = os.path.join(folder, 'shot.png')
            html_path = os.path.join(folder, 'html.txt')
            info_path = os.path.join(folder, 'info.txt')
            driver.save_screenshot(shot_path)
            with open(html_path, 'w', encoding='utf-8') as fw:
                fw.write(driver.page_source)
            with open(info_path, 'w', encoding='utf-8') as fw:
                fw.write(str(url))
            print('visit ' + url + ' success!')
        else:
            print('visit ' + url + ' fail!')
    
    driver.quit()
    # time.sleep(100)