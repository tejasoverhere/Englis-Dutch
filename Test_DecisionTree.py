import math
import DecisionTreeNode as d
import pickle

class Test_DecisionTree():
    __slots__ = "hypothesis", "file_path"

    def __init__(self, hypothesis, file_path):
        self.hypothesis = hypothesis
        self.file_path = file_path

    def Test(self):
        f = pickle.load(open("D:\\wd","rb"))

        string = "effect is that alive changes value (since alive was true";

        # printPrediction(f,Classify(string))

        f1 = open('C:\\Users\\migte\\Downloads\\WikiLanguageClassify-master\\WikiLanguageClassify-master\\test_10.dat', encoding="utf8")
        for line in f1:
            self.printPrediction(f, self.Classify(line.strip("\n")))



    def printPrediction(self,f,l):
        if l[f.val-1] == 1:
            if not isinstance(f.left,d.DecisionTreeNode):
                print(f.left)
            else:
                self.printPrediction(f.left,l)
        else:
            if not isinstance(f.right,d.DecisionTreeNode):
                print(f.right)
            else:
                self.printPrediction(f.right,l)



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
        if len(l) == 5:
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

