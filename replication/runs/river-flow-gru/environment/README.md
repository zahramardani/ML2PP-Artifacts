# Execution environment

The currently available project notes identify Python 3.8.19 and TensorFlow
2.2.0. Exact versions for NumPy, pandas, scikit-learn, statsmodels, XGBoost,
Prophet, Matplotlib and other transitive dependencies were not recoverable
from the reviewed package.

`requirements.template.txt` is therefore not a dependency lock. Replace it
with the original `pip freeze`, Conda lock, Poetry lock or container digest
before claiming exact reproduction. Record the operating system, CPU/GPU,
CUDA/cuDNN versions where applicable, Java/JDK version, generator build, and
the exact command for every run.
