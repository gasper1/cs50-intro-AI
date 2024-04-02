from logic import *
import copy

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# A, B, C possible statements
people = ['A', 'B', 'C']
statement_symbols = []

# Baseline knowledge
knowledge = And()

for p_talking in people[0]:
    PKnight = Symbol(f"{p_talking} is a Knight")
    PKnave = Symbol(f"{p_talking} is a Knave")
    # Map in the knowledge that each person can be either Knight or Knave (exclusive or)
    knowledge.add(Or(PKnight, PKnave))
    knowledge.add(Not(And(PKnight, PKnave)))
    for p_object in people:
        # Map in the knowledge the possible inferences from what knight/kaves say
        PsaysOKnight = Symbol(f'{p_talking}says{p_object}Knight')
        PsaysOKnave = Symbol(f'{p_talking}says{p_object}Knave')
        OKnight = Symbol(f"{p_object} is a Knight")
        OKnave = Symbol(f"{p_object} is a Knave")
        rule0 = Not(And(PKnight, PsaysOKnave))
        rule1 = Implication(And(PKnight, PsaysOKnight), OKnight)
        rule2 = Implication(And(PKnave, PsaysOKnight), OKnave)
        knowledge.add(rule0)
        knowledge.add(rule1)
        knowledge.add(rule2)
        if p_talking != p_object:
            rule3 = Implication(And(PKnight, PsaysOKnave), OKnave)
            rule4 = Implication(And(PKnave, PsaysOKnave), OKnight)
            knowledge.add(rule3)
            knowledge.add(rule4)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = copy.deepcopy(knowledge)
knowledge0.add(Symbol('AsaysAKnight'))
knowledge0.add(Symbol('AsaysAKnave'))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = copy.deepcopy(knowledge)
knowledge1.add(Symbol('AsaysAKnave'))
knowledge1.add(Symbol('AsaysBKnave'))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = copy.deepcopy(knowledge)
AsaysAlikeB = Symbol('AsaysAlikeB')
BsaysAdiffersB = Symbol('BsaysAdiffersB')
knowledge2.add(AsaysAlikeB)
knowledge2.add(BsaysAdiffersB)
knowledge2.add(Implication(And(AKnight, AsaysAlikeB), BKnight))
knowledge2.add(Implication(And(AKnave, AsaysAlikeB), BKnight))
knowledge2.add(Implication(And(BKnight, BsaysAdiffersB), AKnave))
knowledge2.add(Implication(And(BKnave, BsaysAdiffersB), AKnave))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

AsaysAKnight = Symbol('AsaysAKnight')
AsaysAKnave = Symbol('AsaysAKnave')
BsaysAsaysAKnave = Symbol('BsaysAsaysAKnave')
BsaysCKnave = Symbol('BsaysCKnave')
CsaysAKnight = Symbol('CsaysAKnight')

knowledge3 = And(

    # knowledge3 not generalized. Rules written specifically for this problem.
    # Rules of the game - as in generalization for-loop above
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # Constraint on statement (could be extended also to B and C, but not relevant for puzzle 3)
    Not(And(AKnight, AsaysAKnave)),
    Not(And(AKnave, AsaysAKnave)),

    # Puzzle 3 statements
    Or(AsaysAKnight, AsaysAKnave),
    BsaysAsaysAKnave,
    BsaysCKnave,
    CsaysAKnight,

    # Implication of statements
    Implication(And(BKnight, BsaysAsaysAKnave), AsaysAKnave),
    Implication(And(BKnave, BsaysAsaysAKnave), Not(AsaysAKnave)),
    Implication(And(AKnight, AsaysAKnight), AKnight),
    Implication(And(AKnave, AsaysAKnight), AKnave),
    Implication(And(BKnight, BsaysCKnave), CKnave),
    Implication(And(BKnave, BsaysCKnave), CKnight),
    Implication(And(CKnight, CsaysAKnight), AKnight),
    Implication(And(CKnave, CsaysAKnight), AKnave),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
