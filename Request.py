from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# تنظیمات برای اجرای مرورگر به صورت headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # مرورگر بدون رابط گرافیکی
chrome_options.add_argument("--disable-gpu")  # برای جلوگیری از مشکلات گرافیکی
chrome_options.add_argument("--no-sandbox")  # رفع مشکلات در برخی سیستم‌ها

# راه‌اندازی وب‌درایور
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# باز کردن صفحه دیوار
url = 'https://divar.ir/s/tehran'
driver.get(url)

# انتظار برای بارگذاری کامل آگهی‌ها
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#post-list-container-id'))
)

# اسکرول خودکار برای بارگذاری آگهی‌های بیشتر
for _ in range(5):  # تعداد دفعات اسکرول بیشتر می‌شود
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # منتظر می‌مانیم تا آگهی‌ها بارگذاری شوند

# جستجو برای آگهی‌ها و استخراج قیمت و سایر اطلاعات
ads = driver.find_elements(By.CSS_SELECTOR,
                           '#post-list-container-id > div.post-list-eb562 > div > div > div > div > div > div:nth-child(2) > article > a > div > div.kt-new-post-card__body.unsafe-body-e8ec8 > div.unsafe-rows-f31f9 > div > span')

# استخراج و چاپ آگهی‌هایی که قیمت توافقی دارند
found = False
for ad in ads:
    try:
        # بررسی اینکه آیا این آگهی قیمت توافقی دارد یا خیر
        if 'توافقی' in ad.text:
            found = True
            # استخراج لینک
            link_tag = ad.find_element(By.XPATH, "./ancestor::article//a")
            link = link_tag.get_attribute('href') if link_tag else 'بدون لینک'

            # چاپ اطلاعات آگهی
            print(f'قیمت: توافقی') 
            print(f'لینک: {link}')
            print('-' * 40)
    except Exception as e:
        print(f"خطا در پردازش آگهی: {e}")

# اگر آگهی‌هایی یافت نشد
if not found:
    print("هیچ آگهی با قیمت توافقی یافت نشد.")

# بستن مرورگر
driver.quit()