from flask_shorty import app, db
from flask_shorty.models import Shorties
from flask_shorty.forms import FindForm, CreateForm, UpdateForm
from flask import flash, render_template, request, redirect, url_for
from datetime import datetime, timedelta

import string
import random


# Hashing Algo
def hash7():
    characters_62 = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        hash7_array = random.choices(characters_62, k=7)
        hash7_str = "".join(hash7_array)
        check_exists = Shorties.query.filter_by(short=hash7_str).first()
        if not check_exists:
            return hash7_str

def warn_expires():
    all_shorties = Shorties.query.all()
    if all_shorties:
        for shorty in all_shorties:
            shorty_expiry = shorty.expiry_time
            if shorty_expiry <= datetime.now().replace(microsecond=0) + timedelta(days=1):
                flash(f"Your link '{shorty.name}: {shorty.short}' will expire within 24 hours. To extend please manage shorties.", "warning")

def check_expiries():
    all_shorties = Shorties.query.all()
    if all_shorties:
        for shorty in all_shorties:
            shorty_expiry = shorty.expiry_time
            if shorty_expiry <= datetime.now().replace(microsecond=0):
                db.session.delete(shorty)
                db.session.commit()
                flash(f"Old link: {shorty.name}: {shorty.short} has now expired.", "danger")


@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def home():
    # Warn expires
    warn_expires()
    # Check for expiries
    check_expiries()
    # Handle FindForm
    form = FindForm()
    if request.method == "POST":
        name = request.form['name']
        shorty = Shorties.query.filter_by(name=name).first()
        not_shorty = "Sorry we couldn't find a shorty matching that name!"
        if shorty:
            return render_template('home.html', title='Get Shorty! - Home', shorty=shorty, form=form)
        elif not shorty:
            return render_template('home.html', title='Get Shorty! - Home', not_shorty=not_shorty, form=form)

    # Records Table
    return render_template('home.html', title='Get Shorty! - Home', form=form)


@app.route("/generate", methods=['POST', 'GET'])
def generate():
    # Form
    form = CreateForm()
    if request.method == "POST":

        # Check name
        name = request.form['name']
        found_name = Shorties.query.filter_by(name=name).first()
        if found_name:
            flash('Please use unique names for your short urls', 'danger')
            return render_template('generate.html', title="Generate", form=form)

        # Check long
        long = request.form['long_url']
        found_url = Shorties.query.filter_by(long=long).first()

        if found_url:
            flash('You already shortened this one. Your link should appear below', 'warning')
            return redirect(url_for('display_shorty', url=found_url.short))
        else:
            short_url = hash7()
            # set expiry_time
            expiry_time = form.expiry_time.data
            time_now = datetime.now().replace(microsecond=0)

            if expiry_time:
                if expiry_time <= time_now:
                    flash(
                        'Time travel to the past has not yet been invented!', 'danger')
                    return render_template('generate.html', title="Generate", form=form)
                
                new_record = Shorties(name, long, short_url, expiry_time, time_now)
                db.session.add(new_record)
                db.session.commit()
                flash('Shorty successfully generated with custom expiry time', 'success')
                return redirect(url_for('display_shorty', url=short_url))
            else:    
                new_record = Shorties(name, long, short_url, (time_now + timedelta(days=3)), time_now)
                db.session.add(new_record)
                db.session.commit()
                flash('Shorty successfully generated', 'success')
                return redirect(url_for('display_shorty', url=short_url))
    else:
        return render_template('generate.html', title='Generate', form=form, legend='Generate Shorty')


@app.route("/display/<url>")
def display_shorty(url):
    return render_template('display_shorty.html', display_shorty=url, title='Your latest shorty')


# Make shorty work
@app.route('/<short_url>')
def redirect_to_long(short_url):
    long_url = Shorties.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1 class="text-danger">The Url does not exist</h1>'


@app.route("/all_urls")
def all_urls():
    # Warn expires
    warn_expires()
    # Check expiries
    all_shorties = Shorties.query.all()
    for shorty in all_shorties:
        shorty_expiry = shorty.expiry_time
        if shorty_expiry <= datetime.now().replace(microsecond=0):
            db.session.delete(shorty)
            db.session.commit()
            flash(f"Old link: {shorty.name}: {shorty.short} has expired", "danger")
    # All records Table
    all_records = Shorties.query.order_by(Shorties.id)
    return render_template('all_urls.html', title='Manage Shorties', all_records=all_records)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    shorty = Shorties.query.get_or_404(id)
    current_shorty = shorty.short
    current_long = shorty.long
    # Form
    form = UpdateForm()
    form.name.data = shorty.name
    form.expiry_time.data = shorty.expiry_time

    if request.method == 'POST':
        expiry_time = request.form['expiry_time']
        time_now = datetime.now().replace(microsecond=0)
        # Check Date
        name = request.form['name']
        expiry_time_obj = datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S')
        if expiry_time_obj <= time_now:
            flash('Time Travel has not yet been invented. The amount spacetime would need to be warped is mind-boggling!', 'danger')
            return render_template('update.html', title="Update Shorty", long=current_long, form=form, legend=current_shorty)

        shorty.name = name
        shorty.expiry_time = expiry_time
        db.session.commit()
        flash('Shorty successfully updated!', 'success')
        return redirect(url_for('all_urls'))
    else:
        return render_template('update.html', title='Update Shorty', long=current_long, form=form, legend=current_shorty)


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    if request.method == "POST":
        # url = Shorties.query.get_or_404(id)
        url = Shorties.query.filter_by(id=id).first()
        db.session.delete(url)
        db.session.commit()
        flash(f'The short link with id {id} has been deleted!', 'success')
        return redirect(url_for('all_urls'))