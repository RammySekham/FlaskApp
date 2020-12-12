import dash_bootstrap_components as dbc
import dash_core_components as dcc


def option_menu(values, label, **kwargs):
    options = [{"label": s, "value": s} for s in values]
    kwargs["value"] = kwargs.get("value", values[0])

    if len(options) <= 3:
        component = dbc.RadioItems
        kwargs["inline"] = True
    else:
        component = dbc.Select

    return dbc.FormGroup([dbc.Label(label), component(options=options, **kwargs)])


def dcc_multiselect(values, label, **kwargs):
    options = [{"label": s, "value": s} for s in values]
    kwargs["value"] = kwargs.get("value", values[0])

    return dcc.Dropdown(options=options, **kwargs, multi=True)
