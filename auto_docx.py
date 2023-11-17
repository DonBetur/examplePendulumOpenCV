import datetime
from pathlib import Path

from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage, Listing

OUTPUT_FOLDER = Path("./otchet/")
DOCX_TEMPLATE_PATH = OUTPUT_FOLDER.joinpath("automated_report_template.docx")
REPORT_OUTPUT_PATH = OUTPUT_FOLDER.joinpath("generated_report.docx")
TEMPORARY_IMAGE_PATH_PLOT = OUTPUT_FOLDER.joinpath("../results.png")
TEMPORARY_IMAGE_PATH_MARKER = OUTPUT_FOLDER.joinpath("../marker.png")
SCRIPT_TO_INSERT_PATH = OUTPUT_FOLDER.joinpath("../main.py")

# Импортируем шаблон
docx_template = DocxTemplate(DOCX_TEMPLATE_PATH)

# Импортируем картинку с сохраненным графиком в документ
image = InlineImage(docx_template, str(TEMPORARY_IMAGE_PATH_PLOT), Cm(12))
marker_image = InlineImage(docx_template, str(TEMPORARY_IMAGE_PATH_MARKER), Cm(12))

# Прочитаем код из какого-нибудь скрипта для вставки в отчёт
with open(SCRIPT_TO_INSERT_PATH, "r") as f:
    the_listing_with_newlines = f.read()

# Сопоставляем метки в документе docx с объектами Python
context = {
    "title": "ДЗ компьютерное зрение в python",
    "students": "Томаев, Никитченков, Моисеев, Обыденный, Якупов",
    "day": datetime.datetime.now().strftime("%d"),
    "month": datetime.datetime.now().strftime("%b"),
    "year": datetime.datetime.now().strftime("%Y"),
    "image": image,
    "marker": marker_image,
    "listing": Listing(the_listing_with_newlines),
}

# Render automated report
docx_template.render(context)
docx_template.save(REPORT_OUTPUT_PATH)
