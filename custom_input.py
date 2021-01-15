"""
    textblob is used for processing textual data.
    It provides a API for NLP, Sentiment Analysis, Translation etc.
"""
import csv

from textblob import TextBlob
from textblob import Word

"""
    ntlk is a library for Sentiment Analysis
"""


# Required for first time
import nltk
nltk.download('punkt')
nltk.download('brown')


class CustomSentiment:
    lenOfList = 0
    result = []
    final = []

    @classmethod
    def spellCheckInput(cls, lstToCheck):
        spellCheckWords = []

        for w in lstToCheck:
            check = Word(w)
            spellCheckWords.append(check.spellcheck()[0][1])

        avg = 0
        for i in spellCheckWords:
            avg += i

        avg = avg / len(spellCheckWords)
        if avg <= len(spellCheckWords) - 1:
            return True, avg

    @classmethod
    def sentimentAnalyze(cls, sentenceLstToCheck):

        for i in sentenceLstToCheck:
            CustomSentiment.lenOfList += 1
            print("Analyzing: " + i.__str__() + "%s %s" % (" ..........", "Done"))
            sentence = TextBlob(i.string)
            CustomSentiment.result.append(sentence.sentiment)

        for res in CustomSentiment.result:
            if res[0] > 0:
                CustomSentiment.final.append("Positive")
                print("Positive")
            elif res[0] == 0:
                CustomSentiment.final.append("Neutral")
                print("Neutral")
            else:
                CustomSentiment.final.append("Negative")
                print("Negative")

    @classmethod
    def analyze(cls):

        global rows
        textToAnalyze = input("\nEnter text: ")
        assert len(textToAnalyze) != 0, "Input cannot be empty"

        print("\n************************************************************"
              "\nResults: \n")

        testSentence = TextBlob(textToAnalyze)
        wordsList = testSentence.words

        res = cls.spellCheckInput(wordsList)

        if res is not None:
            if res[0]:
                print("SpellCheck confidence: " + res[1].__str__())
                sentences = testSentence.sentences
                print("Sentences found: " + sentences.__str__())
                nouns = testSentence.noun_phrases
                print("Nouns found: " + nouns.__str__() + "\n")

                cls.sentimentAnalyze(sentences)

                choice = input("\nDo you want to save results to a file? (y/N): ")
                if choice == "y" or choice == "Y" or choice == "Yes" or choice == "yes":
                    field = ["Sentence", "Result", "Polarity", "Subjective"]
                    rows = []
                    for i in range(0, CustomSentiment.lenOfList):
                        rows.append([sentences[i].string, CustomSentiment.final[i], CustomSentiment.result[i][0],
                                     CustomSentiment.result[i][1]])

                    try:
                        with open('results_sentiment.csv', 'w') as f:
                            write = csv.writer(f)

                            write.writerow(field)
                            write.writerows(rows)
                            print("Saved results_sentiment.csv successfully!")
                    except:
                        print("Error Saving file")

                print("************************************************************")
            else:
                print("Your input has spelling errors or more nouns."
                      "\n(Or cannot be analyzed)."
                      "\nPlease check and try again."
                      "\n************************************************************")
        else:
            print("Your input has spelling errors or more nouns."
                  "\n(Or cannot be analyzed)."
                  "\nPlease check and try again."
                  "\n************************************************************")
