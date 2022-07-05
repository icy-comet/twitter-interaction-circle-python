# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from enum import IntEnum, auto

# {username: {1: int, 2:int, 3:int}, ...}
InteractionsLedger = dict[str, dict[int, int]]
# [{username: str, score: float, avatar_url: str}, ...]
FilteredLedger = list[dict]
# {username: avatar_url, ...}
AvatarLedger = dict[str, str]
# [[layer radius, number of users in the layer, gap size, list of users in the layer], ...]
LayerConfig = list[list[int | list[dict]]]


class Interaction(IntEnum):
    like = auto()
    retweet = auto()
    reply = auto()
