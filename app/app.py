import streamlit as st
import pickle
import pandas as pd

rf_model = pickle.load(open("rf_pipe.sav", "rb"))
svm_model = pickle.load(open("svm_pipe.sav", "rb"))
nn_model = pickle.load(open("nn_pipe.sav", "rb"))

# all models to select from
all_models = {
    "Random forest": rf_model,
    "Support vector machine": svm_model,
    "Neural network": nn_model,
}

# all countries to select from
countries = [
    "US",
    "HK",
    "ES",
    "GB",
    "CA",
    "AU",
    "IT",
    "CH",
    "DE",
    "MX",
    "NZ",
    "DK",
    "JP",
    "PL",
    "SE",
    "FR",
    "NL",
    "IE",
    "SI",
    "SG",
    "BE",
    "NO",
    "GR",
    "LU",
    "AT",
]

# all categroeis/sub-categories to select from
categories = {
    "Food": [
        "Restaurants",
        "Vegan",
        "Spaces",
        "Drinks",
        "Food Trucks",
        "Farms",
        "Events",
        "Bacon",
        "Community Gardens",
        "Cookbooks",
        "Small Batch",
    ],
    "Film & Video": ["Comedy", "Documentary"],
    "Theater": ["Spaces", "Plays"],
    "Journalism": ["Print", "Video", "Photo", "Audio", "Web"],
    "Design": [
        "Interactive Design",
        "Toys",
        "Product Design",
        "Graphic Design",
        "Typography",
        "Civic Design",
        "Architecture",
    ],
    "Comics": ["Graphic Novels", "Webcomics"],
    "Music": ["Rock", "Punk", "Pop", "R&B"],
    "Technology": ["Software", "Sound"],
    "Publishing": [
        "Fiction",
        "Letterpress",
        "Literary Spaces",
        "Literary Journals",
        "Poetry",
    ],
    "Art": ["Conceptual Art"],
}


def predict_outcome(model, data):

    # build dict of data to predict from
    dict_data = {
        "country": data[0],
        "parent_name": data[1],
        "name": data[2],
        "goal_usd": data[3],
        "total_days_active": data[4],
        "launch_time": data[5],
    }

    # build dataframe and transpose to ensure data is in the right structure
    data = pd.DataFrame.from_dict(dict_data, orient="index").T

    # return prediction
    return model.predict(data)


def main():
    st.title("Predict your Kickstarter's Success!")

    current_model = st.sidebar.selectbox("Select the model you want to use", all_models)

    # get user input for inputs to the model prediction
    country = st.sidebar.selectbox("The country the Project is based in", countries)
    parent_name = st.sidebar.selectbox("Category", categories)
    name = st.sidebar.selectbox("Sub-Category", categories[parent_name])
    goal_usd = st.sidebar.text_input("target funding goal ($USD)")
    total_days_active = st.sidebar.text_input(
        "How long will the project be live? (days)"
    )
    launch_time = st.sidebar.text_input(
        "How long will the project be visible before going live? (days)"
    )

    # create button to generate prediction
    if st.button("Predict the outcome!"):
        prediction = predict_outcome(
            all_models[current_model],
            [country, parent_name, name, goal_usd, total_days_active, launch_time,],
        )
        st.write(prediction)


if __name__ == "__main__":
    main()

