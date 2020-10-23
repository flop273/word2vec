from gensim.models import word2vec
model = word2vec.Word2Vec.load("aozora.model")
results = model.most_similar(positive="曹操", topn=10)
for result in results:
    print(result[0], '\t', result[1])