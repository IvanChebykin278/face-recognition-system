import os
from flask import Flask
from cfenv import AppEnv
from hdbcli import dbapi


app = Flask(__name__)
env = AppEnv()

port = int(os.environ.get('PORT', 3000))
hana = env.get_service(name='hdi_db')

@app.route('/')
def hello():
    conn = dbapi.connect(address=hana.credentials['host'], port=int(hana.credentials['port']), user=hana.credentials['user'], password=hana.credentials['password'], userkey="clientkeys")

    cursor = conn.cursor()
    cursor.execute("select CURRENT_UTCTIMESTAMP from DUMMY", {})
    ro = cursor.fetchone()
    cursor.close()
    conn.close()

    return "Current time is: " + str(ro["CURRENT_UTCTIMESTAMP"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)