from bs4 import BeautifulSoup
from requests import get
import requests.exceptions as err

""""
CODED BY EMRE ATAKURU
   SUBJECT : UNOFFICAL TURENG API
   WHICH TECHNOLOGIES USED : WEB SCRAPİNG.

   SOCIAL MEDIA ACCOUNTS.
            @Github : Emre Atakuru
            @Instagram : @emreatakuru
            
            Also known as : DAĞIZTANLI08
"""
class Tureng_translate(object):
    def __init__(self,word = "" ,language_ = "" ,dict_ = {} ,start = 0):
        try:
            #You don't access this methods outside from class because variable names start with "__"
            self.__language = {"EN-TR":"turkce-ingilizce",
            "EN-DE":"almanca-ingilizce",
            "EN-ES":"ispanyolca-ingilizce",
            "EN-FR":"fransizca-ingilizce",
            "TR-EN":"turkce-ingilizce",
            "DE-EN":"almanca-ingilizce",
            "FR-EN":"fransizca-ingilizce",
            "ES-EN":"ispanyolca-ingilizce"}
            self.__transform_lang = language_
            self.start = start
            self.__word = word
            self.__mean = ""
            self.__category = ""
            self.__dict_ = dict_
            
            if self.start == 1:
                self.__tureng_url = "https://tureng.com/tr/{}".format(self.__language[language_]) + "/" + self.__word
                if language_.startswith("EN"):
                    self.__translate_ing_to_other()
                elif not language_.startswith("EN") and language_ in self.__language:
                    self.__translate_other_to_ing()
                else:
                    pass
            else:
                pass
            
        except KeyError:
            print("İnput invalid Language transform.")

    #Created for send request.
    def __request_html(self):
        try:
            return(get(self.__tureng_url).content)
        except err.ConnectTimeout:
            print("Connection Time Out.")
        except err.ConnectionError:
            print("Connection error / No Internet access.")

    @property
    def show_languages(self) -> list:
        """"
        You can show which languages word to transform.
        """
        languages = [l for l in self.__language.keys()]
        return(languages)

    @property
    def dict_return(self) -> dict:
        return(self.__dict_)

    @property
    def show_the_word_to_translate(self) -> str:
        return(self.__word)

    @property
    def show_the_language_transform(self) -> str:
        return(self.__transform_lang)
    
    def __setdict(self,counter = 0,last_counter = 0) -> None:
        last_kategori = None
        for m in range(1,len(self.__category),3):
            
            last_kategori_compare = self.__category[m].get_text()

            if last_kategori == last_kategori_compare:
                self.__dict_[self.__category[m].get_text() + str(last_counter + 1)] = self.__mean[counter].get_text()
                last_kategori = last_kategori_compare
                last_counter += 1
                
            else:
                self.__dict_[self.__category[m].get_text()] = self.__mean[counter].get_text()
                last_kategori = last_kategori_compare
                last_counter = 0                    
            counter +=1

        # Error if you input Turkish Word but Language transform is like (EN-TR). You should input (TR-EN)
        check_list = [x for x in self.__dict_.values()]
        if check_list[0] == check_list[1]:
            raise TypeError("İnvalid language transform.")

    #Translate word from other to English
    def __translate_other_to_ing(self) -> None:
      try:
          word_url_r = BeautifulSoup(self.__request_html(),'html.parser')
          table_word_r = word_url_r.find_all('table',id = 'englishResultsTable')
          self.__mean = table_word_r[0].find_all('td',class_ = 'en tm')
          self.__category = table_word_r[0].find_all('td',class_ = 'hidden-xs')
          self.__setdict()

      except IndexError:
          print("Word not found.")

    #Translate word from English to Another Function..
    def __translate_ing_to_other(self) -> None:
        try:
            word_url = BeautifulSoup(self.__request_html(),'html.parser')
            table_word = word_url.find_all('table',id = "englishResultsTable")
            self.__mean = table_word[0].find_all('td',class_ = 'tr ts')
            self.__category = table_word[0].find_all('td',class_ = 'hidden-xs')
            self.__setdict()        
        
        except IndexError:
            print("Word not found.")


    

