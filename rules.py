import re


def positive_score_calculate(processed_text, polarity_file):
    score = 0
    positive_words = []  # Pozitif kelimelerin bir listesini oluşturacağız
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines())  # Polarity kelimelerini yükle

    for sentence in processed_text:
        for word_info in sentence:
            word = word_info["Kök"].lower()

            # Eğer kelime polarity kelimeleri arasında yer alıyorsa
            if word in text_words:
                ekler = word_info["Ekler"].split("+")

                # Negatif eki olan veya olumsuzluk durumları varsa bu kelimeyi atla
                if ("Neg" in ekler and ayirt_et(word_info["Kelime"])) or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:
                    continue  # Negatif olduğu için atla, score artırma

                # Eğer kelime pozitifse ve yukarıdaki koşullara girmiyorsa, score'u artır
                print(f"Pozitif Kelime : {word_info['Kelime']}")
                positive_words.append(word_info['POS'])  # Pozitif kelimeyi listeye ekle
                score += 1  # Pozitif kelime bulundu, skoru artır

    return score, positive_words  # Score ve pozitif kelimeler listesini döndür


def negative_score_calculate(processed_text, polarity_file):
    score = 0
    negative_words_with_pos = []  # Negatif kelimeleri ve onların "Pos" değerlerini tutacak liste

    # Polarity kelimelerini yükle
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines())

    for sentence in processed_text:
        for word_info in sentence:
            word = word_info["Kök"].lower()
            ekler = word_info["Ekler"].split("+")
            
            # Negatif kelime kontrolü
            if word in text_words or ("Neg" in ekler and ayirt_et(word_info["Kelime"])) or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:
                print(f"Negatif Kelime: {word_info['Kelime']}")  # Debug amacıyla
                score += 1  # Negatif kelime bulundu, skoru artır
                
                # Negatif kelime bulunduğunda, kelimenin "Pos" değeri olarak bir varsayım yapabiliriz.
                # Örneğin, kelimenin olumlu anlam taşıyan benzer bir kelime olduğunu düşünerek bunu
                # negatif olarak işaretleyebiliriz, ancak burada herhangi bir işlem yapmadık.
                # Bu kısmı, pozitif kelimelerle daha derinlemesine bir analiz için güncelleyebilirsin.
                negative_words_with_pos.append(word_info['POS'])  # Negatif kelimeleri listele

    return score, negative_words_with_pos  # Skor ve negatif kelimelerin listesi


       
def equal_score(processed_text, polarity_file_neg,polarity_file_pos):
    # Negatif ve pozitif skorları ve kelimeleri al
    neg_score, neg_words = negative_score_calculate(processed_text, polarity_file_neg)
    pos_score, pos_words = positive_score_calculate(processed_text, polarity_file_pos)

    # Fiil sayısını hesaplamak için yardımcı fonksiyon
    def count_verbs(words):
        verb_count = 0
        for word_info in words:
            # Kelimenin türü (POS tag) 'Verb' mi diye kontrol et
            if "Verb" in words:  # 'Tür' kısmında 'Verb' olup olmadığını kontrol ediyoruz
                verb_count += 1
        return verb_count

    # Negatif ve pozitif kelimelerdeki fiil sayısını hesapla
    neg_verbs_count = count_verbs(neg_words)
    pos_verbs_count = count_verbs(pos_words)

    # Sonuçları döndür
    if neg_verbs_count <= pos_verbs_count:
        print(f"Negatif ve pozitif kelimelerdeki fiil sayısı eşit: {neg_verbs_count}")
        return True
    else:
        print(f"Negatif kelimelerdeki fiil sayısı: {neg_verbs_count}, Pozitif kelimelerdeki fiil sayısı: {pos_verbs_count}")
        return False

def conjunctions_control(processed_text):
    conjunctions = {'ama', 'fakat', 'oysa', 'hâlbuki',"rağmen"}
    for sentence in processed_text:
        for word_info in sentence:
            if word_info["Kelime"] in conjunctions:
                return True
    return False


def end_with_degil(processed_text):
    if len(processed_text) > 0:
        last_sentence = processed_text[-1]
        if last_sentence[-2]["Kök"] == "değil":
            return True

    return False   


def ironic_punctuation(processed_text):
    # Son üç kelimenin kökleri sırasıyla "(", "!" ve ")" ise, ironik noktalama işareti bulunduğunu bildirir
    if len(processed_text) > 0:
        last_sentence = processed_text[-1]
        if len(last_sentence) >= 3:  
            if last_sentence[-3]["Kök"] == "(" and last_sentence[-2]["Kök"] == "!" and last_sentence[-1]["Kök"] == ")":
                print("İronik Noktalama İşareti Bulundu")
                return True

    return False


def positive_degil_control(processed_text, polarity_file):
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines()) 
    
    for sentence in processed_text:
        for i, word_info in enumerate(sentence):
            word = word_info["Kök"].lower()
            ekler = word_info["Ekler"].split("+")
            if word in text_words: 
                # Check if none of the specified suffixes are present
                if not any(ek in ekler for ek in ["Unable", "Without", "WithoutHavingDoneSo"]) and not ("Neg" in ekler and ayirt_et(word_info["Kelime"])):   
                    # Check the next word if it exists
                    if i + 1 < len(sentence):
                        next_word_info = sentence[i + 1]
                        next_word = next_word_info["Kök"].lower()
                        if next_word == "değil":
                            print(f"Pozitif Kelime ama değil ile : {word_info['Kelime']}")
                            return True
                
    return False

def negative_degil_control(processed_text, polarity_file):
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines()) 
    
    for sentence in processed_text:
        for i, word_info in enumerate(sentence):
            word = word_info["Kök"].lower()
            ekler = word_info["Ekler"].split("+")
            if word in text_words or ("Neg" in ekler and ayirt_et(word_info["Kelime"])) or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:  
                # Check the next word if it exists
                if i + 1 < len(sentence):
                    next_word_info = sentence[i + 1]
                    next_word = next_word_info["Kök"].lower()
                    if next_word == "değil":
                        print(f"Negatif + değil : {word_info['Kelime']}")
                        return True
                
            
                
    return False


def check_before_comma(processed_text, polarity_file):
    # Dosyadaki kelimeleri bir sete yükle
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines())
    
    if len(processed_text) > 0:
        last_sentence = processed_text[-1]
        if len(last_sentence) >= 3:
            # Eğer ikinci veya üçüncü eleman "," ise
            if last_sentence[1]["Kök"] == "," or last_sentence[2]["Kök"] == ",":
                # İlk 1 veya 2 kelimeyi al
                first_two_words = [last_sentence[0]["Kök"]]
                if len(last_sentence) > 1:
                    first_two_words.append(last_sentence[1]["Kök"])
                
                # İlk 1 veya 2 kelimenin dosyada olup olmadığını kontrol et
                for word in first_two_words:
                    if word.lower() in text_words:  # Küçük harfe çevirerek karşılaştır
                        return True
    return False


def ne_ne_control(processed_text):
    ne_count = 0
    for sentence in processed_text:
        for word_info in sentence:
            if word_info["Kelime"] == "ne":
                ne_count += 1
    
    if ne_count == 2:
        return True
    return False



def ayirt_et(kelime):
    """
    Türkçedeki -ma/-me ekini 'isim-fiil' mi yoksa 'olumsuzluk' mu diye ayırt etmeye çalışan geliştirilmiş fonksiyon.
    """
    isim_fiil_musteresi = re.compile(
        r'^(.*?)(ma|me|mı|mi)([yğ][ıiüuae])(?!n).*',  # "ma", "me" + "y[ıiüuae]" ama "yın" hariç
        re.IGNORECASE
    )

    olumsuzluk_musteresi = re.compile(
        r'^(.*?)(ma|me|mı|mi)(?![yğ][ıiüuae]).*',  # Burada "y[ıiüuae]" ekini engelliyoruz
        re.IGNORECASE
    )

    if isim_fiil_musteresi.match(kelime):
        return False

    elif olumsuzluk_musteresi.match(kelime):
        return True

    # 3) HİÇBİRİ UYMADIYSA
    else:
        return False


def check_before_hic(processed_text, polarity_file):
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines())

    for sentence in processed_text:
        for i, word_info in enumerate(sentence):
            word = word_info["Kök"].lower()
            if word in text_words:
                # Check the previous word if it exists
                if i - 1 >= 0:
                    previous_word_info = sentence[i - 1]
                    previous_word = previous_word_info["Kök"].lower()
                    if previous_word == "hiç" or previous_word == "amma":
                        print(f"Pozitif kelimenin öncesinde 'hiç' bulundu: {word_info['Kelime']}")
                        return True

    return False
