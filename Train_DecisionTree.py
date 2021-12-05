import math
import DecisionTreeNode as d
import pickle

class Train_DecisionTree():

    __slots__ = "filename","dumpfilename","depth"
    def __init__(self,a,b,c="5"):
        self.filename = a
        self.dumpfilename = b
        self.depth =int(c)


    def train(self):
        f = open(self.filename,encoding="utf8")  # Put self.filename here

        data = []

        num_A = 0

        count_total =0

        while(f.readable()):
            a = f.readline()
            a = a.strip(" ").strip("\n")
            l = a.split("|")
            if len(l) != 2:
                break
            data.append(self.Classify(l[1],l[0]))
            if (l[0] == 'en'):
                num_A += 1
            if count_total==360:
                print("1")
            count_total+=1

        attribute_list = []
        for i in range(1,len(data[0])):
            attribute_list.append(i)

        f = self.genDTree(data,attribute_list,data,self.depth)
        pickle.dump(f,open(self.dumpfilename,"wb"))



    def genDTree(self,l,attributes,parent_l,depth):
        if len(l) == 0:
            return self.Plurality(parent_l)
        elif self.calculateH2(l)==0:
            if l[0][0] == 1:
                return 'en'
            else:
                return 'nl'
        elif attributes is None or attributes == [] or (depth == len(l[0])-1):
            return self.Plurality(l)
        else:
            print(self.calculateH2(l))
            pos = self.get_BestGain(l,attributes)
            if pos == -1:
                print(self.calculateH2(l))
            attributes_new =[]
            for i in attributes:
                if i != pos:
                    attributes_new.append(i)
            root = d.DecisionTreeNode(pos)
            l1,l2 = self.getSublists(pos,l)   #l1 is the one with 1's, l2 is the one with 0's
            root.left=self.genDTree(l1,attributes_new,l,int(depth+1))
            root.right = self.genDTree(l2,attributes_new, l,int(depth+1))
        return root



    def getSublists(self,pos,l):
        subl_True = []
        subl_False = []
        for j in l:
            f = j[pos]
            if f == 1:
                subl_True.append(j)
            else:
                subl_False.append(j)

        return subl_True,subl_False

    def calculateH(self,num, total):
        if num == 0:
            return 0;
        if num == total:
            return 0;
        p = num / total
        q = 1 - p
        return -1 * ((p * math.log(p, 2)) + (q * math.log(q, 2)))

    def calculateH2(self,l):
        num = 0
        total = len(l)
        for j in l:
            if j[0] == 1:
                num+=1
        if num == 0:
            return 0;
        if num == total:
            return 0;

        p = num / total
        q = 1 - p
        return -1 * ((p * math.log(p, 2)) + (q * math.log(q, 2)))

    def Gain(self,p1, t1, p2, t2, total):
        a = self.calculateH(p1, t1)
        fracA = t1 / total
        b = self.calculateH(p2, t2)
        fracB = t2 / total
        return (fracA * a) + (fracB * b)

    def get_BestGain(self,l,attributeList):
        H_Goal = self.calculateH2(l)
        total_True = 0
        total_False = 0
        numA_True = 0
        numA_False = 0
        chosen_row = 0
        Importance = -1
        max = -1;
        max_pos = -1
        count_total = len(l)

        for i in range(1, len(l[0])):
            if i not in attributeList:
                continue
            total_True = 0
            total_False = 0
            numA_True = 0
            numA_False = 0
            for j in l:
                if j[i] == 1:
                    total_True += 1
                    if j[0] == 1:
                        numA_True += 1
                else:
                    total_False += 1
                    if j[0] == 1:
                        numA_False += 1
            # print("for row " + str(i) + ", Gain: " + str(
            #     H_Goal - self.Gain(numA_True, total_True, numA_False, total_False, count_total)))
            Importance = H_Goal - self.Gain(numA_True, total_True, numA_False, total_False, count_total)
            if Importance > max:
                max = Importance
                max_pos = i

        max_pos = max_pos
        print("Root Position chosen : " + str(max_pos) + "\n")
        return max_pos

    def Classify(self,line , language):
        words = line.split()
        words_lower = line.lower().split()
        words_upper = line.upper().split()
        if language == 'en':
            l = [1]
        else:
            l = [0]


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
        if len(l) == 2:
            l.append(0)


        # Attribute 3 : average word length > 5 then dutch, else english
        if sum(len(l) for l in words) / len(words) > 5:
            l.append(0)
        else:
            l.append(1)

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
        if len(l) == 6:
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

        #Attribute 9 : check for the word "the" , more likely to be English
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

    def Plurality(self,l):
        num = 0
        total = len(l)
        for j in l:
            if j[0] == 1:
                num += 1
        if num >= total-num :    #if 1's are greater or equal
            return 'en'
        else:
            return 'nl'

if __name__ == '__main__':
    Test();