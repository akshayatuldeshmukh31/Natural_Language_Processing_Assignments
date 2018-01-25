import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    table = list()
    sequence = list()

    for i in range(L):
        table.append(list())
        for j in range(N):
            table[-1].append([-float("inf"), 0])

    for i in range(N):
        sequence.append(-1)

    # Start index
    for tag_ind in range(L):
        table[tag_ind][0][0] = start_scores[tag_ind] + emission_scores[0][tag_ind]
        table[tag_ind][0][1] = 1
        
    # Middle indices - 2 to N
    for word_ind in range(1,N):
        for tag_ind in range(L):
            for prev_tag_ind in range(L):
                tmp = table[prev_tag_ind][word_ind-1][0] + trans_scores[prev_tag_ind][tag_ind] + emission_scores[word_ind][tag_ind]

                if tmp > table[tag_ind][word_ind][0]:
                    table[tag_ind][word_ind][0] = tmp
                    table[tag_ind][word_ind][1] = prev_tag_ind

    # Last index
    start_backward_scan_point = None
    final_prob = -float("inf")

    for tag_ind in range(L):
        tmp = table[tag_ind][N-1][0] + end_scores[tag_ind]
        if tmp > final_prob:
            final_prob = tmp
            start_backward_scan_point = tag_ind

    for word_ind in range(N-1,-1,-1):
        sequence[word_ind] = start_backward_scan_point
        start_backward_scan_point = table[start_backward_scan_point][word_ind][1]

    # y = []
    # for i in xrange(N):
    #     # stupid sequence
    #     y.append(i % L)
    # # score set to 0
    return (final_prob, sequence)
