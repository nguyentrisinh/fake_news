from googletrans import Translator
def divide_trans(data,number):
    details = data
    details_list = details.split()

    translated_text = ''
    try:
        r = int(len(details_list) / number)
        for i in range(number):
            trans = Translator()
            if (r == number-1):
                translated_text += ' ' +trans.translate(' '.join(x for x in details_list[r * i:len(details_list)]),
                                                   dest='vi').text
            else:
                translated_text +=' '+ trans.translate(' '.join(x for x in details_list[r * i:r * (i + 1)]), dest='vi').text
    except Exception as e:
        print(e)

    return translated_text