# -*- coding: utf-8 -*-
import codecs
import json
procedimentos = json.load(open('count.json'))
municipios = json.load(open('municipios.json'))


def gerar_cabecalho(mes, ano, procedimento, quantidade,
        municipio, numero_municipio):
    return \
        u'"Distribuição de %s (Competência: %02d/%s - Quantidade: %d)"\n' \
        u'"Município: %s (%s)"\n' % \
        (procedimento, mes, ano, quantidade, municipio, numero_municipio)


def write_file(file_str, metodo, municipio, mes, ano):
    filename = '%s %s %02d%s.txt' % (metodo, municipio, mes, ano)
    with codecs.open(filename,'w',encoding='utf8') as f:
        f.write(file_str)
        f.close()

def update_count_json(content):
    with codecs.open('count.json','w',encoding='utf8') as f:
        f.write(json.dumps(content, sort_keys=True, indent=4))
        f.close()


def generate_file(mes, ano, tipo, quantidade, municipio):
    digito = 0
    cod_rio = '33'
    counter = 0
    line = '';
    procedimento = procedimentos[tipo]
    numero_municipio = municipios[municipio]
    file_str = gerar_cabecalho(
        mes, ano, procedimento["nome"], quantidade, municipio, numero_municipio)
    final_ano = ano[-2:]
    prev_last = procedimento["last"]
    new_last = prev_last + quantidade
    procedimento["last"] = new_last
    last_digit = procedimento["last_digit"]
    if (last_digit == 10):
        last_digit = -1
    for i in range(prev_last + 1, new_last):
        last_digit += 1
        if counter == 0:
            line = '"'
        counter += 1
        n = '%07d' % i
        last_digit = last_digit % 11
        n = n + '-'
        n += '%d' % (last_digit % 10)
        number = cod_rio + final_ano + procedimento["number"] + n
        line += number
        if counter < 4 and i != new_last - 1:
            line += "  !  "
        else:
            counter = 0
            line += ' "\n'
            file_str += line
    write_file(file_str, procedimento["nome"], municipio, mes, ano)
    procedimento["last_digit"] = last_digit
    update_count_json(procedimentos)


# AIH 331810-0
# AIH ELETIVA 331850029795-9
# APAC 331820325548-8
# APAC ELETIVA 331860009030-0

generate_file(5, '2018','apac', 50000, u'GERAL')

# generate_file(5, '2018','apac_e', 50000, u'GERAL')

# generate_file(5, '2018','aih_e', 50000, u'GERAL')

# generate_file(5, '2018','aih', 50000, u'GERAL')
