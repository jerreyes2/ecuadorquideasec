import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# mysqlclient

MYSQL_LOCAL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bd_ecuadorquideas_ec',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',

    }
}

MYSQL_REMOTO = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'admin_ecuadorquideasec',
        'USER': 'admin_aquiles',
        'PASSWORD': '6Wa8!S7VqAk4',
        'HOST': '18.223.106.228',
        'PORT': '3306'

    }

}