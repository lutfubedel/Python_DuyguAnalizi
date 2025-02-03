import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import zeyrek
from nltk.corpus import stopwords
import rules

# Gerekli NLTK paketlerini indirin
#nltk.download("all")
#nltk.download('punkt')
#nltk.download('stopwords')

def process_text_with_zeyrek(text, analyzer):
    """
    Zeyrek analizörü ile metni işleyen fonksiyon. Kelime, kök, ekler ve pos değerlerini döndürür.
    Eğer cümlede 'ama' veya 'fakat' gibi bağlaçlar varsa, o kelimelerden önceki kelimeleri kaldırır.
    """
    sentences = sent_tokenize(text)  # Metni cümlelere ayır
    processed_sentences = []

    # Türkçe StopWords listesini al
    #turkish_stopwords = set(stopwords.words('turkish'))
    
    # Bağlaçlar listesi (ama, fakat gibi)
    conjunctions = {'ama', 'fakat','oysa',"hâlbuki","rağmen"}

    for sentence in sentences:
        words = word_tokenize(sentence)  # Kelimelere ayır

        # Cümledeki bağlaçlardan önceki kelimeleri kaldır
        for conjunction in conjunctions:
            if conjunction in words:
                index = words.index(conjunction)
                words = words[index:]  # Bağlaçtan önceki kelimeleri çıkar

        # Zeyrek ile kelimeleri köklere, eklerine ve POS değerine ayır
        sentence_info = []
        for word in words:
            word_lower = word.lower()  # Büyük-küçük harf duyarlılığını kaldır
            analysis = analyzer.analyze(word_lower)
            if analysis:
                root = analysis[0][0].lemma  # Kelimenin kökü
                suffixes = "+".join(analysis[0][0].morphemes[1:])  # Kelimenin ekleri
                pos = analysis[0][0].pos  # Kelimenin türü (POS)
                sentence_info.append({
                    'Kelime': word,
                    'Kök': root,
                    'Ekler': suffixes if suffixes else 'Yok',
                    'POS': pos
                })
            else:
                sentence_info.append({
                    'Kelime': word,
                    'Kök': word,
                    'Ekler': 'Yok',
                    'POS': 'Bilinmiyor'  # Eğer POS bulunamazsa
                })

        processed_sentences.append(sentence_info)

    return processed_sentences

def analyze_sentence(processed_text):
    # Flagleri başlat
    input_data = {
        "positive_score_gte_negative": False,
        "negative_score_gt_positive": False,
        "positive_degil" : False,
        "negative_degil" : False,
        "ironic_punctuation": False,
        "negative_beforeComma" : False,
        "positive_beforeComma" : False,
        "ne_ne" : False,
        "end_with_degil" : False,
        "conjunctions_word": False,
        "hic_before_pos": False,
        "hic_before_neg": False,

        "go_resolve_tie" : True,
    }
    
    input_data["positive_degil"] = rules.positive_degil_control(processed_text, "polarity_positive.txt")
    input_data["negative_degil"] = rules.negative_degil_control(processed_text, "polarity_negative.txt")

    input_data["negative_beforeComma"] = rules.check_before_comma(processed_text,"polarity_negative.txt")
    input_data["positive_beforeComma"] = rules.check_before_comma(processed_text,"polarity_positive.txt")

    input_data["ironic_punctuation"] = rules.ironic_punctuation(processed_text)
    input_data["ne_ne"] = rules.ne_ne_control(processed_text)

    positive_score, neg_words = rules.positive_score_calculate(processed_text, "polarity_positive.txt")
    negative_score, pos_wordas = rules.negative_score_calculate(processed_text, "polarity_negative.txt")

    input_data["end_with_degil"] = rules.end_with_degil(processed_text)

    input_data["hic_before_pos"] = rules.check_before_hic(processed_text,"polarity_positive.txt")
    input_data["hic_before_neg"] = rules.check_before_hic(processed_text,"polarity_negative.txt")

    if(negative_score == 0 and positive_score == 0):
        input_data["conjunctions_word"] = rules.conjunctions_control(processed_text)

    if(positive_score > negative_score):
        input_data["positive_score_gte_negative"] = True
    
    elif(negative_score > positive_score):
        input_data["negative_score_gt_positive"] = True

    else:
        if(rules.equal_score(processed_text,"polarity_negative.txt","polarity_positive.txt")):
            input_data["positive_score_gte_negative"] = True
        else:
            input_data["negative_score_gt_positive"] = True

    return input_data

def run_fsm(fsm, input_data):
    """
    FSM'i çalıştırır ve bir son duruma ("positive" veya "negative") ulaşana kadar devam eder.
    """
    current_state = "start"

    while current_state not in ["Pozitif", "Negatif"]:

        # Mevcut durumdaki geçişleri al
        transitions = fsm.get(current_state, {})
        transition_found = False

        # Geçiş koşullarını kontrol et ve uygun bir sonraki duruma ilerle
        for condition, next_state in transitions.items():
            if condition in input_data and input_data[condition]:
                current_state = next_state
                transition_found = True
                break
        
        if not transition_found:
            raise ValueError(f"Durum '{current_state}' için geçerli bir geçiş bulunamadı.")
    
    return current_state

def polarity_prediction(sentence):
    """
    Main fonksiyonu, dosyayı yükler, analizörleri başlatır, metni işler ve sonucu yazdırır.
    """
    # Analizörleri başlat
    analyzer = zeyrek.MorphAnalyzer()

    # Metni işle
    processed_text = process_text_with_zeyrek(sentence, analyzer)

    # İşlenmiş metni yazdır
    #display_processed_text(processed_text)

    # FSM tanımı
    fsm = {
        "start": 
        {
            "ironic_punctuation": "Negatif",
            "ne_ne": "Negatif",
            "positive_degil": "Negatif",
            "negative_degil": "Pozitif",
            "negative_beforeComma": "Negatif",
            "positive_beforeComma": "Pozitif",
            "end_with_degil" : "Negatif",
            "conjunctions_word": "Negatif",
            "hic_before_pos": "Negatif",
            "hic_before_neg": "Pozitif",
            "go_resolve_tie": "resolve_tie",
        },
        "resolve_tie": 
        {
            "positive_score_gte_negative": "Pozitif",
            "negative_score_gt_positive": "Negatif",
        },
    } 

    # Girdi verilerini analiz et
    input_data = analyze_sentence(processed_text)

    # FSM çalıştır
    predicted_class = run_fsm(fsm, input_data)
    
    print(f"FSM Tahmini: {predicted_class}")
    return predicted_class



