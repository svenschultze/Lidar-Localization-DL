from lldl.model import residual, shallow

def load(name):
    if name is "residual":
        model =  residual.build_model()
    elif name is "shallow":
        model =  shallow.build_model()
    else:
        raise Exception("Model name must be one of ['residual', 'shallow']")

    return model