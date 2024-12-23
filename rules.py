def negation_suffix_control(processed_text):
    # Olumsuzluk eklerini kontrol et
    for sentence in processed_text:
        for word_info in sentence:
            ekler = word_info["Ekler"].split("+")
            if word_info["Kök"] != "değil":
                if "Neg" in ekler or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:
                    print(f"Olumsuzluk eki bulundu: {word_info['Kelime']}")
                    return True   
    return False

def double_negation_control(processed_text, polarity_file):
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines()) 
        
    for sentence in processed_text:
        for i, word_info in enumerate(sentence):
            word = word_info["Kök"].lower()
            ekler = word_info["Ekler"].split("+")
            
            # Kontrol edilen kelime negatif mi?
            is_negative = word in text_words or any(ek in ekler for ek in ["Neg", "Unable", "Without", "WithoutHavingDoneSo"])
            
            if is_negative:
                # Bir sonraki kelime var mı ve negatif mi?
                if i + 1 < len(sentence):
                    next_word_info = sentence[i + 1]
                    next_word = next_word_info["Kök"].lower()
                    next_ekler = next_word_info["Ekler"].split("+")
                    
                    is_next_negative = next_word in text_words or any(ek in next_ekler for ek in ["Neg", "Unable", "Without", "WithoutHavingDoneSo"])
                    
                    if is_next_negative:
                        print(f"Çifte Negatif Kelimeler: {word_info['Kelime']} ve {next_word_info['Kelime']}")
                        return True
    
    return False



def positive_polarity_control(processed_text, polarity_file):
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines()) 

    for sentence in processed_text:
        for i, word_info in enumerate(sentence):
            word = word_info["Kök"].lower()
            if word in text_words:
                ekler = word_info["Ekler"].split("+")
                if "Neg" in ekler or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:
                    print(f"Pozitif Kelime ama Olumsuzluk eki : {word_info['Kelime']}")
                    return False
                if i + 1 < len(sentence):
                    next_word_info = sentence[i + 1]
                    next_word = next_word_info["Kök"].lower()
                    if next_word == "değil":
                        print(f"Pozitif Kelime ama değil ile : {word_info['Kelime']}")
                        return False
                
                
                print(word)
                return True 
    return False

def negative_polarity_control(processed_text, polarity_file):
    with open(polarity_file, "r", encoding="utf-8") as file:
        text_words = set(file.read().strip().lower().splitlines()) 

    for sentence in processed_text:
        for word_info in sentence:
            word = word_info["Kök"].lower()
            ekler = word_info["Ekler"].split("+")
            
            if word_info["Kök"] == "değil":
                return True

            # Eğer kelime hem text_words içinde hem de belirtilen eklerden birini içeriyorsa atla
            if word in text_words and any(ek in ekler for ek in ["Neg", "Unable", "Without", "WithoutHavingDoneSo"]):
                continue
            
            # Eğer sadece text_words içinde veya sadece eklerden birini içeriyorsa negatif olarak kabul et
            if word in text_words or any(ek in ekler for ek in ["Neg", "Unable", "Without", "WithoutHavingDoneSo"]):
                print(f"Negative Word : {word_info['Kelime']}")
                return True 
    
    return False




def positive_score_calculate(processed_text, polarity_file):
    score = 0
    if(positive_polarity_control(processed_text, polarity_file)):
        with open(polarity_file, "r", encoding="utf-8") as file:
            text_words = set(file.read().strip().lower().splitlines()) 

        for sentence in processed_text:
            for word_info in sentence:
                word = word_info["Kök"].lower()
                if word in text_words:
                    ekler = word_info["Ekler"].split("+")
                    if word in text_words or "Neg" in ekler or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:
                        print(f"Pozitif Kelime : {word_info['Kelime']}")
                    else:
                        score +=1

                    print(word)

    return score

def negative_score_calculate(processed_text, polarity_file):
    score = 0
    if(negative_polarity_control(processed_text, polarity_file)):
        with open(polarity_file, "r", encoding="utf-8") as file:
            text_words = set(file.read().strip().lower().splitlines()) 

        for sentence in processed_text:
            for word_info in sentence:
                word = word_info["Kök"].lower()
                ekler = word_info["Ekler"].split("+")
                if word in text_words or "Neg" in ekler or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:
                    score +=1
                    print(word)

    return score



def ironic_punctuation(processed_text):
    # Son üç kelimenin kökleri sırasıyla "(", "!" ve ")" ise, ironik noktalama işareti bulunduğunu bildirir
    if len(processed_text) > 0:
        last_sentence = processed_text[-1]
        if last_sentence[-1]["Kök"] == "!" or last_sentence[-1]["Kök"] == "?" :
            print("İronik Noktalama İşareti Bulundu")
            return True
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
                if not any(ek in ekler for ek in ["Neg", "Unable", "Without", "WithoutHavingDoneSo"]):   
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
            if word in text_words or "Neg" in ekler or "Unable" in ekler or "Without" in ekler or "WithoutHavingDoneSo" in ekler:  
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


