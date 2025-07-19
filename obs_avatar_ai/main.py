# main.py
import logging
from pathlib import Path
from core_config import BASE_DIR

# Configure logging *before* any other imports
logging.basicConfig(
    filename=str(BASE_DIR / "error.log"),
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Now import and run the main program
from project_geprot import main

if __name__ == "__main__":
    main()
