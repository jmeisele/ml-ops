from flask import Flask, request, jsonify
import numpy as np
import pickle

# my_random_forect = pickle.load(open("random_forest.pkl"), 'rb')

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return '<h1>Hello from docker compose model service #2!</h1>'

# @app.route('/predict', methods=['POST'])
# def make_prediction():
#     # Plenty of error checking here
#     data = request.get_json(force=True)

#     #Parse request json into list of values
#     predict_request = [data['a'], data['b'], data['c'], data['d']]

#     #Convert list into numpy array
#     predict_array = np.array(predict_request)

#     # Reshape into 1d array
#     predict_1d = predict_array.reshape(1, -1)

#     # Assign prediction response value to y_hat
#     y_hat = my_random_forect.predict(predict_1d)

#     # Return our prediction to the client
#     output = {'y_hat': str([y_hat[0]])}
#     return jsonify(results=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)