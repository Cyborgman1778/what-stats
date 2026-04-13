from pathlib import Path
import sys
from pprint import pprint
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
from app.services import whatsapp_chat_parser, data_analyzer
def main():
    chat_path = BACKEND_ROOT / "tests" / "resources" / "chat_sintetico_extenso.txt"
    file_bytes = chat_path.read_bytes()
    df = whatsapp_chat_parser.parse_chat_to_dataframe(file_bytes, chat_path.name)
    print("Columnas:", df.columns.tolist())
    print("Numero de mensajes:", len(df))
    print()
    print(df.head())
    print()
    stats = data_analyzer.analyze_chat_data(df)
    pprint(stats, indent=4, sort_dicts=False)
if __name__ == "__main__":
    main()