# Decree generator

Python script that generates a lot of decrees from samples.
Скрипт для генерации файлов приказов из образцов.



## Usage/Использование

```
$ python3 gen.py -h
usage: gen.py [-h] [-i] [-f format] [-s path] [-o path] [-v] size

Decrees generator

positional arguments:
  size                  Max size of output dir. For example: 10KB, 10MB, 10GB

options:
  -h, --help            show this help message and exit
  -i, --image           use images (logo, signature, seal) in decree
  -f format, --format format
                        formats to save (docx: d, pdf: p, jpg: j)
  -s path, --samples path
                        path to dir with samples
  -o path, --out path   path for output files
  -v, --verbose         verbose output

Example: python3 gen.py 50MB -f dp -s samples -o decrees -vv

$ python3 gen.py 50MB -i -f dp -s samples/ -o output_decrees/
2022-12-04 20:38:42.542 | WARNING  | __main__:main:169 - Generation is started...
2022-12-04 20:39:15.208 | WARNING  | __main__:generate:136 - Approximate generation time: 1.13 min.
2022-12-04 20:39:52.709 | WARNING  | __main__:generate:124 - Size of output_decrees/ dir: 53422132 bytes
2022-12-04 20:39:52.709 | WARNING  | __main__:main:171 - Generation is finished!
```



## Samples description/Описание образцов

![description one](https://github.com/cadnev/decree_gen/blob/main/raw/img/desc1.jpg)
![description two](https://github.com/cadnev/decree_gen/blob/main/raw/img/desc2.jpg)



## Структура проекта

Проект содержит в себе: 

- `raw/img`- директория, в которой содержатся изображения, 
  используемые в `README.md`; 

- `samples` – директория, в которой содержатся размеченные данные 
  для генерации приказов; 

- `.gitignore`; 

- `README.md`; 

- `auxil.py` - модуль, содержащий вспомогательные функции; 

- `change_case.py` – модуль, позволяющий склонять инструкции и 
  ответственных по падежам; 

- `consts.py` – модуль, содержащий основные константные 
  параметры, используемые при генерации; 

- `gen.py` - основной файл проекта; 

- `requirements.txt`; 

- `russian_datetime.py` - надстройка над классом `date`
  встроенного модуля `datetime`; 

- `write.py` – модуль, содержащий функции для создания файлов с 
  приказами. 



## Описание файлов

### auxil.py

Модуль с дополнительными функциями, используемыми при работе скрипта.

- ```python
  logger_config(v: int) -> None 
  # Конфигурирует логгер.
  ```

- ```python
  generate_date(standart_format=False, unixtime=False) -> str 
  # Генерирует случайную дату. 
  # standard_format задает формат даты. 
  # При unixtime=True возвращает массив, где 1-ый элемент –str, второй 
  # – float.
  ```

- ```python
  check_size_format(size: str, pat=re.compile(r"^\d*[KMG]B$")) -> str 
  # Проверяет формат параметра (аргумента) скрипта. Например, 1KB, 
  # 5MB, 10GB. При несоответствии вызывает ArgumentTypeError.
  ```

- ```python
  size_to_bytes(size: str) -> int 
  # Переводит 1KB в 1024.
  ```

- ```python
  getsize(out: str) -> int 
  # Возвращает размер файлов в директории out в байтах. 
  ```

- ```python
  to_roman(n: int) -> str 
  # Переводит арабское число в римское. 
  ```

- ```python
  add_numbering(instruction: list) -> list 
  # Нумерует каждую инструкцию, рандомно определяет уровень 
  # вложенности инструкции. 
  ```

- ```python
  check_abiword() -> int 
  # Проверяет наличие abiword в системе. Возвращает 0 при успешном 
  # выполнении или вызывает исключение. 
  ```

- ```python
  check_os() -> str 
  # Возвращает название используемой ОС.
  ```

- ```python
  parse_formats(fmts: str) -> str 
  # Проверяет расширение файлов в аргументе (параметре) скрипта на 
  # соответствие заданному формату. 
  ```

- ```python
  mm_to_px(mm: int, dpi=300) -> int 
  # Переводит из миллиметров в пиксели.
  ```

- ```python
  PDFunits_to_px(units: int, dpi=300) -> int 
  # Переводит из pdf units в пиксели. 
  ```

- ```python
  calculate_logo_coords() -> list
  # Считает координаты логотипа в документе.
  ```

- ```python
  calculate_sign_coords(tmx: int, tmy: int, new_page=False) -> list
  # Считает координаты подписи в документе. 
  ```

- ```python
  calculate_seal_coords(sign_coords: list, new_page=False) -> list 
  # Считает координаты печати в документе. 
  ```

- ```python
  calculate_borders(original_coords: list, 
      creator_and_date=False, task=False) -> list 
  # Добавляет смещение к границам текста. 
  ```

- ```python
  calculate_text_coords(pdf_path: str, data: tuple) -> list
  # Считает координаты параграфов с текстом. 
  ```

### 

### change_case.py

Модуль для изменения падежей в тексте ответственных. 



### consts.py

Модуль с основными константными параметрами, использующимися 
при генерации приказов. 

Массив `formats`содержит форматы дат, аналогичные форматам в библиотеке `datetime`. 



### gen.py

Основной файл проекта, запускается для генерации приказов. 

- ```python
  load_samples(samples_dir: str) -> tuple 
  # Загружает образцы из указанной директории. Возвращает кортеж с 
  # данными. 
  ```

- ```python
  generate(data: tuple, out: str, formats: str, size: int, 
  samples_dir: str, is_image: bool) -> None 
  # Запускает процесс генерации приказов, вызывая функции из других 
  # модулей. 
  ```

- ```python
  get_args() -> argparse.Namespace
  # Парсит флаги скрипта
  ```

- ```python
  main() -> None
  # Главная функция скритпа. 
  ```



### russian_datetime.py

Модуль, переопределяющий метод класса `date` стандартной библиотеки `datetime`. Нужен, чтобы метод `strftime` переводил месяц из числа в строку на рускком языке. 



### write.py

Модуль, содержащий функции для записи приказов в файл. 

- ```python
  extend_instruction(instruction: list, samples_dir: str) -> list 
  # Добавляет ответственных и дедлайн в задачу с шансом 25%, если они 
  # отсутствуют. 
  ```

- ```python
  write_docx(header: str, name: str, intro: str, 
  instruction: list, responsible: str, creator: str, date: 
  str, out: str, count: int, logo: str, sign: str, seal: 
  str) -> str 
  # Создает docx документ с приказом. Через аргументы функция 
  # принимает полный текст с приказом (шапка, название, введение…), 
  # директорию с выходными файлами, порядковый номер приказа, пути к 
  # изображениям (логотип, подпись, печать). Возвращает путь к 
  # сгенерированному документу. 
  ```

- ```python
  write_json(instruction: list, responsible_arr: list, 
  date: list, out: str, count: int) -> str 
  # Создает разметку для приказа. Возвращает путь к сгенерированному 
  # файлу. 
  ```

- ```python
  write_pdf_linux(docx_path: str, out: str, count: int) -> str 
  # Конвертирует docx в pdf. Возвращает путь к сгенерированному 
  # документу. 
  ```

- ```python
  write_jpg(out: str, count: int) -> None 
  # Конвертирует pdf в jpg. 
  ```

- ```python
  extract_tm(pdf_path: str, page_num: int) -> tuple 
  # Функция для метода extract_text.
  # Считает координаты последнего параграфа в документе.
  ```

- ```python
  write_coords(json_path: str, pdf_path: str) -> None 
  # Добавляет координаты изображений в pdf файле в json разметку. 
  ```



## Формат файлов с образцами

### execution_control.txt

`Контроль над исполнением распоряжения оставить за {ablt}` – на место 
фигурных скобок будет подставляться ответственный в заданном падеже (ablt 
– творительный, accs – винительный).



### responsible.json

```json
[ 
    "{Министр} {генерал} полиции Российской Федерации В.{{КОЛОКОЛЬЦЕВ}}",  
    "КОЛОКОЛЬЦЕВ",
    "В.",
    "",
    "Министр генерал полиции Российской Федерации" 
 ]
```

Первый элемент массива – строка с ответственным, которая пойдет в приказ. 

В одинарных фигурных скобках – слово из должности (профессии), у которого нужно изменить падеж. 

В двойных фигурных скобках – слово из имени, у которого нужно изменить падеж. 

Это сделано так, потому что профессии и имена склоняют две разные библиотеки. 

Следующие элементы заносятся в разметку: 

- Второй элемент массива – фамилия; 

- Третий элемент массива – имя; 

- Четвертый элемент массива – отчество; 

- Пятый элемент массива – должность. 