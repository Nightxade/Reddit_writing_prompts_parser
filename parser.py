import random
import nltk
from nltk.tokenize import word_tokenize
import praw as praw
from praw.models import MoreComments
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

# ---------------------------
# INSERT PRAW_INFO
# ---------------------------


# Define subreddit
subreddit = reddit.subreddit("WritingPrompts")

# Receive part of speech input
pos_input = input("Do you wish to modify a verb or a noun? (V/N)")

is_verb = False
# Receive word input
if pos_input == 'V':
    is_verb = True
    word_input = input("Enter a verb: ")
elif pos_input == 'N':
    word_input = input("Enter a noun: ")
else:
    print("Invalid Input. Enter V or N")
    quit()

# Create adjectives and adverbs sets
adjectives = set()
adverbs = set()


for submission in subreddit.top(limit=50):
    # print(submission.title)
    top_level_comments = list(submission.comments)

    # Delete auto mod comment
    del top_level_comments[0]

    # Iterate through other comments
    for comment in top_level_comments:

        # POS in text
        text_pos = []

        # check if it's more comments link
        if isinstance(comment, MoreComments):
            continue

        text = str(comment.body)

        if text == "[deleted]" or text == "[removed]":
            continue

        # print(text)
        length = len(text)

        # Split text
        txt_arr = word_tokenize(text)
        ans = nltk.pos_tag(txt_arr)

        # print(text)

        # Loop through all words and filter out into corresponding sets
        for i in range(len(ans)):
            word = ans[i]

            # Word and Part of Speech
            w = word[0]
            pos = word[1]

            # If it has a non-alphabetic character or is one character, continue
            if not w.isalpha() or len(w) <= 1: continue

            if word_input == w:
                if not is_verb:
                    adjective = True
                    index = i - 1
                    while adjective:
                        # Check for adjective
                        adj_w = ans[index][0]
                        adj_pos = ans[index][1]

                        # If it has a non-alphabetic character or is one character, continue
                        if not adj_w.isalpha() or len(adj_w) <= 1:
                            index -= 1
                            continue

                        if adj_pos == 'JJ' or adj_pos == 'JJR' or adj_pos == 'JJS':
                            adjectives.add(adj_w)
                            index -= 1
                        else:
                            adjective = False

                else:
                    adverb = True
                    index = i - 1
                    while adverb:
                        # Check for adjective
                        adv_w = ans[index][0]
                        adv_pos = ans[index][1]

                        # If it has a non-alphabetic character or is one character, continue
                        if not adv_w.isalpha() or len(adv_w) <= 1:
                            index -= 1
                            continue

                        if adv_pos == 'RB' or adv_pos == 'RBR' or adv_pos == 'RBS':
                            adverbs.add(adv_w)
                            index -= 1
                        else:
                            adverb = False

                    adverb = True
                    index = i + 1
                    while adverb:
                        # Check for adjective
                        adv_w = ans[index][0]
                        adv_pos = ans[index][1]

                        # If it has a non-alphabetic character or is one character, continue
                        if not adv_w.isalpha() or len(adv_w) <= 1:
                            index += 1
                            continue

                        if adv_pos == 'RB' or adv_pos == 'RBR' or adv_pos == 'RBS':
                            adverbs.add(adv_w)
                            index += 1
                        else:
                            adverb = False


if not is_verb:
    print("Potential adjectives: ", end="")
    for adj in adjectives:
        print(adj, end=", ")
else:
    print("Potential adverbs: ", end="")
    for adv in adverbs:
        print(adv, end=", ")
