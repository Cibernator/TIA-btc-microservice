from flask import Flask, jsonify
import data_fetcher

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    data = data_fetcher.fetch_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
