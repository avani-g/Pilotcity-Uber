# Things to include:
# Flesch reading score (uses sentence length and avaerage syllables/word)
# Sentence length and average sentence length
# nouns/sentence
# slang?

# @author: Avani Goyal

import flask
from flask import request

from textatistic import Textatistic
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import string

app = flask.Flask(__name__)
app.config["DEBUG"] = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@app.route('/getScores/<text>', methods=['GET'])
def getScores(text):

    returnText = ""
    returnText = returnText + "<b>"+"Text under analysis:"+"</b>" + "<br>" + text
    print(f"{bcolors.HEADER}Text:{bcolors.ENDC}", text)

    readability_scores = Textatistic(text).scores
    returnText = returnText + "<br><br><b>Scores: </b>" + str(readability_scores)
    print("\nScores:", readability_scores)

    # Basic Info -------------------------------------------------------
    print("\n", "Basic Info:", "\n")
    print("Sentence Count:", Textatistic(text).sent_count)
    print("Word Count:", Textatistic(text).word_count)
    print("Character Count:", Textatistic(text).char_count)
    print("Syllable Count:", Textatistic(text).sybl_count)
	
    returnText = returnText + "<br><b>Basic Info: </b><br><b>Word Count:</b>" + str(Textatistic(text).word_count)+"<br><b>Character Count: </b>"+str(Textatistic(text).char_count)+"<br><b>Syllable Count: </b>"+str(Textatistic(text).sybl_count)
	

    # Complicated Info -------------------------------------------------
    print("\n", "Complicated Info:", "\n")
    print("Not Dale-Chall Count:", Textatistic(text).notdalechall_count)
        # number of words not on Dale-Chall list of words understood by 80% of 4th graders
        # the lower the better
        # could maybe calculate percentage of total words
        # find which ones aren't on the list and tell the writer
    print("Poly Syllable World Count:", Textatistic(text).polysyblword_count) # polysyblword_count	number of words with three or more syllables.

    returnText = returnText + "<br><br><b>Complicated Info: </b><br><b>Not Dale-Chall Count:</b>" + str(Textatistic(text).notdalechall_count)+"<br><b>Poly Syllable World Count: </b>"+str(Textatistic(text).polysyblword_count)


    # Scores ------------------------------------------------------------
    print("\n", "Scores:", "\n")
    returnText = returnText + "<br><br><b>Scores:</b>"

    if Textatistic(text).dalechall_score < 5:
        dc_grade = "Grade 4 and Below"
    elif Textatistic(text).dalechall_score < 6:
        dc_grade = "Grades 5-6"
    elif Textatistic(text).dalechall_score < 7:
        dc_grade = "Grades 7-8"
    elif Textatistic(text).dalechall_score < 8:
        dc_grade = "Grades 9-10"
    elif Textatistic(text).dalechall_score < 9:
        dc_grade = "Grades 11-12"
    elif Textatistic(text).dalechall_score < 10:
        dc_grade = "College"
    else:
        dc_grade = "College Graduate"
    print("Dale-Chall Score: ", Textatistic(text).dalechall_score, "(", dc_grade, ")")
        # *uses perecentage of hard words (not on Dale-Chall list) and average sentence length*
        # Raw score = 0.1579*(PDW) + 0.0496*(ASL) + 3.6365 (for 3rd grade and below)
        # Here,
        # PDW = Percentage of difficult words not on the Dale–Chall word list.
        # ASL = Average sentence length
        # if PDW > 5% -> Adjusted Score = Raw Score + 3.6365, otherwise Adjusted Score = Raw Score (for 4th grade and above)
    returnText = returnText + "<br><b>Dale-Chall Score: </b>"+str(Textatistic(text).dalechall_score) + " ( " + dc_grade + " )"


    # NOT USING THIS METHOD BECUASE ITS SIILAR TO THE FLESCH ONE AND DOESN'T HAVE A GOOD SCORING SYSTEM

    # if Textatistic(example1).fleschkincaid_score < 10:
    #     fk_grade = "Professional"
    # elif Textatistic(example1).fleschkincaid_score < 30:
    #     fk_grade = "College Graduate"
    # elif Textatistic(example1).fleschkincaid_score < 50:
    #     fk_grade = "College"
    # elif Textatistic(example1).fleschkincaid_score < 60:
    #     fk_grade = "10th - 12th"
    # elif Textatistic(example1).fleschkincaid_score < 70:
    #     fk_grade = "8th - 9th"
    # elif Textatistic(example1).fleschkincaid_score < 80:
    #     fk_grade = "7th"
    # elif Textatistic(example1).fleschkincaid_score < 90:
    #     fk_grade = "6th"
    # elif Textatistic(example1).fleschkincaid_score <= 100:
    #     fk_grade = "5th"
    # else:
    #     fk_grade = "Over 100?? Super Readable I guess"
    # print("Flesch-Kincaid Score:", Textatistic(example1).fleschkincaid_score, "(", fk_grade, ")")
    #     # *uses words per sentence and syllables per word*
    #     # 206.835 = 1.015(total words / total sentences) - 84.6 (total syllables / total words)


    print("SMOG Score:", Textatistic(text).smog_score, "(", "Grade", int(Textatistic(text).smog_score), ")")
        # *just uses the polysyllable count*
        # SMOG grading = 3 + √(polysyllable count).
        # Here, polysyllable count = number of words of more than two syllables in a
        # sample of 30 sentences.
    returnText = returnText + "<br><b>SMOG Score:</b> " + str(Textatistic(text).smog_score) + " ( Grade " +  str(int(Textatistic(text).smog_score)) + " ) "

    if Textatistic(text).flesch_score < 30:
        fs_grade = "College Graduate"
    elif Textatistic(text).flesch_score < 50:
        fs_grade = "College"
    elif Textatistic(text).flesch_score < 60:
        fs_grade = "10th - 12th"
    elif Textatistic(text).flesch_score < 70:
        fs_grade = "8th - 9th"
    elif Textatistic(text).flesch_score < 80:
        fs_grade = "7th"
    elif Textatistic(text).flesch_score < 90:
        fs_grade = "6th"
    elif Textatistic(text).flesch_score <= 100:
        fs_grade = "5th"
    else:
        fs_grade = "Over 100?? Super Readable I guess"
    print("Flesch Score:", Textatistic(text).flesch_score, "(", fs_grade, ")")
        # *uses average sentence length and syllables per word*
        # Reading Ease score = 206.835 - (1.015 × ASL) - (84.6 × ASW)
        # Here,
        # ASL = average sentence length (number of words divided by number of sentences)
        # ASW = average word length in syllables (number of syllables divided by number of words)
    returnText = returnText + "<br><b>Flesch Score:</b> " + str(Textatistic(text).flesch_score) + " ( " + fs_grade + " ) "

    print("Gunning fog Score:", Textatistic(text).gunningfog_score, "(", "Grade", int(Textatistic(text).gunningfog_score), ")")
        # *uses average sentence length and percentage of words with more than 2 syllables*
        # Grade level= 0.4 * ( (average sentence length) + (percentage of Hard Words) )
        # Here, Hard Words = words with more than two syllables.
    returnText = returnText + "<br><b>Gunning fog Score:</b> " + str(Textatistic(text).gunningfog_score) + " ( Grade " + str(int(Textatistic(text).gunningfog_score)) + " ) "

    print("\n\n")
    returnText = returnText + "<br><br>"

    sentences = sent_tokenize(text)

    words_per_sentence = []


    print(f"{bcolors.OKBLUE}Tips:{bcolors.ENDC}")
    returnText = returnText + "<b>Tips:</b>"

    punctuation_list = [",", ".", "-", "'", "\"", ":", ";", "—", "!", "?"]

    returnTextTips = ""
    for sentence in sentences:
        words_per_sentence.append([Textatistic(sentence).word_count, sentence])

        # tagged_sent = nltk.pos_tag(nltk.word_tokenize(sentence.translate(str.maketrans('', '', string.punctuation))))
        tagged_sent = nltk.pos_tag(nltk.word_tokenize(sentence))
        tagged_sent_no_pn = ""
        nouns = []
        for (word, tag) in tagged_sent:
            if tag != 'NNP' and tag != 'NNPS':
                if word not in punctuation_list:
                    tagged_sent_no_pn += word + " "
                    #print(word, tag)
                if tag == 'NN' or tag == 'NNS':
                    nouns.append(word)

        if len(nouns) > 5:
            print(f"{bcolors.FAIL}Too many nouns {bcolors.ENDC}" + "(" + str(len(nouns)) + "):", sentence, "\n")
            returnTextTips = returnTextTips + "<br>Too many nouns (" + str(len(nouns)) + "): " + sentence
            print(f"{bcolors.BOLD}nouns:{bcolors.ENDC}", nouns, "\n")


        if Textatistic(tagged_sent_no_pn + ".").notdalechall_count > 2: # CHANGE NUMBER LATER
            print(f"{bcolors.FAIL}Too many difficult words {bcolors.ENDC}" + "(" + str(Textatistic(tagged_sent_no_pn + ".").notdalechall_count) + "):", sentence)
            returnTextTips = returnTextTips + "<br>Too many difficult words (" + str(Textatistic(tagged_sent_no_pn + ".").notdalechall_count) + "): " + sentence
			
            print(f"{bcolors.BOLD}No proper nouns:{bcolors.ENDC}", tagged_sent_no_pn, "\n")
            returnTextTips = returnTextTips + "<br><font color=red>No proper nouns: </font>" + tagged_sent_no_pn
            print(f"{bcolors.OKGREEN}Consider changing: {bcolors.ENDC}")
            returnTextTips = returnTextTips + "<br><font color=green>Consider changing: </font>"
            for w in nltk.word_tokenize(tagged_sent_no_pn):
                if Textatistic(w + ".").notdalechall_count != 0:
                    print(w)
                    returnTextTips = returnTextTips + "<br>" + w
        print("\n")
        returnTextTips = returnTextTips + "<br>"

        if Textatistic(tagged_sent_no_pn + ".").polysyblword_count > 0: #  CHANGE NUMBER LATER
            print(f"{bcolors.FAIL}Too many long words {bcolors.ENDC}" + "(" + str(Textatistic(tagged_sent_no_pn + ".").polysyblword_count) + "):", sentence)
            returnTextTips = returnTextTips + "<br>Too many long words (" + str(Textatistic(tagged_sent_no_pn + ".").polysyblword_count) +")" + sentence
            print(f"{bcolors.BOLD}No proper nouns:{bcolors.ENDC}", tagged_sent_no_pn, "\n")
            returnTextTips = returnTextTips + "<br>No proper nouns: " + tagged_sent_no_pn + "<br>"
            print(f"{bcolors.OKGREEN}Consider changing: {bcolors.ENDC}")
            returnTextTips = returnTextTips + "<font color=green>Consider changing:</font>"
            for x in nltk.word_tokenize(tagged_sent_no_pn):
                if Textatistic(x + ".").polysyblword_count != 0:
                    print(x)
                    returnTextTips = returnTextTips + "<br>" + x
        print("\n")
        returnTextTips = returnTextTips + "<br>"

    for (num, sent) in words_per_sentence:
        if num > 23:
            print(f"{bcolors.FAIL}Shorten sentence{bcolors.ENDC}" " (" + str(num) + " words):", sent, "\n")
            returnTextTips = returnTextTips + "<br>Shorten sentence (" + str(num) + " words): " + sent + "<br>"
            #print("Shorten sentence (" + str(num) + "):", sent, "\n")
    
    returnTextTipsWithoutLines = returnTextTips.replace('<br>','')
    if (returnTextTipsWithoutLines == ""):
	    returnTextTips = " There are no recommendations. You are all good."
    returnText = returnText + returnTextTips
    print("Starting")
    print(returnTextTips)
    return returnText

# EXAMPLE Text
example1 = "There was a cat. The cat had a hat. The cat was sad. The cat bought a magic car."

example2 = "Bo, the Portuguese water dog who became the first presidential pet in the Obama White House, romping in the halls of power, died on Saturday. Bo, who was 12, had cancer, Michelle Obama said on Instagram. President Barack Obama said the family had lost a true friend and loyal companion. For more than a decade, Bo was a constant, gentle presence in our lives — happy to see us on our good days, our bad days, and everyday in between, Mr. Obama wrote on Twitter. He tolerated all the fuss that came with being in the White House, had a big bark but no bite, loved to jump in the pool in the summer, was unflappable with children, lived for scraps around the dinner table, and had great hair. "

#getScores(example1)
#getScores(example2)

app.run()