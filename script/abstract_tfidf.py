import re
import jieba
import os


class TFIDF_ABS:
    # step1加载数据
    def __init__(self, text, count):
        # 获取当前文件所在文件夹的路径
        current_folder_path = os.path.dirname(os.path.abspath(__file__))
        self.idf_file = os.path.join(current_folder_path, 'stopwords.txt')
        self.stopwords = self.stopwordslist()
        self.text = text
        self.count = count

    # step2清洗数据
    def clear_data(self):
        text = re.sub(r'[[0-9]*]', ' ', self.text)  # 去除类似[1]，[2]
        # sentences = text.split('\n')  # 分句
        sentences = [sentence for sentence in re.split(r'[？！。;；\n\r]', text) if sentence]
        # print('sentences', sentences)
        return sentences

    # step3加载停用词
    def stopwordslist(self):
        stopwords = [line.strip() for line in open(self.idf_file, 'r', encoding='utf-8').readlines()]
        return stopwords

    # step4统计文本词频
    def count_words(self):
        word2count = {}  # line 1
        for word in jieba.cut(self.text):  # 对整个文本分词
            if word not in self.stopwords:
                if word not in word2count.keys():
                    word2count[word] = 1
                else:
                    word2count[word] += 1
        for key in word2count.keys():
            word2count[key] = word2count[key] / max(word2count.values())
        # print(word2count)
        return word2count

    # step5计算句子得分
    def get_sentence_score(self):
        word2count = self.count_words()
        sentences = self.clear_data()
        sent2score = {}
        for sentence in sentences:
            for word in jieba.cut(sentence):  # 将sentence分词，对每个word循环
                if word in word2count.keys():  # 使用if检查word2count.keys()中是否存在该单词
                    if len(sentence) < 100:  # 这里我指定计算句子长度小于300的那部分，你可以根据需要更改
                        if sentence not in sent2score.keys():
                            sent2score[sentence] = word2count[word]
                        else:
                            sent2score[sentence] += word2count[word]
        # print('sent2score', sent2score)
        return sent2score

    # step6字典排序
    def dic_order_value_and_get_key(self):
        dicts = self.get_sentence_score()
        # 字典根据value排序，并且获取value排名前几的key
        final_result = []
        # 先对字典排序
        sorted_dic = sorted([(k, v) for k, v in dicts.items()], reverse=True)
        tmp_set = set()  # 定义集合 会去重元素
        for item in sorted_dic:
            tmp_set.add(item[1])
        for list_item in sorted(tmp_set, reverse=True)[:self.count]:
            for dic_item in sorted_dic:
                if dic_item[1] == list_item:
                    final_result.append(dic_item[0])
        print('final_result', final_result)
        return final_result


