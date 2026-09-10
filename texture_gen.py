import random
from enum import Enum
from collections.abc import Callable

class TexturePool:
    def __init__(self,
                 name: str,
                 textures: list[str], 
                 tones,#: list[tuple[int, int, int]], 
                 predicate: Callable[[float, float], bool]
                 ):
        self.name = name
        self.textures = textures
        self.tones = tones
        self.predicate = predicate
        self.texture = None
        self.tone = None

    def test(self, planet) -> bool:
        return self.predicate(planet.get("pl_rade") or 1, planet.get("pl_eqt") or 255)

    def get_texture(self) -> str:
        if not self.texture: self.texture = random.choice(self.textures)
        return self.texture

    def get_tone(self) -> tuple[int, int, int]:
        if not self.tone: self.tone = random.choice(self.tones)
        return self.tone

def __between(value: float, lower: float, upper: float) -> bool: return value >= lower and value <= upper

bases = [
    TexturePool(name="Rocky",
        textures=[
            "base1.jpg",
            "base2.jpg",
            "base4.jpg",
            "base8.jpg",
            "base9.jpg",
            "base10.jpg",
        ],
        tones=[
            ((107, 101, 96), (227, 217, 209)),
            ((153, 107, 76), (209, 140, 120)),
            ((125, 80, 49), (179, 63, 39)),
            ((144, 111, 61), (204, 150, 70)),
            ((117, 52, 0), (224, 111, 19)),
            ((172, 95, 21), (150, 147, 144)),
            ((179, 122, 139), (178, 88, 207)),
            ((101, 88, 56), (235, 188, 70)),
            ((108, 122, 106), (121, 230, 106)),
            ((47, 46, 161), (78, 212, 61)),
            ((228, 75, 237), (240, 126, 17))
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            pl_rade < 2.5,
            pl_eqt < 1000
        ])),
    TexturePool(name="Desert",
        textures=[
            "base2.jpg",
            "base3.jpg",
            "base4.jpg",
            "base11.jpg",
            "base12.jpg",
        ],
        tones=[
            ((184, 142, 103), (211, 192, 114)),
            ((223, 163, 110), (247, 208, 139)),
            ((189, 111, 76), (255, 98, 50)),
            ((163, 59, 67), (245, 72, 89)),
            ((181, 101, 184), (233, 169, 235))
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            pl_rade < 2.5,
            pl_eqt > 700
        ])),
    TexturePool(name="Ocean",
        textures=[
            "base3.jpg",
            "base5.jpg",
            "base11.jpg",
            "base12.jpg",
        ],
        tones=[
            ((27, 75, 116), (73, 161, 237)),
            ((13, 80, 146), (20, 131, 242)),
            ((19, 95, 145), (68, 161, 222)),
            ((40, 187, 135), (138, 240, 204)),
            ((55, 59, 163), (227, 58, 240))
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            pl_rade < 2.5,
            __between(pl_eqt, 273, 373)
        ])),
    TexturePool(name="Ice Giant",
        textures=[
            "base1.jpg",
            "base2.jpg",
            "base3.jpg",
            "base5.jpg",
        ],
        tones=[
            ((166, 205, 240), (200, 225, 247)),
            ((125, 130, 255), (168, 170, 231)),
            ((151, 158, 230), (255, 255, 255))
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            __between(pl_rade, 2.5, 7),
            pl_eqt < 273
        ])),
    TexturePool(name="Gas Giant",
        textures=[
            "base3.jpg",
            "base5.jpg",
            "base6.jpg",
            "base7.jpg",
        ],
        tones=[
            ((147, 56, 61), (255, 0, 251)),
            ((228, 76, 39), (232, 159, 111)),
            ((158, 113, 142), (252, 108, 202)),
            ((246, 158, 84), (255, 216, 132)),
            ((165, 108, 53), (237, 208, 157)),
            ((97, 93, 107), (189, 172, 235)),
            ((74, 69, 99), (49, 103, 204)),
            ((16, 139, 217), (187, 15, 217)),
            ((0, 142, 67), (105, 240, 168)),
            ((172, 157, 154), (255, 192, 179)),
            ((113, 68, 47), (255, 81, 0)),
            ((81, 196, 63), (217, 193, 59)),
            ((236, 20, 242), (86, 239, 245)),
            ((252, 34, 34), (237, 192, 73))
        ],
        predicate=lambda pl_rade, pl_eqt: any([
            pl_rade > 7,
            all([
                pl_rade > 2.5,
                pl_eqt > 200
            ]),
        ])),
]

details = [
    TexturePool(name="Scarce Clouds",
        textures=[
            "detail1.png",
        ],
        tones=[
            (220, 220, 215),
            (235, 230, 215),
            (200, 210, 215),
            (245, 235, 220)
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            __between(pl_rade, 0.5, 2.5),
            __between(pl_eqt, 200, 700),
            random.random() < 0.9
        ])),
    TexturePool(name="Cloudy",
        textures=[
            "detail2.png",
        ],
        tones=[
            (245, 245, 240),
            (225, 235, 240),
            (235, 230, 225),
            (210, 220, 225)
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            __between(pl_rade, 0.8, 2),
            __between(pl_eqt, 300, 600),
            random.random() < 0.6
        ])),
    TexturePool(name="Ice Caps",
        textures=[
            "detail3.png",
        ],
        tones=[
            (235, 245, 255),
            (250, 250, 245),
            (215, 235, 245),
            (225, 230, 225)
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            pl_rade < 2.5,
            pl_eqt < 220,
            random.random() < 0.8
        ])),
    TexturePool(name="Haze",
        textures=[
            "detail4.png",
        ],
        tones=[
            (190, 210, 220),
            (210, 190, 160),
            (220, 205, 180),
            (180, 200, 210),
            (200, 180, 150),
            (210, 210, 195)
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            __between(pl_rade, 1.5, 2),
            pl_eqt > 300,
            random.random() < 0.4
        ])),
    TexturePool(name="Gas Storms",
        textures=[
            "detail5.png",
            "detail6.png",
            "detail7.png",
        ],
        tones=[
            (176, 90, 63),
            (186, 146, 136),
            (254, 179, 121),
            (123, 196, 211),
            (208, 160, 158),
            (102, 139, 121)
        ],
        predicate=lambda pl_rade, pl_eqt: any([
            pl_rade > 7,
            all([
                pl_rade > 2.5,
                pl_eqt > 200,
            ]),
        ])),
]

atmospheres = [
    TexturePool(name="Cold",
        textures=[],
        tones=[
            (70, 150, 255),
            (101, 135, 247),
            (74, 192, 224),
            (92, 224, 187),
            (214, 190, 247)
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            pl_eqt < 250
        ])),
    TexturePool(name="Warm",
        textures=[],
        tones=[
            (190, 212, 247),
            (117, 183, 240),
            (130, 229, 245),
            (232, 245, 130),
            (245, 189, 130),
            (92, 255, 87)
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            __between(pl_eqt, 200, 600)
        ])),
    TexturePool(name="Hot",
        textures=[],
        tones=[
            (247, 62, 62),
            (237, 120, 52),
            (247, 219, 57),
            (247, 129, 186),
            (255, 237, 246)
        ],
        predicate=lambda pl_rade, pl_eqt: all([
            pl_eqt > 500
        ])),
]

def get_base(planet) -> TexturePool:
    options = [item for item in bases if item.test(planet)]
    if len(options) == 0: options = bases
    return random.choice(options)
    
def get_details(planet) -> list[TexturePool]:
    return [item for item in details if item.test(planet)]

def get_atmosphere(planet) -> TexturePool:
    options = [item for item in atmospheres if item.test(planet)]
    if len(options) == 0: options = atmospheres
    return random.choice(options)