DROP TABLE IF EXISTS tb_people;
                       
CREATE TABLE IF NOT EXISTS tb_people (
    id UUID PRIMARY KEY,
    apelido VARCHAR(32) UNIQUE,
    nome VARCHAR(100) NOT NULL,
    nascimento DATE NOT NULL,
    stack VARCHAR(32) ARRAY,
    consulta VARCHAR           
);
            
CREATE INDEX IF NOT EXISTS idx_consulta ON tb_people(consulta);
