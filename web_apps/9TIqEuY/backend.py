import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dataiku import pandasutils as pdu
from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = "/Users/mmiyazaki/chromedriver"
driver = webdriver.Chrome(PATH)
driver.set_window_position(-10000,0)
driver.implicitly_wait(10) # this lets webdriver wait 10 seconds for the website to load
driver.get("https://tabelog.com/")

inputRestaurant = driver.find_element_by_id("sk")
inputRestaurant.send_keys('らぁ麺 鳳仙花')

inputArea = driver.find_element_by_id("sa")
inputArea.send_keys('東京')

driver.find_element_by_id('js-global-search-btn').click()

# driver.find_element_by_class_name('list-rst__rst-name')

list_res = driver.find_elements(By.CLASS_NAME, 'list-rst__rst-name-target')

link_ramen = list_res[0].get_attribute("href")

link_ramen



# This loads dummy data into a dataframe
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
}) \
 \
# Uncomment the following to read your own dataset
#dataset = dataiku.Dataset("YOUR_DATASET_NAME_HERE")
#df = dataset.get_dataframe()

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
