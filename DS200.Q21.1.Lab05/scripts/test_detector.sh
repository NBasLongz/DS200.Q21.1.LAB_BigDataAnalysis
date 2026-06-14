#!/bin/bash
cd /mnt/f/DS200.Q21.1.Lab05
source venv/bin/activate

echo "=== Test 1: import check ===" 
python -c "
import sys
sys.path.insert(0, 'src')
print('Step 1: sys.path ok')
from config import Config
print('Step 2: config ok, MODEL_PATH=', Config.MODEL_PATH)
import logging
logging.basicConfig(level='INFO', format='%(levelname)s %(message)s')
log = logging.getLogger('test')
log.info('Step 3: logging ok')
print('Step 4: trying ultralytics...')
try:
    from ultralytics import YOLO
    print('Step 5: ultralytics ok')
    m = YOLO(Config.MODEL_PATH)
    print('Step 6: YOLO model loaded ok')
except Exception as e:
    print('Step 5 FAIL:', e)
print('Step 7: done')
" 2>&1
echo "=== DONE ==="
