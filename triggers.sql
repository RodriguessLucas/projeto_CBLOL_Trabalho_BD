CREATE OR REPLACE FUNCTION encerrar_contrato_apos_aposentadoria()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.data_fim_carreira IS NOT NULL AND (OLD.data_fim_carreira IS NULL OR OLD.data_fim_carreira <> NEW.data_fim_carreira) THEN
        UPDATE contratos
        SET data_fim = NEW.data_fim_carreira
        WHERE id_jogador = NEW.id
          AND data_fim IS NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_encerrar_contrato_apos_aposentadoria
AFTER UPDATE ON jogadores
FOR EACH ROW
EXECUTE FUNCTION encerrar_contrato_apos_aposentadoria();


CREATE OR REPLACE FUNCTION validar_datas_contrato()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.data_fim IS NOT NULL AND NEW.data_fim < NEW.data_inicio THEN
        RAISE EXCEPTION 'Data de fim nao pode ser anterior a data de inicio.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_validar_datas_contrato
BEFORE INSERT OR UPDATE ON contratos
FOR EACH ROW
EXECUTE FUNCTION validar_datas_contrato();

CREATE OR REPLACE FUNCTION impedir_contratos_duplicados()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contratos
        WHERE id_jogador = NEW.id_jogador AND data_fim IS NULL
    ) THEN
        RAISE EXCEPTION 'Jogador ja possui um contrato ativo.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_impedir_contratos_duplicados
BEFORE INSERT ON contratos
FOR EACH ROW
EXECUTE FUNCTION impedir_contratos_duplicados();
