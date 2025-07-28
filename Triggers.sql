

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

-- funcao para verificar se a data de inico do contrato e valida
create or replace function verificar_data_inicio_contrato()
returns trigger as $$
declare
    fundacao_time date;
begin
    -- obter a data de fundacao do time referente ao contrato
    select data_fundacao into fundacao_time
    from times
    where id = new.id_time;
    -- verifica se a data de inicio do contrato e anterior a fundacao do time
    if new.data_inicio < fundacao_time then
        raise exception 'a data de inicio do contrato (%), nao pode ser anterior a fundacao do time (%)',
            new.data_inicio, fundacao_time;
    end if;

    return new;
end;
$$ language plpgsql;
create trigger trg_verifica_data_inicio_contrato
before insert or update on contratos
for each row
execute function verificar_data_inicio_contrato();

-- funcao para impedir o time de entrar em um campeonato que tenha comecado antes de sua data de fundacao
create or replace function impedir_participacao_antes_fundacao()
returns trigger as $$
declare
    fundacao_time date;
    inicio_campeonato date;
begin
    -- procura a data de fundacao
    select data_fundacao into fundacao_time
    from times
    where id = new.id_time;

    -- procura a data de inicio
    select data_inicio into inicio_campeonato
    from campeonatos
    where id = new.id_campeonato;

    -- compara as datas
    if inicio_campeonato < fundacao_time then
        raise exception 'o time nao pode participar de um campeonato que comecou antes da sua fundacao (% < %)',
            inicio_campeonato, fundacao_time;
    end if;

    return new;
end;
$$ language plpgsql;

create trigger trg_impedir_participacao_antes_fundacao
before insert or update on participacoes
for each row
execute function impedir_participacao_antes_fundacao();


-- funcao que nao deixa times com menos de 5 jogadores participarem
create or replace function validar_times_com_cinco_jogadores()
returns trigger as $$
declare
    numjogador_time1 int;
    numjogador_time2 int;
begin
    -- conta os jogadores ativos do time 1 na data atual
    select count(*) into numjogador_time1
    from contratos
    where id_time = new.id_time1
      and data_inicio <= current_date
      and (data_fim is null or data_fim >= current_date);

    -- conta os jogadores ativos do time 2 na data atual
    select count(*) into numjogador_time2
    from contratos
    where id_time = new.id_time2
      and data_inicio <= current_date
      and (data_fim is null or data_fim >= current_date);

    -- verifica se o time1 tem menos de 5 jogadores
    if numjogador_time1 < 5 then
        raise exception 'o time1 (id=%) nao possui ao menos 5 jogadores ativos atualmente', new.id_time1;
    end if;

    -- verifica se o time2 tem menos de 5 jogadores
    if numjogador_time2 < 5 then
        raise exception 'o time2 (id=%) nao possui ao menos 5 jogadores ativos atualmente', new.id_time2;
    end if;

    return new;
end;
$$ language plpgsql;
create trigger trg_validar_times_com_cinco_jogadores
before insert or update on partidas
for each row
execute function validar_times_com_cinco_jogadores();





