CREATE TABLE asistencia (
  id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  trabajador_id int(11) NOT NULL,
  obra varchar(150) DEFAULT NULL,
  fecha date NOT NULL,
  hora_entrada time DEFAULT NULL,
  hora_salida time DEFAULT NULL,
  foto_entrada varchar(255) DEFAULT NULL,
  lat_entrada decimal(10,7) DEFAULT NULL,
  lng_entrada decimal(10,7) DEFAULT NULL,
  foto_salida varchar(255) DEFAULT NULL,
  lat_salida decimal(10,7) DEFAULT NULL,
  lng_salida decimal(10,7) DEFAULT NULL,
  estado varchar(20) NOT NULL DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuario (
  id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  usuario varchar(50) NOT NULL,
  password varchar(255) NOT NULL,
  rol enum('admin','supervisor') NOT NULL DEFAULT 'supervisor',
  estado tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE trabajador (
  id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  dni varchar(8) NOT NULL,
  nombres varchar(100) NOT NULL,
  apellidos varchar(100) NOT NULL,
  cargo varchar(100) DEFAULT NULL,
  estado tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ALTER

ALTER TABLE asistencia
    ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    ADD COLUMN created_by INT DEFAULT NULL,
    ADD COLUMN updated_by INT DEFAULT NULL;

ALTER TABLE asistencia
    ADD CONSTRAINT fk_asistencia_trabajador
        FOREIGN KEY (trabajador_id)
        REFERENCES Trabajadores(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    ADD CONSTRAINT fk_asistencia_created_by
        FOREIGN KEY (created_by)
        REFERENCES Usuarios(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    ADD CONSTRAINT fk_asistencia_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES Usuarios(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL;