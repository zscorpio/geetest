# -*- coding: utf-8 -*-
import urllib.request
import copy
import cv2
import ddddocr
import flask
import json
import numpy as np

server = flask.Flask(__name__)

det = ddddocr.DdddOcr(det=True, show_ad=False)
ocr = ddddocr.DdddOcr(beta=True, show_ad=False)


def get_match_result(target, source):
    output = [None] * 2
    keys = list(source.keys())

    if len(target) == 2:
        match_size = 0

        for i in range(len(keys)):
            if target[i] in source and source[target[i]]:
                match_size += 1
                output[i] = source[target[i]]

        if match_size == 0:
            output[0] = source[keys[0]]
            output[1] = source[keys[1]]

        if match_size == 1:
            remaining_key = keys[0] if len(keys) > 0 else None
            if not output[0]:
                output[0] = source[remaining_key]
            if not output[1]:
                output[1] = source[remaining_key]

    if len(target) == 3:
        output = [None] * 3
        match_size = 0

        for i in range(len(keys)):
            if target[i] in source and source[target[i]]:
                match_size += 1
                output[i] = source[target[i]]

        if match_size == 1:
            output = [None] * 3

        if match_size == 2:
            remaining_key = keys[0] if len(keys) > 0 else None
            if not output[0]:
                output[0] = source[remaining_key]
            if not output[1]:
                output[1] = source[remaining_key]
            if not output[2]:
                output[2] = source[remaining_key]

    coords = [None] * len(output)

    for i, v in enumerate(output):
        if v:
            coords[i] = [(v[0] + v[2]) / 2, (v[1] + v[3]) / 2]

    return coords


def process_image(image_data):
    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    order = image[344:384, 0:150]
    _, order = cv2.imencode('.jpg', order)
    target = ocr.classification(order.tobytes())

    new = copy.copy(image)
    new[340:390, 0:400] = (0, 0, 0)
    new = cv2.imencode('.jpg', new)[1]
    poses = det.detection(new.tobytes())

    source = {}
    for box in poses:
        x1, y1, x2, y2 = box
        part = image[y1:y2, x1:x2]
        img = cv2.imencode('.jpg', part)[1]
        result = ocr.classification(img.tobytes())
        if len(result) > 1:
            result = result[0]
        source[result] = [x1, y1, x2, y2]

    return target, source


@server.route('/geetest_click', methods=['GET'])
def geetest_click():
    image_url = flask.request.args.get('image_url')

    try:
        with urllib.request.urlopen(image_url) as response:
            image_data = response.read()
        target, source = process_image(image_data)

        return {
            'target': target,
            'source': source,
            'coords': get_match_result(target, source)
        }
    except Exception as e:
        return {
            'error': str(e)
        }, 500


@server.errorhandler(500)
def handle_error(e):
    res = {"error": "服务器内部错误"}
    return json.dumps(res), 500


if __name__ == "__main__":
    server.run(port=9991, host='0.0.0.0', debug=False)
