import streamlit as st
import requests as req
import pandas as pd

from datetime import datetime

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

# url = 'https://taxifare.lewagon.ai/predict'
url = 'https://txx-345342954465.europe-west1.run.app/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''

# 1. ask the user to select the parameters of the ride
pickup_date = st.date_input("Enter pickup date:", value=datetime.today())
pickup_time = st.time_input("Enter pickup time:", value=datetime.now().time())
pickup_longitude = st.number_input("Enter pickup longitude:", value=0.0)
pickup_latitude = st.number_input("Enter pickup latitude:", value=0.0)
dropoff_longitude = st.number_input("Enter dropoff longitude:", value=0.0)
dropoff_latitude = st.number_input("Enter dropoff latitude", value=0.0)
passenger_count = st.number_input("Enter passenger count", min_value=1, max_value=8, value=1)

pickup_datetime = datetime.combine(pickup_date, pickup_time)

# 2. build a dictionary
params = {
    "pickup_datetime": pickup_datetime.strftime('%Y-%m-%d %H:%M:%S'),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

df = pd.DataFrame(
[[pickup_latitude,pickup_longitude],
 [dropoff_latitude,dropoff_longitude]],
columns=["lat", "lon"],)
st.map(df)

if st.button("Get Fare Prediction"):
    try:
        # 3. call the API
        response = req.get(url, params=params)
        data = response.json()

        # 4. retrieve the prediction and display it
        fare = data.get("fare", "Error retrieving fare")
        print(data)
        st.success(f"The predicted fare is: ${fare}")

    except Exception as e:
        st.error(f"Error occurred: {e}")
