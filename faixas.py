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
    increment = 11
    cod_rio = '33'
    counter = 0
    line = '';
    procedimento = procedimentos[tipo]
    numero_municipio = municipios[municipio]
    file_str = gerar_cabecalho(
        mes, ano, procedimento["nome"], quantidade, municipio, numero_municipio)
    final_ano = ano[-2:]
    prev_last = procedimento["last"] + increment
    new_last = prev_last + quantidade * increment
    procedimento["last"] = new_last
    update_count_json(procedimentos)
    for i in range(prev_last, new_last, increment):
        if counter == 0:
            line = '"'
        counter += 1
        n = '%08d' % i
        n = n[:-1] + '-' + n[-1]
        number = cod_rio + final_ano + procedimento["number"] + n
        line += number
        if counter < 4 and i != new_last - 11:
            line += "  !  "
        else:
            counter = 0
            line += ' "\n'
            file_str += line
    write_file(file_str, procedimento["nome"], municipio, mes, ano)


generate_file(5, '2018','apac', 24998, u'RIO DE JANEIRO')