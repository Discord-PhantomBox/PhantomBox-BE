import joblib

from model.label_model import TextRequest, LabelTextResponse

model = joblib.load("labeling_model.pkl")

async def predict_emotion(text: str):
    pred = model.predict([text])
    return pred[0]

async def labeling(label_request : TextRequest) -> LabelTextResponse:
    label_text = label_request.text
    label = await predict_emotion(label_text)
    return LabelTextResponse(label=label)

