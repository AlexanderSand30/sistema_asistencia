ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE asistencia
    ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    ADD COLUMN created_by INT DEFAULT NULL,
    ADD COLUMN updated_by INT DEFAULT NULL;

ALTER TABLE asistencia
    ADD CONSTRAINT fk_asistencia_trabajador
        FOREIGN KEY (trabajador_id)
        REFERENCES trabajador(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    ADD CONSTRAINT fk_asistencia_created_by
        FOREIGN KEY (created_by)
        REFERENCES usuario(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    ADD CONSTRAINT fk_asistencia_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES usuario(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL;


ALTER TABLE trabajador
	MODIFY COLUMN estado ENUM(
    	'admin',
        'supervisor',
        'operador'
	) NOT NULL DEFAULT 'operador',
    ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    ADD COLUMN created_by INT DEFAULT NULL,
    ADD COLUMN updated_by INT DEFAULT NULL;

ALTER TABLE asistencia

    ADD CONSTRAINT fk_trabajador_created_by
        FOREIGN KEY (created_by)
        REFERENCES usuario(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    ADD CONSTRAINT fk_trabajador_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES usuario(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL;