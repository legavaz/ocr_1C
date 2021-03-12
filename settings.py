

DEBUG = True

pdf_ext = ['pdf']

# tesseract
tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# часть пути для удаления из полного имени файла
del_path_half = r"\\l-pack\net\Сканер"

# ИНТЕГРАЦИЯ С 1С
# Получение списка всех контрагентов
# http://localhost/danv_copy_lpack_buh3/hs/Customer/all

URL_1C_API = 'http://192.168.21.145/analitic/hs/'
LOGIN_1C = '1CV8'
PASSWORD_1C = '1CV8'


def settings():
    return None