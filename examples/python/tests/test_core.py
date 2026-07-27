import numpy as np

from ml2pp_reference.core import USE_CASES, metrics, supervised, synthetic_frame


def test_all_synthetic_schemas_and_shapes():
    for key, cfg in USE_CASES.items():
        frame = synthetic_frame(key, rows=200)
        assert {"timestamp", *cfg.inputs}.issubset(frame.columns)
        x, y = supervised(frame, cfg)
        assert x.shape[1:] == (cfg.n_in, len(cfg.inputs))
        assert y.shape[1] == cfg.n_out


def test_metrics_are_exact_for_perfect_prediction():
    actual = np.array([[1.0, 2.0], [2.0, 3.0]])
    result = metrics(actual, actual)
    assert (result[["mae", "mse", "rmse"]] == 0).all().all()
    assert (result["r2"] == 1).all()

