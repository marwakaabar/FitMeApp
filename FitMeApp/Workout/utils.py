import pandas as pd
from .models import Progress
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def get_user_progress_data(user):
    # Récupérer les données de progrès pour un utilisateur donné
    progress_data = Progress.objects.filter(user=user)
    data = {
        'date_completed': [],
        'duration': [],
        'repetitions': [],
        'weight': [],
        'is_done': []
    }

    for progress in progress_data:
        data['date_completed'].append(progress.date_completed)
        data['duration'].append(progress.duration.total_seconds() if progress.duration else 0)
        data['repetitions'].append(progress.repetitions or 0)
        data['weight'].append(progress.weight or 0)
        data['is_done'].append(progress.is_done)

    return pd.DataFrame(data)


def train_model(user):
    df = get_user_progress_data(user)
    X = df[['duration', 'repetitions', 'weight']]
    y = df['is_done']  # Ou toute autre métrique que vous voulez prédire

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model

def predict_performance(user, new_data):
    model = train_model(user)
    prediction = model.predict([new_data])  # new_data = [duration, repetitions, weight]
    return prediction