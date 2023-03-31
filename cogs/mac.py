import nextcord
from nextcord.ext import commands
from sklearn import datasets, model_selection, svm, metrics, linear_model
import joblib
import os
import json

class MachineLearning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def train(self, ctx, model_type: str, dataset: str = "iris"):
        if model_type.lower() not in ['svm', 'logistic_regression']:
            await ctx.send("Currently supported model types: 'svm' and 'logistic_regression'.")
            return

        if dataset.lower() != "iris":
            await ctx.send("Currently, only the 'iris' dataset is supported.")
            return

        # Load the Iris dataset
        iris = datasets.load_iris()
        X_train, X_test, y_train, y_test = model_selection.train_test_split(
            iris.data, iris.target, test_size=0.3, random_state=42
        )

        # Train the selected model
        if model_type.lower() == 'svm':
            clf = svm.SVC(kernel='linear', C=1)
        elif model_type.lower() == 'logistic_regression':
            clf = linear_model.LogisticRegression(max_iter=1000)

        clf.fit(X_train, y_train)

        # Save the trained model
        model_filename = f'{model_type}_iris_model.pkl'
        joblib.dump(clf, model_filename)

        await ctx.send(f"Model '{model_type}' has been trained and saved as '{model_filename}'.")

    @commands.command()
    async def evaluate(self, ctx, model_filename: str):
        if not os.path.isfile(model_filename):
            await ctx.send("The specified model file does not exist.")
            return

        # Load the Iris dataset
        iris = datasets.load_iris()
        X_train, X_test, y_train, y_test = model_selection.train_test_split(
            iris.data, iris.target, test_size=0.3, random_state=42
        )

        # Load the trained model
        clf = joblib.load(model_filename)

        # Evaluate the model
        y_pred = clf.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        classification_report = metrics.classification_report(y_test, y_pred, target_names=iris.target_names)

        await ctx.send(f"Model evaluation:\nAccuracy: {accuracy:.2f}\n\nClassification report:\n{classification_report}")

    @commands.command()
    async def predict(self, ctx, model_filename: str, *input_data: float):
        if not os.path.isfile(model_filename):
            await ctx.send("The specified model file does not exist.")
            return

        if len(input_data) != 4:
            await ctx.send("Please provide exactly 4 input features.")
            return

        # Load the Iris dataset
        iris = datasets.load_iris()

        # Load the trained model
        clf = joblib.load(model_filename)

        # Make a prediction
        prediction = clf.predict([input_data])[0]
        predicted_class = iris.target_names[prediction]

        await ctx.send(f"Predicted class: {predicted_class} (class index: {prediction})")

def setup(bot):
    bot.add_cog(MachineLearning(bot))