import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import zeyrek
import string
import stanza
import pandas as pd
from nltk.corpus import stopwords

# Gerekli NLTK paketlerini indirin
nltk.download('punkt')
nltk.download('stopwords')


def load_excel_file(file_path):
    """
    Excel dosyasını yükleyip, 'Cümle' sütununu döndüren fonksiyon.
    """
    df = pd.read_excel(file_path, engine='openpyxl')
    return df['Cümle'].tolist()  # 'Cümle' sütununu listeye dönüştür


def initialize_analyzers():
    """
    Zeyrek ve Stanza analizörlerini başlatan fonksiyon.
    """
    analyzer = zeyrek.MorphAnalyzer()
    nlp = stanza.Pipeline('tr')
    return analyzer, nlp


def remove_punctuation(text):
    """
    Noktalama işaretlerini kaldıran fonksiyon.
    """
    words = word_tokenize(text)
    words = [word for word in words if word not in string.punctuation]
    return ' '.join(words)


def process_text_with_zeyrek_and_stanza(text, analyzer, nlp):
    """
    Zeyrek ve Stanza analizörleri ile metni işleyen fonksiyon.
    """
    sentences = sent_tokenize(text)  # Metni cümlelere ayır
    processed_sentences = []

    # Türkçe StopWords listesini al
    turkish_stopwords = set(stopwords.words('turkish'))

    for sentence in sentences:
        clean_sentence = remove_punctuation(sentence)  # Noktalama işaretlerini kaldır
        words = word_tokenize(clean_sentence)  # Kelimelere ayır

        # Zeyrek ile kelimeleri köklere indir
        stemmed_words = []
        for word in words:
            word_lower = word.lower()  # Büyük-küçük harf duyarlılığını kaldır
            if word_lower in turkish_stopwords:  # Stopwords listesinde olan kelimeleri atla
                continue
            analysis = analyzer.analyze(word)
            if analysis:
                stem = analysis[0][0].lemma  # Kelimenin kökü
                stemmed_words.append(stem)
            else:
                stemmed_words.append(word)  # Eğer kök bulunamazsa olduğu gibi ekle

        # Stanza ile kelimelerin dilbilgisel görevlerini çözümle
        doc = nlp(' '.join(stemmed_words))  # Stanza ile çözümle

        sentence_info = []
        for word in doc.sentences[0].words:
            sentence_info.append({
                'Kelime': word.text,
                'Kök': word.lemma,
                'Tür': word.pos,
                'Bağımlılık': word.deprel
            })
        
        processed_sentences.append(sentence_info)
    
    return processed_sentences


def display_processed_text(processed_text):
    """
    İşlenmiş metni formatlı şekilde yazdıran fonksiyon.
    """
    print("----------------------------------------------------------------------------------------------------------")
    for i, sentence in enumerate(processed_text):
        print(f"Cümle {i+1}:")
        for word_info in sentence:
            print(f"Kelime: {word_info['Kelime']}, Kök: {word_info['Kök']}, Tür: {word_info['Tür']}, Bağımlılık: {word_info['Bağımlılık']}")
        print("----------------------------------------------------------------------------------------------------------")


def main(file_path):
    """
    Main fonksiyonu, dosyayı yükler, analizörleri başlatır, metni işler ve sonucu yazdırır.
    """
    sentences = load_excel_file(file_path)
    analyzer, nlp = initialize_analyzers()

    # İlk cümleyi işleme
    print("-"*20)
    print(sentences[30])
    print("-"*20)
    
    processed_text = process_text_with_zeyrek_and_stanza(sentences[30], analyzer, nlp)

    # Sonuçları yazdır
    display_processed_text(processed_text)


# Ana fonksiyonu çağır
if __name__ == '__main__':
    file_path = 'ornek.xlsx'  # Dosya yolunu buraya yazın
    main(file_path)
