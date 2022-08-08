import base64
# ic = ImageCaptcha()
# ic.write('1a8c', '1a8c' + '.png', format='png')
# generate_captcha()
from io import BytesIO
from random import randint

from captcha.image import ImageCaptcha


def generate_captcha():
    list = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]
    chars = ""
    for i in range(4):
        chars += list[randint(0, 62)]
    from io import BytesIO

    BytesIO()
    image = ImageCaptcha().generate_image(chars)
    import base64

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())
    # image.show()
    # image.tostring()
    #
    # return image.tobytes()


class Captcha:
    @classmethod
    def get_captcha(cls):
        list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        chars = ""
        for i in range(4):
            chars += list[randint(0, 62)]
        image = ImageCaptcha().generate_image(chars)

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        data = buffer.getvalue()
        return "data:image/png;base64," + base64.b64encode(data).decode()


ic = ImageCaptcha()
ic.write("1a8u", "1a8c" + ".png", format="png")
