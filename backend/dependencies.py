from fastapi import HTTPException, Depends, Request

def get_ia_model(request: Request):
    ia_model = getattr(request.app.state, "ia_modelo", None)
    if ia_model is None:
        raise HTTPException(
            status_code=500, detail="O modelo de IA não está inicializado."
        )
    return ia_model