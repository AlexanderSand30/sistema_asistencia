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
    ADD COLUMN fecha_nac DATE NULL AFTER cargo,
    ADD COLUMN fecha_ingreso DATE NULL AFTER fecha_nac,
    ADD COLUMN fecha_cese DATE NULL AFTER fecha_ingreso,
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

ALTER TABLE usuario
    MODIFY COLUMN rol ENUM(
        'superadmin',
        'admin',
        'supervisor',
        'operador'
    ) NOT NULL DEFAULT 'operador',

    ADD COLUMN nro_documento varchar(15) UNIQUE NULL AFTER id,
    ADD COLUMN created_by INT NULL AFTER estado,
    ADD COLUMN updated_by INT NULL AFTER created_by,

    ADD COLUMN created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        AFTER updated_by,

    ADD COLUMN updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
        AFTER created_at,

    ADD COLUMN deleted_by INT NULL AFTER updated_at,
    ADD COLUMN deleted_at DATETIME NULL AFTER deleted_by,
    ADD CONSTRAINT fk_usuario_created_by
        FOREIGN KEY (created_by) REFERENCES usuario(id),

    ADD CONSTRAINT fk_usuario_updated_by
        FOREIGN KEY (updated_by) REFERENCES usuario(id),

    ADD CONSTRAINT fk_usuario_deleted_by
        FOREIGN KEY (deleted_by) REFERENCES usuario(id),
    ADD CONSTRAINT uq_usuario_usuario UNIQUE (usuario);

