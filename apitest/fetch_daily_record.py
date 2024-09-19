#!/usr/bin/python3
import requests


    """
    section of the flask app responsible for gettng data
    from the external api and update the database with the lastest
    record after querying it and fetching the last item in the database
    """
@app.route('/co2', methods=['GET'])
def fetch_co2_data():
    url = 'https://daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com/api/co2-api'
    headers = {
        'x-rapidapi-host': 'daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com',
        'x-rapidapi-key': '62f0ec2bfdmshdb1f8417ca787b3p179058jsn54953359a295'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the latest record from the database
    latest_record = CO2Record.query.order_by(CO2Record.date.desc()).first()

    # Loop through each record in the response
    for record in data:
        date_string = f"{record['year']}-{record['month']}-{record['day']}"
        # Check if the record is newer than the latest record in the database
        if latest_record is None or date_string > latest_record.date:
            co2_record = CO2Record(date=date_string, cycle=record['cycle'], trend=record['trend'])
            db.session.add(co2_record)

    db.session.commit()
    return 'New CO2 records fetched and saved!'
