import streamlit as st
from streamlit_phone_number import st_phone_number
import sqlite3, os

@st.dialog(" ")
def verify_course():
    st.write("Введите свои данные, чтобы отказаться от курса обучения")
    st.dialog(title='Отказаться от курса', width="large", dismissible=True, icon=None, on_dismiss="on_dismiss")
    name_student = st.text_input("Введите ФИО обучаемого", placeholder="Введите ФИО обучаемого")
    tel = st_phone_number("Введите номер телефона: ", placeholder="+7(999)-999-99-99", default_country="RU")
    if st.button(label='Просмотреть информацию о курсе обучения', width='content', key='look'):
        if tel == None:
            st.write("Введите номер телефона")
        elif len(name_student) == 0:
            st.write("Введите ФИО обучаемого")
        else:
            with sqlite3.connect('Education.db') as db:
                cursor = db.cursor()
                sql = 'SELECT * FROM Education  WHERE Tel = ?'
                cursor.execute(sql, (str(tel),))
                zapis_on_courses = cursor.fetchall()
                if zapis_on_courses == []:
                    st.write("По этому номеру телефона и имени нет активных записей на курсы обучения")
                else:
                    for zapis_on_course in zapis_on_courses:
                        st.write(f"Вы записаны на курс: {zapis_on_course[4]}, время занятий - {zapis_on_course[5]}")

# Создание баз данных, если их еще не существует
with sqlite3.connect('Education.db') as db:
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS Education (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Tel TEXT NOT NULL,
                e_mail TEXT NOT NULL,
                course TEXT NOT NULL,
                time_course TEXT NOT NULL)
        """
    cursor.execute(sql)
with sqlite3.connect('Additional_course.db') as db:
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS Additional_course (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Tel TEXT NOT NULL,
                e_mail TEXT NOT NULL,
                course TEXT NOT NULL,
                time_course TEXT NOT NULL)
        """
    cursor.execute(sql)

# Подсчет количества записей в базе данных по каждому курсу
def count_place(name):
    global VAKANCY
    with sqlite3.connect('Education.db') as db:
        cursor = db.cursor()
        sql = 'SELECT COUNT(*) FROM Education  WHERE course = ?'
        cursor.execute(sql, (str(name),))
        free_place = cursor.fetchone()[0]
        if free_place == 0 or free_place == None:
            st.subheader(f"Свободных мест осталось 5 из 5",  text_alignment="center")
            VAKANCY = False
        elif free_place == 5:
            st.subheader(f"Набор на курс закрыт.", text_alignment="center")
            VAKANCY = True
        else:
            st.subheader(f"Свободных мест осталось {5 - int(free_place)} из 5", text_alignment="center")
            VAKANCY = False
        return free_place, VAKANCY

# запись на курсы основной группы
@st.dialog(" ")
def page_index(name_edu):
    st.write("Введите свои данные, чтобы записаться на " + name_edu)
    st.dialog(title='Записаться на ' + name_edu, width="large", dismissible=True, icon=None, on_dismiss="on_dismiss")
    name_student = st.text_input("Введите ФИО обучаемого", placeholder="Введите ФИО обучаемого")
    email = st.text_input('Введите адрес электронной почты:')
    if name_edu == 'Python':
        time_course = st.selectbox(
            "Выберите удобное для Вас время обучения:",
            ("Сб 10:00", "Сб 11:00"),
        )
    elif name_edu == 'Excel':
        time_course = st.selectbox(
            "Выберите удобное для Вас время обучения:",
            ("Пт 15:00", "Пт 16:00"),
        )
    elif name_edu == 'ОГЭ по информатике':
        time_course = st.selectbox(
            "Выберите удобное для Вас время обучения:",
            ("Сб 12:00", "Сб 13:00"),
        )
    tel = st_phone_number("Введите номер телефона: ", placeholder="+7(999)-999-99-99", default_country="RU")
    if st.button(label='Отправить', width='content', key='send'):
        if tel == None:
            st.write("Введите номер телефона")
        elif len(name_student) == 0:
            st.write("Введите ФИО обучаемого")
        else:
            with sqlite3.connect('Education.db') as db:
                cursor = db.cursor()
                sql = 'INSERT INTO Education (Name, Tel, e_mail, course, time_course) VALUES(?,?,?,?,?)'
                cursor.execute(sql, (str(name_student), str(tel), str(email), str(name_edu), str(time_course)))
                st.write(f"Вы записаны на курс {name_edu}. Время занятий - {time_course}")
    file_path = "dogovor.docx"
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            st.download_button(
                label="Скачать договор (DOCX)",
                data=f,
                file_name="dogovor.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

# Заявка на дополнительные курсы
@st.dialog(" ")
def additional_course(name_edu):
    st.write("Введите свои данные, чтобы записаться на дополнительный курс " + name_edu)
    st.dialog(title='Записаться на ' + name_edu, width="large", dismissible=True, icon=None, on_dismiss="on_dismiss")
    name_student = st.text_input("Введите ФИО обучаемого", placeholder="Введите ФИО обучаемого")
    email = st.text_input('Введите адрес электронной почты:')
    if name_edu == 'Python':
        time_course = st.selectbox(
            "Время проведения дополнительного курса:",
            ("Пн 09:00",),
        )
    elif name_edu == 'Excel':
        time_course = st.selectbox(
            "Время проведения дополнительного курса:",
            ("Пн 10:00",),
        )
    elif name_edu == 'ОГЭ по информатике':
        time_course = st.selectbox(
            "Время проведения дополнительного курса:",
            ("Пн 11:00",),
        )
    tel = st_phone_number("Введите номер телефона: ", placeholder="+7(999)-999-99-99", default_country="RU")
    if st.button(label='Отправить', width='content', key='send_add'):
        with sqlite3.connect('Additional_course.db') as db:
            cursor = db.cursor()
            sql = 'INSERT INTO Additional_course (Name, Tel, e_mail, course, time_course) VALUES(?,?,?,?,?)'
            cursor.execute(sql, (str(name_student), str(tel), str(email), str(name_edu), str(time_course)))
            st.write(f"Вы записаны на курс {name_edu}. Время занятий - {time_course}")



st.title("Добро пожаловать!", text_alignment="center")
st.header("Вы попали на страницу, где можете выбрать подходящий для себя или своего ребенка курс по IT-направлению.", text_alignment="center")
st.header("Мы находимся по адресу: пгт.Морки ул.Механизаторов, д.10В (в здании магазина 'ФАНТ', 2 этаж)", text_alignment="center")
st.subheader("Для учебы Вам понадобится личный ноутбук и желание.", text_alignment="center")
st.subheader("Стоимость 1 занятия (45 минут) составляет 500 рублей. Количество занятий в неделю - 1. Обучение по договору.", text_alignment="center")
st.set_page_config(layout="wide")
col1, col2, col4 = st.columns(3, gap='large')

with col1:
    st.subheader('Python с нуля', text_alignment="center")
    st.image('python_logo.jpg', width=600, caption='Python')
    st.text("""Вы познакомитесь с основами языка Python, \
научитесь самостоятельно писать программный код для своего первого приложения, \
изучите дополнительные библиотеки NumPy (математические функции и работа с массивами), \
Pandas (работа с таблицами данных), изучите основы анализа данных и построите свою первую\
модель машинного обучения для предсказания результатов, а также сможете создать такой же сайт, \
на котором Вы сейчас находитесь.""", text_alignment="justify")
    count_p = count_place("Python")
    if VAKANCY:
        btn_new_course_1 = st.button('Подать заявку на дополнительную группу', width=600, key='new_course_1')
        if btn_new_course_1:
            additional_course(name_edu='Python')
    else:
        btn_1 = st.button('Записаться', width=600, key='Python')
        if btn_1:
            page_index(name_edu='Python')

with col2:
    st.subheader('Excel с нуля', text_alignment="center")
    st.image('excel_logo_2.png', width=600, caption='Excel')
    st.text("""Вы познакомитесь с основами Excel, \
научитесь создавать и грамотно структурировать рабочие книги и листы, \
работать с формулами и функциями, форматировать данные и строить наглядные диаграммы и графики, \
использовать фильтры, сортировку и сводные таблицы - для быстрой аналитики.""", text_alignment="justify")
    st.space("stretch")
    count_e = count_place('Excel')
    if VAKANCY:
        btn_new_course_2 = st.button('Подать заявку на дополнительную группу', width=600, key='new_course_2')
        if btn_new_course_2:
            additional_course(name_edu='Excel')
    else:
        btn_2 = st.button('Записаться', width=600, key='Excel')
        if btn_2:
            page_index(name_edu='Excel')

with col4:
    st.subheader('ОГЭ по информатике', text_alignment="center")
    st.image('OGE_inf_logo_3.png', width=600, caption='ОГЭ')
    st.text("""Вы подготовитесь к экзамену по информатике, научитесь решать задачи, похожие на те, что будут на экзамене, \
        научитесь решать все типы экзаменационных задач с учётом актуальных требований ФИПИ.""",
            text_alignment="justify")
    st.space("stretch")
    count_o = count_place('ОГЭ по информатике')
    if VAKANCY:
        btn_new_course_3 = st.button('Подать заявку на дополнительную группу', width=600, key='new_course_3')
        if btn_new_course_3:
            additional_course(name_edu='ОГЭ по информатике')
    else:
        btn_4 = st.button('Записаться', width=600, key='OGE')
        if btn_4:
            page_index(name_edu='ОГЭ по информатике')

verify_courses = st.button(label='Проверить свою запись на курсы', width='content', key='verify_course')

@st.dialog(" ")
def verify_course():
    st.write("Введите свои данные, чтобы отказаться от курса обучения")
    st.dialog(title='Отказаться от курса', width="large", dismissible=True, icon=None, on_dismiss="on_dismiss")
    name_student = st.text_input("Введите ФИО обучаемого", placeholder="Введите ФИО обучаемого")
    tel = st_phone_number("Введите номер телефона: ", placeholder="+7(999)-999-99-99", default_country="RU")
    if st.button(label='Просмотреть информацию о курсе обучения', width='content', key='look'):
        if tel == None:
            st.write("Введите номер телефона")
        elif len(name_student) == 0:
            st.write("Введите ФИО обучаемого")
        else:
            with sqlite3.connect('Education.db') as db:
                cursor = db.cursor()
                sql = 'SELECT * FROM Education  WHERE Tel = ?'
                cursor.execute(sql, (str(tel),))
                zapis_on_courses = cursor.fetchall()
                if zapis_on_courses == []:
                    st.write("По этому номеру телефона и имени нет активных записей на курсы обучения")
                else:
                    for zapis_on_course in zapis_on_courses:
                        st.write(f"Вы записаны на курс: {zapis_on_course[4]}, время занятий - {zapis_on_course[5]}")

if verify_courses:
    verify_course()

st.write("Телефон для связи: +7-922-282-96-15")