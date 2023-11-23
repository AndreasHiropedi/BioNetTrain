import app.globals
import dash
import dash_bootstrap_components as dbc
import json

from dash import html, dcc, callback, Input, Output, MATCH, State, clientside_callback
from models.random_forest.random_forest import RandomForest
from models.ridge_regressor.ridge_regressor import RidgeRegressor
from models.mlp.multilayer_perceptron import MultiLayerPerceptron
from models.svm.support_vector_machine import SupportVectorMachine


def create_layout(model_count):
    """
    This function creates all pages for the model inputs.
    """

    return html.Div(
        id={'type': 'input-page', 'index': model_count},
        children=[
            html.Div(
                id='input-page-header',
                children=[
                    html.H1(
                        children=[f"Model {model_count} parameters"]
                    )
                ]
            ),
            html.Div(
                id='input-page-contents',
                children=[
                    model_input_guidelines(),
                    html.Div(
                        id='input-cards-container',
                        children=[
                            dbc.Col(
                                children=[
                                    model_input_parameters_card(model_count)
                                ],
                                style={'width': '40%', 'margin-left': '30px'}
                            ),
                            dbc.Col(
                                children=[
                                    model_input_feature_selection_card(model_count),
                                    model_input_unsupervised_learning_card(model_count),
                                    model_input_hyperparameter_optimisation_card(model_count),
                                ],
                                style={'width': '30%', 'margin-left': '200px'}
                            )
                        ]
                    ),
                    html.Div(
                        id='button-wrapper',
                        children=[
                            submit_button(model_count),
                            delete_button(model_count)
                        ]
                    ),
                    delete_model_popup(model_count),
                    confirm_deleted_model_popup(model_count),
                    submit_model_popup(model_count),
                    input_validation_popup(model_count),
                    file_validation_popup(model_count)
                ]
            ),
            html.Div(id={'type': 'dummy-div', 'index': model_count}, style={'display': 'none'}),
            html.Div(id={'type': 'javascript-trigger', 'index': model_count}, style={'display': 'none'})
        ]
    )


def submit_button(model_count):
    """
    This function creates the submit button
    """

    return html.Button(
        'Submit model selection',
        id={'type': 'submit-button', 'index': model_count},
        n_clicks=0,
        style={
            'margin-top': '40px',
            'font-size': '16pt',
            'font-weight': 'bold',
            'text-align': 'center',
            'border': '1px solid black',
            'color': 'white',
            'background': 'blue',
            'margin-left': '500px',
            'padding': '0.75rem 1.25rem',
            'cursor': 'pointer'
        }
    )


def delete_button(model_count):
    """
    This function creates the delete button
    """

    return html.Button(
        'Delete model',
        id={'type': 'delete-button', 'index': model_count},
        n_clicks=0,
        style={
            'margin-top': '40px',
            'font-size': '16pt',
            'font-weight': 'bold',
            'text-align': 'center',
            'border': '1px solid black',
            'color': 'white',
            'background': 'red',
            'margin-left': '70px',
            'padding': '0.75rem 1.25rem',
            'cursor': 'pointer'
        }
    )


def delete_model_popup(model_count):
    """
    This function creates a popup for when the 'delete model' button is pressed
    """

    return dbc.Modal(
        id={'type': 'delete-model-popup', 'index': model_count},
        children=[
            dbc.ModalHeader(
                dbc.ModalTitle(f"Are you sure you want to delete model {model_count}?"),
                close_button=False,
                id='delete-modal-header'
            ),
            html.Hr(
                style={
                    'height': '3px',
                    'color': 'black',
                    'background': 'black'
                }
            ),
            dbc.ModalBody(
                children=[
                    dbc.Button(
                        html.H4(
                            "Yes",
                            style={
                                'font-size': '12pt',
                                'margin-top': '5px'
                            }
                        ),
                        id={'type': "yes-button", 'index': model_count},
                        n_clicks=0,
                        style={
                            'margin-left': '60px',
                            'border': '2px solid black',
                            'cursor': 'pointer',
                            'height': '35px',
                            'background': 'blue',
                            'color': 'white'
                        }
                    ),
                    dbc.Button(
                        html.H4(
                            "No",
                            style={
                                'font-size': '12pt',
                                'margin-top': '5px'
                            }
                        ),
                        id={'type': "no-button", 'index': model_count},
                        n_clicks=0,
                        style={
                            'margin-right': '60px',
                            'border': '2px solid black',
                            'cursor': 'pointer',
                            'height': '35px',
                            'background': 'red',
                            'color': 'white'
                        }
                    )
                ],
                id='delete-modal-body'
            )
        ],
        keyboard=False,
        backdrop='static',
        is_open=False,
        style={
            'top': '20px',
            'width': '25%',
            'margin-left': '600px',
            'position': 'fixed',
            'background': 'white',
            'color': 'black',
            'border': '3px solid blue'
        }
    )


def confirm_deleted_model_popup(model_count):
    """
    This function creates a popup that confirms the model was successfully deleted
    """

    return dbc.Modal(
        id={'type': 'confirm-model-deletion-popup', 'index': model_count},
        children=[
            dbc.ModalHeader(
                dbc.ModalTitle(f"Model {model_count} successfully deleted"),
                close_button=False,
                id='confirm-modal-header'
            ),
            html.Hr(
                style={
                    'height': '3px',
                    'color': 'black',
                    'background': 'black'
                }
            ),
            dbc.ModalBody(
                children=[
                    html.P(
                        f"You have now successfully deleted model {model_count}. To see this completed deletion, "
                        f"please refresh the app's main tab (entitled BioNetTrain). You may now close this tab."
                    ),
                    dbc.Button(
                        html.H4(
                            "Close",
                            style={
                                'font-size': '12pt',
                                'margin-top': '5px'
                            }
                        ),
                        id={'type': "close-button", 'index': model_count},
                        n_clicks=0,
                        style={
                            'margin-left': '190px',
                            'border': '2px solid black',
                            'cursor': 'pointer',
                            'height': '40px',
                            'background': 'blue',
                            'color': 'white',
                            'margin-bottom': '20px'
                        }
                    )
                ],
                id='confirm-modal-body'
            )
        ],
        keyboard=False,
        is_open=False,
        backdrop='static',
        style={
            'top': '20px',
            'width': '30%',
            'margin-left': '600px',
            'position': 'fixed',
            'background': 'white',
            'color': 'black',
            'border': '3px solid black'
        }
    )


def submit_model_popup(model_count):
    """
    This function creates a popup for when a model selection is submitted
    """

    return dbc.Modal(
        id={'type': 'submit-model-popup', 'index': model_count},
        children=[
            dbc.ModalHeader(
                id='submit-modal-header',
                children=[dbc.ModalTitle(f"Submitting user input for model {model_count} ...")],
                close_button=False
            )
        ],
        keyboard=False,
        is_open=False,
        backdrop='static',
        style={
            'top': '340px',
            'width': '30%',
            'margin-left': '600px',
            'position': 'fixed',
            'background': 'white',
            'color': 'black',
            'border': '3px solid black'
        }
    )


def completion_popup(model_count):
    """
    This function creates a popup for when a model selection was
    submitted and executed successfully.
    """

    return dbc.Modal(
        id={'type': 'complete-submission-popup', 'index': model_count},
        children=[
            dbc.ModalHeader(
                id='complete-modal-header',
                children=[
                    dbc.ModalTitle(f"Model {model_count} has been successfully created"),
                    html.Div("✓", style={
                        'color': 'white',
                        'fontSize': '20px',
                        'fontWeight': 'bold',
                        'backgroundColor': 'green',
                        'borderRadius': '50%',
                        'width': '30px',
                        'height': '30px',
                        'textAlign': 'center',
                        'lineHeight': '30px',
                        'marginRight': '10px',
                        'display': 'inline-block',
                        'margin-left': '20px'
                    })
                ],
                close_button=False
            ),
            dbc.ModalBody(
                dbc.Button(
                    html.H4(
                        "Close",
                        style={
                            'font-size': '12pt',
                            'margin-top': '5px'
                        }
                    ),
                    id={'type': "close-complete-button", 'index': model_count},
                    n_clicks=0,
                    style={
                        'margin-left': '190px',
                        'border': '2px solid black',
                        'cursor': 'pointer',
                        'height': '40px',
                        'background': 'blue',
                        'color': 'white',
                        'margin-bottom': '20px',
                    }
                )
            )
        ],
        keyboard=False,
        is_open=False,
        backdrop='static',
        style={
            'top': '60px',
            'width': '30%',
            'margin-left': '600px',
            'position': 'fixed',
            'background': 'white',
            'color': 'black',
            'border': '3px solid black'
        }
    )


def input_validation_popup(model_count):
    """
    This function creates a popup alerting the user that they haven't filled in all
    model input fields/ used invalid inputs
    """

    return dbc.Modal(
        id={'type': 'input-validation-popup', 'index': model_count},
        children=[
            dbc.ModalHeader(
                dbc.ModalTitle(f"Input fields error"),
                close_button=False,
                id='alert-modal-header'
            ),
            html.Hr(
                style={
                    'height': '3px',
                    'color': 'black',
                    'background': 'black'
                }
            ),
            dbc.ModalBody(
                children=[
                    html.P(
                        f"You have not filled in all the input fields for model {model_count}, or have provided "
                        f"an invalid value in the input fields. Please check your inputs and try again."
                    ),
                    dbc.Button(
                        html.H4(
                            "Close",
                            style={
                                'font-size': '12pt',
                                'margin-top': '5px'
                            }
                        ),
                        id={'type': "close-alert-button", 'index': model_count},
                        n_clicks=0,
                        style={
                            'margin-left': '190px',
                            'border': '2px solid black',
                            'cursor': 'pointer',
                            'height': '40px',
                            'background': 'blue',
                            'color': 'white',
                            'margin-bottom': '20px'
                        }
                    )
                ],
                id='alert-modal-body'
            )
        ],
        keyboard=False,
        is_open=False,
        backdrop='static',
        style={
            'top': '20px',
            'width': '30%',
            'margin-left': '600px',
            'position': 'fixed',
            'background': 'white',
            'color': 'black',
            'border': '3px solid black'
        }
    )


def file_validation_popup(model_count):
    """
    This function creates a popup alerting the user that they haven't uploaded the training
    and testing data/ provided invalid data.
    """

    return dbc.Modal(
        id={'type': 'file-validation-popup', 'index': model_count},
        children=[
            dbc.ModalHeader(
                dbc.ModalTitle(f"Invalid file upload"),
                close_button=False,
                id='file-modal-header'
            ),
            html.Hr(
                style={
                    'height': '3px',
                    'color': 'black',
                    'background': 'black'
                }
            ),
            dbc.ModalBody(
                children=[
                    html.P(
                        "The provided input for the training and testing data was missing or invalid. Please go "
                        "back to the main page and try again."
                    ),
                    dbc.Button(
                        html.H4(
                            "Close",
                            style={
                                'font-size': '12pt',
                                'margin-top': '5px'
                            }
                        ),
                        id={'type': "close-file-button", 'index': model_count},
                        n_clicks=0,
                        style={
                            'margin-left': '190px',
                            'border': '2px solid black',
                            'cursor': 'pointer',
                            'height': '40px',
                            'background': 'blue',
                            'color': 'white',
                            'margin-bottom': '20px'
                        }
                    )
                ],
                id='file-modal-body'
            )
        ],
        keyboard=False,
        is_open=False,
        backdrop='static',
        style={
            'top': '20px',
            'width': '30%',
            'margin-left': '600px',
            'position': 'fixed',
            'background': 'white',
            'color': 'black',
            'border': '3px solid black'
        }
    )


def model_input_guidelines():
    """
    This function handles the user guidelines for the model inputs page.
    """

    return html.Div(
        id='input-user-guide',
        children=[
            html.H2("User Guidelines"),
            html.P(
                "Below are some guidelines and information about the functionality of the model inputs page, "
                "and some specific information about the individual selection tools available. "
            ),
            html.Div(
                id='input-info-wrapper',
                children=[
                    html.Div(
                        id='input-params-guidelines',
                        children=[
                            html.H4("1. Input parameters"),
                            html.Hr(),
                            html.P(
                                "Here the user selects all the necessary information to create a model (to train and "
                                "test). This includes information such as the model type, the feature descriptor, "
                                "the kmer size (if kmer is selected as a feature descriptor), and the feature "
                                "normalisation algorithm. In addition, the user can opt to enable feature selection, "
                                "unsupervised learning, and hyperparameter optimisation, which would then prompt them "
                                "to input more information (see the sections below)."
                            )
                        ],
                        style={
                            'background': '#f8d7da',
                            'color': '#721c24',
                            'borderColor': '#f5c6cb'
                        }
                    ),
                    html.Div(
                        id='feature-selection-guidelines',
                        children=[
                            html.H4("2. Feature selection"),
                            html.Hr(),
                            html.P(
                                "If the user enables feature selection, they will then need to choose a "
                                "feature selection algorithm, as well as the number of features in the selected model "
                                "to be used by the feature selection algorithm. "
                            )
                        ],
                        style={
                            'background': '#e2e3e5',
                            'color': '#383d41',
                            'borderColor': '#d6d8db'
                        }
                    ),
                    html.Div(
                        id='unsupervised-learning-guidelines',
                        children=[
                            html.H4("3. Unsupervised learning"),
                            html.Hr(),
                            html.P(
                                "If the user enables unsupervised learning, they will then need to choose a "
                                "dimensionality reduction algorithm, as well as the number of dimensions of "
                                "dimensions to be used by the dimensionality reduction algorithm. "
                            )
                        ],
                        style={
                            'background': '#cce5ff',
                            'color': '#004085',
                            'borderColor': '#b8daff'
                        }
                    ),
                    html.Div(
                        id='hyper-opt-guidelines',
                        children=[
                            html.H4("4. Hyperparameter optimisation"),
                            html.Hr(),
                            html.P(
                                "If the user enables hyperparameter optimisation, they will then need to input the "
                                "number of iterations for which they wish to run the Bayesian-Opt hyperparameter "
                                "optimisation algorithm. "
                            )
                        ],
                        style={
                            'background': '#fff3cd',
                            'color': '#856404',
                            'borderColor': '#ffeeba'
                        }
                    )
                ]
            )
        ]
    )


def model_input_parameters_card(model_count):
    """
    This function creates the input parameters card
    """

    return dbc.Card(
        id='parameters-card',
        children=[
            dbc.CardHeader(
                id='card-header-input',
                children=["Input parameters"]
            ),
            dbc.CardBody(
                id='card-body-input',
                children=[
                    model_selection_dropdown(model_count),
                    feature_descriptor_dropdown(model_count),
                    kmer_size_dropdown(model_count),
                    feature_normalization_dropdown(model_count),
                    feature_selection_question(model_count),
                    use_unsupervised_learning_question(model_count),
                    hyperparameter_optimisation_question(model_count)
                ]
            )
        ]
    )


def model_input_feature_selection_card(model_count):
    """
    This function creates the feature selection card
    """

    return dbc.Card(
        id={'type': 'feature-card', 'index': model_count},
        children=[
            dbc.CardHeader(
                id='card-header-input',
                children=['Feature selection']
            ),
            dbc.CardBody(
                id='card-body-input',
                children=[
                    feature_selection_algorithm_dropdown(model_count),
                    feature_number_input(model_count)
                ]
            )
        ],
        style={'display': 'none'}
    )


def model_input_unsupervised_learning_card(model_count):
    """
    This function creates the feature selection card
    """

    return dbc.Card(
        id={'type': 'unsupervised-card', 'index': model_count},
        children=[
            dbc.CardHeader(
                id='card-header-input',
                children=['Unsupervised learning']
            ),
            dbc.CardBody(
                id='card-body-input',
                children=[
                    dimension_reduction_algorithm_dropdown(model_count),
                    dimension_number_input(model_count)
                ]
            )
        ],
        style={'display': 'none'}
    )


def model_input_hyperparameter_optimisation_card(model_count):
    """
    This function creates the hyperparameter optimisation card
    """

    return dbc.Card(
        id={'type': 'hyperparameters-card', 'index': model_count},
        children=[
            dbc.CardHeader(
                id='card-header-input',
                children=['Hyperparameter optimisation']
            ),
            dbc.CardBody(
                id='card-body-input',
                children=[hyperparameter_optimisation_number_input(model_count)]
            )
        ],
        style={'display': 'none'}
    )


def model_selection_dropdown(model_count):
    """
    This function creates the dropdown that allows the user to select
    the type of model they wish to train.
    """

    return html.Div(
        id='model-selection',
        children=[
            html.H6(
                "Select the model type:",
                id='select-model'
            ),
            dcc.Dropdown(
                id={'type': 'model-type-dropdown', 'index': model_count},
                options=[
                    {'label': 'Random Forest', 'value': 'rf'},
                    {'label': 'Multi-layer Perceptron', 'value': 'mlp'},
                    {'label': 'Support Vector Machine', 'value': 'svm'},
                    {'label': 'Ridge Regressor', 'value': 'rr'}
                ],
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '32px'
                },
                searchable=False,
                persistence=True
            )
        ]
    )


def feature_descriptor_dropdown(model_count):
    """
    This function creates the dropdown that allows the user to select
    the type of feature descriptor they wish to use.
    """

    return html.Div(
        id='feature-descriptor',
        children=[
            html.H6(
                "Select feature descriptor:",
                id='select-descriptor'
            ),
            dcc.Dropdown(
                id={'type': 'feature-descriptor-dropdown', 'index': model_count},
                options=[
                    {'label': 'Kmer', 'value': 'kmer'},
                    {'label': 'Binary', 'value': 'binary'},
                ],
                searchable=False,
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '32px'
                },
                persistence=True
            )
        ]
    )


def kmer_size_dropdown(model_count):
    """
    This function creates the dropdown that allows the user to select
    the kmer size to be used (if kmer is selected as the feature descriptor).
    """

    return html.Div(
        id={'type': 'kmer-descriptor', 'index': model_count},
        children=[
            html.H6(
                "Select kmer size:",
                id='select-kmer'
            ),
            dcc.Dropdown(
                id={'type': 'kmer-size-dropdown', 'index': model_count},
                options=[
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                    {'label': '3', 'value': '3'},
                    {'label': '4', 'value': '4'},
                    {'label': '5', 'value': '5'},
                ],
                searchable=False,
                persistence=True,
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '32px'
                }
            )
        ],
        style={'display': 'none'}
    )


def feature_normalization_dropdown(model_count):
    """
    This function creates the dropdown that allows the user to select
    the type of feature normalization algorithm to be used.
    """

    return html.Div(
        id='normalization-descriptor',
        children=[
            html.H6(
                "Select feature normalization method:",
                id='select-normalization'
            ),
            dcc.Dropdown(
                id={'type': 'feature-normalization-dropdown', 'index': model_count},
                options=[
                    {'label': 'ZScore', 'value': 'zscore'},
                    {'label': 'MinMax', 'value': 'minmax'},
                ],
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '32px'
                },
                searchable=False,
                persistence=True
            )
        ]
    )


def feature_selection_question(model_count):
    """
    This function allows the user to enable/ disable feature selection
    for the model they have selected.
    """

    return html.Div(
        id='feature-selection-q',
        children=[
            html.H6(
                "Would you like to enable feature selection?",
                id='select-feature'
            ),
            dcc.RadioItems(
                id={'type': 'feature-selection-question', 'index': model_count},
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                ],
                value='no',
                inline=True,
                labelStyle={'margin-right': '50px', 'margin-left': '50px'},
                style={
                    'width': '60%',
                    'font-size': '14pt',
                    'text-align': 'center'
                },
                persistence=True
            )
        ]
    )


def feature_selection_algorithm_dropdown(model_count):
    """
    This function allows the user to choose the feature selection
    algorithm to be used (in case feature selection is enabled).
    """

    return html.Div(
        id='algorithm-descriptor',
        children=[
            html.H6(
                "Select feature selection algorithm:",
                id='select-algorithm'
            ),
            dcc.Dropdown(
                id={'type': 'feature-selection-dropdown', 'index': model_count},
                options=[
                    {'label': 'Chi-Square', 'value': 'chi'},
                    {'label': 'Information Gain', 'value': 'gain'},
                    {'label': 'F-Score', 'value': 'f-score'},
                    {'label': 'Pearson Correlation', 'value': 'pearson'},
                    {'label': 'Mutual Information', 'value': 'mutual'},
                ],
                searchable=False,
                persistence=True,
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '20px'
                }
            )
        ]
    )


def feature_number_input(model_count):
    """
    This function allows the user to choose the number of features
    to be used by the feature selection algorithm (in case feature selection
    is enabled).
    """

    return html.Div(
        id='feature-number',
        children=[
            html.H6(
                "Enter number of selected features:",
                id='select-feature-number'
            ),
            dcc.Input(
                id={'type': 'feature-number-input', 'index': model_count},
                type='number',
                min=1,
                max=100,
                step=1,
                persistence=True,
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '32px'
                }
            )
        ]
    )


def use_unsupervised_learning_question(model_count):
    """
    This function allows the user to choose if they wish to use unsupervised
    learning for the visualisations (if yes, the user will need to input some
    dimensionality reduction parameters).
    """

    return html.Div(
        id='unsupervised-learning-q',
        children=[
            html.H6(
                "Would like to use unsupervised learning?",
                id='use-unsupervised'
            ),
            dcc.RadioItems(
                id={'type': 'unsupervised-learning-question', 'index': model_count},
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                ],
                value='no',
                inline=True,
                labelStyle={'margin-right': '50px', 'margin-left': '50px'},
                style={
                    'width': '60%',
                    'font-size': '14pt',
                    'text-align': 'center'
                },
                persistence=True
            )
        ]
    )


def dimension_reduction_algorithm_dropdown(model_count):
    """
    This function allows the user to choose the dimension reduction
    algorithm to be used (in case unsupervised learning is enabled).
    """

    return html.Div(
        id='dimension-algorithm-descriptor',
        children=[
            html.H6(
                "Select dimension reduction method:",
                id='select-dimension-algorithm'
            ),
            dcc.Dropdown(
                id={'type': 'dimension-reduction-dropdown', 'index': model_count},
                options=[
                    {'label': 'PCA', 'value': 'pca'},
                    {'label': 'tsne', 'value': 'tsne'},
                    {'label': 'UMAP', 'value': 'umap'},
                ],
                searchable=False,
                persistence=True,
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '20px'
                }
            )
        ]
    )


def dimension_number_input(model_count):
    """
    This function allows the user to choose the number of dimensions
    to be used by the dimensionality reduction algorithm (in case unsupervised learning
    is enabled).
    """

    return html.Div(
        id='dimension-number',
        children=[
            html.H6(
                "Enter number of dimensions:",
                id='select-dimension-number'
            ),
            dcc.Input(
                id={'type': 'dimension-number-input', 'index': model_count},
                type='number',
                min=1,
                max=10,
                step=1,
                persistence=True,
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '32px'
                }
            )
        ]
    )


def hyperparameter_optimisation_question(model_count):
    """
    This function allows the user to choose if they wish to use hyperparameter
    optimisation for the selected model.
    """

    return html.Div(
        id='hyper-opt-q',
        children=[
            html.H6(
                f"Would like to use hyperparameter optimisation?",
                id='use-hyper-opt'
            ),
            dcc.RadioItems(
                id={'type': 'hyper-opt-question', 'index': model_count},
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                ],
                value='no',
                inline=True,
                labelStyle={'margin-right': '50px', 'margin-left': '50px'},
                style={
                    'width': '60%',
                    'font-size': '14pt',
                    'text-align': 'center'
                },
                persistence=True
            )
        ]
    )


def hyperparameter_optimisation_number_input(model_count):
    """
    This function allows the user to choose the number of iterations
    to be used by the hyperparameter optimisation algorithm (in case hyperparameter
    optimisation is enabled).
    """

    return html.Div(
        id='loop-number',
        children=[
            html.H6(
                "Enter number of iterations:",
                id='select-iteration-number'
            ),
            dcc.Input(
                id={'type': 'iteration-number-input', 'index': model_count},
                type='number',
                min=1,
                max=100,
                step=1,
                persistence=True,
                style={
                    'width': '91.5%',
                    'font-size': '12pt',
                    'text-align': 'center',
                    'margin-left': '32px'
                }
            )
        ]
    )


@callback(
    Output({'type': 'feature-card', 'index': MATCH}, 'style'),
    Input({'type': 'feature-selection-question', 'index': MATCH}, 'value')
)
def enable_feature_selection(answer):
    """
    This callback function ensures the correct functionality
    for enabling/ disabling feature selection.
    """

    if answer == 'yes':
        return {
            'display': 'block',
            'background': 'white',
            'color': 'black',
            'width': '100%',
            'margin-top': '20px',
            'border': '2px solid black',
        }

    elif answer == 'no':
        return {'display': 'none'}


@callback(
    Output({'type': 'unsupervised-card', 'index': MATCH}, 'style'),
    Input({'type': 'unsupervised-learning-question', 'index': MATCH}, 'value')
)
def enable_unsupervised(answer):
    """
    This callback function ensures the correct functionality
    for enabling/ disabling unsupervised learning.
    """

    if answer == 'yes':
        return {
            'display': 'block',
            'background': 'white',
            'color': 'black',
            'width': '100%',
            'margin-top': '20px',
            'border': '2px solid black',
        }

    elif answer == 'no':
        return {'display': 'none'}


@callback(
    Output({'type': 'hyperparameters-card', 'index': MATCH}, 'style'),
    Input({'type': 'hyper-opt-question', 'index': MATCH}, 'value')
)
def enable_hyperopt(answer):
    """
    This callback function ensures the correct functionality
    for enabling/ disabling hyperparameter optimisation.
    """

    if answer == 'yes':
        return {
            'display': 'block',
            'background': 'white',
            'color': 'black',
            'width': '100%',
            'margin-top': '20px',
            'border': '2px solid black',
        }

    elif answer == 'no':
        return {'display': 'none'}


@callback(
    Output({'type': 'kmer-descriptor', 'index': MATCH}, 'style'),
    Input({'type': 'feature-descriptor-dropdown', 'index': MATCH}, 'value')
)
def show_kmer_dropdown(value):
    """
    This callback function ensures the correct functionality
    for enabling/ disabling Kmer usage for feature description.
    """

    if value == 'kmer':
        return {
            'margin-top': '-10px',
            'display': 'flex',
            'align-items': 'center'
        }

    return {'display': 'none'}


@callback(
    Output({'type': 'delete-model-popup', 'index': MATCH}, 'is_open'),
    [Input({'type': 'delete-button', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'no-button', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'yes-button', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'delete-model-popup', 'index': MATCH}, 'is_open')],
)
def press_delete_button(delete_clicks, no_clicks, yes_clicks, is_open):
    """
    This callback handles the functionality of the delete button
    """

    ctx = dash.callback_context

    if not ctx.triggered:
        # No buttons were clicked
        return is_open

    # Extract the index part from the triggered_id
    triggered_id = ctx.triggered[0]['prop_id']
    new_split = triggered_id.split(".")
    big_string = new_split[0].strip("{}")
    another_split = big_string.split(",")

    # Get index value from index part
    index_part = another_split[0]
    index_value = index_part[-1]

    # If the delete button was pressed more, the pop-up should be visible
    if delete_clicks > no_clicks and yes_clicks == 0:
        return True

    # If the no button was pressed more, the pop-up should be hidden
    elif no_clicks >= delete_clicks:
        return False

    elif yes_clicks >= 0:
        del app.globals.MODELS_LIST[f'Model {index_value}']
        return False

    return is_open


@callback(
    Output({'type': 'confirm-model-deletion-popup', 'index': MATCH}, 'is_open'),
    [Input({'type': 'close-button', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'yes-button', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'confirm-model-deletion-popup', 'index': MATCH}, 'is_open')],
)
def deletion_confirmation_popup(close_clicks, yes_clicks, is_open):
    """
    This callback handles the functionality of the confirmation pop-up
    """

    ctx = dash.callback_context

    if not ctx.triggered:
        # No buttons were clicked
        return is_open

    # If the yes button was pressed, the pop-up should be visible
    if yes_clicks > close_clicks:
        return True

    # If the close button was pressed, the pop-up should be hidden
    elif close_clicks >= yes_clicks:
        return False

    return is_open


@callback(
    Output({'type': 'javascript-trigger', 'index': MATCH}, 'children'),
    [Input({'type': 'confirm-model-deletion-popup', 'index': MATCH}, 'is_open'),
     Input({'type': 'delete-model-popup', 'index': MATCH}, 'is_open'),
     Input({'type': 'submit-model-popup', 'index': MATCH}, 'is_open'),
     Input({'type': 'input-validation-popup', 'index': MATCH}, 'is_open'),
     Input({'type': 'file-validation-popup', 'index': MATCH}, 'is_open')],
    [State({'type': 'confirm-model-deletion-popup', 'index': MATCH}, 'id'),
     State({'type': 'delete-model-popup', 'index': MATCH}, 'id'),
     State({'type': 'submit-model-popup', 'index': MATCH}, 'id'),
     State({'type': 'input-validation-popup', 'index': MATCH}, 'id'),
     State({'type': 'file-validation-popup', 'index': MATCH}, 'id')]
)
def convert_to_json(
        is_open1,
        is_open2,
        is_open3,
        is_open4,
        is_open5,
        modal1_id,
        modal2_id,
        modal3_id,
        modal4_id,
        modal5_id
):
    """
    This callback converts data to JSON format (used when freezing background
    when popup appears).
    """

    data = {
        "is_open1": is_open1,
        "is_open2": is_open2,
        "is_open3": is_open3,
        "is_open4": is_open4,
        "is_open5": is_open5,
        "modal1_id": modal1_id,
        "modal2_id": modal2_id,
        "modal3_id": modal3_id,
        "modal4_id": modal4_id,
        "modal5_id": modal5_id
    }

    return json.dumps(data)


# This callback handles the freezing of the background
clientside_callback(
    """
    function(data) {
        var details = JSON.parse(data);
        if (details.is_open1) {
            var modalId = details.modal1_id.type + '-' + details.modal1_id.index;
            disablePageInteractions(modalId);
        } else if (details.is_open2) {
            var modalId = details.modal2_id.type + '-' + details.modal2_id.index;
            disablePageInteractions(modalId);
        } else if (details.is_open3) {
            var modalId = details.modal3_id.type + '-' + details.modal3_id.index;
            disablePageInteractions(modalId);
        } else if (details.is_open4) {
            var modalId = details.modal4_id.type + '-' + details.modal4_id.index;
            disablePageInteractions(modalId);
        } else if (details.is_open5) {
            var modalId = details.modal5_id.type + '-' + details.modal5_id.index;
            disablePageInteractions(modalId);
        } else {
            enablePageInteractions();
        }
    }
    """,
    Output({'type': 'dummy-div', 'index': MATCH}, 'children'),
    Input({'type': 'javascript-trigger', 'index': MATCH}, 'children')
)


def validate_user_input(
        model_type,
        feature_descriptor,
        kmer_size,
        feature_normalization,
        feature_selection_ans,
        feature_selection,
        feature_number,
        unsupervised_learning_ans,
        dimension_reduction_algorithm,
        dimension_number,
        hyperopt_ans,
        hyperopt_iterations
):
    """
    This function is used to ensure all the input fields have been correctly filled.
    """

    # Checks to see all necessary inputs are present
    if not model_type or not feature_descriptor or not feature_normalization:
        return False

    elif feature_descriptor == 'kmer' and not kmer_size:
        return False

    elif feature_selection_ans == "yes" and (not feature_selection or not feature_number):
        return False

    elif unsupervised_learning_ans == "yes" and (not dimension_reduction_algorithm or not dimension_number):
        return False

    elif hyperopt_ans == "yes" and not hyperopt_iterations:
        return False

    # Checks to see all given number inputs are valid
    elif dimension_number and (dimension_number < 1 or dimension_number > 10):
        return False

    elif feature_number and (feature_number < 1 or feature_number > 100):
        return False

    elif hyperopt_iterations and (hyperopt_iterations < 1 or hyperopt_iterations > 100):
        return False

    return True


@callback(
    [Output({'type': 'submit-model-popup', 'index': MATCH}, 'is_open'),
     Output({'type': 'input-validation-popup', 'index': MATCH}, 'is_open'),
     Output({'type': 'file-validation-popup', 'index': MATCH}, 'is_open')],
    [Input({'type': 'submit-button', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'close-alert-button', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'close-file-button', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'model-type-dropdown', 'index': MATCH}, 'value'),
     Input({'type': 'feature-descriptor-dropdown', 'index': MATCH}, 'value'),
     Input({'type': 'kmer-size-dropdown', 'index': MATCH}, 'value'),
     Input({'type': 'feature-normalization-dropdown', 'index': MATCH}, 'value'),
     Input({'type': 'feature-selection-question', 'index': MATCH}, 'value'),
     Input({'type': 'feature-selection-dropdown', 'index': MATCH}, 'value'),
     Input({'type': 'feature-number-input', 'index': MATCH}, 'value'),
     Input({'type': 'unsupervised-learning-question', 'index': MATCH}, 'value'),
     Input({'type': 'dimension-reduction-dropdown', 'index': MATCH}, 'value'),
     Input({'type': 'dimension-number-input', 'index': MATCH}, 'value'),
     Input({'type': 'hyper-opt-question', 'index': MATCH}, 'value'),
     Input({'type': 'iteration-number-input', 'index': MATCH}, 'value')],
    [State({'type': 'submit-model-popup', 'index': MATCH}, 'is_open'),
     State({'type': 'input-validation-popup', 'index': MATCH}, 'is_open'),
     State({'type': 'file-validation-popup', 'index': MATCH}, 'is_open')]
)
def press_submit_button(
        submit_clicks,
        close_input_clicks,
        close_file_clicks,
        model_type,
        feature_descriptor,
        kmer_size,
        feature_normalization,
        feature_selection_ans,
        feature_selection,
        feature_number,
        unsupervised_learning_ans,
        dimension_reduction_algorithm,
        dimension_number,
        hyperopt_ans,
        hyperopt_iterations,
        is_submit_open,
        is_invalid_open,
        is_file_open
):
    """
    This callback handles the functionality of the submit button
    """

    ctx = dash.callback_context

    if not ctx.triggered:
        # No buttons were clicked
        return is_submit_open, is_invalid_open, is_file_open

    # if the submit button was clicked
    elif submit_clicks > (close_input_clicks + close_file_clicks):
        training_data = app.globals.TRAINING_DATA
        testing_data = app.globals.TESTING_DATA
        querying_data = app.globals.QUERYING_DATA

        # if the required files were not uploaded or uploaded in the wrong format
        if training_data is None or testing_data is None:
            return False, False, True

        # perform input validation
        if not validate_user_input(model_type, feature_descriptor, kmer_size, feature_normalization,
                                   feature_selection_ans, feature_selection, feature_number, unsupervised_learning_ans,
                                   dimension_reduction_algorithm, dimension_number, hyperopt_ans, hyperopt_iterations):
            return False, True, False

        # set model based on input parameters
        model = None

        if model_type == 'rf':
            model = RandomForest()

        elif model_type == 'mlp':
            model = MultiLayerPerceptron()

        elif model_type == 'svm':
            model = SupportVectorMachine()

        elif model_type == 'rr':
            model = RidgeRegressor()

        # set model info based on inputs

        # set model data
        model.set_training_data(training_data)
        model.set_testing_data(testing_data)
        if querying_data is not None:
            model.set_querying_data(querying_data)

        # set model parameters
        model.set_feature_encoding_method(feature_descriptor)
        model.set_feature_normalization_algorithm(feature_normalization)
        if kmer_size:
            model.set_kmer_size(kmer_size)
        if feature_selection_ans == "yes":
            model.set_feature_selection_algorithm(feature_selection)
            model.set_feature_number(feature_number)
        if hyperopt_ans == "yes":
            model.set_hyper_opt_iterations(hyperopt_iterations)
        if unsupervised_learning_ans == "yes":
            model.set_dimensionality_reduction_algorithm(dimension_reduction_algorithm)
            model.set_dimension_number(dimension_number)

        # TODO: TRAIN AND TEST THE MODEL

        # Extract the index part from the triggered_id
        triggered_id = ctx.triggered[0]['prop_id']
        new_split = triggered_id.split(".")
        big_string = new_split[0].strip("{}")
        another_split = big_string.split(",")

        # Get index value from index part
        index_part = another_split[0]
        index_value = index_part[-1]

        # Store model in the globally available list
        app.globals.MODELS_LIST[f'Model {index_value}'] = model

        return True, False, False

    return False, False, False
