import sqlite3
from random import randint

db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' убивает все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY, 
            name VARCHAR)''' 
    )
    do('''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY, 
                question VARCHAR, 
                answer VARCHAR, 
                wrong1 VARCHAR, 
                wrong2 VARCHAR)'''
    )
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id) )'''
    )
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def add_questions():
    questions = [
        ('Начнем с простого. Вы услышали, что ваш ребенок начал фолловить Билли Айлиш. Что означает «фолловить»?', 'Подписаться на его соцсети', 'Преследовать человека', 'Стать его фанатом'),
        ('Продолжая тему соцсетей. Говорить «лайк» уже не модно. Какое слово выберете, чтобы быть на одной волне с ребенком?', 'Лойс', 'Лаке',  'Дизлайк'),
        ('Пятничный вечер. Ваш ребенок отпрашивается на гиг. Чтобы решить, стоит ли его отпускать, нужно понять, что это вообще такое', 'Так это же он на концерт собрался. Мы вместе покупали билеты', 'Может, это встреча гиков? Соберутся у кого-то дома в компьютерные игры порубиться. Вроде бы ничего плохого', 'Наверное, сейчас так называют вписки — узнаю, кто будет еще и у кого дома все это происходит'),
        ('Не за горами Новый год, и современные дети с нетерпением ждут анбоксинга. Где его взять и что делать, чтобы не разочаровать ребенка?', 'Распаковывать подарки. Особенно круто, если это еще все заснять и на ютуб выложить', 'Идти на боксерский матч вместо новогодней елки', 'Валяться дома и смотреть без остановки сериалы'),
        ('На выходных вы запланировали совместный поход в кино. Ребенок выбрал «криповый фильм». Что в итоге будете смотреть?', 'Никаких положительных ассоциаций слово у меня не вызывает. Это точно ужастик', 'Что-то историческое. «Криповый» — наверняка плохой, значит будет жанр, который мой ребенок не любит', 'Очень похоже на «хиповый». Кино про моду что ли?'),
        ('Вы пришли домой с работы — в раковине гора немытой посуды, в детской беспорядок. Реакция вашего ребенка: «Ну не агрись, пожалуйста». Что бы это могло значить?', 'Не злись и не ругайся. Я сейчас все уберу', 'Не приставай ко мне со своей уборкой. Я уроки делаю', 'Не плачь. Кто ж знал, что ты так расстроишься из-за какой-то посуды'),
        ('Ребенок рассказывает, что поругался с другом, потому что тот вечно флексит. В чем причина ссоры?', 'Друг хвастается дорогими вещами', 'Друг постоянно за спиной распускает неприятные слухи', 'Друг прогуливает школу'),
        ('Ребенок говорит, что вам давно пора научиться войсить. Что это значит?', 'Отправлять голосовые сообщения в мессенджере. Все я умею, просто писать больше люблю', 'Видимо, надо записываться на уроки вокала — петь учиться', 'Кажется, мне давно пора заговорить на английском — с ребенком не поспоришь'),
        
        ('Как называется страна, в которую попали дети?', 'Нарния', 'Царство Белой Колдуньи', 'Фавния'),
        ('Как зовут фавна?', 'мистер Тумнус', 'мистер Льюис', 'мистер Думнус'),
        ('Сколько ребят?', '4', '5' , '3'),
        ('Как зовут девочку, которая первая открыла Нарнию?', 'Люси', 'Лиззи', 'Луиза'),
        ('Кто самый старший?', 'Питер', 'Эдмунд', 'Сьюзен'),
        ('Чем Белая Колдунья угостила Эдмунда?', 'рахат-лукумом', 'леденцом', 'мороженым'),
        ('Как называется замок, в котором правили Нарнией дети?', 'Кэр-Параваль', 'Пэр-Караваль', 'Кэр-Караваль'),
        ('Какими подарками одарил Санта Сьюзен?', 'рог и лук со стреламии', 'целебный напиток и кинжал', 'кинжал и рог'),
        ('Какое время года всегда в Нарнии?', 'зима', 'лето', 'осень'),
        ('Как зовут льва?', 'Аслан', 'Золотой', 'Олан'),
        
        ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного'),
        ('Каким станет зеленый утес, если упадет в Красное море?', 'Мокрым?', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Облако'),
        ('Что такое у меня в кармашке?', 'Кольцо', 'Кулак', 'Дырка')
    ]
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2) VALUES (?,?,?,?)''', questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Насколько хорошо вы знаете молодежный сленг?', ),
        ('Тест на знание Нарнии', ),
        ('Викторина-непоймикакая', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Добавить связь (y / n)?")
    while answer != 'n':
        quiz_id = int(input("id викторины: "))
        question_id = int(input("id вопроса: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y / n)?")
    close()


def get_question_after(last_id=0, vict_id=1):
    ''' возвращает следующий вопрос после вопроса с переданным id
    для первого вопроса передается значение по умолчанию '''
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content 
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id '''
    cursor.execute(query, [last_id, vict_id] )

    result = cursor.fetchone()
    close()
    return result 

def get_quises():
    ''' возвращает список викторин (id, name) 
    можно брать только викторины, в которых есть вопросы, но пока простой вариант '''
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result 

def check_answer(q_id, ans_text):
    query = '''
            SELECT question.answer 
            FROM quiz_content, question 
            WHERE quiz_content.id = ? 
            AND quiz_content.question_id = question.id
        '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()    
    # print(result)
    if result is None:
        return False # не нашли
    else:
        if result[0] == ans_text:
            # print(ans_text)
            return True # ответ совпал
        else:
            return False # нашли, но ответ не совпал

def get_quiz_count():
    ''' необязательная функция '''
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open()
    cursor.execute(query)
    result = cursor.fetchone()
    close()
    return result 

def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close()
    return rand_id

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    show_tables()
    add_links()
    show_tables()
    # print(get_question_after(0, 3))
    # print(get_quiz_count())
    # print(get_random_quiz_id())
    pass
    
if __name__ == "__main__":
    main()

