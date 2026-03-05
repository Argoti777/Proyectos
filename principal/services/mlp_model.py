import joblib
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from principal.models import PartidoHistoricoMLP


MODEL_PATH = "mlp_model.joblib"
SCALER_PATH = "mlp_scaler.joblib"


def entrenar_mlp():
    qs = PartidoHistoricoMLP.objects.all()

    if qs.count() < 300:
        raise ValueError("Datos insuficientes para entrenar la MLP (mínimo 300 partidos)")

    # --------- Dataset ---------
    X = []
    y = []

    for p in qs:
        X.append([
            p.elo_local,
            p.elo_visitante,
            p.diff_elo,
            p.partidos_local,
            p.partidos_visitante
        ])
        y.append(p.resultado)

    X = np.array(X)
    y = np.array(y)

    # --------- Normalización ---------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --------- Modelo ---------
    model = MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        solver="adam",
        max_iter=2000,
        random_state=42
    )

    model.fit(X_scaled, y)

    # --------- Guardado ---------
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    return {
        "muestras": len(y),
        "accuracy": model.score(X_scaled, y)
    }


def cargar_mlp():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler
