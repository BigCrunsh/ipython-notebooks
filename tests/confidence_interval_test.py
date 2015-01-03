"""
Confidence interval notebook extraction.
"""

import projects.confidence_interval as ci
import numpy as np

class TestAccuracyEstimator(object):
    """
    Test class for accuracy estimator.
    """

    @classmethod
    def setup(cls):
        """
        Setup tests
        """
        samples = np.array([
            [13, 0, 12, 25],
            [12, 0, 10, 28],
            [10, 0, 19, 21]
        ]).T
        arr = np.zeros((3,), dtype=[
            ('TP', 'float'), ('TN', 'float'), ('FP', 'float'), ('FN', 'float')
        ])
        arr['TP'], arr['TN'] = samples[0], samples[1]
        arr['FP'], arr['FN'] = samples[2], samples[3]

        cls.estimator = ci.AccuracyEstimator(arr)

    def test_num_draws(self):
        """Accuracy: Validate number of draws"""
        expected = [50, 50, 50]
        got = self.estimator.num_draws
        np.testing.assert_equal(got, expected)

    def test_num_correct(self):
        """Accuracy: Validate number of correct draws"""
        expected = [13, 12, 10]
        got = self.estimator.num_correct
        np.testing.assert_equal(got, expected)

    def test_value(self):
        """Accuracy: Validate estimate"""
        expected = [0.26, 0.24, 0.2]
        got = self.estimator.value
        np.testing.assert_almost_equal(got, expected)

    def test_stderr(self):
        """Accuracy: Validate standard error estimate"""
        expected = [0.06203225, 0.06039868, 0.05656854]
        got = self.estimator.stderr
        np.testing.assert_almost_equal(got, expected)

class TestPrecisionEstimator(object):
    """
    Test class for precision estimator.
    """

    @classmethod
    def setup(cls):
        """
        Setup tests
        """
        samples = np.array([
            [13, 0, 12, 25],
            [12, 0, 10, 28],
            [10, 0, 19, 21]
        ]).T
        arr = np.zeros((3,), dtype=[
            ('TP', 'float'), ('TN', 'float'), ('FP', 'float'), ('FN', 'float')
        ])
        arr['TP'], arr['TN'] = samples[0], samples[1]
        arr['FP'], arr['FN'] = samples[2], samples[3]

        cls.estimator = ci.PrecisionEstimator(arr)

    def test_num_draws(self):
        """Precision: Validate number of draws"""
        expected = [50, 50, 50]
        got = self.estimator.num_draws
        np.testing.assert_equal(got, expected)

    def test_num_eff_draws(self):
        """Precision: Validate number of efficient draws"""
        expected = [25, 22, 29]
        got = self.estimator.num_eff_draws
        np.testing.assert_equal(got, expected)

    def test_value(self):
        """Precision: Validate estimate"""
        expected = [0.52, 0.54545455, 0.34482759]
        got = self.estimator.value
        np.testing.assert_almost_equal(got, expected)

    def test_stderr(self):
        """Precision: Validate standard error estimate"""
        expected = [0.09991997, 0.10615895, 0.08826323]
        got = self.estimator.stderr
        np.testing.assert_almost_equal(got, expected)

class TestRecallEstimator(object):
    """
    Test class for recall estimator.
    """

    @classmethod
    def setup(cls):
        """
        Setup tests
        """
        samples = np.array([
            [13, 0, 12, 25],
            [12, 0, 10, 28],
            [10, 0, 19, 21]
        ]).T
        arr = np.zeros((3,), dtype=[
            ('TP', 'float'), ('TN', 'float'), ('FP', 'float'), ('FN', 'float')
        ])
        arr['TP'], arr['TN'] = samples[0], samples[1]
        arr['FP'], arr['FN'] = samples[2], samples[3]

        cls.estimator = ci.RecallEstimator(arr)

    def test_num_draws(self):
        """Recall: Validate number of draws"""
        expected = [50, 50, 50]
        got = self.estimator.num_draws
        np.testing.assert_equal(got, expected)

    def test_num_eff_draws(self):
        """Recall: Validate number of efficient draws"""
        expected = [38, 40, 31]
        got = self.estimator.num_eff_draws
        np.testing.assert_equal(got, expected)

    def test_value(self):
        """Recall: Validate estimate"""
        expected = [0.34210526, 0.3, 0.32258065]
        got = self.estimator.value
        np.testing.assert_almost_equal(got, expected)

    def test_stderr(self):
        """Recall: Validate standard error estimate"""
        expected = [0.07696022, 0.07245688, 0.08395897]
        got = self.estimator.stderr
        np.testing.assert_almost_equal(got, expected)

class TestFMeasureEstimator(object):
    """
    Test class for F-Measure estimator.
    """

    @classmethod
    def setup(cls):
        """
        Setup tests
        """
        samples = np.array([
            [13, 0, 12, 25],
            [12, 0, 10, 28],
            [10, 0, 19, 21]
        ]).T
        arr = np.zeros((3,), dtype=[
            ('TP', 'float'), ('TN', 'float'), ('FP', 'float'), ('FN', 'float')
        ])
        arr['TP'], arr['TN'] = samples[0], samples[1]
        arr['FP'], arr['FN'] = samples[2], samples[3]

        cls.arr = arr
        cls.estimator = ci.FMeasureEstimator(arr, 0.3)

    def test_num_draws(self):
        """F-measure: Validate number of draws"""
        expected = [50, 50, 50]
        got = self.estimator.num_draws
        np.testing.assert_equal(got, expected)

    def test_num_eff_draws(self):
        """F-measure: Validate number of efficient draws"""
        expected = [34.1, 34.6, 30.4]
        got = self.estimator.num_eff_draws
        np.testing.assert_almost_equal(got, expected)

    def test_value(self):
        """F-measure: Validate estimate"""
        expected = [0.38123167, 0.34682081, 0.32894737]
        got = self.estimator.value
        np.testing.assert_almost_equal(got, expected)

        np.testing.assert_almost_equal(
            ci.FMeasureEstimator(self.arr, 0.0).value,
            ci.RecallEstimator(self.arr).value
        )

        np.testing.assert_almost_equal(
            ci.FMeasureEstimator(self.arr, 1.0).value,
            ci.PrecisionEstimator(self.arr).value
        )

    def test_stderr(self):
        """F-measure: Validate standard error estimate"""
        expected = [0.07711392, 0.07579905, 0.07923189]
        got = self.estimator.stderr
        np.testing.assert_almost_equal(got, expected)

        np.testing.assert_almost_equal(
            ci.FMeasureEstimator(self.arr, 0.0).stderr,
            ci.RecallEstimator(self.arr).stderr
        )

        np.testing.assert_almost_equal(
            ci.FMeasureEstimator(self.arr, 1.0).stderr,
            ci.PrecisionEstimator(self.arr).stderr
        )

class TestNormalCIs(object):
    """
    Test class for confidence intervals under normal assumption.
    """

    @classmethod
    def setup(cls):
        """
        Setup tests
        """
        samples = np.array([
            [13, 0, 12, 25],
            [12, 0, 10, 28],
            [10, 0, 19, 21]
        ]).T
        arr = np.zeros((3,), dtype=[
            ('TP', 'float'), ('TN', 'float'), ('FP', 'float'), ('FN', 'float')
        ])
        arr['TP'], arr['TN'] = samples[0], samples[1]
        arr['FP'], arr['FN'] = samples[2], samples[3]

        cls.cms = arr

    def test_ci_wald_acc(self):
        """Validate Wald intervals"""
        estimator = ci.AccuracyEstimator(self.cms)

        expected = np.array([
            (0.13841902475292037, 0.38158097524707968),
            (0.12162077134103225, 0.35837922865896776),
            (0.089127694052025766, 0.31087230594797427)
        ])
        got = ci.NormalCIs.ci_wald(estimator)
        np.testing.assert_almost_equal(got, expected)

class TestBinomialPropertionCIs(object):
    """
    Test class for confidence intervals for binomial proportions.
    """

    @classmethod
    def setup(cls):
        """
        Setup tests
        """
        samples = np.array([
            [13, 0, 12, 25],
            [12, 0, 10, 28],
            [10, 0, 19, 21]
        ]).T
        arr = np.zeros((3,), dtype=[
            ('TP', 'float'), ('TN', 'float'), ('FP', 'float'), ('FN', 'float')
        ])
        arr['TP'], arr['TN'] = samples[0], samples[1]
        arr['FP'], arr['FN'] = samples[2], samples[3]

        cls.estimator = ci.AccuracyEstimator(arr)

    def test_ci_agresti_coull(self):
        """Validate Agresti Coull intervals"""
        expected = np.array([
            (0.15757100260674056, 0.39667584497727154),
            (0.14159960372603347, 0.37550114782331306),
            (0.11050245456583023, 0.33230610491418494)
        ])
        got = ci.BinomialPropertionCIs.ci_agresti_coull(self.estimator)
        np.testing.assert_almost_equal(got, expected)

    def test_ci_wilson(self):
        """Validate Wilson score intervals"""
        expected = np.array([
            (0.1587152749355239, 0.39553157264848843),
            (0.14297391396991732, 0.37412683757942922),
            (0.11243750015776115, 0.33037105932225413)
        ])
        got = ci.BinomialPropertionCIs.ci_wilson(self.estimator)
        np.testing.assert_almost_equal(got, expected)
