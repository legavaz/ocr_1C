import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from ot_tools import get_files, post_obj, request_api_1c, print_ip
import settings


def return_name(file_name):
    f_n = 'file_name'
    arr_f_n = os.path.basename(file_name).split('.')
    if len(arr_f_n) > 0:
        f_n = arr_f_n[0]
        f_n = f_n.replace(' ', '_')
    return f_n


class OcrObj:
    """
    filename = полное имя файла
    temp_path = временная директория хранения файлов
    short = короткое имя файла
    textField = результат текст полученный из изображения
    word_locathions = массив словарей с координатами
    (TODO)del_path_half = Удалить часть пути из filename при передачи данных api

    создает объект
    Параметр (filename:string)
    На входе файл pdf, на выходе текстовый файл
    """

    def __init__(self, filename, del_path_half='', force=True):
        if settings.DEBUG:
            print('Анализ:{0}'.format(filename))
        self.filename = filename
        self.textField = ''
        self.word_locathions = []
        self.del_path_half = del_path_half
        self.short = return_name(filename)
        self.ext = filename[-3:]

        if force:
            self.ocr_post()
        else:
            r_data = request_api_1c(param='files/inf/' + self.short)
            if not r_data['result']:
                self.ocr_post()
            else:
                print(self.short, 'существует')

    def ocr_post(self):
        """

        :return:
        """
        # 1)перевод файла пнг в изображение, на каждый лист свое изображение
        if self.ext in settings.pdf_ext:
            images = convert_from_path(self.filename)
        else:
            images = [Image.open(self.filename)]

        sheets = 0
        # 2)Для каждого изображения блок распознования
        # image_to_string - просто текст
        # image_to_data - с разбивкой по координатам, качеством
        for each_img in images:
            sheets += 1
            image_text = pytesseract.image_to_string(each_img, lang='rus+eng')

            # Сохраняем файл для передачи в базу
            # w, h = each_img.size
            # new_w = 680
            # new_h = int(new_w * h / w)
            # new_image = each_img.resize((new_w, new_h), Image.ANTIALIAS)
            # new_image = new_image.convert('L')
            # name_tf = '{0}\{1}{2}.png'.format(tempfile.gettempdir(), self.short, '_L')
            # new_image.save(name_tf, 'png')
            # print(name_tf)

            # удалим лишние символы
            image_text_r = ''
            for line in image_text.splitlines():
                if len(line.strip()) > 0:
                    image_text_r = image_text_r + '\n' + line

            self.textField += '#sheets:' + str(sheets) + image_text_r
            img_data = pytesseract.image_to_data(image=each_img, lang='rus+eng')

            for i, el in enumerate(img_data.splitlines()):
                if i == 0:
                    continue
                el = el.split()
                try:
                    word = el[11]
                    a = dict(x=int(el[6]), y=int(el[7]), w=int(el[8]), h=int(el[9]), conf=int(el[10]), word=word,
                             sheets=sheets,
                             is_digit=word.isdigit(),
                             is_alpha=word.isalpha(),
                             is_mix=word.isalnum())

                    self.word_locathions.append(a)
                except ValueError:
                    continue
                except IndexError:
                    continue
            post_obj(self)


def main_func():
    # pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

    r_data = request_api_1c(param='files/dir/')
    for scan_path_dir in r_data:
        files = get_files(scan_path_dir['dir'])
        qty_files = len(files)
        print('В папке {0} найдено {1} файлов.'.format(scan_path_dir, qty_files))
        i = 0
        for file in files:
            if settings.DEBUG:
                i += 1
                print('{0}/{1}'.format(i, qty_files))
            OcrObj(filename=file, del_path_half=settings.del_path_half, force=scan_path_dir['force'])


print_ip()
main_func()
