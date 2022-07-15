# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math
from io import BytesIO
from pathlib import Path
import requests
from PIL import Image, ImageDraw
from src.constants import *

COMMON_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def build_layer_config(data: FilteredLedger, layer_config: LayerConfig) -> LayerConfig:
    """Generate a LayerConfig from the final ledger and the set constants.

    Parameters
    ----------
    data : FilteredLedger
        Ledger/list of users, their scores and avatar URLs.
    layer_config : LayerConfig
        Constant part of the LayerConfig.

    Returns
    -------
    LayerConfig
        A config data structure that translates to the image.
    """

    prev_usr_idx = 1
    layer_config[0].append([data[0]])
    for idx in range(1, len(layer_config)):
        curr_usr_idx = prev_usr_idx + layer_config[idx][1]
        layer_config[idx].append(data[prev_usr_idx:curr_usr_idx])
        prev_usr_idx = curr_usr_idx

    return layer_config


def download_avatar(avatar_url: str, placeholder_img: Path) -> BytesIO | Path:
    """Download the binary content off of the given URL and return a bytes buffer of the same.

    Parameters
    ----------
    avatar_url : str
        URL to download content/avatar from.
    placeholder_img : Path
        Image to use if no avatar URL is passed
        e.g. when the account is deleted

    Returns
    -------
    BytesIO | Path
        A bytes buffer of the downloaded content or
        the path to the placeholder image.
    """

    if avatar_url:
        r = requests.get(avatar_url, headers=COMMON_REQUEST_HEADERS)
        r.raise_for_status()
        return BytesIO(r.content)
    else:
        return placeholder_img


def create_mask(image: Image) -> Image:
    """Return a centered circular mask for any image.

    Parameters
    ----------
    image : Image
        Image to return the mask for.

    Returns
    -------
    Image
        Mask Image.
    """

    h, w = image.size
    mask_size = (h * 3, w * 3)
    alpha = Image.new("L", mask_size, 0)
    ImageDraw.Draw(alpha).pieslice([(0, 0), mask_size], 0, 360, fill=255)
    return alpha.resize(image.size, Image.LANCZOS)


def create_image(
    bg_size: tuple[int],
    bg_color: str,
    layer_config: LayerConfig,
    placeholder_img_path: Path = None,
    debug_img_path: Path = None,
) -> Image:
    """Final call to translate the passed LayerConfig into a picture.

    Parameters
    ----------
    bg_size : tuple[int]
        Background's height and width in pixels.
    bg_color : str
        Background's color as hex string.
    layer_config : LayerConfig
        Final LayerConfig structure to translate.
    placeholder_img_path : Path, optional
        Local path passed to `download_avatar`, by default None
    debug_img_path : Path, optional
        Useful only in debugging.
        The given image is used in place of actual avatars to save download time, by default None

    Returns
    -------
    Image
        A PIL.Image constructed from the LayerConfig.
    """

    bg = Image.new(mode="RGB", size=bg_size, color=bg_color)
    print("created background")

    print("creating circles. might take time...")

    for layer_idx in range(len(layer_config)):
        R, count, gap_size, users = layer_config[layer_idx]
        gaps_count = count - 1
        circumference = 2 * math.pi * R
        base_usr_img_angle = 360 / count
        usr_img_hw = math.floor(((circumference - (gaps_count * gap_size)) / count))

        # handle the central avatar size
        if layer_idx == 0:
            usr_img_hw = layer_config[1][0] + 40

        for user_idx in range(len(users)):
            if debug_img_path:
                avatar = Image.open(debug_img_path)
            else:
                avatar = Image.open(
                    download_avatar(users[user_idx]["avatar_url"], placeholder_img_path)
                )
            avatar = avatar.convert("RGB").resize((usr_img_hw, usr_img_hw))

            angle = math.radians(base_usr_img_angle * user_idx + gap_size)

            # +center of the background image
            avatar_center_x = math.floor(math.cos(angle) * R + (bg.size[0] / 2))
            avatar_center_y = math.floor(math.sin(angle) * R + (bg.size[1] / 2))

            bg.paste(
                avatar,
                (
                    # Image.paste needs top left co-ordinates
                    # the avatar being a square, subtracting half of its height and width returns the top left co-ordinates
                    math.floor(avatar_center_x - (usr_img_hw / 2)),
                    math.floor(avatar_center_y - (usr_img_hw / 2)),
                ),
                create_mask(avatar),
            )

    return bg
