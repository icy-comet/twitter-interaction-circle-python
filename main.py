import json
from pathlib import Path
import src.exceptions as exceptions
from src.constants import LayerConfig
from src.data_collection import collect_data
from src.image_creation import build_layer_config, create_image

# from src.encoding import encode_img_to_b64


class Config:
    # Twitter username to scan
    USERNAME = "AniketTeredesai"
    # hex of the desired background color
    BG_CLR = "#448dd9"
    # (height, width)
    BG_SIZE = (1000, 1000)
    # layer config constants
    # [[layer radius, number of users in the layer, gap size], ...]
    LAYER_CONFIG: LayerConfig = [
        [0, 1, 0],
        [200, 8, 25],
        [330, 15, 25],
        [450, 26, 20],
    ]
    # each page returns maximum of 200 tweets and likes
    FAVORITES_PAGES_TO_FETCH = 1
    TIMELINE_PAGES_TO_FETCH = 1


def main(debug: bool = False):

    d = Path("res/circles_dump.json").resolve()
    i = Path("res/circles.jpg").resolve()
    p = Path("res/placeholder_avatar.png").resolve()

    try:
        if debug and d.exists():
            q = Path("res/debug_avatar.jpg").resolve()
            with open(d, "r") as f:
                lc = json.load(f)
        else:
            q = None
            ledger = collect_data(
                Config.USERNAME,
                Config.TIMELINE_PAGES_TO_FETCH,
                Config.FAVORITES_PAGES_TO_FETCH,
                Config.LAYER_CONFIG,
            )

            lc = build_layer_config(ledger, Config.LAYER_CONFIG)

            with open(d, "w") as f:
                json.dump(lc, f)

        image = create_image(Config.BG_SIZE, Config.BG_CLR, lc, p, q)
        image.save(i, "jpeg")
        # data_str = encode_img_to_b64(image)

    except (exceptions.InactiveUser, exceptions.InvalidUser, exceptions.ApiError) as e:
        print(e)


if __name__ == "__main__":
    # main(debug=True)
    main()
