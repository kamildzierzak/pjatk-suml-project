import os

# Main routes
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "ml", "data")
CONSTELLATIONS_DIR = os.path.join(BASE_DIR, "ml", "data", "constellations")
MODELS_DIR = os.path.join(BASE_DIR, "ml", "models")
SCRIPTS_DIR = os.path.join(BASE_DIR, "ml", "scripts")

# Data and processing parameters
IMG_SIZE = 96
BATCH_SIZE = 4
VALIDATION_SPLIT = 0.2

# Model training parameters
EPOCHS = 8
EPOCHS_FINE_TUNE = 8
LEARNING_RATE = 0.0001
FINE_TUNE_LR = 0.00001

# Data augmentation configuration
AUGMENATION_CONFIG = {
    "horizontal_flip": True,
    "rotation_range": 5,
    "zoom_range": 0.2,
    "brightness_range": [0.9, 1.1],
    # "width_shift_range": 0.1,
    # "height_shift_range": 0.1,
    # "shear_range": 0.2,
}

# Model backbone
BACKBONES = {
    "resnet": {
        "model": "tensorflow.keras.applications.ResNet50",
        "preprocess": "tensorflow.keras.applications.resnet50.preprocess_input",
    },
    "mobilenet": {
        "model": "tensorflow.keras.applications.MobileNetV2",
        "preprocess": "tensorflow.keras.applications.mobilenet_v2.preprocess_input",
    },
    "efficientnet": {
        "model": "tensorflow.keras.applications.EfficientNetB0",
        "preprocess": "tensorflow.keras.applications.efficientnet.preprocess_input",
    },
}

DEFAULT_BACKBONE = "mobilenet"

# Lista konstelacji: łacińska nazwa, skrót łaciński, polska nazwa
# https://teleskopy.pl/gwiazdozbiory.html
constellations = [
    ("Andromeda", "And", "Andromeda"),
    ("Antlia", "Ant", "Pompa (Wodna)"),
    ("Apus", "Aps", "Rajski Ptak"),
    ("Aquarius", "Aqr", "Wodnik"),
    ("Aquila", "Aql", "Orzeł"),
    ("Ara", "Ara", "Ołtarz"),
    ("Aries", "Ari", "Baran"),
    ("Auriga", "Aur", "Woźnica"),
    ("Bootes", "Boo", "Wolarz"),
    ("Caelum", "Cae", "Rylec"),
    ("Camelopardalis", "Cam", "Żyrafa"),
    ("Cancer", "Cnc", "Rak"),
    ("Canes Venatici", "CVn", "Psy Gończe"),
    ("Canis Maior", "CMa", "Wielki Pies"),
    ("Canis Minor", "CMi", "Mały Pies"),
    ("Capricornus", "Cap", "Koziorożec"),
    ("Carina", "Car", "Kil"),
    ("Cassiopeia", "Cas", "Kasjopea"),
    ("Centaurus", "Cen", "Centaur"),
    ("Cepheus", "Cep", "Cefeusz"),
    ("Cetus", "Cet", "Wieloryb"),
    ("Chamaeleon", "Cha", "Kameleon"),
    ("Circinus", "Cir", "Cyrkiel"),
    ("Columba", "Col", "Gołąb"),
    ("Coma Berenices", "Com", "Warkocz Bereniki"),
    ("Corona Australis", "CrA", "Korona Południowa"),
    ("Corona Borealis", "CrB", "Korona Północna"),
    ("Corvus", "Crv", "Kruk"),
    ("Crater", "Crt", "Puchar"),
    ("Crux", "Cru", "Krzyż (Południa)"),
    ("Cygnus", "Cyg", "Łabędź"),
    ("Delphinus", "Del", "Delfin"),
    ("Dorado", "Dor", "Złota Ryba"),
    ("Draco", "Dra", "Smok"),
    ("Equuleus", "Equ", "Źrebię (Mały Koń)"),
    ("Eridanus", "Eri", "Erydan"),
    ("Fornax", "For", "Piec"),
    ("Gemini", "Gem", "Bliźnięta"),
    ("Grus", "Gru", "Żuraw"),
    ("Hercules", "Her", "Herkules"),
    ("Horologium", "Hor", "Zegar"),
    ("Hydra", "Hya", "Hydra"),
    ("Hydrus", "Hyi", "Wąż Wodny"),
    ("Indus", "Ind", "Indianin"),
    ("Lacerta", "Lac", "Jaszczurka"),
    ("Leo", "Leo", "Lew"),
    ("Leo Minor", "LMi", "Mały Lew"),
    ("Lepus", "Lep", "Zając"),
    ("Libra", "Lib", "Waga"),
    ("Lupus", "Lup", "Wilk"),
    ("Lynx", "Lyn", "Ryś"),
    ("Lyra", "Lyr", "Lutnia (Lira)"),
    ("Mensa", "Men", "Góra Stołowa"),
    ("Microscopium", "Mic", "Mikroskop"),
    ("Monoceros", "Mon", "Jednorożec"),
    ("Musca", "Mus", "Mucha"),
    ("Norma", "Nor", "Węgielnica"),
    ("Octans", "Oct", "Oktant"),
    ("Ophiuchus", "Oph", "Wężownik"),
    ("Orion", "Ori", "Orion"),
    ("Pavo", "Pav", "Paw"),
    ("Pegasus", "Peg", "Pegaz"),
    ("Perseus", "Per", "Perseusz"),
    ("Phoenix", "Phe", "Feniks"),
    ("Pictor", "Pic", "Malarz"),
    ("Pisces", "Psc", "Ryby"),
    ("Piscis Austrinus", "PsA", "Ryba Południowa"),
    ("Puppis", "Pup", "Rufa"),
    ("Pyxis", "Pyx", "Kompas (Okrętowy)"),
    ("Reticulum", "Ret", "Sieć (Siatka)"),
    ("Sagitta", "Sge", "Strzała"),
    ("Sagittarius", "Sgr", "Strzelec"),
    ("Scorpius", "Sco", "Skorpion"),
    ("Sculptor", "Scl", "Rzeźbiarz"),
    ("Scutum", "Sct", "Tarcza Sobieskiego"),
    ("Serpens", "Ser", "Wąż"),
    ("Sextans", "Sex", "Sekstant"),
    ("Taurus", "Tau", "Byk"),
    ("Telescopium", "Tel", "Luneta"),
    ("Triangulum", "Tri", "Trójkąt"),
    ("Triangulum Australe", "TrA", "Trójkąt Południowy"),
    ("Tucana", "Tuc", "Tukan"),
    ("Ursa Maior", "UMa", "Wielka Niedźwiedzica"),
    ("Ursa Minor", "UMi", "Mała Niedźwiedzica"),
    ("Vela", "Vel", "Żagiel"),
    ("Virgo", "Vir", "Panna"),
    ("Volans", "Vol", "Ryba Latająca"),
    ("Vulpecula", "Vul", "Lis (Lisek)"),
]

CLASS_NAMES = [constellation[0] for constellation in constellations]
