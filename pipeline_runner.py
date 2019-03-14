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
    def __init__(self, pipeline, param_pkl_files=()):
        self.pipeline = pipeline
        self.output_dict = {}
        self.var_dict = {}
        for pkl_filename in param_pkl_files:
            tmp_dict = pickle.load(open(pkl_filename, "rb"))
            self.var_dict.update(tmp_dict)

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


if __name__ == '__main__':
    model = DocClusterModel(['tokenize_zh', 'norm_tf_idf', 'norm_lsa', 'train_kmeans'],
                            ['idf_10k.pkl', 'lsa_body_model.pkl'])
    trained_kmeans = model.run_pipe(corpus)
    pickle.dump(trained_kmeans, open('trained_kmeans.pkl', "wb"))

    model = DocClusterModel(['tokenize_zh', 'norm_tf_idf', 'norm_lsa', 'test_cluster_id'],
                            ['idf_10k.pkl', 'lsa_body_model.pkl', 'trained_kmeans.pkl'])
    cluster_id = model.run_pipe([text])
    print(cluster_id)
