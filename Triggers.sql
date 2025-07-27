create or replace function encerrar_contrato_apos_aposentadoria()
returns trigger as $$
begin
    -- verifica se houve atualizacao no data_fim_carreira e se nao era nulo 
    if new.data_fim_carreira is not null and (old.data_fim_carreira is null or old.data_fim_carreira <> new.data_fim_carreira) then
        -- atualiza contratos ativos do jogador, colocando data_fim igual a data_fim_carreira
        update contratos
        set data_fim = new.data_fim_carreira
        where id_jogador = new.id
          and data_fim is null;
    end if;

    return new;
end;
$$ language plpgsql;

create trigger trg_encerrar_contrato_apos_aposentadoria
after update on jogadores
for each row
execute function encerrar_contrato_apos_aposentadoria();


-- funcao para validar datas de contrato
create or replace function validar_datas_contrato()
returns trigger as $$
begin
    if new.data_fim is not null and new.data_fim < new.data_inicio then
        raise exception 'Data de fim nao pode ser anterior a data de inicio.';
    end if;
    return new;
end;
$$ language plpgsql;


create trigger trg_validar_datas_contrato
before insert or update on contratos
for each row
execute function validar_datas_contrato();

-- funcao para impedir contratos duplicados
create or replace function impedir_contratos_duplicados()
returns trigger as $$
begin
    if exists (
        select 1 from contratos
        where id_jogador = new.id_jogador and data_fim is null
    ) then
        raise exception 'Jogador ja possui um contrato ativo.';
    end if;
    return new;
end;
$$ language plpgsql;


create trigger trg_impedir_contratos_duplicados
before insert on contratos
for each row
execute function impedir_contratos_duplicados();

