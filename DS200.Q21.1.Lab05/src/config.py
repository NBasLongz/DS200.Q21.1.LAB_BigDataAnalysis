import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    HOST            = "localhost"
    RECEIVER_PORT   = 6100
    DETECTOR_PORT   = 6200
    STORAGE_PORT    = 6300
    RECV_BYTES      = 65536

    MODEL_PATH  = os.path.join(PROJECT_ROOT, "models", "yolo", "yolo12n.pt")
    CONFIDENCE  = 0.30
    PERSON_CLS  = 0

    SPARK_MASTER  = "local[*]"
    SPARK_APP     = "DS200_PersonCounter"
    SPARK_BATCH_S = 1

    OUTPUT_DIR   = os.path.join(PROJECT_ROOT, "output")
    RESULTS_FILE = os.path.join(OUTPUT_DIR, "detections.json")

    LOG_LEVEL = "INFO"
    LOG_FMT   = "%(asctime)s [%(name)-14s] %(levelname)-8s %(message)s"


os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
