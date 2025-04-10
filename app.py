from flask import Flask, render_template
from justcode import get_exchange_rates

app = Flask(__name__)

@app.route('/')
def home():
    exchange_rates = get_exchange_rates()
    # get_exchange_rates("myr") buat diatas
    return render_template('subpage_idrmy.html', exchange_rates=exchange_rates)

@app.route('/cny')
def subpage_idrth():
    exchange_rates = get_exchange_rates()
    # get_exchange_rates("thb")
    return render_template('subpage_idth.html', exchange_rates=exchange_rates) #tambahkan read data excel


@app.route('/home')
def home_page():
    return render_template('home_page.html')

@app.route('/subpage_idrmy')
def subpage_idrmy():
# panggil excel (sesuai sheets)
# assign data excel ke variabel (list) (contoh : data excel cny = pandas.read_excel(sheet_name=cny))
# assign data excel ke variabel (list) (contoh : data excel myr = pandas.read_excel(sheet_name=myr))
# assign data excel ke variabel (list) (contoh : data excel jpy = pandas.read_excel(sheet_name=jpy))
# assign data excel ke variabel (list) (contoh : data excel thb = pandas.read_excel(sheet_name=thb))
# panggil index terakhir dari list tersebut (data terakhir excel A = data excel A [len(data excel A)-1])


    return render_template('subpage_idrmy.html')

@app.route('/subpage_refenitive')
def subpage_refenitive():
    return render_template('subpage_refenitive.html')


if __name__ == '__main__':
    app.run(debug=True)