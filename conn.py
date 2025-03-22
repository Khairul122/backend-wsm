import pymysql

db_config = {
    "host": "bex01irce3djnhpwjand-mysql.services.clever-cloud.com",
    "user": "uo8juyg29uxlsbav",
    "password": "0X733MLaud2qAcrzJCoB",
    "database": "bex01irce3djnhpwjand",
    "port": 3306
}

def get_connection():
    return pymysql.connect(**db_config)
