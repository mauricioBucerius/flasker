from flask import Flask, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

"""
    Running the Flask Server:
    export FLASK_ENV=development        # Setzt die Umgebungsvariable auf Entwicklung
    export FLASK_APP=python_file.py     # Flask die zu startende Python Datei
    flask run                           # startet den Flask Server 
"""

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"


# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Index route decorator
@app.route('/')
# Function for the index Route and returns a template
def index():
    first_name = "Mauricio"
    stuff = "This is <strong>Bold</strong>"
    favorite_pizza = ['Pepperoni', 'Cheese', 41]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           pizze=favorite_pizza)


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None         # Da beim Aufruf der Webseite kein Name angegeben ist
    form = NamerForm()  # Creating the Class

    # Validate Form
    if form.validate_on_submit():
        name = form.name.data   # Was als Name drin steht, wird validiert
        form.name.data = ''     # löschen für nächste Benutzung
        flash("Form Submitted Successful")               # Shows the message, which flashes
    return render_template('name.html',
                           name=name,
                           form=form)


# passing a name: localhost:5000/user/maui
@app.route('/user/<name>')
# in <> wird als dynamische Variable übergeben
# Filter Commands (mehr oder weniger Funktionen) in Jinja2:
# -> Werden mit "|" hinter die Variable geschrieben
# safe          lässt HTML Code zu, der weitergegeben werden soll
# capitalize
# lower
# upper
# title         alle Anfangsbuchstaben werden groß geschrieben
# trim
# striptags     entfernt sämtlichen HTML Code aus dem Input -> um Injections (Haker) zu vermeiden
# -> und noch viele mehr in der Dokumentation von Jinja2
def user(name):
    return render_template("user.html", user_name=name)


# Error Handling
@app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html"), 404


@app.errorhandler(500)
def error_500(e):
    return render_template("error_500.html"), 500


# startet als development Umgebung die Webseite
if __name__ == "__main__":
    app.run(debug=True, port="1337")