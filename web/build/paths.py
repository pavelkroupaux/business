# Cesty pro build. Všechno se počítá od umístění této složky (05 Web/repo/build),
# takže build běží stejně v Obsidianu na Macu i v jiném prostředí.
import os
B = os.path.dirname(os.path.abspath(__file__)) + '/'          # 05 Web/repo/build/
R = os.path.abspath(os.path.join(B, '..', '..', '..', '..')) + '/'  # složka, ve které je Career
CAREER = R + 'Career/'
REPO = CAREER + '05 Web/repo/'
FONTDIR = B + 'fonts/'
DRAFT = B + '_draft/'
os.makedirs(DRAFT, exist_ok=True)
