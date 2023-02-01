import re
import string
from pathlib import Path

from num2words import num2words
from PyPDF2 import PdfReader

class TextPreprocessor():
    def __init__(self, pdf_directory_location):
        self.location = pdf_directory_location
        self.bold_font_regex_pattern = 'Bold'
        self.refer_slide_regex_pattern = '\(Refer Slide Time:[\d: ]*\)'
        self.tmp_data = []

    def _visitor_text_fn(self, text, transformation, text_matrix, font_dict, font_size):
        text = re.sub("\n", "", text).strip()
        if((not font_dict) and (not text)):
            return 
        font_name = font_dict['/BaseFont']
        if(re.search(self.bold_font_regex_pattern, font_name)):
            return 
        if(re.search(self.refer_slide_regex_pattern, text)):
            return
        # print(text)
        self.tmp_data.append(text)
    
    def _remove_punctuations(self):
        punctuations = string.punctuation + "’"
        translation_table = {ord(i): None for i in punctuations}
        cleaned_data = [x.translate(translation_table) for x in self.tmp_data]
        cleaned_data = [x.lower() for x in cleaned_data]
        return cleaned_data

    def _repl_fn(self, match_obj):
        num_to_word = num2words(match_obj.group(0), lang="en")
        num_to_word = num_to_word.replace(",", "")
        num_to_word = num_to_word.replace("-", " ")
        return num_to_word

    def _convert_num_to_word(self):
        num_to_word_converter = lambda x : re.sub(r"\d+", self._repl_fn, x)
        data = [num_to_word_converter(x) for x in self.tmp_data] 
        return data
    
    def _create_txt_files(self, file):
        file_path = Path(file)
        txt_file_name = file_path.parent / f"{file_path.stem}.txt"
        with open(txt_file_name, 'w') as txt_fp:
            txt_fp.write(" ".join(self.tmp_data))
        file_path.unlink(missing_ok=True)


    def execute(self):
        for file in Path(self.location).iterdir():
            if(file.suffix != ".pdf"):
                continue
            self.tmp_data = []
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page.extract_text(visitor_text=self._visitor_text_fn)
                self.tmp_data = self._remove_punctuations()
                self.tmp_data = self._convert_num_to_word()
            self._create_txt_files(file)

if __name__=='__main__':
    text_preprocessor = TextPreprocessor('Data/Transcripts')
    text_preprocessor.execute()