import numpy as np
from sklearn.linear_model import LinearRegression

subjects = ['Math', 'English', 'Kiswahili', 'Science', 'Social']


# ================= SUBJECT RISK =================
def subject_risk(record):
    risks = []
    for i, sub in enumerate(subjects):
        if record[i+3] < 50:
            risks.append(sub)
    return risks


# ================= TOTAL MARKS =================
def total_marks(record):
    return sum(record[3:8])


# ================= ML TREND PREDICTION =================
def ml_predict_trend(records):
    """
    Predicts declining subjects using Linear Regression
    records = list of student records across terms
    """

    if len(records) < 2:
        return []  # Not enough data

    declining_subjects = []

    for i in range(5):  # 5 subjects
        scores = [r[i+3] for r in records]

        X = np.array(range(len(scores))).reshape(-1, 1)
        y = np.array(scores)

        model = LinearRegression()
        model.fit(X, y)

        future = model.predict([[len(scores)]])[0]

        if future < scores[-1]:
            declining_subjects.append(subjects[i])

    return declining_subjects