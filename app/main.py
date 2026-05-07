from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def main():
    return {'message': 'App working properly'}
