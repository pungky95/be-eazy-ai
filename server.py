import os
from io import BytesIO
from flask import Flask, request, send_file
from bg import remove

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    global model, alpha_matting, alpha_matting_foreground_threshold, alpha_matting_background_threshold, alpha_matting_erode_structure_size
    file_content = ""

    if request.method == "POST":
        if "file" not in request.files:
            return {"error": "file is required"}, 400
        if "api-key" not in request.form:
            return {"error": "api key is required"}, 400

        api_key = request.form.get("api-key", type=str)
        if api_key != "YmUtZWFzeQ":
            return {"error": "api key is invalid"}, 400

        model = request.form.get("model", type=str, default="u2net")
        if model not in ("u2net", "u2netp"):
            return {"error": "model is invalid value"}, 400

        file_content = request.files["file"].read()
        alpha_matting = request.form.get("is_smooth", type=int, default=0) == 1 if True else False;

        alpha_matting_foreground_threshold = request.args.get("alpha_matting_foreground_threshold", type=int,
                                                              default=240)
        alpha_matting_background_threshold = request.args.get("alpha_matting_background_threshold", type=int,
                                                              default=10)
        alpha_matting_erode_structure_size = request.args.get("alpha_matting_erode_structure_size", type=int,
                                                              default=10)

    if file_content == "":
        return {"error": "File content is empty"}, 400

    try:
        return send_file(BytesIO(remove(
            file_content,
            model,
            alpha_matting,
            alpha_matting_foreground_threshold,
            alpha_matting_background_threshold,
            alpha_matting_erode_structure_size
        )), mimetype="image/png", )
    except Exception as e:
        app.logger.exception(e, exc_info=True)
        return {"error": "oops, something went wrong!"}, 500


def main():
    port = int(os.environ.get('PORT', 8080))
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    main()
