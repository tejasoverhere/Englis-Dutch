import sys
import Test_Adaboost as ad
import Test_DecisionTree as dt
import pickle

class Test():

    __slots__  =  "hypothesis","file_path"
    def __init__(self,hypothesis,file_path):
        self.hypothesis=hypothesis
        self.file_path = file_path


    def run(self):
        pickle.load(open(self.hypothesis, "rb"))
        if isinstance(pickle.load(open(self.hypothesis, "rb")),tuple):
            call = ad.Test_Adaboost(self.hypothesis,self.file_path)
            call.test()
        else:
            call = dt.Test_DecisionTree(self.hypothesis,self.file_path)
            call.Test()

if __name__ == '__main__':
    if len(sys.argv)!=3:
        hypothesis = input("Enter the hypothesis file path")
        file_path = input("Enter file path for the testing data")
    else:
        hypothesis = sys.argv[1]
        file_path = sys.argv[2]
    a = Test(hypothesis,file_path)
    a.run()



