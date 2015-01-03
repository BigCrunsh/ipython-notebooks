"""
Confidence interval notebook extraction.
"""

from scipy.stats import norm
import numpy as np

class AccuracyEstimator(object):
    """
    Accuracy estimator:
    Estimates accuracy and standard error from contigency table.
    """
    def __init__(self, conf_mats):
        self.num_correct = conf_mats['TP'] + conf_mats['TN']
        self.num_draws = conf_mats['TP'] + conf_mats['TN'] + \
                         conf_mats['FP'] + conf_mats['FN']
        self.value = self.num_correct/(1.0*self.num_draws)
        sample_var = self.value*(1.0-self.value)
        self.stderr = np.sqrt(sample_var/self.num_draws)

class PrecisionEstimator(object):
    """
    Precision estimator:
    Estimates precision and standard error from contigency table.
    """
    def __init__(self, conf_mats):
        self.num_draws = conf_mats['TP'] + conf_mats['TN'] + \
                         conf_mats['FP'] + conf_mats['FN']
        self.num_eff_draws = conf_mats['TP'] + conf_mats['FP']

        # estimates of means
        m_tp = conf_mats['TP'] / (1.0*self.num_draws)
        m_fp = conf_mats['FP'] / (1.0*self.num_draws)
        num_val = m_tp
        den_val = m_tp + m_fp
        self.value = num_val/den_val

        # estimates of variances
        tp_var = m_tp*(1.0-m_tp)
        fp_var = m_fp*(1.0-m_fp)
        num_var = tp_var
        # var(m_tp+m_fp)
        den_var = tp_var + fp_var - 2.0*(m_tp*m_fp) # = den_val*(1.0-den_val)

        # cov(tp, fp)
        cov = tp_var - m_tp*m_fp # = num_val*(1.0-den_val)

        # estimate sample variance of num/den by delta method
        sample_var = \
            (num_var - 2*self.value*cov + np.power(self.value, 2)*den_var) / \
            np.power(den_val, 2)
        # TODO(cs): double-check / justify num_eff_draws instead of num_draws
        self.stderr = np.sqrt(sample_var/self.num_eff_draws)

class RecallEstimator(object):
    """
    Recall estimator:
    Estimates recall and standard error from contigency table.
    """
    def __init__(self, conf_mats):
        self.num_draws = conf_mats['TP'] + conf_mats['TN'] + \
                         conf_mats['FP'] + conf_mats['FN']
        self.num_eff_draws = conf_mats['TP'] + conf_mats['FN']

        # estimates of means
        m_tp = conf_mats['TP'] / (1.0*self.num_draws)
        m_fn = conf_mats['FN'] / (1.0*self.num_draws)
        num_val = m_tp
        den_val = m_tp + m_fn
        self.value = num_val/den_val

        # estimates of variances
        tp_var = m_tp*(1.0-m_tp)
        fn_var = m_fn*(1.0-m_fn)
        num_var = tp_var
        # var(m_tp+m_fn)
        den_var = tp_var + fn_var - 2.0*(m_tp*m_fn) # = den_val*(1.0-den_val)

        # cov(tp, fn)
        cov = tp_var - m_tp*m_fn # = num_val*(1.0-den_val)

        # estimate sample variance of num/den by delta method
        sample_var = \
            (num_var - 2*self.value*cov + np.power(self.value, 2)*den_var) / \
            np.power(den_val, 2)
        # TODO(cs): double-check / justify num_eff_draws instead of num_draws
        self.stderr = np.sqrt(sample_var/self.num_eff_draws)

class FMeasureEstimator(object):
    """
    F-Measure estimator:
    Estimates F-Measure and standard error from contigency table.
    """
    def __init__(self, conf_mats, eta=0.5):
        self.num_draws = conf_mats['TP'] + conf_mats['TN'] + \
                         conf_mats['FP'] + conf_mats['FN']
        self.num_eff_draws = conf_mats['TP'] + \
                             eta*conf_mats['FP'] + (1.0-eta)*conf_mats['FN']

        # estimates of means
        m_tp = conf_mats['TP'] / (1.0*self.num_draws)
        m_fp = conf_mats['FP'] / (1.0*self.num_draws)
        m_fn = conf_mats['FN'] / (1.0*self.num_draws)
        num_val = m_tp
        den_val = m_tp + eta*m_fp + (1.0-eta)*m_fn
        self.value = num_val/den_val

        # estimates of variances
        tp_var = m_tp*(1.0-m_tp)
        fp_var = m_fp*(1.0-m_fp)
        fn_var = m_fn*(1.0-m_fn)
        num_var = tp_var
        # var(tp+eta*fp+(1.0-eta)*fn)
        den_var = tp_var + eta*eta*fp_var + (1.0-eta)*(1.0-eta)*fn_var - \
             2.0*(eta*m_tp*m_fp + (1.0-eta)*m_tp*m_fn + eta*(1-eta)*m_fp*m_fn)

        # cov(tp, tp+eta*fp+(1.0-eta)*fn)
        cov = tp_var - eta*m_tp*m_fp - (1.0-eta)*m_tp*m_fn

        # estimate sample variance of num/den by delta method
        sample_var = \
            (num_var - 2*self.value*cov + np.power(self.value, 2)*den_var) / \
            np.power(den_val, 2)
        # TODO(cs): double-check / justify num_eff_draws instead of num_draws
        self.stderr = np.sqrt(sample_var/self.num_eff_draws)

class NormalCIs(object):
    """
    Confidence intervals with normal assumption.
    """

    @staticmethod
    def ci_wald(estimator, alpha=0.05):
        """
        Standard Wald interval. This implementation is faster than
        # norm.interval(1.0-alpha, loc=X.mean(), scale=X.std()/sqrt(n))
        since it does not compute z_alpha for each run.
        """
        z_a = norm.ppf(1.0-alpha/2.0)

        width = z_a*estimator.stderr
        return [(p-z, p+z) for (p, z) in zip(estimator.value, width)]

class BinomialPropertionCIs(object):
    """
    Confidence intervals for binomial propoertions.
    """

    @staticmethod
    def ci_agresti_coull(estimator, alpha=0.05):
        """
        Agresti-Coull interval. It adjusts the quantatites by adding z_alpha2
        (approx. 2 for alpha=0.05) positive and negative pseudo counts and apply
        standard Wald interval.
        """
        z_a = norm.ppf(1-alpha/2.0)
        z_a2 = z_a*z_a

        num_draws_adj = estimator.num_draws+z_a2
        val_adj = (estimator.num_correct+z_a2/2.0)/num_draws_adj
        var_adj = val_adj*(1.0-val_adj)
        stderr_adj = np.sqrt(var_adj/num_draws_adj)

        width = z_a*stderr_adj
        return [(p-z, p+z) for (p, z) in zip(val_adj, width)]

    @staticmethod
    def ci_wilson(estimator, alpha=0.05):
        """
        Wilson interval.
        """
        val = estimator.value
        z_a = norm.ppf(1-alpha/2.0)
        z_a2 = z_a*z_a

        stderr_adj = np.sqrt(val-val*val+z_a2/(4.0*estimator.num_draws))/ \
            (np.sqrt(estimator.num_draws)+z_a2/np.sqrt(estimator.num_draws))
        val_adj = (val+z_a2/(2.0*estimator.num_draws))/ \
            (1.0+z_a2/estimator.num_draws)

        width = z_a*stderr_adj
        return [(p-z, p+z) for (p, z) in zip(val_adj, width)]
