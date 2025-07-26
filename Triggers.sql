create or replace function encerrar_contrato_apos_aposentadoria()
returns trigger as $$
begin
    -- verifica se houve atualização no data_fim_carreira e se nao era nulo 
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
