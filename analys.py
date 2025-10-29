import sklearn

x, y = sklearn.datasets.load_iris(return_X_y=True)
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
    x, y, test_size=0.3, random_state=42
)
model = sklearn.linear_model.LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)
y_predict = model.predict(x_test)
accuracy = sklearn.metrics.accuracy_score(y_test, y_predict)
print(accuracy)
