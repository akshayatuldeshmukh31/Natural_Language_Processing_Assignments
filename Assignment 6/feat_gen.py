#!/bin/python
import nltk

company_set = set()
product_set = set()
location_set = set()
person_set = set()
sports_team_set = set()
tv_show_set = set()
award_set = set()
festival_set = set()
newspapers_set = set()
transportation_set = set()
recurring_events_set = set()
holiday_set = set()
other_set = set()
agency_set = set()
movie_set = set()

business_brand_set = set()
random_set = set()

vocab_to_tag_dict = dict()

not_required_puncs = set(["/", ","])

path = "./data/lexicon/"

def preprocess_line(line_tokens):

    i = 0
    length = len(line_tokens)

    while i!=len(line_tokens):
        if len(line_tokens[i])==1 and (line_tokens[i] in not_required_puncs):
            del line_tokens[i]
            length = length - 1
        # elif line_tokens[i][-1] in not_required_puncs:
        #     line_tokens[i] = line_tokens[i][:-1]
        #     i = i + 1
        else:
            i = i + 1

    return line_tokens

def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """

    for sent in train_sents:
        tmp = list()
        for i in range(len(sent)):
            tmp.append(unicode(sent[i]))
        pos_tags = nltk.pos_tag(tmp)
        for tag_tuple in pos_tags:
            if vocab_to_tag_dict.get(tag_tuple[0], -1)==-1:
                vocab_to_tag_dict[tag_tuple[0]] = tag_tuple[1]

    # B-company
    for filename in ["automotive.make", "business.consumer_company", "business.sponsor", "cvg.cvg_developer", "venture_capital.venture_funded_company"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in company_set:
                        company_set.add(tok)
                    if tok.lower() not in company_set:
                        company_set.add(tok.lower())
                    if tok.upper() not in company_set:
                        company_set.add(tok.upper())

    # B-product
    for filename in ["automotive.model", "business.consumer_product", "product"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in product_set:
                        product_set.add(tok)
                    if tok.lower() not in product_set:
                        product_set.add(tok.lower())
                    if tok.upper() not in product_set:
                        product_set.add(tok.upper())

    # B-geo-loc
    for filename in ["location", "location.country"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in location_set:
                        location_set.add(tok)
                    if tok.lower() not in location_set:
                        location_set.add(tok.lower())
                    if tok.upper() not in location_set:
                        location_set.add(tok.upper()) 

    # B-person
    for filename in ["lastname.5000", "people.family_name", "people.person", "people.person.lastnames"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in person_set:
                        person_set.add(tok)
                    if tok.lower() not in person_set:
                        person_set.add(tok)


    # B-sportsteam
    for filename in ["sports.sports_team"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in sports_team_set:
                        sports_team_set.add(tok)
                    if tok.lower() not in sports_team_set:
                        sports_team_set.add(tok.lower())
                    if tok.upper() not in sports_team_set:
                        sports_team_set.add(tok.upper())
    # B-tvshow
    for filename in ["tv.tv_program"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in tv_show_set:
                        tv_show_set.add(tok)
                    if tok.lower() not in tv_show_set:
                        tv_show_set.add(tok.lower())
                    if tok.upper() not in tv_show_set:
                        tv_show_set.add(tok.upper()) 

    # for filename in ["award.award"]:
    #     with open(path + filename, "r") as fp:
    #         for line in fp:
    #             line_tokens = preprocess_line(line.strip().split())

    #             for tok in line_tokens:
    #                 if tok not in award_set:
    #                     award_set.add(tok)
    #                 if tok.lower() not in award_set:
    #                     award_set.add(tok.lower())
    #                 if tok.upper() not in award_set:
    #                     award_set.add(tok.upper()) 

    for filename in ["base.events.festival_series"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in festival_set:
                        festival_set.add(tok)
                    if tok.lower() not in festival_set:
                        festival_set.add(tok.lower())
                    if tok.upper() not in festival_set:
                        festival_set.add(tok.upper()) 

    for filename in ["book.newspaper"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in newspapers_set:
                        newspapers_set.add(tok)
                    if tok.lower() not in newspapers_set:
                        newspapers_set.add(tok.lower())
                    if tok.upper() not in newspapers_set:
                        newspapers_set.add(tok.upper())

    for filename in ["transportation.road"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in transportation_set:
                        transportation_set.add(tok)
                    if tok.lower() not in transportation_set:
                        transportation_set.add(tok.lower())
                    if tok.upper() not in transportation_set:
                        transportation_set.add(tok.upper())

    for filename in ["sports.sports_league","time.recurring_event"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in recurring_events_set:
                        recurring_events_set.add(tok)
                    if tok.lower() not in recurring_events_set:
                        recurring_events_set.add(tok.lower())
                    if tok.upper() not in recurring_events_set:
                        recurring_events_set.add(tok.upper())

    for filename in ["time.holiday"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in holiday_set:
                        holiday_set.add(tok)
                    if tok.lower() not in holiday_set:
                        holiday_set.add(tok.lower())
                    if tok.upper() not in holiday_set:
                        holiday_set.add(tok.upper())

    for filename in ["lower.10000"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in other_set:
                        other_set.add(tok)
                    if tok.lower() not in other_set:
                        other_set.add(tok.lower())
                    if tok.upper() not in other_set:
                        other_set.add(tok.upper()) 

    for filename in ["movies"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in movie_set:
                        movie_set.add(tok)
                    if tok.lower() not in movie_set:
                        movie_set.add(tok)
                    if tok.upper() not in movie_set:
                        movie_set.add(tok)

    for filename in ["government.government_agency"]:
        with open(path + filename, "r") as fp:
            for line in fp:
                line_tokens = preprocess_line(line.strip().split())

                for tok in line_tokens:
                    if tok not in agency_set:
                        agency_set.add(tok)
                    if tok.lower() not in agency_set:
                        agency_set.add(tok.lower())
                    if tok.upper() not in agency_set:
                        agency_set.add(tok.upper()) 

    pass

def long_word_form(word):
    form = list()

    for ch in word:
        if ch.isupper():
            form.append("X")
        elif ch.islower():
            form.append("x")
        else:
            form.append(ch)

    return "".join(form)

def preprocess(word):

    new_word = ""

    for i in range(len(word)):
        if word[i].isalnum():
            new_word += word[i]
    return unicode(new_word)

def short_word_form(word):
    form = list()
    flag = 0

    for ch in word:
        if ch.isupper():
            if flag!=1:
                form.append("X")
                flag = 1
        elif ch.islower():
            if flag!=2:
                form.append("x")
                flag = 2
        else:
            form.append(ch)
            flag = 0

    return "".join(form)

def has_puncs(word):
    for ch in word:
        if not ch.isalnum():
            return True
    return False

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = preprocess(unicode(sent[i]))
    # word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    # if len(word)>0:
    #     if word[0].isupper():
    #         ftrs.append("FCASE")
    # if has_puncs(word):
    #     ftrs.append("PUNCS")
    if word in company_set or word.lower() in company_set or word.upper() in company_set:
        ftrs.append("COMPANY")
    if word in product_set or word.lower() in product_set or word.upper() in product_set:
        ftrs.append("PRODUCT")
    if word in location_set or word.lower() in location_set or word.upper() in location_set:
        ftrs.append("LOCATION")
    if word in person_set or word.lower() in person_set or word.upper() in person_set:
        ftrs.append("PERSON")
    if word in sports_team_set or word.lower() in sports_team_set or word.upper() in sports_team_set:
        ftrs.append("SPORTS_TEAM")
    if word in tv_show_set or word.lower() in tv_show_set or word.upper() in tv_show_set:
        ftrs.append("TV_SHOW")
    if word in newspapers_set or word.lower() in newspapers_set or word.upper() in newspapers_set:
        ftrs.append("NEWSPAPER")
    if word in transportation_set or word.lower() in transportation_set or word.upper() in transportation_set:
        ftrs.append("TRANSPORT")
    if word in festival_set or word.lower() in festival_set or word.upper() in festival_set or word in recurring_events_set or word.lower() in recurring_events_set or word.upper() in recurring_events_set or word in holiday_set or word.lower() in holiday_set or word.upper() in holiday_set:
        ftrs.append("RECURRING_EVENT")
    if word in other_set or word.lower() in other_set or word.upper() in other_set:
        ftrs.append("OTHER")
    if word in movie_set or word.lower() in movie_set or word.upper() in movie_set:
        ftrs.append("MOVIE")
    if word in agency_set or word.lower() in agency_set or word.upper() in agency_set:
        ftrs.append("GOVT_AGENCY")
    
    ftrs.append(short_word_form(word))
    ftrs.append(long_word_form(word))

    # if vocab_to_tag_dict.get(word, -1)!=-1:
    #     ftrs.append("POS_" + vocab_to_tag_dict[word])

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)

        if i < len(sent)-1:
            if (word in location_set or word.lower() in location_set or word.upper() in location_set) and (unicode(sent[i+1]) in location_set or unicode(sent[i+1]).lower() in location_set or unicode(sent[i+1]).upper() in location_set):
                ftrs.append("BIGRAM_LOCATION")
            if (word in sports_team_set or word.lower() in sports_team_set or word.upper() in sports_team_set) and (unicode(sent[i+1]) in sports_team_set or unicode(sent[i+1]).lower() in sports_team_set or unicode(sent[i+1]).upper() in sports_team_set):
                ftrs.append("BIGRAM_SPORTS_TEAM")
            if (word in movie_set or word.lower() in movie_set or word.upper() in movie_set) and (unicode(sent[i+1]) in movie_set or unicode(sent[i+1]).lower() in movie_set or unicode(sent[i+1]).upper() in movie_set):
                ftrs.append("BIGRAM_MOVIES")
            # if len(word)>0 and len(unicode(sent[i+1]))>0:
            #     if word[0].isupper() and unicode(sent[i+1])[0].isupper():
            #         ftrs.append("UPPER_UPPER")
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "MUMBaI" ]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
