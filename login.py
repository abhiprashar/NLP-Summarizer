import spacy
import string
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
import string
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS
import http.server
import cgi

text = """Samsung recently cancelled its in-person MWC 2021 event, instead, committing to an online-only format. The South Korean tech giant recently made it official, setting a time and date for the Samsung Galaxy MWC Virtual Event.

The event will be held on June 28 at 17:15 UTC(22:45 IST) and will be live-streamed on YouTube. In its release, Samsung says that it will introduce its "ever-expanding Galaxy device ecosystem". Samsung also plans to present the latest technology and innovation efforts in relation to the growing importance of smart device security.

Samsung will also showcase its vision for the future of smartwatches to provide new experiences for users and new opportunities for developers. Samsung also shared and image for the event with silhouettes of a smartwatch, a smartphone, a tablet and a laptop."""
# Text summarization function
def summarize_text(raw_text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(raw_text)

    # ... (include the rest of your text summarization code here)
    # Your code to process the doc and generate the summary goes here

    word_frequency = {}
    for word in doc:
        if word.text.lower() not in STOP_WORDS and word.text.lower() not in string.punctuation:
            if word.text not in word_frequency.keys():
                word_frequency[word.text] = 1
            else:
                word_frequency[word.text] += 1

    max_freq = max(word_frequency.values())

    for word in word_frequency.keys():
        word_frequency[word] = word_frequency[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_frequency.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_frequency[word.text]
                else:
                    sent_scores[sent] += word_frequency[word.text]

    select_len = int(len(sent_tokens) * 0.25)

    summary = nlargest(select_len, sent_scores, key=sent_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary

class FileUploadHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_type, _ = cgi.parse_header(self.headers['content-type'])
        if content_type == 'multipart/form-data':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            uploaded_file = form['file']
            if not uploaded_file:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "No file uploaded"}')
                return

            try:
                raw_text = uploaded_file.file.read().decode('utf-8')
                summary = summarize_text(raw_text)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(f'{{"summary": "{summary}"}}'.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid request"}')

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')

    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, FileUploadHandler)
    print('Server running on http://localhost:8000/')
    httpd.serve_forever()

