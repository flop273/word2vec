from gensim.models import word2vec
docs = word2vec.LineSentence("wakachi_text.txt")
model = word2vec.Word2Vec(docs, size=100, min_count=5, window=5, iter=3)
model.save("aozora.model")