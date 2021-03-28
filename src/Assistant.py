import json
import speech_recognition as recognition
from nltk import word_tokenize, corpus
from Constants import SETTINGS_PATH, CORPUS_LANGUAGE, SPEECH_LANGUAGE
from CustomException import CustomException


class Assistant:
    def __init__(self):
        self.recognizer = recognition.Recognizer()
        self.stopWords = set(corpus.stopwords.words(CORPUS_LANGUAGE))
        self.stopWords.remove('são')
        self.stopWords.add('quais')

        self.__loadSettingsFile()

    def init(self):
        try:
            question = self.__listen()
            if not question:
                raise CustomException('Não consegui entender o que você falou. Vamos tentar novamente\n')
            
            tokens = self.__tokenizeQuestion(question)
            
            if not tokens:
                raise CustomException('Could not tokenize question')
            
            isValidQuestion, validTokensCount = self.__validateTokens(tokens)
            if not isValidQuestion:
                raise CustomException('Não sei responder essa pergunta. :(')
            
            firstKey, secondKey = self.__extractValue(tokens, validTokensCount)
            
            print({self.data[firstKey][secondKey]}, '\n')
        except KeyboardInterrupt as error:
            raise error
        except Exception as error:
            print("Ocorreu um erro inesperado: {0}".format(error))

    def __listen(self):
        question = None

        with recognition.Microphone() as microphone:
            self.recognizer.adjust_for_ambient_noise(microphone)

            print('Estou pronto pra te ouvir...')
            speech = self.recognizer.listen(microphone)

            try:
                question = self.recognizer.recognize_google(speech, language=SPEECH_LANGUAGE)
                question = question.lower()

                print(f'{question}?')

                return question
            except recognition.UnknownValueError:
                return None

    def __loadSettingsFile(self):
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as settingsFile:
            settings = json.load(settingsFile)

            self.name = settings['name']
            self.data = settings['data']
            self.allowedExpressions = settings['allowedExpressions']

            settingsFile.close()

    def __tokenizeQuestion(self, question):
        tokens = word_tokenize(question, CORPUS_LANGUAGE)

        if tokens:
            if tokens.pop(0).lower() != self.name:
                raise CustomException('Você deve falar o nome do assistente para fazer a pergunta.')
            
            return self.__removeStopWords(tokens)
        

    def __removeStopWords(self, tokens):
        filteredTokens = []

        for token in tokens:
            if token.lower() not in self.stopWords:
                filteredTokens.append(token)

        return filteredTokens

    def __validateTokens(self, tokens):
        isValid = False
        validTokensCount = 0

        for allowedExpression in self.allowedExpressions:
            allowedTokens = word_tokenize(allowedExpression, CORPUS_LANGUAGE)
            allowedTokensCount = len(allowedTokens)

            if allowedTokensCount <= len(tokens):
                intersection = list(set(allowedTokens) & set(tokens))
                intersectionItemsCount = len(intersection)

                if intersectionItemsCount == allowedTokensCount:
                    validTokensCount = allowedTokensCount
                    isValid = True
                    break

        return isValid, validTokensCount

    def __extractValue(self, tokens, validTokensCount):
        
        if validTokensCount == 1 and "capital" in tokens:
            return "capital", tokens[-1].lower()
        
        if "cidade" in tokens and "brasil" in tokens:
            return "cidade", tokens.pop(0).lower()
        
        if "afluentes" in tokens:
            tokens.remove("afluentes")
            tokens.remove("rio")
            river = " ".join(tokens).lower().strip()
            return "afluente", river
