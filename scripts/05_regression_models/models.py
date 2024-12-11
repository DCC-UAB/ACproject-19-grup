from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import PolynomialFeatures

class RegressionModels:
    def __init__(self, model_type="linear", **kwargs):
        """
        Inicializa un modelo basado en el tipo.
        model_type: 'linear', 'ridge', 'lasso', 'random_forest', 'xgboost', 'gradient_boosting', 'svr', 'polynomial_regression'.
        kwargs: hiperparámetros del modelo.
        """
        if model_type == "linear":
            self.model = LinearRegression(**kwargs)
        elif model_type == "ridge":
            self.model = Ridge(**kwargs)
        elif model_type == "lasso":
            self.model = Lasso(**kwargs)
        elif model_type == "random_forest":
            self.model = RandomForestRegressor(**kwargs)
        elif model_type == "xgboost":
            self.model = XGBRegressor(**kwargs)
        elif model_type == "gradient_boosting":
            self.model = GradientBoostingRegressor(**kwargs)
        elif model_type == "svr":
            self.model = SVR(**kwargs)
        elif model_type == "polynomial_regression":
            self.model = PolynomialFeatures(**kwargs)
        else:
            raise ValueError("Modelo no reconocido.")

    def train(self, X_train, y_train):
        """Entrena el modelo."""
        self.model.fit(X_train, y_train.ravel())

    def predict(self, X_test):
        """Realiza predicciones."""
        return self.model.predict(X_test)

    def get_model(self):
        """Devuelve el modelo subyacente."""
        return self.model
