import io
from contextlib import redirect_stdout
from os.path import dirname, join

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
current_dir = dirname(__file__)
templates = Jinja2Templates(join(current_dir, "templates"))


def capture_code(code_str: str):
    try:
        with io.StringIO() as buf, redirect_stdout(buf):
            exec(code_str)
            output = buf.getvalue()
            message = "Code successfully run"
            success = True
    except Exception as e:
        output = str(e)
        message = f"Code failed with exception: {type(e).__name__}"
        success = False
    return output, message, success


"""
ROUTES
"""


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/run", response_class=HTMLResponse)
async def run(request: Request, code_str: str = Form()):
    result = {"code_str": code_str}
    result["output"], result["message"], result["success"] = capture_code(code_str)
    return templates.TemplateResponse(
        request=request, name="results.html", context=result
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
