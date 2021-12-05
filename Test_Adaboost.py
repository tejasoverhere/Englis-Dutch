import math
import DecisionTreeNode as d
import pickle
import sys

class Test_Adaboost():
    __slots__ = "hypothesis","file_path"

    def __init__(self,hypothesis,file_path):
        self.hypothesis=hypothesis
        self.file_path = file_path
    def test(self):
        h,z = pickle.load(open(self.hypothesis,"rb"))
        f1 = open(self.file_path, encoding="utf8")
        for line in f1:
            self.printPrediction(h,z, self.Classify(line.strip("\n")))



    def printPrediction(self,h,z,l):
        en = 0
        for i in range(len(h)):
            if l[h[i].val-1] == 1:
                en+= z[i]
            else:
                en-=z[i]
        if en >=0:
            print('en')
        else:
            print('nl')






    def Classify(self,line):

        words = line.split()
        words_lower = line.lower().split()
        words_upper = line.upper().split()
        l = []


        #Attribute 1 : check for ij
        if "ij" in line:
            l.append(0)
        else:
            l.append(1)



        freq_words_en = ['is','a','to']
        freq_words_dutch = ['ik','je','het','de','dat','een']
        # Attribute 2 : check for english common words
        for w in freq_words_en:
            if w in words_lower:
                l.append(1)
                break
        if len(l) == 1:
            l.append(1)


        # Attribute 3 : average word length > 5 then dutch, else english
        if sum(len(l) for l in words) / len(words) > 5:
            l.append(1)
        else:
            l.append(0)

        # Attribute 4 : check for words starting with q, likelier to be english
        flag = 0
        for word in words_lower:
            if word[0] == 'q':
                flag+=1
        if flag==0:
            l.append(0)
        else:
            l.append(1)


        # Attribute 5 : starts with g , likelier to be dutch
        if flag == 0:
            for word in words_lower:
                if word[0] == 'g':
                    flag += 1
        if flag == 0:
            l.append(1)
        else:
            l.append(0)

        freq_words_dutch = ['ik', 'je', 'het', 'de', 'dat', 'een','zijn']
        # Attribute 6 : check for dutch common words
        for w in freq_words_dutch:
            if w in words_lower:
                l.append(0)
                break
        if len(l)==5:
            l.append(1)

        # Attribute 7 : check for e, more likely to be in dutch
        if "e" in line:
            l.append(0)
        else:
            l.append(1)

        # Attribute 8 : check for s, more likely to be in english
        if "s" in line:
            l.append(1)
        else:
            l.append(0)

        # Attribute 9 : check for the word "the" , more likely to be English
        if "the" in words_lower:
            l.append(1)
        else:
            l.append(0)

        #Attribute 10 : check for double vowels
        double_vowels = ['aa','ae','ai''ao','au','ea','ee','ei''eo','eu','ia','ie','ii''io','iu','oa','oe','oi''oo','ou','ua','ue','ui''uo','uu']
        l.append(0)
        for w in double_vowels:
            if w in words_lower:
                l[-1]= 1
                break

        return l