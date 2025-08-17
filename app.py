from flask import Flask, render_template, request
import wikipedia

app = Flask(__name__)

# You can change the language here if you want, e.g., 'am' for Amharic
wikipedia.set_lang("en")

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    search_term = None
    if request.method == 'POST':
        search_term = request.form.get('query')
        if search_term:
            try:
                # Search Wikipedia for the term
                # .summary() gets the first paragraph
                summary = wikipedia.summary(search_term, sentences=2)
            except wikipedia.exceptions.PageError:
                summary = "ስለዚህ ጉዳይ መረጃ ማግኘት አልተቻለም።"
            except wikipedia.exceptions.DisambiguationError as e:
                summary = f"በርካታ ተመሳሳይ ቃላት ተገኝተዋል። እባክዎ ጥያቄዎን ያብራሩ። {e.options}"
            except Exception as e:
                summary = f"ስህተት ተፈጥሯል: {e}"
        else:
            summary = "እባክዎ የሚፈልጉትን ቃል ይጻፉ።"
            
    return render_template('index.html', summary=summary, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
