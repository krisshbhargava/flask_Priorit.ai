from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/maintenance-request', methods=['GET', 'POST'])
def maintenance_request():
    if request.method == 'POST':
        # handle form submission
        student_id = request.form.get('student_id')
        building = request.form.get('building')
        category = request.form.get('category')
        description = request.form.get('description')

        # process form and redirect to success
        return redirect(url_for('success'))

    return render_template('maintenance_request.html')


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)