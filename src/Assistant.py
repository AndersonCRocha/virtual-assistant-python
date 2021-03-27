import json
import speech_recognition as recognition
from nltk import word_tokenize, corpus
from Constants import SETTINGS_PATH, CORPUS_LANGUAGE, SPEECH_LANGUAGE


class Assistant:
    def __init__(self):
        self.recognizer = recognition.Recognizer()
        self.stopWords = set(corpus.stopwords.words(CORPUS_LANGUAGE))
        self.stopWords.remove('qual')

        self.__loadSettingsFile()

    def listen(self):
        with recognition.Microphone() as microphone:
            self.recognizer.adjust_for_ambient_noise(microphone)

            print('Ask a question...')
            speech = self.recognizer.listen(microphone)

            try:
                print('Sending to google recognizer')

                question = self.recognizer.recognize_google(
                    speech, language=SPEECH_LANGUAGE)
                question = question.lower()

                print('Question: ', question)
            except Exception as error:
                print('Erro: ', str(error))

    def __loadSettingsFile(self):
        with open(SETTINGS_PATH, 'r') as settingsFile:
            settings = json.load(settingsFile)

            self.name = settings['name']
            self.questions = settings['questions']
            self.answers = settings['answers']

            settingsFile.close()

    def __removeStopWords(self, text):
        pass

    def __tokenizeQuestion(self, question):
        tokens = None

        tokens = word_tokenize(question, CORPUS_LANGUAGE)

        if tokens:
            tokens = self.__removeStopWords(tokens)

            if len(tokens) >= 3:
                for token in tokens:
                    pass

    def __recognizeQuestion(self):
        pass

    def __extractValue(self):
        pass
