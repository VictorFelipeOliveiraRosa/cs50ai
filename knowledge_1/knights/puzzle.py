from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(Or(BKnave, BKnight)),
    Not(Or(CKnave, CKnight)),
    Or(AKnight, AKnave, And(AKnight, AKnave)),
    Not(And(AKnight, AKnave)),
    Not(AKnight),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Not(And(AKnight, BKnave)),
    Not(And(AKnight, BKnight)),
    Not(Or(CKnave, CKnight)),
    Implication(Not(And(BKnave, BKnight)), BKnight),
    Implication(And(AKnight, AKnave), AKnave),
)


# Puzzle 2
# A says "We are the same kind."
# # B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, Not(And(BKnight, BKnave))),
    Or(AKnave, Not(BKnave)),
    Or(AKnave, BKnave),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),
    Implication(AKnave, BKnight)
    # Implication(And(AKnave, Or(BKnave, BKnight)), AKnave),
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(And(BKnight, AKnave), And(BKnave, AKnight)),
    Or(And(BKnave, CKnight), And(BKnight, CKnave)),
    Or(And(CKnave, AKnave), And(CKnight, AKnight)),
    # And(Or(CKnave, CKnight), AKnight),
    # And(Or(BKnave, BKnight), CKnave),
    # And(Or(BKnave, BKnight), AKnave),
    # Or(AKnave, AKnight),
    Or(
        # And(AKnave, Not(BKnave), Not(CKnight)),
        And(AKnight, Not(BKnight), Not(CKnave)),
        # And(BKnight, Not(AKnight), Not(CKnight)),
        And(BKnave, Not(AKnave), Not(CKnave)),
        # And(CKnave, Not(AKnight), Not(BKnave)),
        And(CKnight, Not(AKnave), Not(BKnight)),
    ),
    Implication(Not(And(BKnight, CKnave)), AKnight),
    Implication(Not(And(AKnave, CKnave)), BKnave),
    Implication(Not(And(AKnave, BKnight)), CKnight),
    # Not(And(AKnave, AKnight)),
    # Not(And(BKnave, BKnight)),
    # Not(And(CKnave, CKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
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
