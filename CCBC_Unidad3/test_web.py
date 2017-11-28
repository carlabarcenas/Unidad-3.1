from flask import Flask, render_template, request, redirect, escape
from module_cilindro import area
from config import config
import psycopg2
from use_database import UseDatabase

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    with open('newtest.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    connection = None
    params = config()

    with UseDatabase(params) as cursor:

        _SQL = """INSERT INTO log
              (phrase, letters, ip, browser_string, results)
              VALUES
              (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['r'],
                              req.form['h'],
                              req.remote_addr,
                              req.user_agent.browser,
                              str(res)))

@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('newtest.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Radio', 'Altura', 'Direccion', 'Usuario', 'Resultado')
    return render_template('viewlog.html', the_title='Calculo del area de un cilindro', the_row_titles=titles, the_data=contents,)

@app.route('/viewlogdb')
def view_log_db() -> 'html':
    params = config()
    with UseDatabase(params) as cursor:
        _SQL = """select phrase, letters, ip, browser_string, results from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Radio', 'Altura', 'Direccion', 'Usuario', 'Resultado')
    return render_template('viewlog.html',
                           the_title='Calculo del area de un cilindro',
                           the_row_titles=titles,
                           the_data=contents,)

@app.route('/')
def hello() -> '302':
    return redirect('/entry')


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Calculo del area de un cilindro')


@app.route('/exec_equation', methods=['GET', 'POST'])
def execute() -> 'html':
    r = int(request.form['r'])
    h = int(request.form['h'])
    title = 'Calculo del area de un cilindro'
    result = area(r, h)
    log_request(request, result)
    return render_template('result.html',
                           the_title=title,
                           the_r=r,
                           the_h=h,
                           the_result=result, )


if __name__ == '__main__':
    app.run('localhost', 5001, debug=True)
