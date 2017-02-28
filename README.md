## Algorithm
### Data structure
```python
# morpheme
m = {
  value: "하다",
  tag: "VV"
}

# word : sequence of morpheme
w = mmm...

# sentence : sequence of word and space
s = w w w w....
```
### Process & Function
```python
def backoff(prevprev_morpheme, prev_morpheme):
    try:
        result = trigram_lm[prevprev_morpheme][prev_morpheme]
    except KeyError as e:
        try:
            result = bigram_lm[prev_morpheme]
        except KeyError as e:
            result = unigram_lm
    return result

def backoff_iter(prevprev_morpheme, prev_morpheme, prediction_list):
    result = backoff(preprev_morpheme, prev_morpheme)
    for item in result:
        if item.tag == end_of_word:
            prediction_list[-1].append(item)
            return
        if item.tag == [prevprev_morpheme.tag, prev_morphem.tag]:
            prediction_list[-1].append(item)
            backoff_iter(prev_morpheme, item, prediction_list)

def prediction(input_word):
    morpheme_list = word_to_morpheme(input_word)
    seed_morpheme_list = backoff(morpheme_list[-2], morpheme_list[-1])

    prediction_list = []
    for item in seed_morpheme_list:
        if item.tag == [morpheme_list[-2].tag, morpheme_list[-1].tag]:
            prediction_list.append([])
            backoff_iter(prev_morpheme, item, prediction_list)

    return prediction_list
```
