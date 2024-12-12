from database.config import start_db, destroy_db
from database.config import session
from database.models import User, Recipe

start_db()
user = session.query(User).first()

recipe = Recipe(name='papa', user_id=user.id)
recipe2= Recipe(name='miojo', user_id=user.id)
session.add(recipe)
session.add(recipe2)
session.commit()

receita1 = session.query(Recipe).first()
print(receita1)
print(receita1.usuario)
print(receita1.user_id)

print(receita1.usuario.id)





destroy_db()