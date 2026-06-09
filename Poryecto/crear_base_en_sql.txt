CREATE DATABASE sistema_paqueteria;


USE sistema_paqueteria;



CREATE TABLE paquete (
    id_paquete INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    peso DECIMAL(10,2)
);



CREATE TABLE socio (
    id_socio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)
);



CREATE TABLE region (
    id_region INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(50)
);




CREATE TABLE vehiculo (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50)
);


CREATE TABLE rutas (
    id_rutas INT AUTO_INCREMENT PRIMARY KEY,

    id_region INT,
    id_vehiculo INT,

    tiempo_esperado DECIMAL(10,2),
    distancia DECIMAL(10,2),

    FOREIGN KEY (id_region)
        REFERENCES region(id_region),

    FOREIGN KEY (id_vehiculo)
        REFERENCES vehiculo(id_vehiculo)
);




CREATE TABLE entrega (
    id_entrega INT AUTO_INCREMENT PRIMARY KEY,

    id_rutas INT,
    id_paquete INT,
    id_socio INT,

    modo VARCHAR(50),
    tiempo_entrega DECIMAL(10,2),

    retraso VARCHAR(3),

    clima VARCHAR(50),

    costo DECIMAL(10,2),

    calificacion INT,

    FOREIGN KEY (id_rutas)
        REFERENCES rutas(id_rutas),

    FOREIGN KEY (id_paquete)
        REFERENCES paquete(id_paquete),

    FOREIGN KEY (id_socio)
        REFERENCES socio(id_socio)
);