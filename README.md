### #research
### python server of korean word suggestion system
## korean word prediction

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

### How to run
```python
python setup.py
python run.py
```

### Courpus
- target/pure.txt
- lm_raw/bi/bigram_raw_{0~7}.txt
- lm_raw/tri/trigram_raw_{0~7}.txt
- lm_raw/uni/unigram_raw_{0~7}.txt
