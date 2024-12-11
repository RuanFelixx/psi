from database.config import start_db, destroy_db
from database.models import User
from database.config import session
from sqlalchemy import text


start_db()

#user = User(name='Marquin')
#print(user)

sql = text("SELECT * FROM users")
usuarios1 = session.execute(sql).all()
print(type(usuarios1))
usuarios2 = session.scalars(sql)
for user in usuarios2:
    print(user)

destroy_db()