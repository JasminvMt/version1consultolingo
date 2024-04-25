# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import requests
import random

# Function to fetch population data
def fetch_population_data():
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tps00001?format=JSON&time=2023&geo=BE&geo=BG&geo=CZ&geo=DK&geo=DE&geo=EE&geo=IE&geo=EL&geo=ES&geo=FR&geo=HR&geo=IT&geo=CY&geo=LV&geo=LT&geo=LU&geo=HU&geo=MT&geo=NL&geo=AT&geo=PL&geo=PT&geo=RO&geo=SI&geo=SK&geo=FI&geo=SE&indic_de=JAN&lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        population_values = data['value']
        geo_index_to_code = {str(v): k for k, v in data['dimension']['geo']['category']['index'].items()}
        geo_code_to_name = data['dimension']['geo']['category']['label']
        population_data = {geo_code_to_name[geo_index_to_code[k]]: v for k, v in population_values.items() if k in geo_index_to_code}
        return population_data
    else:
        st.error(f"Failed to retrieve data: {response.status_code}")
        return {}

# Function to generate a question
def generate_question(population_data):
    if not population_data:
        return "No data available to generate a question", [], None
    correct_country, correct_population = random.choice(list(population_data.items()))
    incorrect_answers = set()
    while len(incorrect_answers) < 3:
        method = random.choice(['percent', 'fixed', 'factor'])
        if method == 'percent':
            adjustment = random.choice([0.9, 0.95, 1.05, 1.1])
            new_population = int(correct_population * adjustment)
        elif method == 'fixed':
            adjustment = random.randint(100000, 500000)
            new_population = correct_population + random.choice([-1, 1]) * adjustment
        elif method == 'factor':
            adjustment = random.choice([0.85, 0.9, 0.95, 1.05, 1.1, 1.2])
            new_population = int(correct_population * adjustment)
        if new_population != correct_population:
            incorrect_answers.add(new_population)
    options = list(incorrect_answers) + [correct_population]
    random.shuffle(options)
    question = f"What is the population of {correct_country}?"
    return question, options, correct_population

# Streamlit interface
st.title('Population Quiz')
if 'data' not in st.session_state:
    st.session_state.data = fetch_population_data()

if st.session_state.data:
    question, options, correct_answer = generate_question(st.session_state.data)
    st.subheader(question)
    option_indices = [f"{idx + 1}: {option}" for idx, option in enumerate(options)]
    user_choice = st.radio("Choose the correct answer:", option_indices)
    
    if st.button("Submit"):
        if int(user_choice.split(': ')[0]) == options.index(correct_answer) + 1:
            st.success("Correct!")
        else:
            st.error("Incorrect!")
        st.write(f"The correct population is {correct_answer}.")
else:
    st.error("Unable to load population data.")
    
