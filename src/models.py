from uuid import uuid4

from configs.database import database


class PersonModel(database.Model):
    __tablename__ = "tb_people"

    id = database.Column(database.String, default=lambda: str(uuid4()), primary_key=True)
    nickname = database.Column(database.String(32), unique=True, nullable=False, index=True)
    name = database.Column(database.String(100), nullable=False)
    birth = database.Column(database.String(12), nullable=False)
    stack = database.Column(database.String)
    
    def validate(self):
        if not self.nickname or len(self.nickname) > 32:
            raise TypeError("nickname is a required field and must be 32 characters or less")
        
        if not self.name or len(self.name) > 100:
            raise TypeError("name is a required field and must be 100 characters or less")
        
        if not self.birth or len(self.birth) > 10:
            raise TypeError("birth is a required field and must be 10 characters")
        
        if self.stack:
            if not isinstance(self.stack, list):
                raise TypeError("stack must be an array")
            
            for stack in self.stack:
                if len(stack) > 32:
                    raise TypeError("stack name must be 32 characters or less")
            self.stack = ",".join(self.stack)

    def to_json(self):
        return {
            "id": self.id,
            "nome": self.name,
            "apelido": self.nickname,
            "nascimento": self.birth,
            "stack": (self.stack or "").split(",")
        }