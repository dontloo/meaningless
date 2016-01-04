import timeit
import numpy as np
import theano
import theano.tensor as tt


def compile_theano_version4(number_of_matrices, n):
    import theano.typed_list
    L = theano.typed_list.TypedListType(tt.TensorType(theano.config.floatX, broadcastable=(None, None)))()
    res = tt.zeros(n, dtype=theano.config.floatX)
    for i in range(number_of_matrices):
        res += tt.dot(L[i].T, L[i])
    return theano.function([L], res)


def compile_theano_version5(number_of_matrices, n):
    import theano.typed_list
    L = theano.typed_list.TypedListType(tt.TensorType(theano.config.floatX, broadcastable=(None, None)))()

    def merge_sum(lo, hi):
        if hi-lo == 2:
            return tt.dot(L[lo].T, L[lo])+tt.dot(L[lo+1].T, L[lo+1])
        if hi-lo == 1:
            return tt.dot(L[lo].T, L[lo])
        return merge_sum(lo, (lo+hi)/2) + merge_sum((lo+hi)/2, hi)

    res = merge_sum(0, number_of_matrices)
    return theano.function([L], res)


# why can't get any speed up
def compile_theano_version6(number_of_matrices, n):
    import theano.typed_list
    L = theano.typed_list.TypedListType(tt.TensorType(theano.config.floatX, broadcastable=(None, None)))()
    # res, _ = theano.reduce(fn=lambda i, tmp: tmp+tt.dot(L[i].T, L[i]),
    #                        outputs_info=tt.zeros((n, n), dtype=theano.config.floatX),
    #                        sequences=[theano.tensor.arange(number_of_matrices, dtype='int64')])
    # return theano.function([L], res)
    res, _ = theano.scan(fn=lambda i: tt.dot(L[i].T, L[i]),
                         sequences=[theano.tensor.arange(number_of_matrices, dtype='int64')])
    return theano.function([L], res.sum(axis=0))


def compile_theano_version1(number_of_matrices, n):
    assert number_of_matrices > 0
    assert n > 0
    L = [tt.matrix(dtype=theano.config.floatX) for _ in xrange(number_of_matrices)]
    res = tt.zeros(n, dtype=theano.config.floatX)
    for M in L:
        res += tt.dot(M.T, M)
    return theano.function(L, res)


def compile_theano_version2(number_of_matrices):
    assert number_of_matrices > 0
    L = [tt.matrix(dtype=theano.config.floatX) for _ in xrange(number_of_matrices)]
    concatenated_L = tt.concatenate(L, axis=0)
    res = tt.dot(concatenated_L.T, concatenated_L)
    return theano.function(L, res)


def compile_theano_version3():
    concatenated_L = tt.matrix(dtype=theano.config.floatX)
    res = tt.dot(concatenated_L.T, concatenated_L)
    return theano.function([concatenated_L], res)


def numpy_version1(*L):
    assert len(L) > 0
    n = L[0].shape[1]
    res = np.zeros((n, n), dtype=L[0].dtype)
    for M in L:
        res += np.dot(M.T, M)
    return res


def numpy_version2(*L):
    concatenated_L = np.concatenate(L, axis=0)
    return np.dot(concatenated_L.T, concatenated_L)


def main():
    iteration_count = 100
    number_of_matrices = 200
    n = 100
    min_x = 20
    dtype = 'float32'
    theano.config.floatX = dtype

    theano_version1 = compile_theano_version1(number_of_matrices, n)
    theano_version2 = compile_theano_version2(number_of_matrices)
    theano_version3 = compile_theano_version3()
    theano_version4 = compile_theano_version4(number_of_matrices, n)
    theano_version5 = compile_theano_version5(number_of_matrices, n)
    theano_version6 = compile_theano_version6(number_of_matrices, n)

    L = [np.random.standard_normal(size=(x, n)).astype(dtype)
         for x in range(min_x, number_of_matrices + min_x)]

    start = timeit.default_timer()
    numpy_res1 = np.sum(numpy_version1(*L)
                        for _ in xrange(iteration_count))
    print 'numpy_version1', timeit.default_timer() - start

    start = timeit.default_timer()
    numpy_res2 = np.sum(numpy_version2(*L)
                        for _ in xrange(iteration_count))
    print 'numpy_version2', timeit.default_timer() - start

    start = timeit.default_timer()
    theano_res1 = np.sum(theano_version1(*L)
                         for _ in xrange(iteration_count))
    print 'theano_version1', timeit.default_timer() - start

    start = timeit.default_timer()
    theano_res2 = np.sum(theano_version2(*L)
                         for _ in xrange(iteration_count))
    print 'theano_version2', timeit.default_timer() - start

    start = timeit.default_timer()
    theano_res3 = np.sum(theano_version3(np.concatenate(L, axis=0))
                         for _ in xrange(iteration_count))
    print 'theano_version3', timeit.default_timer() - start

    start = timeit.default_timer()
    theano_res4 = np.sum(theano_version4(L)
                         for _ in xrange(iteration_count))
    print 'theano_version4', timeit.default_timer() - start

    start = timeit.default_timer()
    theano_res5 = np.sum(theano_version5(L)
                         for _ in xrange(iteration_count))
    print 'theano_version5', timeit.default_timer() - start

    start = timeit.default_timer()
    theano_res6 = np.sum(theano_version6(L)
                         for _ in xrange(iteration_count))
    print 'theano_version6', timeit.default_timer() - start

    assert np.allclose(numpy_res1, numpy_res2, rtol=1e-1)
    assert np.allclose(numpy_res2, theano_res1, rtol=1e-1)
    assert np.allclose(theano_res1, theano_res2, rtol=1e-1)
    assert np.allclose(theano_res2, theano_res3, rtol=1e-1)
    assert np.allclose(theano_res3, theano_res4, rtol=1e-1)
    assert np.allclose(theano_res4, theano_res5, rtol=1e-1)
    assert np.allclose(theano_res3, theano_res6, rtol=1e-1)


main()
