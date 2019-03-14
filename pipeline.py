from gensim.models import ldamodel
from semsim.read_files import *
import scipy.sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
from sklearn import metrics
import pickle
from semsim.doc_cluster_util import *
import semsim.util as ut


class DocClusterModel:
    """
    train - test separation
    model - parameter separation
    a model is defined by:
    1. trained files (parametric or non-parametric)
    2. a pipeline (how to apply the trained models)
    # a possible alternative is to specify the pipeline at test time
    # so that there could be different ways of using trained models
    # but this would cause unnecessary test time overheads
    """
    def __init__(self, pipeline, var_dict):
        self.pipeline = pipeline
        self.var_dict = var_dict
        self.output_dict = {}

    def run_pipe(self, corpus):
        self.var_dict['corpus'] = corpus
        for fn_name in self.pipeline:
            res = self.apply(fn_name)
            self.var_dict.update(res)
            if fn_name.startswith("train_") or fn_name.startswith("test_"):
                self.output_dict.update(res)

        return self.output_dict

    def apply(self, fn_name):
        if fn_name == 'norm_tf_idf':
            tf_idf_svec = get_tf_idf(self.var_dict['tkn_corpus'], self.var_dict['idf'], self.var_dict['dict_idx'])
            norm_tfidf_svec = sps_mat_norm(tf_idf_svec)
            res = {'norm_tfidf_svec': norm_tfidf_svec}

        elif fn_name == 'tokenize_hanlp':
            tkn_corpus = tokenize_hanlp(self.var_dict['corpus'])
            res = {'tkn_corpus': tkn_corpus}

        elif fn_name == 'norm_lsa':
            lsa_corpus = self.var_dict['lsa'].transform(self.var_dict['norm_tfidf_svec'])
            res = {'lsa_corpus': lsa_corpus}

        elif fn_name == 'train_idf':
            dict_idx = build_dict(self.var_dict['tkn_corpus'], freq=4)
            idf = fit_idf(self.var_dict['tkn_corpus'], dict_idx)
            res = {'dict_idx': dict_idx, 'idf': idf}

        elif fn_name == 'train_kmeans':
            alg = KMeans(**self.var_dict['cluster_params'])
            alg.fit(self.var_dict['lsa_corpus'])
            res = {'partition': KMeansPartition(alg)}

        elif fn_name == 'train_norm_lsa':
            lsa = make_pipeline(TruncatedSVD(128), Normalizer(copy=False))
            lsa.fit_transform(self.var_dict['norm_tfidf_svec'])
            res = {'lsa': lsa}

        elif fn_name == 'test_cluster_id':
            clsuter_id = self.var_dict['partition'].partition_id(self.var_dict['lsa_corpus'])
            res = {'cluster_id': clsuter_id}

        else:
            raise ValueError("unsupported function" + fn_name)
        return res


def load_vars(file_list):
    var_dict = {}
    for filename in file_list:
        var_dict.update(pickle.load(open(filename, "rb")))
    return var_dict


if __name__ == '__main__':
    # title, body = read_news_doc(r"C:\Users\donglwan\Desktop\data\news\forclustering.txt")
    # title, body = read_news_doc(r"C:\Users\donglwan\Desktop\data\news\news-train.txt", lim=2000)
    # cate, title, body = read_news_doc_lab(r"C:\Users\donglwan\Desktop\data\news\sougouCA5.cate.txt")
    cate, title, body = read_news_doc_lab(r"C:\Users\donglwan\Desktop\data\news\demo.cate.txt")
    # cate, title, body = read_news_doc_lab(r"C:\Users\donglwan\Desktop\data\news\forclustering.cate.txt")

    # # train idf
    # model = DocClusterModel(['tokenize_hanlp', 'train_idf'], {})
    # idf = model.run_pipe(body)
    # pickle.dump(idf, open("idf_2k.pkl", "wb"))
    #
    # # fit lsa
    # model = DocClusterModel(['tokenize_hanlp', 'norm_tf_idf', 'train_norm_lsa'], load_vars(['idf_2k.pkl']))
    # lsa = model.run_pipe(body)
    # pickle.dump(lsa, open("lsa_body_model.pkl", "wb"))

    # clustering
    var_dict = load_vars(['idf_2k.pkl', 'lsa_body_model.pkl'])
    var_dict['cluster_params'] = {'n_clusters': 3, 'random_state': 0, 'init': 'k-means++'}
    model = DocClusterModel(['tokenize_hanlp', 'norm_tf_idf', 'norm_lsa', 'train_kmeans'], var_dict)
    trained_kmeans = model.run_pipe(body)
    pickle.dump(trained_kmeans, open('trained_kmeans.pkl', "wb"))

    # test cluster partition
    model = DocClusterModel(['tokenize_hanlp', 'norm_tf_idf', 'norm_lsa', 'test_cluster_id'], load_vars(['idf_2k.pkl', 'lsa_body_model.pkl', 'trained_kmeans.pkl']))
    pickle.dump(model, open('test_model_1.pkl', "wb"))
    cluster_id = model.run_pipe(["高考第一天　期盼写满千万父母的双眼", "奥迪３款重量级新车将国产　捍卫霸主地位"])
    print(cluster_id)
