import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


def make_fn(w, b):
    return lambda x: -(w[0]*x+b)/w[1]


def plot_fn(lst, a, b):
    for fn, color, label in lst:
        x = np.array([a, b])
        y = fn(x)
        plt.plot(x, y, color, label=label)
    plt.legend(loc=2)


mean_1 = np.array([0, 10])
mean_2 = np.array([10, 0])
mean_3 = np.array([30, -20])
cov = 10*np.eye(2)
sample_1 = np.random.multivariate_normal(mean_1, cov, 100)
sample_2 = np.random.multivariate_normal(mean_2, cov, 100)
sample_2 = np.concatenate([sample_2, np.random.multivariate_normal(mean_3, cov, 100)])
plt.plot(sample_1[:, 0], sample_1[:, 1], "go", sample_2[:, 0], sample_2[:, 1], "yo")

data = np.concatenate([sample_1, sample_2])
label = np.concatenate([-np.ones(len(sample_1)), np.ones(len(sample_2))])


clf = linear_model.LinearRegression(fit_intercept=True, normalize=False)
clf.fit(data, label)
fn_lin = make_fn(clf.coef_, clf.intercept_)


clf = linear_model.LogisticRegression(fit_intercept=True)
clf.fit(data, label)
fn_log = make_fn(clf.coef_[0], clf.intercept_)


clf = linear_model.SGDClassifier(loss="hinge", penalty='none')
clf.fit(data, label)
fn_hin1 = make_fn(clf.coef_[0], clf.intercept_)
clf.fit(data, label)
fn_hin2 = make_fn(clf.coef_[0], clf.intercept_)
clf.fit(data, label)
fn_hin3 = make_fn(clf.coef_[0], clf.intercept_)

lst = [(fn_lin, "r", "MSE"), (fn_log, "b", "cross entropy"), (fn_hin1, "c", "hinge"), (fn_hin2, "c", "hinge"), (fn_hin3, "c", "hinge")]

plot_fn(lst, -10, 40)
plt.show()
