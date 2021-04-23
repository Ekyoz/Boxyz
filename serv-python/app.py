from flask import Flask, request, render_template, session, redirect, jsonify
import requests
import json
from remote import addremote, delremote, remotenum, access

app = Flask(__name__)
url="http://192.168.1.29:3000/assistant"
num = remotenum()

#--------------------------------------------Home----------------------------------------#
@app.route('/remote', methods=['GET'])
def remote():
    info = request.args.get('info')
    with open(access, "r") as f:
        remote = json.load(f)
    if info == "num":
        return str(num)
    if info == "json":
        return jsonify(str(remote))
    if info is None or info == "":
        return 'Argument missing!'

@app.route('/add_remote', methods = ['GET'])
def add_remote():
    mac = request.args.get('mac')
    name = request.args.get('name')
    func_on = request.args.get('func_on')
    func_off = request.args.get('func_off')
    ip = request.args.get('ip')
    with open(access, "r") as f:
        remote = json.load(f)
    if mac in remote:
        return 'Already exist'
    if mac and name and func_off and func_on and ip is not None:
        addremote(mac, name, func_on, func_off, ip)
        return 'Ok, remote was added with mac: ' + mac +'.'
    elif mac or name or func_off or func_on or ip is None:
        return 'Error, Argument missing! \n Check this!'


@app.route('/del_remote', methods=['GET'])
def del_remote():
    key = request.args.get('keys')
    with open(access, "r") as f:
        remote = json.load(f)
    try:
        if key in remote.keys():
            delremote(key)
            return 'Ok, remote was deleted with mac' + key +'.'
        else:
            return 'This remote not existe!'
    except:
        return 'Error! Check argument.'


@app.route('/button', methods = ['GET'])
def button():
    status = request.args.get('stat')
    mac = request.args.get('mac')
    with open(access, "r") as f:
        remote = json.load(f)
    if mac in num:
        if status == "on":
            requests.post(url=url, data=remote[mac]["func_on"])
            return 'Ok, turn on!'
        elif status == "off":
            requests.post(url=url, data=remote[mac]["func_off"])
            return 'Ok, turn off!'
    else:
        return 'Remote not exist!'



if __name__ == "__main__":
    app.run(port=3030, host='0.0.0.0', debug=True)

