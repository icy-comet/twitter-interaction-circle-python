# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


class InvalidUser(Exception):
    """Raised if the passed in username doesn't exist with Twitter."""

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"{self.username} isn't a valid username."


class ApiError(Exception):
    """Raised if something goes wrong while communicating with the Twitter API.s"""

    def __str__(self):
        return "Something went wrong with the API."
