from django import template



register = template.Library()

FORBIDDEN_WORDS = {
   'Дурак': 'Дур***',
   'Негодяй': 'Негод***',
}

@register.filter()
def censor(text):
   text_list = text.split()
   for word in text_list:
      if word in FORBIDDEN_WORDS:
         text = text.replace(word, word[0] + (len(word) - 1)*'*')
   return text


