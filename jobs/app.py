from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dashboard import dashapp


#added in the dash application 3.6.20

PATH = "db/jobs.sqlite"
#app = Flask(__name__)
server = Flask(__name__)

#creating dash app
#app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')

#calls the function in the dashapp file to start up the dash app
app = dashapp.Add_Dash(server)

#rending dash app
@app.route('/dash')
def renderDash():
    return render_template('dashboard.html', dash_url=dashapp.url_base)

##renders the index file
@server.route('/')
@server.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


##new job form
@server.route('/newjob', methods=['GET', 'POST'])
def newjob():
    employers = execute_sql('SELECT * FROM employer')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        salary = str(request.form['salary'])
        #salary = salary.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+KkMmBb"})
        employerid = request.form['employer']

        execute_sql('INSERT INTO job ( title, description, salary, employer_id) VALUES (?, ?, ?, ?)',
                    (title, description, salary, employerid),
                    commit=True)

        redirect(url_for('jobs'))

    return render_template('newjob.html', employers=employers)


@server.route('/job/<job_id>')
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?',
                      [job_id],
                      single=True
                      )
    return render_template('job.html', job=job)


@server.route('/employer/<employer_id>')
def employer(employer_id):
    employer = execute_sql('SELECT * FROM employer WHERE id=?',
                           [employer_id],
                           single=True)
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?',
                       [employer_id])

    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?',
                          [employer_id])
    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)


@server.route('/employer/<employer_id>/review', methods=['GET', 'POST'])
def review(employer_id):
    if request.method == 'POST':
        review = request.form['review']
        rating = request.form['rating']
        title = request.form['title']
        status = request.form['status']
        date = datetime.datetime.now().strftime("%m/%d/%Y")

        execute_sql('INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)',
                    (review, rating, title, date, status, employer_id),
                    commit=True)
        redirect(url_for('employer', employer_id=employer_id))

    return render_template('review.html', employer_id=employer_id)


def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection


def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit is True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results


##Called anytime the application is "torndown", should be where the connection is closed
@server.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()
    return connection


if __name__ == "__main__":
    app.run(debug = True)