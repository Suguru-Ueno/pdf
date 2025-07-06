import fitz  # PyMuPDF
from fpdf import FPDF
from googletrans import Translator
from pathlib import Path
import sys
from tqdm import tqdm

# 翻訳器初期化
translator = Translator()

class JapanesePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("NotoSans", "", "./fonts/NotoSansJP-Regular.ttf")
        self.set_font("NotoSans", size=12)


# PDFを読み込んでテキスト抽出
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ""
    for page in tqdm(doc, desc="テキスト抽出中"):
        all_text += page.get_text()
    doc.close()
    return all_text

# テキストを日本語に翻訳
# def translate_text(text, src='en', dest='ja'):
#     translated = translator.translate(text, src=src, dest=dest)
#     return translated.text

def translate_text(text, src='en', dest='ja'):
    translated_text = ""
    for paragraph in tqdm(text.split('\n'), desc="翻訳中"):
        if paragraph.strip():
            try:
                translated = translator.translate(paragraph, src=src, dest=dest)
                translated_text += paragraph + "\n"
                translated_text += translated.text + "\n"
                translated_text += "\n"
            except Exception as e:
                print(f"翻訳エラー: {e}")
                translated_text += paragraph + "\n"
                translated_text += "[翻訳失敗]\n"
                translated_text += "\n"
    return translated_text


# # 翻訳結果をPDFとして保存
# def save_translated_text_to_pdf(text, output_path):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=12)
#     for line in text.split('\n'):
#         pdf.multi_cell(0, 10, line)
    pdf.output(output_path)


# 翻訳結果をPDFとして保存
def save_translated_text_to_pdf(text, output_path):
    pdf = JapanesePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    for line in tqdm(text.split('\n'), desc="書き込み中"):
        pdf.multi_cell(0, 10, line)
    
    pdf.output(output_path)


# 実行部分
if __name__ == '__main__':
    FILE_NAME = "Decision_Trees.pdf"  # あなたのPDFファイル名に置き換えてください
    
    INPUT_DIR_PATH = ".\input_pdf\\"
    input_pdf_path = INPUT_DIR_PATH + FILE_NAME

    OUTPUT_DIR_PATH = ".\output_pdf\\"
    output_pdf_path = OUTPUT_DIR_PATH + FILE_NAME

    
    file_path = Path(output_pdf_path)
    if file_path.exists():
        print("翻訳済みファイルが存在するため、処理を中断します。")
        print(f"再度翻訳する場合は、 「{OUTPUT_DIR_PATH}」配下に「{FILE_NAME}」ファイルがない状態にしてください。")
        sys.exit()

    english_text = extract_text_from_pdf(input_pdf_path)
    japanese_text = translate_text(english_text)
    save_translated_text_to_pdf(japanese_text, output_pdf_path)

    print("翻訳と保存が完了しました！")