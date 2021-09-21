import os
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CrawlProducts:
    def __init__(self):
        self.browser = None
        self.init_driver()

    def options_driver(self):
        CHROMEDRIVER_PATH = './chromedriver'
        WINDOW_SIZE = "1000,2000"
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument(
            '--disable-gpu') if os.name == 'nt' else None  # Windows workaround
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument(
            "--disable-feature=IsolateOrigins,site-per-process")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--ignore-certificate-error-spki-list")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControllered")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # open Browser in maximized mode
        chrome_options.add_argument("--start-maximized")
        # overcome limited resource problems
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_argument('disable-infobars')
        chrome_options.page_load_strategy = 'none'
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                  options=chrome_options
                                  )
        return driver

    def init_driver(self):
        self.browser = self.options_driver()

    def get_into_link(self, link):
        self.browser.get(link)

    def write_csv(self, content, file_name):
        with open(file_name, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(content)
        csvfile.close()

    def show_all_prods(self):
        count = 1
        sleep(0.5)
        btn = ['txtbtnmore', 'btn-light']
        for b in btn:
            try:
                while True:
                    button = self.browser.find_element_by_class_name(b)
                    self.browser.execute_script(
                        "arguments[0].click();", button)
                    try:
                        point = self.browser.find_element_by_class_name(
                            'mf-senors')
                        return count
                    except:
                        pass
                    count += 1
                    sleep(0.5)
            except:
                pass
        return count

    def show_all_categories(self):
        try:
            button = self.browser.find_element_by_class_name(
                'js--chapter-viewmore')
            self.browser.execute_script(
                "arguments[0].click();", button)
        except:
            pass

    def get_all_categories(self):
        selector = f"//a[contains(@class,'chapter-img')]"
        a_tags = self.browser.find_elements_by_xpath(selector)
        return set([link.get_attribute('href') for link in a_tags])

    def get_all_prods_link(self, url=None):
        selector = f"//a[contains(@href,'{url}')]"
        a_tags = self.browser.find_elements_by_xpath(selector)
        return set([link.get_attribute('href') for link in a_tags])

    def get_all_details_prod(self):
        try:
            title = self.browser.find_element_by_class_name('st-name').text
            price = self.browser.find_element_by_class_name(
                'st-price-main').text
            option = self.browser.find_element_by_class_name('st-select').text
            promo = self.browser.find_element_by_class_name(
                'st-boxPromo__list--more').text
            info = self.browser.find_element_by_class_name(
                'st-param').find_element_by_css_selector('ul').text
            rate = self.browser.find_element_by_class_name(
                'st-rating__link').text
            return [title, price, option, info, promo, rate]
        except Exception as e:
            pass
        try:
            title = self.browser.find_element_by_class_name('fs-dttname').text
            out_date = 'Het Hang'
            return [title, out_date]
        except Exception as e:
            pass
        return 'Unknown'

    def get_target_link(self):
        cate_links = ['https://fptshop.com.vn/dien-gia-dung',
                      'https://fptshop.com.vn/phu-kien']
        target_link = []
        for i in range(0, 2):
            self.get_into_link(cate_links[i])
            self.show_all_categories()
            cates = self.get_all_categories()
            target_link += cates,
        target_link += ['https://fptshop.com.vn/dien-thoai',
                        'https://fptshop.com.vn/may-tinh-xach-tay',
                        'https://fptshop.com.vn/apple',
                        'https://fptshop.com.vn/may-tinh-bang',
                        ],
        target_link = [j for i in target_link for j in i]
        return target_link

    def crawl(self):
        target_link = self.get_target_link()
        for link in target_link:
            self.get_into_link(link)
            # Print information into screen
            print('------------- In link: ', link)
            print('------------- Processing ...')
            sleep(1)
            url = link[link.rindex('/') + 1:]
            num_pages = self.show_all_prods()
            prods_link = list(self.get_all_prods_link(url))
            # Print information into screen
            print('------------- Total pages:', num_pages)
            print('------------- Total products:', len(prods_link))
            print(
                '######################################################################')
            for i, prod in enumerate(prods_link):
                print(f'------------- Processing product {i + 1}:', prod)
                self.get_into_link(prod)
                result = self.get_all_details_prod()
                self.write_csv(result, f'{url}.csv')
        self.browser.close()


if __name__ == '__main__':
    crawl_obj = CrawlProducts()
    crawl_obj.crawl()
