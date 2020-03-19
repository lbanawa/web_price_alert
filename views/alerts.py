from flask import Blueprint, render_template, request, redirect, url_for
from models.alert import Alert
from models.item import Item
from models.store import Store

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/')
def index():
    alerts = Alert.all()
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
def new_alert():
    if request.method == 'POST':
        alert_name = request.form['name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price() # get the price from the page, store it in self.price
        item.save_to_mongo()

        Alert(alert_name, item._id, price_limit).save_to_mongo()

    return render_template('alerts/new_alert.html')

# when a user accesses this endpoint, flask will take the string from the url -the alert id- and give it to us
@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
def edit_alert(alert_id):
    # go into database, retrieve alert with this id
    alert = Alert.get_by_id(alert_id)

    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])

        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('alerts/edit_alert.html', alert=alert)