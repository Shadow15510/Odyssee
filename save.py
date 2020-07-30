import requests
import os

specials = "éèêàâùûîïô '0123456789#азертыуиоп́сдфгхйклмщхцвбнАЗЕРТЫУИОПQСДФГХЙКЛМЩХЦВБНЁёЖжЩщЪъЬьЭэЮюЯяΑΆΒΓΔΕΈΖΗΉΘΙΊΚΛΜΝΞΟΌΠΡΣΤΥΎΦΧΨΩΏ·αάβγδεέζηήθιϊΐίκλμνξοόπρσςτυϋΰύφχψωώ"

def save_convert(text):
    result = ""
    text = text.replace("@", "")
    for letter in text:
        result += letter if letter not in specials else "@{}".format(specials.find(letter))
    return result

def save_revert(text):
    for i in range(len(specials) - 1, -1, -1):
        text = text.replace("@{}".format(i), specials[i])
    return text

domain = "https://odyssee.pythonanywhere.com"
password = os.environ["save_site"]

def save_send(data):
    requests.get("{}/send/{}/{}".format(domain, password, data.replace(" ", "")))

def save_read():
    return requests.get("{}/read/{}".format(domain, password)).text

def save_delete():
    requests.get("{}/del/{}".format(domain, password))

