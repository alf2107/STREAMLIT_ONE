import streamlit as st
from streamlit_phone_number import st_phone_number
import os
from st_supabase_connection import SupabaseConnection

# настройка соединения с БД
conn = st.connection(
    'supabase',
    type = SupabaseConnection
)
# функция проверки записи на курс
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
            zapis_on_courses = conn.table('education').select('*').eq('tel', tel).eq('name', name_student).execute()
            if zapis_on_courses.data == []:
                st.write("По этому номеру телефона и имени нет активных записей на курсы обучения")
            else:
                for zapis_on_course in zapis_on_courses.data:
                    st.write(f"Вы записаны на курс: {zapis_on_course['course']}, время занятий - {zapis_on_course['time_course']}")

# Подсчет количества записей в базе данных по каждому курсу
def count_place(name):
    global VAKANCY, VAKANCY_10, VAKANCY_11, VAKANCY_12, VAKANCY_13

    if name == 'Python':
        free_place = conn.table('education').select('*', count="exact").eq('course', name).execute()
        number_int = int(free_place.count)
        if free_place.count == 0 or free_place.count == None:
            st.markdown(f" ##### Свободных мест осталось:", text_alignment="center")
            st.markdown(f" ##### Пт 16:00 - 8 из 8", text_alignment="center")
            VAKANCY = False
        elif free_place.count == 8:
            st.markdown(f" ##### Набор на курс закрыт.", text_alignment="center")
            VAKANCY = True
        else:
            st.markdown(f" ##### Свободных мест осталось:", text_alignment="center")
            st.markdown(f" ##### Пт 16:00 - {8 - (number_int)} из 8", text_alignment="center")
            VAKANCY = False
        return number_int, VAKANCY

    if name == 'Excel':
        free_place = conn.table('education').select('*', count="exact").eq('course', name).execute()
        number_int = int(free_place.count)
        if free_place.count == 0 or free_place.count == None:
            st.markdown(f" ##### Свободных мест осталось:",  text_alignment="center")
            st.markdown(f" ##### Пт 15:00 - 8 из 8", text_alignment="center")
            VAKANCY = False
        elif free_place.count == 8:
            st.markdown(f" ##### Набор на курс закрыт.", text_alignment="center")
            VAKANCY = True
        else:
            st.markdown(f" ##### Свободных мест осталось:", text_alignment="center")
            st.markdown(f" ##### Пт 15:00 - {8 - (number_int)} из 8", text_alignment="center")
            VAKANCY = False
        return number_int, VAKANCY

    if name == 'ЕГЭ по информатике':
        free_place_12 = conn.table('education').select('*', count="exact").eq('course', name).eq('time_course', "Сб 12:00").execute()
        number_int_12 = int(free_place_12.count)
        free_place_13 = conn.table('education').select('*', count="exact").eq('course', name).eq('time_course', "Сб 13:00").execute()
        number_int_13 = int(free_place_13.count)
        if free_place_12.count == 0 or free_place_12.count == None:
            st.markdown(f" ##### Свободных мест осталось:",  text_alignment="center")
            st.markdown(f" ##### Сб 12:00 - 8 из 8", text_alignment="center")
            VAKANCY_12 = False
        elif free_place_12.count == 8:
            st.markdown(f" ##### Набор на курс (Сб 12:00) закрыт.", text_alignment="center")
            VAKANCY_12 = True
        else:
            st.markdown(f" ##### Свободных мест осталось:", text_alignment="center")
            st.markdown(f" ##### Сб 12:00 - {8 - (number_int_12)} из 8", text_alignment="center")
            VAKANCY_12 = False

        if free_place_13.count == 0 or free_place_13.count == None:
            st.markdown(f" ##### Сб 13:00 - 8 из 8", text_alignment="center")
            VAKANCY_13 = False
        elif free_place_13.count == 8:
            st.markdown(f" ##### Набор на курс (Сб 13:00) закрыт.", text_alignment="center")
            VAKANCY_13 = True
        else:
            st.markdown(f" ##### Сб 13:00 - {8 - (number_int_13)} из 8", text_alignment="center")
            VAKANCY_13 = False
        return number_int_12, number_int_13, VAKANCY_12, VAKANCY_13

    if name == 'ОГЭ по информатике':
        free_place_10 = conn.table('education').select('*', count="exact").eq('course', name).eq('time_course', "Сб 10:00").execute()
        number_int_10 = int(free_place_10.count)
        free_place_11 = conn.table('education').select('*', count="exact").eq('course', name).eq('time_course', "Сб 11:00").execute()
        number_int_11 = int(free_place_11.count)
        if free_place_10.count == 0 or free_place_10.count == None:
            st.markdown(f" ##### Свободных мест осталось:",  text_alignment="center")
            st.markdown(f" ##### Сб 10:00 - 8 из 8", text_alignment="center")
            VAKANCY_10 = False
        elif free_place_10.count == 8:
            st.markdown(f" ##### Набор на курс (Сб 10:00) закрыт.", text_alignment="center")
            VAKANCY_10 = True
        else:
            st.markdown(f" ##### Свободных мест осталось:", text_alignment="center")
            st.markdown(f" ##### Сб 10:00 - {8 - (number_int_10)} из 8", text_alignment="center")
            VAKANCY_10 = False

        if free_place_11.count == 0 or free_place_11.count == None:
            st.markdown(f" ##### Сб 11:00 - 8 из 8", text_alignment="center")
            VAKANCY_11 = False
        elif free_place_11.count == 8:
            st.markdown(f" ##### Набор на курс (Сб 11:00) закрыт.", text_alignment="center")
            VAKANCY_11 = True
        else:
            st.markdown(f" ##### Сб 11:00 - {8 - (number_int_11)} из 8", text_alignment="center")
            VAKANCY_11 = False
        return number_int_10, number_int_11, VAKANCY_10, VAKANCY_11

# запись на курсы основной группы
@st.dialog(" ")
def page_index(name_edu):
    st.write("Введите свои данные, чтобы записаться на " + name_edu)
    st.dialog(title='Записаться на ' + name_edu, width="large", dismissible=True, icon=None, on_dismiss="on_dismiss")
    name_student = st.text_input("Введите ФИО обучаемого", placeholder="Введите ФИО обучаемого")
    if name_edu == 'Python':
        time_course = st.selectbox(
            "Время проведения занятия:",
            ("Пт 16:00",),
        )
    elif name_edu == 'Excel':
        time_course = st.selectbox(
            "Время проведения занятия:",
            ("Пт 15:00",),
        )
    elif name_edu == 'ОГЭ по информатике':
        if VAKANCY_10:
            time_course = st.selectbox(
                "Время проведения занятия:",
                ("Сб 11:00",),)
        elif VAKANCY_11:
            time_course = st.selectbox(
                "Время проведения занятия:",
                ("Сб 10:00",),)
        else:
            time_course = st.selectbox(
                "Выберите удобное для Вас время обучения:",
                ("Сб 10:00", "Сб 11:00"),
        )
    elif name_edu == 'ЕГЭ по информатике':
        if VAKANCY_12:
            time_course = st.selectbox(
                "Время проведения занятия:",
                ("Сб 13:00",),)
        elif VAKANCY_13:
            time_course = st.selectbox(
                "Время проведения занятия:",
                ("Сб 12:00",),)
        else:
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
            new_row = {
                    "name": name_student,
                    "tel": tel,
                    "course": name_edu,
                    "time_course": time_course
                }
            conn.table("education").insert(new_row).execute()
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
    if name_edu == 'Python':
        time_course = st.selectbox(
            "Время проведения дополнительного курса:",
            ("Пн 16:00",),
        )
    elif name_edu == 'Excel':
        time_course = st.selectbox(
            "Время проведения дополнительного курса:",
            ("Пн 17:00",),
        )
    elif name_edu == 'ОГЭ по информатике':
        time_course = st.selectbox(
            "Время проведения дополнительного курса:",
            ("Пн 14:00",),
        )
    elif name_edu == 'ЕГЭ по информатике':
        time_course = st.selectbox(
            "Время проведения дополнительного курса:",
            ("Пн 15:00",),
        )
    tel = st_phone_number("Введите номер телефона: ", placeholder="+7(999)-999-99-99", default_country="RU")
    if st.button(label='Отправить', width='content', key='send_add'):
        new_row = {
            "name": name_student,
            "tel": tel,
            "course": name_edu,
            "time_course": time_course
        }
        conn.table("additional_course").insert(new_row).execute()
        st.write(f"Вы записаны на курс {name_edu}. Время занятий - {time_course}")


st.title("Добро пожаловать!", text_alignment="center")
st.header("Вы попали на страницу, где можете выбрать подходящий для себя или своего ребенка курс по IT-направлению.", text_alignment="center")
st.header('''Мы находимся по адресу: пгт.Морки ул.Механизаторов, д.10В (в здании магазина "ФАНТ", 2 этаж)''', text_alignment="center")
st.subheader("Для учебы Вам понадобится личный ноутбук и желание.", text_alignment="center")
st.subheader("Стоимость 1 занятия (45 минут) составляет 500 рублей. Количество занятий в неделю - 1. Обучение по договору.", text_alignment="center")
st.set_page_config(layout="wide")
col4, col3, col2, col1 = st.columns(4, gap='large')

with col1:
    st.subheader('Python с нуля', text_alignment="center")
    st.image('python_logo.jpg', width=320, caption='Python')
    st.text("""Вы познакомитесь с основами языка Python, \
научитесь самостоятельно писать программный код для своего первого приложения, \
изучите дополнительные библиотеки NumPy (математические функции и работа с массивами), \
Pandas (работа с таблицами данных), изучите основы анализа данных и построите свою первую \
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
    st.image('excel_logo_2.png', width=320, caption='Excel')
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
with col3:
    st.subheader('ЕГЭ по информатике', text_alignment="center")
    st.image('EGE_inform.jpg', width=320, caption='ЕГЭ')
    st.text("""Вы подготовитесь к экзамену по информатике (ЕГЭ), научитесь решать задачи, похожие на те, что будут на экзамене,\
        научитесь решать все типы экзаменационных задач с учётом актуальных требований ФИПИ.""", text_alignment="justify")
    st.space("stretch")
    count_ege = count_place('ЕГЭ по информатике')
    if VAKANCY_12 and VAKANCY_13:
        btn_new_course_3 = st.button('Подать заявку на дополнительную группу', width=600, key='new_course_3')
        if btn_new_course_3:
            additional_course(name_edu='ЕГЭ по информатике')
    else:
        btn_3 = st.button('Записаться', width=600, key='EGE')
        if btn_3:
            page_index(name_edu='ЕГЭ по информатике')

with col4:
    st.subheader('ОГЭ по информатике', text_alignment="center")
    st.image('OGE_inf_logo_3.png', width=320, caption='ОГЭ')
    st.text("""Вы подготовитесь к экзамену по информатике (ОГЭ), научитесь решать задачи, похожие на те, что будут на экзамене,\
        научитесь решать все типы экзаменационных задач с учётом актуальных требований ФИПИ.""",
            text_alignment="justify")
    st.space("stretch")
    count_o = count_place('ОГЭ по информатике')
    if VAKANCY_10 and VAKANCY_11:
        btn_new_course_4 = st.button('Подать заявку на дополнительную группу', width=600, key='new_course_4')
        if btn_new_course_4:
            additional_course(name_edu='ОГЭ по информатике')
    else:
        btn_4 = st.button('Записаться', width=600, key='OGE')
        if btn_4:
            page_index(name_edu='ОГЭ по информатике')

verify_courses = st.button(label='Проверить свою запись на курсы', width='content', key='verify_course')

if verify_courses:
    verify_course()

st.write("Телефон для связи: +7-987-722-13-23")