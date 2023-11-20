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

CARS_OBSTACLES = {
    "low": [
        "chrysler-pt-cruiser-gt.png",
        "fiat-multipla.png",
        "lada-1200-vaz-2101.png",
        "peugeot-307.png",
        "pontiac-aztek.png",
        "renault-kadjar.png",
        "toyota-prius.png",
    ],
    "medium": [
        "aston-martin-vantage.png",
        "bmw-1-series.png",
        "bmw-m3.png",
        "chevrolet-camaro.png",
        "mercedes-amg-gt-r.png",
        "rolls-royce-spectre.png",
    ],
    "high": [
        "bugatti-chiron.png",
        "ferrari-daytona-sp3.png",
        "lamborghini-aventador-svj.png",
        "lexus-lfa.png",
        "porsche-911-gt3-rs.png"
    ]
}
