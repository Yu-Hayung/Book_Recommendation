import numpy as np
import itertools
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def find_keyword(doc, n_gram_range=(2, 2)):
    okt = Okt()
    tokenized_doc = okt.pos(doc)
    tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'Noun'])

    n_gram_range_num = n_gram_range # 몇개의 조합으로 몇개의 단어를 만들 것인가.

    count = CountVectorizer(ngram_range=n_gram_range_num).fit([tokenized_nouns])
    candidates = count.get_feature_names_out()
    # print(candidates)

    model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
    doc_embedding = model.encode([doc])
    candidate_embeddings = model.encode(candidates)

    top_n = 2
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
    # print("only_sbert", keywords)

    # aa = max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n=top_n, nr_candidates=10)
    # print("max_sum_similar, candi=10", aa)
    #
    # bb = max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n=top_n, nr_candidates=30)
    # print("max_sum_similar, candi=30", bb)

    cc = mmr(doc_embedding, candidate_embeddings, candidates, top_n=top_n, diversity=0.2)
    # print("mmr, diver=0.2", cc)

    dd = mmr(doc_embedding, candidate_embeddings, candidates, top_n=top_n, diversity=0.7)
    # print("mmr, diver=0.7", dd)


    #백단에서 처리 하기 쉽게 처리 예제{"keyword":['군장학생 입대', '어머니 동생']}
    keyword_dic = {"keyword": cc}

    return keyword_dic, cc



def max_sum_sim(doc_embedding, candidate_embeddings, words, top_n, nr_candidates):
    # 문서와 각 키워드들 간의 유사도
    distances = cosine_similarity(doc_embedding, candidate_embeddings)

    # 각 키워드들 간의 유사도
    distances_candidates = cosine_similarity(candidate_embeddings,
                                            candidate_embeddings)

    # 코사인 유사도에 기반하여 키워드들 중 상위 top_n개의 단어를 pick.
    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [candidates[index] for index in words_idx]
    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    # 각 키워드들 중에서 가장 덜 유사한 키워드들간의 조합을 계산
    min_sim = np.inf
    candidate = None
    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]


def mmr(doc_embedding, candidate_embeddings, words, top_n, diversity):

    # 문서와 각 키워드들 간의 유사도가 적혀있는 리스트
    word_doc_similarity = cosine_similarity(candidate_embeddings, doc_embedding)

    # 각 키워드들 간의 유사도
    word_similarity = cosine_similarity(candidate_embeddings)

    # 문서와 가장 높은 유사도를 가진 키워드의 인덱스를 추출.
    # 만약, 2번 문서가 가장 유사도가 높았다면
    # keywords_idx = [2]
    keywords_idx = [np.argmax(word_doc_similarity)]

    # 가장 높은 유사도를 가진 키워드의 인덱스를 제외한 문서의 인덱스들
    # 만약, 2번 문서가 가장 유사도가 높았다면
    # ==> candidates_idx = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10 ... 중략 ...]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    # 최고의 키워드는 이미 추출했으므로 top_n-1번만큼 아래를 반복.
    # ex) top_n = 5라면, 아래의 loop는 4번 반복됨.
    for _ in range(top_n - 1):
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # MMR을 계산
        mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # keywords & candidates를 업데이트
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]


# if __name__ == '__main__':
#     doc = '업무효율 50% 상승 경계를 넘어선 소통 영업 직무는 화주 해운사들과의 긴밀한 소통이 요구됩니다. ' \
#           'OO위원장시절 지속적 소통, 실무자의 입장을 고려하여 학생회의 업무효율을 50% 상승 시킨 경험이 있습니다.' \
#           ' OO위원회는 학생회의 지연제출과 실무자를 고려하지 않은 지침에 대한 문제점이 있었습니다. ' \
#           '기존에는 학생회와 소통할 기회가 학생총회 밖에 없었습니다. 타 학과의 총무와 대화를 통해 지속적인 연락과 ' \
#           '실무자와 소통이 해결 방안임을 파악했습니다. 과대표들과의 소통, 총무들과의 소통을 위해 2개의 채팅방을 개설했습니다.' \
#           ' 1번만 공지하던 일정을 개강총회 이후, 1달 전 1주일 전 3번 직접 전달하였습니다. ' \
#           '동시에 문제 해결을 위한 도움 여부에 대해 문의하였습니다. 실무자 고려를 위해 총무들의 의견을 수렴해 감사의 본분을 유지하는 범위에서 ' \
#           '지침을 수정, 보완하였습니다. 지난 4번의 발견한 문제점을 5개의 묶음으로 정리하여 실무자들의 입장에서 목적 적합하게 재구성하고 ' \
#           '1번씩 지침 개정을 위한 강행규정을 마련했습니다. 소통창구 개설과 실무자를 고려한 지침을 마련해 2주가 걸리던 업무 기간은 1주로 ' \
#           '단축되었습니다. 영업직무는 화주의 만족을 극대화해야 합니다. 이를 위해 문제를 파악하고 사원이 먼저 본선, 해운대리점, ' \
#           '화주 등 관계자들과 지속적인 커뮤니케이션 능력이 필요합니다. 저의 문제해결과 커뮤니케이션 능력은 영업직무에 적합하다 생각합니다.'
#     find_keyword(doc)