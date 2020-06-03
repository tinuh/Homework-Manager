def env(var):
    vars = {
        'DEBUG': True,
        'DATABASE_NAME': 'hmanager',
        'SECRET_KEY': '6$quaimi!xgfz#swhx5!&3q0v6r#x2hhk@uy5q(5f+*83)vqg0',
        'DATABASE_HOST': 'homework.tinu.tech',
        'DATABASE_USER': 'postgres',
        'DATABASE_PWD': 'hmadmin'
    }
    return vars[var]