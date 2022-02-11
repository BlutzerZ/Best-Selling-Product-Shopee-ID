from math import prod
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, sys

def configure():
    while True:
        print("======[ CONFIGURE ]======")

        # MAX PRODUCT INPUT ========================================
        while True:
            try:
                max_product = int(input("Max Product Per SubCategory (default=3): ") or 3)
                break
            except ValueError:
                print("require is int 1-xxx not str")
                input('')
                continue

        # SCROLL WIDTH INPUT ===================================================
        while True:
            try:
                scroll_width = int(input("Scroll Width (default=900): ") or 900)
                break
            except ValueError:
                print("require is int 1-xxx not str")
                input('')
                continue

        # MANY SCROLL INPUT ===================================================
        while True:
            try:
                scroll = int(input("Many Scroll (default=2): ") or 2)
                break
            except ValueError:
                print("require is int 1-xxx not str")
                input('')
                continue


        # SHOW ERROR ===================================================
        while True:
            try:
                show_error = bool(input("Show Error (default=False): ") or False)
                break
            except ValueError:
                print("require is bool not str or int")
                input('')
                continue

        # PRINT RAW PRODCUT ===========================================
        while True:
            try:
                print_raw_product = bool(input("Print Raw Prodcut (default=False): ") or False)
                break
            except ValueError:
                print("require is bool not str or int")
                input('')
                continue

        
        print("Done? ")
        sure = str(input("(Y/n) : ").lower() or 'y')
        if sure == 'y':
            break
        else:
            print("Want to Edit Again?")
            sure = str(input("(Y/n) : ").lower() or 'y')
            if sure == 'y':
                continue
            else:
                print("Exiting.....")
                time.sleep(3)
                sys.exit(0)

    return max_product, scroll_width, scroll, show_error, print_raw_product

def run_driver():
    print("Running Driver....")

    user_agent = "Mozilla/5.0 (Linux; Android 10; SNE-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36"
    profile = webdriver.FirefoxProfile() 
    profile.set_preference("general.useragent.override", user_agent)
    driver = webdriver.Firefox(profile)
    driver.set_window_size(360,640)

    driver.get("https://shopee.co.id/l/category/home")

    return driver

def find_cat(driver):
    print("Generating SubCategory Url....")
    result = {}

    # LIST CAT =====================================
    listCatXpath = "//div[@class='IcWZvy']"
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, listCatXpath))
        )
    listCat = driver.find_elements_by_xpath(listCatXpath)[:-2]
    for cat in listCat:
        catTitle = cat.text
        result[catTitle] = {}
        cat.click()

        # SUB CATS =========================================
        subCatsXpath = "//a[@class='_3_XAho _15P6RK']"
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, subCatsXpath))
            )
        subCats = driver.find_elements_by_xpath(subCatsXpath)

        for subCat in subCats:
            subCatTitle = subCat.text
            subCatUrl = subCat.get_attribute('href')
            result[catTitle][subCatTitle] = subCatUrl
        
    return result

def print_result(result):
    i = 0
    for cat, subCat in result.items():
        print(f"[{i+1}] {cat}")
        i+=1
        print("=> ", end='')
        for key, url in subCat.items():
            print(f"{key}, ", end='')
        print('\n\n')

# get_best_seller(driver, "https://shopee.co.id/Loafers-Boat-Shoes-cat.11042604.11042615")

def get_best_seller(driver, url, max_product=3, scroll_width=900, scroll=2, show_error=False, print_raw_product=False):
    rawhotProduct = {}
    lastHot = 0

    driver.get(url)

    # TERLARIS BTN ===================================================
    terlarisBtnXpath = "//li[@class='stardust-tabs-header__tab']"
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, terlarisBtnXpath))
        )
    terlarisBtn = driver.find_elements_by_xpath(terlarisBtnXpath)[1]
    terlarisBtn.click()

    for i in range(scroll):
        winScroll = scroll_width * i
        driver.execute_script(f"window.scrollTo(0, {winScroll})")
        time.sleep(0.1)


    titleXpath = ".//div[@class='_2Af6Xy']"
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, titleXpath))
        )

    # PRODCUT =====================================================
    products = driver.find_elements_by_xpath("//div[@class='item-card-list__item-card-wrapper']")
    
    for product in products:
        '''
            THIS IS WILL BREAK IF MAX PRODUCT EXCEED ========================
        '''
        if len(rawhotProduct) >= max_product:
            return rawhotProduct
        '''
            ===================================================================
        '''


        try:
            productTitle = product.find_element_by_xpath(".//div[@class='_10Wbs- _2yBx9M _2RXD0_']").text
            productPrice = product.find_element_by_xpath(".//div[@class='zp9xm9 _2waD-b _2baXvo']").text
            productSold = product.find_element_by_xpath(".//div[@class='BunzPh']").text
            productOrigin = product.find_element_by_xpath(".//div[@class='_2-7Lh6']").text
            if print_raw_product:
                print(f"{productTitle} [{productPrice}] - {productSold}")

            intProductSold = productSold.replace(' terjual','').replace('RB+','0000').replace('RB','000')
            intProductSold = int(intProductSold)
            if lastHot <= intProductSold:
                lastHot = intProductSold
                rawhotProduct[productTitle] = {}
                rawhotProduct[productTitle]['Price'] = productPrice
                rawhotProduct[productTitle]['Total'] = productSold
                rawhotProduct[productTitle]['Origin'] = productOrigin

        except Exception as e:
            if show_error:
                print(e)
            continue
    return rawhotProduct

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

if __name__ == "__main__":
    
    clearConsole()
    
    max_product, scroll_width, scroll, show_error, print_raw_product = configure()
    
    driver = run_driver()
    wait = WebDriverWait(driver, 20)

    result = find_cat(driver)

    for cat, subCat in result.items():
        print(f"CATEGORY: {cat} ===============================")
        print('')
        for key, url in subCat.items():
            hotProduct = get_best_seller(
                driver=driver, 
                url=url,
                max_product=max_product,
                scroll_width=scroll_width,
                scroll=scroll,
                show_error=show_error,
                print_raw_product=print_raw_product,
                )
            #print(hotProduct)
            print(f"=> SUB-CATEGORY: {key}")
            print('')
            for product, detail in hotProduct.items():
                print(f"==> Name: {product}")
                for detailName, detailValue in detail.items():
                    print(f"===> {detailName}: {detailValue}")
                
                print('')
