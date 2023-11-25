from flask import Flask,request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from trainingmodel import trainModel
from training_Validation_insertion import train_validation
from predictFromModel import prediction
import flask_monitoringdashboard as dashboard
import json
import pandas as pd

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app=Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/",methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRouteClient():
    try:
        #if request.json['folderPath'] is not None:
        folder_path="Training_data"
            #path = request.json['folderPath']
        if folder_path is not None:
            path = folder_path
            train_valObj = train_validation(path)  # object initialization

            train_valObj.train_validation()  # calling the training_validation function

            trainModelObj = trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")


@app.route("/predict", methods=['GET','POST'])
@cross_origin()
def predictRouteCLient():
        try:
            # Request values from the HTML form
            limit_bal = float(request.form['LIMIT_BAL'])
            sex = int(request.form['SEX'])
            education = int(request.form['EDUCATION'])
            marriage = int(request.form['MARRIAGE'])
            age = int(request.form['AGE'])
            pay_0 = int(request.form['PAY_0'])
            pay_2 = int(request.form['PAY_2'])
            pay_3 = int(request.form['PAY_3'])
            pay_4 = int(request.form['PAY_4'])
            pay_5 = int(request.form['PAY_5'])
            pay_6 = int(request.form['PAY_6'])
            bill_amt1 = float(request.form['BILL_AMT1'])
            bill_amt2 = float(request.form['BILL_AMT2'])
            bill_amt3 = float(request.form['BILL_AMT3'])
            bill_amt4 = float(request.form['BILL_AMT4'])
            bill_amt5 = float(request.form['BILL_AMT5'])
            bill_amt6 = float(request.form['BILL_AMT6'])
            pay_amt1 = float(request.form['PAY_AMT1'])
            pay_amt2 = float(request.form['PAY_AMT2'])
            pay_amt3 = float(request.form['PAY_AMT3'])
            pay_amt4 = float(request.form['PAY_AMT4'])
            pay_amt5 = float(request.form['PAY_AMT5'])
            pay_amt6 = float(request.form['PAY_AMT6'])

            # Create a DataFrame
            df = {
                    "LIMIT_BAL": [limit_bal],
                    "SEX": [sex],
                    "EDUCATION": [education],
                    "MARRIAGE": [marriage],
                    "AGE": [age],
                    "PAY_0": [pay_0],
                    "PAY_2": [pay_2],
                    "PAY_3": [pay_3],
                    "PAY_4": [pay_4],
                    "PAY_5": [pay_5],
                    "PAY_6": [pay_6],
                    "BILL_AMT1": [bill_amt1],
                    "BILL_AMT2": [bill_amt2],
                    "BILL_AMT3": [bill_amt3],
                    "BILL_AMT4": [bill_amt4],
                    "BILL_AMT5": [bill_amt5],
                    "BILL_AMT6": [bill_amt6],
                    "PAY_AMT1": [pay_amt1],
                    "PAY_AMT2": [pay_amt2],
                    "PAY_AMT3": [pay_amt3],
                    "PAY_AMT4": [pay_amt4],
                    "PAY_AMT5": [pay_amt5],
                    "PAY_AMT6": [pay_amt6]
                }

            data = pd.DataFrame(df)

            pred = prediction()  # object initialization
            # predicting for dataset present in database
            result = pred.predictFromModel(data)
            # interpret the prediction result
            print(result)
            if result == 1:
                message = "The person is going to default payment."
            elif result == 0:
                message = "The person is not going to default the payment."
            else:
                print("Hello world")

            # return the message to the 'result' textarea in the form
            return render_template('index.html', prediction_result=message)

        except ValueError:
            return Response("Error Occurred! %s" % ValueError)
        except KeyError:
            return Response("Error Occurred! %s" % KeyError)
        except Exception as e:
            return Response("Error Occurred! %s" % e)

#port=int(os.getenv("Port",5001))
if __name__ == "__main__":
    app.run(debug=True)