from flask import Flask, render_template
from justcode import get_exchange_rates

app = Flask(__name__)

@app.route('/')
def home():
    exchange_rates = get_exchange_rates()
    return render_template('subpage_idrmy.html', exchange_rates=exchange_rates)

@app.route('/home')
def home_page():
    return render_template('home_page.html')

@app.route('/subpage_idrmy')
def subpage_idrmy():
    return render_template('subpage_idrmy.html')

@app.route('/subpage_refenitive')
def subpage_refenitive():
    return render_template('subpage_refenitive.html')


if __name__ == '__main__':
    app.run(debug=True)