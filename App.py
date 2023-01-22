from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'frasquito'
app.config['MYSQL_PASSWORD'] = 'XVOUf8aAh6rZjO6FKnE0'
app.config['MYSQL_DB'] = 'quedelibros'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM books')
  data = cur.fetchall()
  return render_template('index.html', books = data)

@app.route('/add_book', methods=['POST'])
def add_book():
  if request.method =='POST':
    booktitle = request.form['booktitle']
    author = request.form['author']
    genre = request.form['genre']
    startdate = request.form['startdate']
    enddate = request.form['enddate']
    score = request.form['score']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO books (booktitle, author, genre, startdate, enddate, score) VALUES (%s, %s, %s, %s, %s, %s)', (booktitle, author, genre, startdate, enddate, score))
    mysql.connection.commit()
    flash('Se añadió un nuevo libro')
    return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_book(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM books WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-book.html', book = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_book(id):
    if request.method == 'POST':
      booktitle = request.form['booktitle']
      author = request.form['author']
      genre = request.form['genre']
      startdate = request.form['startdate']
      enddate = request.form['enddate']
      score = request.form['score']
      cur = mysql.connection.cursor()
      cur.execute("""
        UPDATE books
        SET booktitle = %s,
            author = %s,
            genre = %s,
            startdate = %s,
            enddate = %s,
            score = %s
        WHERE id = %s
        """, (booktitle, author, genre, startdate, enddate, score, id))
      mysql.connection.commit()
      flash('Se han actualizado los datos del libro')
      return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_book(id):
  cur = mysql.connection.cursor()
  cur.execute('DELETE FROM books WHERE id = {0}'.format(id))
  mysql.connection.commit()
  flash('Se ha eliminado el libro')
  return redirect(url_for('Index'))

if __name__ == '__main__':
  app.run(port = 3020, debug =  True)