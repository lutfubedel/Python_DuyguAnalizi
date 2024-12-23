import jpype
import jpype.imports
from jpype.types import JString

# Java ortamını başlat
jpype.startJVM(
    classpath=["zemberek-all.jar"]
)

# Zemberek sınıflarını içe aktar
from zemberek.morphology import TurkishMorphology
from zemberek.morphology.analysis import SentenceAnalysis

# Zemberek'i başlat
morphology = TurkishMorphology.createWithDefaults()

# Cümle örneği
cumle = "Ahmet okula gidiyor."

# Cümleyi analiz et
analysis = morphology.analyzeAndDisambiguate(JString(cumle))

# Her kelimenin analizini yap
print("Cümledeki fiiller (yüklem olabilecekler):")
for word_analysis in analysis.bestAnalysis():
    kelime = word_analysis.getSurfaceForm()
    en_iyi_analiz = word_analysis.getBestAnalysis()

    # Eğer kelime fiilse yazdır
    if en_iyi_analiz.getPos().shortForm == "Fiil":
        print(f"Kelime: {kelime}, Yüklem olma ihtimali yüksek.")

# Java ortamını kapat
jpype.shutdownJVM()
