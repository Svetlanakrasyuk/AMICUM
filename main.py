import time
import pandas as pd

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    # Создаем page
    browser = playwright.firefox.launch(headless=False, slow_mo=50)
    context = browser.new_context()
    page = context.new_page()
    # Получаем данные со страницы
    page.goto("https://www.python.org/downloads/", timeout=120000)

    # Выбираем таблицу Python releases by version number по css селектору
    elem = page.locator('css=ol.list-row-container:nth-child(4)')

    # Выбираем ссылки для столбца Download
    res = elem.get_by_role('link').filter(has_text='Python').all()
    links = []
    for r in res:
        links.append("https://www.python.org" + r.get_attribute('href'))

    # Выбираем информацию для столбца Release version
    res = elem.get_by_role('link').filter(has_text='Python').all()
    release_version = []
    for r in res:
        release_version.append(r.inner_text())

    # Выбираем ссылки для столбца Release Notes
    res = elem.get_by_role('link').filter(has_text='Notes').all()
    release_notes = []
    for r in res:
        release_notes.append(r.get_attribute('href'))

    # Выбираем информацию для столбца Release date
    release_dates = []
    res = elem.locator('.release-date').all()
    for r in res:
        release_dates.append(r.inner_text())
    time.sleep(5)

    # Создаем объект Pandas для записи в файл xlsx
    df = pd.DataFrame({'Release version': release_version,
                       'Release date': release_dates,
                       'Download': links,
                       'Release Notes': release_notes})

    # Specify a writer
    writer = pd.ExcelWriter('table.xlsx', engine='xlsxwriter')

    # Write your DataFrame to a file
    df.to_excel(writer, 'Sheet1')

    # Save the result
    writer.close()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
