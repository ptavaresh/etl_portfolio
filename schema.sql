-- schema.sql

CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    departamento VARCHAR(100) NOT NULL
);

-- Inserta datos de ejemplo
INSERT INTO empleados (nombre, edad, departamento) VALUES
    ('Juan', 30, 'Ventas'),
    ('María', 25, 'Marketing'),
    ('Carlos', 35, 'IT');
