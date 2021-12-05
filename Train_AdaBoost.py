import math
import DecisionTreeNode as d
import pickle

class Train_Adaboost():
    __slots__ = "filename", "dumpfilename", "stumps"

    def __init__(self, a, b, c="5"):
        self.filename = a
        self.dumpfilename = b
        self.stumps = int(c)
    def train(self):
        f = open(self.filename,encoding="utf8")  # Put FileName here
    
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
    
        h1,z1 = self.Adaboost(data,self.stumps)
        pickle.dump((h1,z1),open(self.dumpfilename,"wb"))
    
    
    
    def genDTree(self,l,attributes,parent_l,w):
    
        #Configuring l as per weights
        n = len(l)
    
        for i in range(len(l)):
            count = [round(j*n) for j in w]
        temp_list = []
        for i in range(len(count)):
            j = l[i]
            for _ in range(count[i]):
                temp_list.append(j)
    
        l = temp_list
        if len(l) == 0:
            return self.Plurality(parent_l)
        elif self.calculateH2(l)==0:
            if l[0][0] == 1:
                return 'en'
            else:
                return 'nl'
        elif attributes is None or attributes == []:
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
            l1,l2 = self.getSublists(pos,l) #l1 is the one with 1's, l2 is the one with 0's
    
            if len(l1) == 0:
                root.left= self.Plurality(l)
            elif self.calculateH2(l1) == 0:
                if l1[0][0] == 1:
                    root.left= 'en'
                else:
                    root.left= 'nl'
            elif attributes_new is None or attributes_new == []:
                root.left= self.Plurality(l1)
            else:
                # root.left = d.DecisionTreeNode(get_BestGain(l1, attributes_new))
                root.left = 'en'
                
            if len(l2) == 0:
                root.right= self.Plurality(l)
            elif self.calculateH2(l2) == 0:
                if l2[0][0] == 1:
                    root.right= 'en'
                else:
                    root.right= 'nl'
            elif attributes_new is None or attributes_new == []:
                root.right= self.Plurality(l2)
            else:
                # root.right = d.DecisionTreeNode(get_BestGain(l2, attributes_new))
                root.right = 'nl'
            
        return root
    
    
    def Adaboost(self,data,K):
        count = len(data)
        error_corrected = 1/(count*2)
        w=[]
        for i in range(count):
            w.append(1/count)
        h = []
        z = []
        attribute_list = []
        for i in range(1, len(data[0])):
            attribute_list.append(i)
            
        for k in range(K):
            h.append(self.genDTree(data,attribute_list,data,w))
            #calculate errors
            error = self.ErrorRate(h[k].val,data,w)
            w = self.Updateweights(h[k].val,data,w,error)
            total_weigth = sum(w)
            for i in range(len(w)):
                w[i]/=total_weigth
            if error == 1:
                error = 0.999999
            if error == 0:
                error= 0.0000001
            z.append(math.log((1-error)/error))
    
        return h,z
    
    
    
    
    
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
    
    def ErrorRate(self,pos,l,w):
        error = 0
        for j in range(len(l)):
            f = l[j][pos]
            if (f == 1 and l[j][0] == 0) or(f == 0 and l[j][0] == 1):
                error +=w[j]
    
        return error
    
    def Updateweights(self,pos,l,w,error):
        delta = float(error/(1-error))
        for j in range(len(l)):
            f = l[j][pos]
            if l[j][0] == l[j][pos]:
                w[j] *= delta
    
        return w
    
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
            #     H_Goal - Gain(numA_True, total_True, numA_False, total_False, count_total)))
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
            l.append(0)
        else:
            l.append(1)
    
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