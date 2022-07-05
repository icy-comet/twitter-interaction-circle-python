# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from io import BytesIO
from base64 import b64encode
from PIL import Image


def encode_img_to_b64(img: Image) -> str:
    """Encode a PIL image to a base64 string.

    Parameters
    ----------
    img : Image
        The image to be encoded.

    Returns
    -------
    str
        Encoded string.
    """

    buffer = BytesIO()
    img.save(buffer, "JPEG")
    return b64encode(buffer.getvalue()).decode("ascii")
