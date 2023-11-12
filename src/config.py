"""Traffic Evader config"""

WIDTH = 960
HEIGHT = 540
FPS = 60
INITIAL_SPEED = 2
LANE_SWITCH_SPEED = 1

LEVELS = {
    "easy": {
        "lanes": 5,
        "lane_width": 90,
        "player": {
            "init_x": WIDTH // 2 - 40,
            "init_lane": 3
        }
    },
    "normal": {
        "lanes": 4,
        "lane_width": 112,
        "player": {
            "init_x": WIDTH // 2 - 95,
            "init_lane": 2
        }
    },
    "hard": {
        "lanes": 3,
        "lane_width": 150,
        "player": {
            "init_x": WIDTH // 2 - 40,
            "init_lane": 2
        }
    }
}
