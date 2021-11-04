from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline



def preprocess_pipeline(num_features, cat_features):
    '''
    Creates a preprocess basic pipeline for numerical and categorical features.
    Paramters
    -----------
    - num_features: list like of labels of numerical features
    - cat_features: list like of lables of categorical features
    
    returns a ColumnTransformer object with two pipelines.
        ColumnTransformer([
            ('categoricals', cat_transformer, cat_features),
            ('numericals', num_transformer, num_features)
        ],
        remainder = 'drop'
    '''
    num_transformer = Pipeline([
            ('imputer_num', SimpleImputer(strategy = 'median')),
            ('scaler', StandardScaler())
        ])
    # transformer for categorical features
    cat_transformer = Pipeline([
            ('imputer_cat', SimpleImputer(strategy = 'most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer([
            ('categoricals', cat_transformer, cat_features),
            ('numericals', num_transformer, num_features)
        ],
        remainder = 'drop'
    )
    return preprocessor