from flask import Flask, request, redirect, jsonify
from flaskext.mysql import MySQL

import json



from datetime import date, datetime

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'fullmeci_crm'
app.config['MYSQL_DATABASE_PASSWORD'] = 'VJKM3pbm45nvg'

app.config['MYSQL_DATABASE_SOCKET'] = None  # необходимо для соединения на windows машине
app.config['MYSQL_DATABASE_DB'] = 'annaDB'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
mysql.init_app(app)

def makeselectLang(selectedlng=-1):
    sql = 'SELECT * FROM language'
    if not cursor:
        return str(db)
    cursor.execute(sql)
    fetch = cursor.fetchall()
    if selectedlng==1:
        pass

    ret='<select id="lng_id" name="lng_id">'
    ret+='<option selected value=0>не указан</option>'
    for line in fetch:
        if line[0]==selectedlng:
            ret += f'<option selected value="{line[0]}">{line[1]}</option>'
        else:
            ret+=f'<option value="{line[0]}">{line[1]}</option>'
    ret+='</select>'
    return ret

def connectMySQL():
    global db, cursor
    try:
        db = mysql.connect()
        cursor = db.cursor()

        return db, cursor
    except  Exception as e:
        return 'Error ' + str(e), None


db, cursor = connectMySQL()


@app.route('/testConnection')
def testConnection():
    #db, cursor = connectMySQL()
    if not cursor:
        return (str(db))
    return 'Wow!!! Connection!!!'


def hw():
    return ('qqq')


@app.route('/searchBooks', methods=['POST', 'GET'])
def searchBooks():
    frm = '''
    <form action="/searchBooks" method="POST">
    <label for="bname">Name:</label><br>
    <input type="text" id="bname" name="bname" value="John">
    <br>
    <br>
    <input type="submit" value="Поиск">
    </form> 
    
    
    
    
    '''
    if request.method == 'POST':
        bname = request.form['bname']
        sql = '  SELECT * FROM books WHERE UPPER(`title`) LIKE UPPER("%'+bname+'%")   '
        #db, cursor = connectMySQL()
        if not cursor:
            return str(db)
        cursor.execute(sql)
        fetch = cursor.fetchall()
        if len(fetch)==0:
            return 'Ничего нет!!!'

        ret = '<div>Найдено '+str(len(fetch))+'</div>'+'<table border=1>'
        for line in fetch:
            ret += '<tr>'
            for col in line:
                ret += '<td>'
                ret += str(col)
                ret += '</td>'
            ret += '</tr>'
        return ret + '</table>'


    return frm

def cls(s):
    return s.replace('"', '\\"', )

@app.route('/editBooks', methods=['POST', 'GET'])
def editBooks():
    id = cls(request.form['id'])
    author = cls(request.form['author'])
    title = cls(request.form['title'])
    price = cls(request.form['price'])
    description = cls(request.form['description'])
    lng_id = cls(request.form['lng_id'])
    sql=f'UPDATE books SET `author`="{author}", `title`="{title}", `description`="{description}", `price`="{price}",`lng_id`="{lng_id}" WHERE id={id}'
    #db, cursor = connectMySQL()
    if not cursor:
        return str(db)
    try:
        cursor.execute(sql)
        db.commit()
        # return 'Запись изменена'
        return redirect('/listBooks')
    except:
        return 'Ошибка ' + sql


@app.route('/addBooks', methods=['POST', 'GET'])
def addBooks():
   if request.method =='GET':
        frm = '''  
        <form  action = "/addBooks" method="POST">
        <label for ="author" >Author:</label><br>
        <input type = "text" id = "author" name = "author"  value = "John B"><br>
        <label for ="title"> Title:</label><br>
        <input type = "text" id = "title" name = "title"  value = "Трое в лодке"><br><br>
        <label for ="price"> Price:</label><br>
        <input type = "number" id = "price" name = "price"  value = "10"><br><br>
        
        <textarea name="description" rows="10" cols="30">
            The cat was playing in the garden.
        </textarea>

        <input    type = "submit"    value = "Записать">
        </form>
        '''

        return frm

   if request.method =='POST':
       author = cls(request.form['author'])
       title = cls(request.form['title'])
       price = cls(request.form['price'])
       description = cls(request.form['description'])

       sql= f'SELECT COUNT(*) FROM books WHERE `author`= "{author}" AND `title`= "{title}"'
       #db, cursor = connectMySQL()
       if not cursor:
           return str(db)
       cursor.execute(sql)
       fetch = cursor.fetchall()
       cnt = fetch[0][0]
       if cnt>0:
           return 'Такая книга уже есть'

       sql = f'INSERT INTO books (author, title,price, description, datePubl  ) VALUES ("{author}", "{title}", "{price}","{description}", now() )  '

       #db, cursor = connectMySQL()
       if not cursor:
           return str(db)
       try:
         cursor.execute(sql)
         db.commit()
         return 'Запись добавлена'
       except:
         return 'Ошибка '+sql


@app.route('/')
def hello_world():
    rat = ""
    rat += '<br><a href="/MyPage">My page</a>'
    rat += '<br><a href="/testConnection">test Connection</a>'
    rat += '<br><a href="/listBooks">List of books</a>'
    rat += '<br><a href="/searchBooks">Search book</a>'
    rat += '<br><a href="/addBooks">Add book</a>'
    return (rat)
    print('в консоль')
    return 'Hello, World1!'


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    #db, cursor = connectMySQL()
    if not cursor:
        return str(db)
    if request.method == 'GET':
        sql = f"SELECT * FROM books WHERE id={id}"
        cursor.execute(sql)
        fetch = cursor.fetchall()
        colnames = cursor.description

        d ={}
        n=0
        for f in colnames:
            d[f[0]]=n
            n+=1


        frm = f'''  
           <form  action = "/editBooks" method="POST">
           <label for ="author" >Author:</label><br>
           <input type = "text" id = "author" name = "author"  value = '{fetch[0][d['author']]}'><br>

           <input type = "hidden" id = "id" name = "id"  value = '{fetch[0][d['id']]}'><br>

           <label for ="title"> Title:</label><br>
           <input type = "text" id = "title" name = "title"  value = '{fetch[0][d['title']]}'><br><br>
           <label for ="price"> Price:</label><br>
           <input type = "number" id = "price" name = "price"  value = '{fetch[0][d['price']]}'><br><br>
           {makeselectLang(fetch[0][d['lng_id']])}<br><br>
           <textarea name="description" rows="10" cols="30">{fetch[0][d['description']]}</textarea>

           <input    type = "submit"    value = "Редактировать">
           </form>
           '''

        return frm


    return f'Редактируем книжку {id}'

@app.route('/listBooks')
def listBooks():
    # db, cursor = connectMySQL()

    if not cursor:
        return str(db)

    sql = 'SELECT `books`.`id`, `books`.`title`, `books`.`author`, `books`.`description`,`books`.`price`,`books`.`datePubl`,  `language`.`lang` FROM books LEFT JOIN language on `language`.`id` = `books`.`lng_id`'
    cursor.execute(sql)
    fetch = cursor.fetchall()

    #####


    ret = '<table border=1>'
    for line in fetch:
        c=0
        ret += '<tr>'
        for col in line:

            ret += '<td>'

            if c == 0:
               ret += f'<a href = "/edit/{line[0]}"> {line[0]} </a>'
            else:
               ret += str(col)
            ret += '</td>'
            c+=1
        ret += '</tr>'
    return ret + '</table>'

@app.route('/MyPage')
def MyPage():
    return '''
    <form action="/AnnaAction" method="POST">
        <input type="text" name="Field1" Value="Default value">
        <input type="submit" name="Oke">
        <input type="submit" name="moke">
         
    </form>
    '''


@app.route('/AnnaAction', methods=['POST','GET'])
def AnnaAction():
    if request.method == 'POST':
        UserInput = request.form['Field1']
        if UserInput == 'Попа':
            return '<p style="color:red">Попа детектед</p>'
        return 'Welcome to AnnaAction: ' + UserInput
    else:
        return 'method post!!!: '


@app.route('/GetParam/<Id>/<Id2>', methods=['GET'])
def GetParam(Id, Id2):
    return 'Param iz ' + Id + ' ' + Id2


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1001, debug=True)

