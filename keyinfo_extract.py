from script.keywords_tfidf import *
import time


class KeyInfoExtract:
    def __init__(self):
        self.kewords_tfidfer = TFIDF()

    def extract_keywords_tfidf(self, text, num_keywords):
        return self.kewords_tfidfer.extract_keywords(text, num_keywords)


def test():
    nlp = KeyInfoExtract()
    with open('E:\重汽代码\质量云文本摘要\新代码\demo_data\demo3.txt', encoding='utf-8') as fr:
        text = fr.readlines()
        text = ''.join(text)
        # print('text', text)
    keywords_textrank = nlp.extract_keywords_tfidf(text, 10)
    # print(keywords_textrank)

    keyword_list_res_noweight = [i[0] for i in keywords_textrank]
    keyword_list_res_weight = [(i[0] + ',' + str(i[1])) for i in keywords_textrank]
    print(keyword_list_res_noweight)
    print(keyword_list_res_weight)
    keyword_list_res1 = '\t'.join(keyword_list_res_noweight)
    keyword_list_res2 = '\t'.join(keyword_list_res_weight)
    keyword_list_res = '不带权重：' + keyword_list_res1 + '\n\n' + '带权重：' + keyword_list_res2
    print(keyword_list_res)


start_time = time.time()
print(start_time)
test()
end_time = time.time()
print(end_time)
print(end_time - start_time)
