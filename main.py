import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor 

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    

@app.route('/create', methods=['GET', 'POST'])
def create():
      
    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['donor']).get()
            amount = request.form['donation']
            Donation(donor=donor, value=amount).save()

        except Donor.DoesNotExist:
            # If donor doesn't exist, create a new donor with the donation amount indicated
            new_donor = Donor(name=request.form['donor'])
            new_donor.save()
            Donation(donor=new_donor, value=request.form['donation']).save()
        
        return redirect(url_for('all')) 

    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

