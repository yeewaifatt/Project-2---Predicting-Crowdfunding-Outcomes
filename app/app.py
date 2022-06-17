import streamlit as st
import pickle
import pandas as pd

model = pickle.load(open("rf_pipe.sav", "rb"))


def predict_outcome(data):

    # form the correct data structure for the model
    dict_data = {
        "country": data[0],
        "parent_name": data[1],
        "name": data[2],
        "goal_usd": data[3],
        "total_days_active": data[4],
        "launch_time": data[5],
    }

    data = pd.DataFrame.from_dict(dict_data, orient="index").T

    return model.predict(data)


def main():
    st.title("Predict your Kickstarter's Success!")

    # get user input for inputs to the model prediction
    country = st.text_input("The country the Project is based in")
    parent_name = st.text_input("Category")
    name = st.text_input("Sub-Category")
    goal_usd = st.text_input("target funding goal")
    total_days_active = st.text_input("date of project termination")
    launch_time = st.text_input("date the project will go live")

    # create button to generate prediction
    if st.button("Predict the outcome!"):
        prediction = predict_outcome(
            [
                country,
                parent_name,
                name,
                goal_usd,
                total_days_active,
                launch_time,
            ]
        )
        st.write(prediction)


if __name__ == "__main__":
    main()

