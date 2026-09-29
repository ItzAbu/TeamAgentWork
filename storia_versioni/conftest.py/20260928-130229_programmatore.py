"""Configurazione pytest: assicura che 'src' sia nel path per gli import."""
import sys
from pathlib import Path

# Aggiungi la directory 'src' al path di Python
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
