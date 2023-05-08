import filecmp
import os
import time
import openpyxl

import allure

from lib.monolith.constants.constant_data import TEST_FILE_XLSX_PATH
from page_objects.monolith.pages.common import BasePage


class DownloadFile(BasePage):
    DOWNLOAD_ITEM = '//downloads-item'
    FILE_LINK = 'id("file-link")'
    CHROME_DOWNLOAD_TAB_URL = 'chrome://downloads/'

    def __init__(self, driver=None):
        super(DownloadFile, self).__init__(driver)
        self.driver = driver

    @allure.step('Open tab with download files')
    def open_download_page(self):
        self.open_page(self.CHROME_DOWNLOAD_TAB_URL)

    @allure.step('Check that file {file_name} downloaded')
    def assert_that_file_downloaded(self, file_name):
        download_files = []
        for _ in range(5):
            download_files = self.driver.execute_script('''
                    var items = document.querySelector('downloads-manager')
                    .shadowRoot.getElementById('downloadsList').items;
                    if (items.every(e => e.state === "COMPLETE"))
                        items.map(e => e.fileUrl || e.file_url);
                        return items;
                    ''')
            if len(download_files) > 0:
                break
            else:
                print('Couldn`t download file.')
                time.sleep(1)
        try:
            assert file_name in download_files[0]['filePath'], \
                f'Couldn`t download file "{file_name}", but found {download_files[0]["filePath"]}'
        except IndexError:
            assert False, 'Didn`t download any file.'

    @allure.step('Check that downloaded file is equal to the uploaded one')
    def assert_that_document_downloaded(self, file_for_upload, downloaded_file):
        uploaded_file = TEST_FILE_XLSX_PATH.format(file_for_upload)
        self.wait_for_download_file_in_dir(downloaded_file)
        assert os.path.exists(downloaded_file), f'File doesn`t exist "{downloaded_file}"'
        assert filecmp.cmp(uploaded_file, downloaded_file, shallow=False), 'Files are not the same!'
        os.remove(downloaded_file)

    def wait_for_download_file_in_dir(self, file_path):
        flag = False
        for _ in range(5):
            flag = True if os.path.exists(file_path) else time.sleep(1)
            if flag:
                break
        assert flag, f'File wasnt`t downloaded "{file_path}"'

    @allure.step('Check that downloaded file equals the test dataset')
    def assert_that_downloaded_file_equals_test_dataset(self, xlsx_file_path, test_dataset):
        self.wait_for_download_file_in_dir(xlsx_file_path)
        assert os.path.exists(xlsx_file_path), f'File doesn`t exist "{xlsx_file_path}"'

        xlsx_sheet = openpyxl.load_workbook(xlsx_file_path)
        parsed_xlsx = xlsx_sheet.active

        for row in test_dataset:
            for col in row:
                #  I am going through the test_dataset cell by cell and compare it with corresponding parsed xlsx cell
                row_index = test_dataset.index(row)
                col_index = row.index(col)

                test_dataset_value = test_dataset[row_index][col_index]

                if test_dataset_value == "skip assert":
                    continue
                else:
                    # For some reason, the first row or column integer in openpyxl parse is 1, not 0.
                    parsed_xlx_value = parsed_xlsx.cell(row=row_index + 1, column=col_index + 1).value

                    assert test_dataset_value == parsed_xlx_value, \
                        f'Downloaded xlsx cell "{row_index}","{col_index}" value is "{parsed_xlx_value}" ' \
                        f'when should be same as dataset cell value "{test_dataset_value}"'

        os.remove(xlsx_file_path)
