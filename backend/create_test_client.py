import asyncio
from app.db.database import get_db
from app.models.animal import Animal
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_client():
    """Cria um cliente de teste para login"""
    
    # Obter sessão do banco
    db_gen = get_db()
    db: Session = next(db_gen)
    
    try:
        # Buscar um animal sem email para transformar em cliente
        animal = db.query(Animal).filter(Animal.email.is_(None)).first()
        
        if not animal:
            print("❌ Nenhum animal encontrado para transformar em cliente")
            return
        
        # Hash da senha
        hashed_password = pwd_context.hash("123456")
        
        # Atualizar o animal com dados de cliente
        animal.email = "teste@cliente.com"
        animal.senha = hashed_password
        animal.tutor_name = "João Silva"
        animal.phone = "11999999999"
        animal.client_active = True
        
        db.commit()
        
        print("✅ Cliente de teste criado com sucesso!")
        print(f"📧 Email: teste@cliente.com")
        print(f"🔑 Senha: 123456")
        print(f"🐕 Animal: {animal.name} ({animal.species})")
        print(f"🆔 ID do Animal: {animal.id}")
        
    except Exception as e:
        print(f"❌ Erro ao criar cliente: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_client()