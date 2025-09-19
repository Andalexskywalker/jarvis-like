from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# toy training set — expand over time
TRAIN = [
    ("add buy milk", "todo.add"),
    ("remember to call mom", "todo.add"),
    ("show todos", "todo.show"),
    ("done 2", "todo.done"),
    ("delete 3", "todo.delete"),
    ("set timer 5m", "timer.set_minutes"),
    ("timer 30s", "timer.set_seconds"),
    ("what time", "clock.time"),
    ("what date", "clock.date"),
    ("calc 2+2", "calc.eval"),
    ("weather in lisbon", "weather.now"),
    ("open youtube", "launch.open"),
]

clf = Pipeline([
    ("vec", TfidfVectorizer(ngram_range=(1,2))),
    ("lr", LogisticRegression(max_iter=1000)),
])
X = [t for t,_ in TRAIN]
y = [l for _,l in TRAIN]
clf.fit(X, y)

def predict_intent(text: str):
    proba = clf.predict_proba([text])[0]
    labels = clf.classes_
    top_i = proba.argmax()
    return labels[top_i], float(proba[top_i])
