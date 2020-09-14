from collections import Counter
import random
import nltk
from nltk import trigrams, bigrams
from nltk.util import ngrams
from collections import Counter, defaultdict


f = open('book2.txt', 'r')
new = f.read()
new = new.strip('\n').lower().replace(',', '')
new = new.split()
resultwords  = [word for word in new]
result = ' '.join(resultwords)

# Tokenise and create counter for unique words count
tokenize_words = nltk.word_tokenize(result)
count_elements = Counter(tokenize_words)

# Method to get unigrams
def get_unigrams(count_elements, lstr):
    # Sort the tokenised words in descending order 
    desc_words = {val: v for val, v in sorted(count_elements.items(), reverse=True, key=lambda item: item[1])}
    output = ""
    ctr = 0
    # Calculating maximum likelihood estimate (MLE)
    desc_len = len(desc_words)
    for word in desc_words:
        desc_words[word] = desc_words[word] / desc_len
    for i in desc_words:
        if i.isalnum():
            ctr += 1
            output += i
            output += " "
        if ctr > 20:
            break
    return lstr + " " + output

# Return bigram generated sentences
def get_bigrams(tokenize_words, lstr):
    # Method to get Bigrams generated sentences
    model_bi = defaultdict(lambda: defaultdict(lambda: 0))
    # Count frequency of co-occurance  
    for word1, word2 in bigrams(tokenize_words):
        model_bi[(word1)][word2] += 1

   # Calculating maximum likelihood estimate (MLE)
    for word1 in model_bi:
        vocab_size = float(sum( model_bi[word1].values()))
        for word2 in  model_bi[word1]:
             model_bi[word1][word2] /= vocab_size
                
    # Create statements
    text = [random.choice(list(model_bi))]
    done = False 
    ctr = 0 # Counter element to break the loop

    while not done:
        ctr += 1
        temp_check = dict()
        # Using the maximum threshold for the probability
        for word in dict(model_bi[text[-1]]):
            temp_check[word] = model_bi[text[-1]][word]
        desc_sorted = {val: v for val, v in sorted(temp_check.items(), reverse=True, key=lambda item: item[1])}
        final_value = list(desc_sorted)[random.randint(0, len(temp_check) - 1)]
        text.append(final_value)
        
        # If no word is available, break
        if text[-2:] == [None, None]:
            done = True
        # Make a threshold of 15 words in a sentence
        if ctr > 15:
          done = True
    # Ouput the sentence generates using Trigram
    return lstr + ' ' + ' '.join([txt for txt in text if txt])
    
# Method to get trigram sentences
def get_trigrams(tokenize_words, lstr):
    # Create a placeholder for model
    model_tri = defaultdict(lambda: defaultdict(lambda: 0))
    
    # Count frequency of co-occurance
    for word1, word2, word3 in trigrams(tokenize_words, pad_right=True, pad_left=True):
        model_tri[(word1, word2)][word3] += 1

    # Calculating maximum likelihood estimate (MLE)
    for prev_words in model_tri:
        vocab_size = float(sum(model_tri[prev_words].values()))
        for word3 in model_tri[prev_words]:
            model_tri[prev_words][word3] /= vocab_size

    # Create sentences using it 
    words = random.choice(list(model_tri))
    text = [words[0], words[1]]
    done = False
    ctr = 0

    while not done:
        ctr += 1
      # Use the maximum threshold for the probbaility
        temp_check = {}
        for word in dict(model_tri[text[-2], text[-1]]):
            temp_check[word] = model_tri[text[-2], text[-1]][word]
        desc_sorted = {val: v for val, v in sorted(temp_check.items(), reverse=True, key=lambda item: item[1])}
        final_value = list(desc_sorted)[random.randint(0, len(temp_check) - 1)]
        text.append(final_value)

        # If no more words available, break
        if text[-2:] == [None, None]:
          done = True

        # Make a threshold of 15 words in a sentence
        if ctr > 15:
          done = True
    # Ouput the sentence generates using Trigram
    return lstr + ' ' + ' '.join([txt for txt in text if txt])

# Method to get four grams sentences
def get_four_grams(result, lstr):
    # Function to generate 4-grams from sentences.
    def extract_ngrams(data, num):
        word1, word2, word3 = "", "", ""
        n_grams = ngrams(nltk.word_tokenize(data), num)
        model_four = defaultdict(lambda: defaultdict(lambda: 0))
        for grams in n_grams:
            word1 = grams[0]
            word2 = grams[1]
            word3 = grams[2]
            word4 = grams[3]
            # Count the frequency of occurance
            model_four[(word1, word2, word3)][word4] += 1
        return model_four
    # Method to get Bigrams generated sentences
    model_four = extract_ngrams(result, 4)
   # Calculating maximum likelihood estimate (MLE)
    for prev_words in model_four:
        vocab_size = float(sum(model_four[prev_words].values()))
        for word4 in model_four[prev_words]:
            model_four[prev_words][word4] /= vocab_size
    
    # Initialise the start
    words = random.choice(list(model_four))
    text = [words[0], words[1], words[2]]
    done = False 
    ctr = 0 # Counter element to break the loop
    
    while not done:
        ctr += 1
        temp_check = dict()
        # Using the maximum threshold for the probability
        for word in dict(model_four[text[-3], text[-2], text[-1]]):
            temp_check[word] = model_four[text[-3], text[-2], text[-1]][word]
        desc_sorted = {val: v for val, v in sorted(temp_check.items(), reverse=True, key=lambda item: item[1])}
        final_value = list(desc_sorted)[random.randint(0, len(temp_check) - 1)]
        text.append(final_value)
        
        # If no word is available, break
        if text[-2:] == [None, None]:
            done = True
        # Make a threshold of 15 words in a sentence
        if ctr > 15:
          done = True
    # Ouput the sentence generates using Trigram
    return lstr + ' ' + ' '.join([txt for txt in text if txt])

print(get_bigrams(tokenize_words, "I suppose"))

print(get_trigrams(tokenize_words, "I suppose"))

print(get_four_grams(result, "I suppose"))

print(get_unigrams(count_elements, "I suppose"))