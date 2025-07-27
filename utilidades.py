# utilidades.py
from datetime import datetime, date

def is_string_valida(texto: str) -> bool:
    """Verifica se o texto não é nulo e contém caracteres alfanuméricos."""
    if not texto or not isinstance(texto, str):
        return False
    texto_verificacao = texto.replace(' ', '').replace('-', '').replace("'", "")
    return texto_verificacao.isalnum()

def is_data_valida(data_str: str) -> bool:
    """Verifica se a string da data está no formato DD/MM/YYYY."""
    if not data_str or not isinstance(data_str, str):
        return False
    try:
        datetime.strptime(data_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def string_to_date(data_str: str) -> date | None:
    """Converte uma string 'DD/MM/YYYY' para um objeto date."""
    try:
        return datetime.strptime(data_str, '%d/%m/%Y').date()
    except (ValueError, TypeError):
        return None

def date_to_string(data_obj: date) -> str:
    """Converte um objeto date para uma string 'DD/MM/YYYY'."""
    if data_obj is None:
        return "Não definido"
    if not isinstance(data_obj, (date, datetime)):
        raise TypeError("A data não é válida.")
    return data_obj.strftime('%d/%m/%Y')