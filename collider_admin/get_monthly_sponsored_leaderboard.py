
from rediz.client import Rediz
from rediz.collider_config_private import REDIZ_COLLIDER_CONFIG, CELLOSE_BOBCAT, OFFCAST_GOOSE
from pprint import pprint

if __name__ == '__main__':
    rdz = Rediz(**REDIZ_COLLIDER_CONFIG)
    pprint( rdz.get_monthly_sponsored_leaderboard(sponsor=OFFCAST_GOOSE) )


