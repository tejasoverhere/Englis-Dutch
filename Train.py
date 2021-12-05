import sys
import Train_AdaBoost as ad
import Train_DecisionTree as dt
import pickle

class Train():

    __slots__  =  "hypothesis","file_path","learning","limit"
    def __init__(self,hypothesis,file_path,learning,limit='8'):
        self.hypothesis=hypothesis
        self.file_path = file_path
        self.learning = learning
        self.limit=limit

    def train(self):
        if self.learning=='dt':
            call = dt.Train_DecisionTree(self.file_path,self.hypothesis,self.limit)
            call.train()
        else:
            call = ad.Train_Adaboost(self.file_path, self.hypothesis, self.limit)
            call.train()


if __name__ == '__main__':
    if len(sys.argv) ==1:
        hypothesis = input("Enter the hypothesis file path")
        file_path = input("Enter file path for the testing data")
        learning = input("Enter dt for Decision Tree Learning, ada for Adaboost learning")
        bool = input("Do you want to specify depth or stump limit? (y/n)")
        if bool == 'n':
            a = Train(hypothesis, file_path, learning)
            a.train()
        else:
            depth = input("Enter depth or stump limit")
            a = Train(hypothesis, file_path, learning, depth)
            a.train()
    elif len(sys.argv)==5:
        hypothesis = sys.argv[1]
        file_path = sys.argv[2]
        learning = sys.argv[3]
        depth = sys.argv[4]
        a = Train(hypothesis,file_path,learning,depth)
        a.train()
    else:
        hypothesis = sys.argv[1]
        file_path = sys.argv[2]
        learning = sys.argv[3]
        a = Train(hypothesis, file_path, learning)
        a.train()
