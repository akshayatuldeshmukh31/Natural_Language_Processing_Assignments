import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.add_state('A')
    f.add_state('B')
    f.add_state('C')
    f.add_state('D')
    f.add_state('E')
    f.add_state('F')
    f.add_state('G')
    f.add_state('H')
    f.initial_state = 'start'

    # *** Transition on MSB - 1 ***
    f.add_arc('start', 'A', ('1'), [kFRENCH_TRANS[100]])

    for i in range(2,9):
    	f.add_arc('start', 'A', (str(i+1)), [kFRENCH_TRANS[i+1] + " " + kFRENCH_TRANS[100]])

    # Transition on middle bit - 0 and 8
    f.add_arc('A', 'B', ('0'), ())
    f.add_arc('A', 'B', ('8'), [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])

    # Transitions on state B - for 0 and 8
    f.add_arc('B', 'B', ('0'), ())

    for i in range(9):
    	f.add_arc('B', 'B', (str(i+1)), [kFRENCH_TRANS[i+1]])

    # Transition on middle bit - 1
    f.add_arc('A', 'C', ('1'), (" "))

    # Transitions on state C
    f.add_arc('C', 'C', ('0'), [kFRENCH_TRANS[10]])

    for i in range(1,7):
    	f.add_arc('C', 'C', (str(i)), [kFRENCH_TRANS[i+10]])
    
    for i in range(7,10):
    	f.add_arc('C', 'C', (str(i)), [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[i]])

    # Transition on middle bit - 2,3,4,5,6
    for i in range(2,7):
    	f.add_arc('A', 'D', (str(i)), [kFRENCH_TRANS[i*10]])

    # Transitions on state D
    f.add_arc('D', 'D', ('0'), ())
    f.add_arc('D', 'D', ('1'), [kFRENCH_AND + " " + kFRENCH_TRANS[1]])

    for i in range(2,10):
    	f.add_arc('D', 'D', (str(i)), [kFRENCH_TRANS[i]])

    # Transition on middle bit - 7
    f.add_arc('A', 'E', ('7'), [kFRENCH_TRANS[60]])
    f.add_arc('E', 'E', ('0'), [kFRENCH_TRANS[10]])
    f.add_arc('E', 'E', ('1'), [kFRENCH_AND + " " + kFRENCH_TRANS[11]])

    # Transition on state E
    for i in range(2,7):
    	f.add_arc('E', 'E', (str(i)), [kFRENCH_TRANS[i+10]])

    for i in range(7,10):
    	f.add_arc('E', 'E', (str(i)), [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[i]])

    # Transition on middle bit - 9
    f.add_arc('A', 'F', ('9'), [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])

    # Transition on state F
    f.add_arc('F', 'F', ('0'), [kFRENCH_TRANS[10]])

    for i in range(1,7):
    	f.add_arc('F', 'F', (str(i)), [kFRENCH_TRANS[i+10]])

    for i in range(7,10):
    	f.add_arc('F', 'F', (str(i)), [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[i]])

    # *** Transition on MSB - 0 ***
    f.add_arc('start', 'G', ('0'), ())

    # Transition on MSB - 0
    f.add_arc('G', 'H', ('0'), ())

    # Transitions on state H
    for i in range(0,10):
    	f.add_arc('H', 'H', (str(i)), [kFRENCH_TRANS[i]])

    # Transition on MSB - 1
    f.add_arc('G', 'C', ('1'), ())

    # Transition on MSB - 2,3,4,5,6
    for i in range(2,7):
    	f.add_arc('G', 'D', (str(i)), [kFRENCH_TRANS[i*10]])

    # Transition on MSB - 7
    f.add_arc('G', 'E', ('7'), [kFRENCH_TRANS[60]])

    # Transition on MSB - 8
    f.add_arc('G', 'B', ('8'), [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])

    # Transition on MSB - 9
    f.add_arc('G', 'F', ('9'), [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])


    f.set_final('B')
    f.set_final('C')
    f.set_final('D')
    f.set_final('E')
    f.set_final('F')
    f.set_final('H')

    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
