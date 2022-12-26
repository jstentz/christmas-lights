from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(data)
    return 'Success!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)