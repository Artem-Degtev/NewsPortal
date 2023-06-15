from django import template


register = template.Library()

FORBIDDEN_WORDS = {
   'Дурак': 'Дур***',
   'Негодяй': 'Негод***',
}

@register.filter()
def censor(value, bw='Дурак'):

   cens = FORBIDDEN_WORDS[bw]
   return f'{value}{cens}'