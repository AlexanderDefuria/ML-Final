
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Test:

    def __init__(self):
        self.part_one_trivial_core = [9, 10, 11, 23, 27]
        self.part_two_trivial_core = [28, 30, 37, 38, 40]
        self.part_three_trivial_core = [43, 45, 46, 49, 50, 51]
        self.part_one_trivial = list(range(1, 28))
        self.part_two_trivial = [28, 29, 30, 32, 34, 37, 38, 40]
        self.part_three_trivial = [43, 44, 45, 46, 48, 49, 50, 51]
        
        self.part_one_proof_core = []
        self.part_two_proof_core = [31, 39, 41, 42]
        self.part_three_proof_core = [47]
        self.part_one_proof = []
        self.part_two_proof = [31, 33, 35, 36, 39, 41, 42]
        self.part_three_proof = [47]

    def pick_proofs(self):
        sections = [
            (self.part_two_proof, self.part_two_proof_core),
            (self.part_two_proof, self.part_two_proof_core),
            (self.part_three_proof, self.part_three_proof_core),
        ]
        questions = []
        for part in sections:
            while True:
                try:
                    group = random.choice(part)
                    choice = random.choice(group)
                    if choice not in questions:
                        questions.append(choice)
                        break
                except:
                    pass
            
        assert len(questions) == 3
        return questions

    def pick_trivials(self):
        questions = []
        for _ in range(3):
            trivial_or_proof = []
            for _ in range(3):
                trivial_or_proof.append(random.choice([True, False]))
            
            for part in enumerate(zip([self.part_one_trivial, self.part_two_trivial, self.part_three_trivial], [self.part_one_trivial_core, self.part_two_trivial_core, self.part_three_trivial_core])):
                if trivial_or_proof[part[0]]:
                    questions.append(random.choice(part[1][0]))
                else:
                    questions.append(random.choice(part[1][1]))
                try:
                    part[1][0].remove(questions[-1])
                    part[1][1].remove(questions[-1])
                except:
                    pass

        assert len(questions) == 9
        return questions
    
def plot():
    
    results = np.zeros(52)
    origin = Test()
    samples = 10000000
    for i in range(samples):
        acceptable = False
        while not acceptable:
            test = Test()
            questions = test.pick_proofs() + test.pick_trivials()
            
            # Check how many questions are core
            core = 0
            for question in questions:
                if question in origin.part_one_trivial_core + origin.part_two_trivial_core + origin.part_three_trivial_core:
                    core += 1
                if question in origin.part_one_proof_core + origin.part_two_proof_core + origin.part_three_proof_core:
                    core += 1
            
            # Check if there are at least half core questions
            if core >= 6:
                acceptable = True
        
        
        for question in questions:
            results[question] += 1
            
    # Get frequency [0,1]
    results = results / 1000
    df = pd.DataFrame(results)
    df = df.drop(0)
    test = Test()
    
    # Get if question is proof or trivial
    question_type = []
    for question in range(1, 52):
        if question in test.part_one_trivial + test.part_two_trivial + test.part_three_trivial:
            question_type.append("Trivial")
        else:
            question_type.append("Proof")
            
    # Get if question is core or not
    question_core = []
    for question in range(1, 52):
        core = test.part_one_trivial_core + test.part_two_trivial_core + test.part_three_trivial_core
        core += test.part_one_proof_core + test.part_two_proof_core + test.part_three_proof_core
        if question in core:
            question_core.append("Core")
        else:
            question_core.append("Not Core")
            
    # Add to dataframe 
    df["Type"] = question_type
    df["Core"] = question_core
    df['Label'] = df["Core"] + " " + df["Type"]
    
    # Plot
    plt.figure(figsize=(16, 6))
    sns.barplot(x=df.index, y=df[0], hue=df["Label"])
    plt.title(f"Question Frequency ({samples} samples)")
    plt.xlabel("Question")
    plt.ylabel("Frequency")
    plt.savefig("question_frequency.png")
    
    
if __name__ == "__main__":
    plot()
    # print(Test().pick_proofs())
    # print(Test().pick_trivials())