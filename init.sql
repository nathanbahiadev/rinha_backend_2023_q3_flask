DROP TABLE IF EXISTS tb_people;
                       
CREATE TABLE IF NOT EXISTS tb_people (
    id VARCHAR(255) PRIMARY KEY,
    apelido VARCHAR(255) UNIQUE,
    nome VARCHAR(255) NOT NULL,
    nascimento VARCHAR(255) NOT NULL,
    stack VARCHAR(255),
    consulta VARCHAR(255)             
);
            
CREATE INDEX IF NOT EXISTS idx_consulta ON tb_people(consulta);
