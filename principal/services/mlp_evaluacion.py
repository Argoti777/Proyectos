import numpy as np
from sklearn.metrics import confusion_matrix, recall_score, log_loss
from sklearn.model_selection import train_test_split

from principal.models import PartidoHistoricoMLP
from principal.services.mlp_model import cargar_mlp


def evaluar_mlp():

    qs = PartidoHistoricoMLP.objects.all()

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

    # -------- split train/test --------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # -------- cargar modelo --------
    model, scaler = cargar_mlp()

    X_test_scaled = scaler.transform(X_test)

    # -------- predicciones --------
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)

    # -------- métricas --------
    matriz = confusion_matrix(y_test, y_pred)

    recall = recall_score(
        y_test,
        y_pred,
        average=None
    )

    loss = log_loss(y_test, y_prob)

    return {
        "matriz": matriz,
        "recall": recall,
        "logloss": loss
    }
