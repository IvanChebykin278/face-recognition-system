def log(argument):
    switcher = {
        1:{
            "seccess":False,
            "message":'arrays with images and names is empty',
            "code": 1
        },
        2:{
            "seccess":False,
            "message":"there must be more than one value",
            "code": 2
        }
    }
    return switcher.get(argument, "Invalid input")