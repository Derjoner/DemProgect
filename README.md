В папке "DemProgect находится сама программа, а также
 - ER-диаграмма ("ER-диаграмма.pdf")
 - Скрипт БД ("furniture+companySQL.sql")

Сам проект активируется через файл "main.py".
В проекте реализованы 4 страницы:
 - Главная, где размещен список материалоров согласно макету (для подсчета требуемого материала была разработана функция "fetch_all_materials", 
   которая выбирает из БД нужные поля и считает требуемое количество)
 - Редактирование материала, где можно изменить данные материала
 - Добавление материала, где можно добавить новый материал
 - Расчет продукции, где можно расчитать сколько продукции выйдет относительно материала (в форме используются индентификаторы, а не названия согласно тз).
   Также сам метот можно воспроизвести отдельно из файла "metod_calculation.py".

П.С
Пришлось достать свой проект из папки дем экзамена, так как некорректно читался путь.
