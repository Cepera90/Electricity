import os
import json
import numpy as np
import pandas as pd
import dill as pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime as dt

import warnings
warnings.filterwarnings("ignore")


def build_and_train():
	elec_raw = pd.read_csv('data-20200131T1110-structure-20190322T1642.csv', header=1)
	# Read csv from https://minenergo.gov.ru/opendata
	elec = elec_raw['Объем выработки электроэнергии, млрд. кВтч'].str.replace(',','.').astype(float)
	# Replace ',' on '.' for change type string to float
	elec = elec.iloc[:72]
	# Chose lines 0-47

	temp_raw = pd.read_csv('wheater_RUS.csv')
	# Read csv from http://weatherarchive.ru/Pogoda/Russia
	temp_raw['Date'] = pd.to_datetime(temp_raw['Date'], format='%Y-%m')
	# Convert string type dates to datetime
	date = temp_raw['Date']
	date = date.iloc[:72]
	temp = temp_raw['Temp']
	temp = temp.iloc[:72]

	elec_new = pd.concat([date, elec, temp], axis=1)
	# Join seies date, elec_gen, temp to DataFrame elec_new
	elec_new = elec_new.rename(columns={"Период": "Period", "Объем выработки электроэнергии, млрд. кВтч": "Elec_gen"})
	elec_new['month'] = elec_new['Date'].dt.strftime('%m')
	elec_new['month'] = elec_new['month'].astype(np.float64)

	month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	for i in range(12):
		elec_new[month_list[i]] = elec_new['month'].apply(lambda x: 1 if x == i + 1 else 0)
	elec_new = elec_new.drop('month', 1)

	column_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Temp']
	X = elec_new[column_names]
	y = elec_new['Elec_gen']
	Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=1)

	model = LinearRegression(fit_intercept=False)
	model.fit(Xtrain, ytrain)

	return(model)

if __name__ == '__main__':
	model = build_and_train()

	with open('model_v1.pk', 'wb') as file:
		pickle.dump(model, file)
