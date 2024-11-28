
from passlib.context import CryptContext
import os
from dotenv import load_dotenv


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


load_dotenv()

def get_env(key: str, default=None):
    return os.getenv(key, default)


load_dotenv()

def get_env(key: str, default=None):
    return os.getenv(key, default)

def verify_string(s: str) -> str:
    res = s.replace(' ', '')
    return res.lower()

def dataraw() -> list:
    return [
        "Jênhv six phênhv sênhz xinh môngl tư ntux txưs",
        "Phuôz jur hangr ntux zuôr yangr. Phuôz jur trôngz  ntux zuôr nao",
        "Jăngx  vix hnuz  hnuz greiv, ntux xangr peiv. Jăngx vêx hnuz dangr, ntux xangr yangr",
        "Yangr nzur tsi thơưv hnuz",
        "Keiz pư nzur ntux  zar yangr, Keiz pư lis ntux zar lul năngs",
        "Puv ntux njuôz zuôr yangr, Puv ntux phuôz đuz  zuôrlul năngs",
        "Hnuz kuz tuôz ntux yangr, Hzuz kuz siz ntux năngs",
        "Langx uôz đăng đêx ntux tsênhv kruôr, Tuô zuôs đăng đêx ntux lul năngs",
        "Kâuv ntux tsâuk, kangz ntux laz, Ndu chiv đhâu pêz hnuz lê mangv môngl",
        "Câul maol lir zang zux zinhl khênhr  fôngv chuô đăngx chuô đuz",
        "Yangz cuz đrơưv txussu, năngx Ntux tsâuk seis",
        "Bâux ndêz zang, ntux tsao cuô",
        "Zangx kơưk zang môngl taox saz ntux yaz txus, Zangx kơưk zang grêl qơư kêl cheix nao tuôx",
        "Hlang đêx njuôl đêx, Txangr qơưlơưrqơư",
        "Trâur tơưl txơưv nqu pang",
        "Pêl hâur đêx đru, tul đêx cxax đru",
        "Đêx muôx txuôk, Nênhs muôx nduôk",
        "Chênhz zênhv uô kôngz lông",
        "Kôngz jông viv qir, Tuôz nênhs jông viv buôk",
        "Greix kangz cxang, Txir kangz flâuz",
        "Pux saz chôngz uôtsi tâu hnangr, Zơưs saz chôngz uô tsi tâu naox",
        "Đêx hluz jông đaor changr, Vêr ndâul chôngz jông uô hnangr",
        "Uô kôngz trơưk six hơưv, Uô luôv njuôl luôv grei",
        "Yangr đangr jông ntâu tâuv, Qơư đangr jông uô naox",
        "Nôngz tơưs câul nyei ntux kruôr, Tinhx kôngz sar nyei ntux năngs",
        "Kôngz tsi jông zaos chiv, Trôngl tsi jông tangl iz siv",
    ]