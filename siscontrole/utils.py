# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

STATE_CHOICES = [
    ('','Selecione um estado'),('AC','Acre'),('AL','Alagoas'),('AM','Amazonas'),('AP','Amapá'),('BA','Bahia'),
    ('CE','Ceará'),('DF','Distrito Federal'),('ES','Espírito Santo'),('GO','Goiás'),('MA','Maranhão'),('MG','Minas Gerais'),
    ('MS','Mato Grosso do Sul'),('MT','Mato Grosso'),('PA','Pará'),('PB','Paraíba'),('PE','Pernambuco'),('PI','Piauí'),
    ('PR','Paraná'),('RJ','Rio de Janeiro'),('RN','Rio Grande do Norte'),('RO','Rondônia'),('RR','Roraima'),('RS','Rio Grande do Sul'),
    ('SC','Santa Catarina'),('SP','São Paulo'),('SE','Sergipe'),('TO','Tocantins'),
]

MESSAGES = {
    'success': {
        'member_add':_('Well done! Member added successfully!'),
        'member_update':_('Well done! Member updated successfully!'),
        'member_remove':_('Well done! Members removed successfully!'),
    },
}

def abbreviate(name, pretty=False):
    names = name.split()
    if len(names) == 2:
        return name
    result = [names[0]]
    tiny_name = False
    for surname in names[1:-1]:
        if len(surname) <= 3:
            result.append(surname)
            tiny_name = True
        else:
            if pretty and tiny_name:
                result.append(surname)
            else:
                result.append(surname[0] + '.')
            tiny_name = False
    result.append(names[-1])
    return ' '.join(result)