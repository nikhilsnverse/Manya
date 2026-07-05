from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# SEO page data
PAGE_DATA = {
    'index': {
        'title': 'Manya Imaging & Diagnostic Point - Best Diagnostic Center in Bilaspur',
        'description': 'Bilaspur\'s trusted diagnostic center offering CT Scan, Digital X-Ray, and advanced imaging services with NABH-approved quality standards. Book your test today.',
        'keywords': 'diagnostic center Bilaspur, CT scan Bilaspur, X-ray Bilaspur, Manya Imaging, medical imaging Bilaspur',
        'og_title': 'Manya Imaging & Diagnostic Point - Bilaspur\'s Trusted Diagnostic Center',
    },
    'about': {
        'title': 'About Us - Manya Imaging & Diagnostic Center Bilaspur',
        'description': 'Learn about Manya Imaging & Diagnostic Point in Bilaspur. Led by Dr. Kumar Devashish with 20+ years of experience in radiology and diagnostic imaging.',
        'keywords': 'about Manya Imaging, Dr. Kumar Devashish, radiologist Bilaspur, diagnostic center team',
    },
    'services': {
        'title': 'Our Services - CT Scan, X-Ray & Imaging in Bilaspur',
        'description': 'Explore our comprehensive diagnostic services including CT Scan, Digital X-Ray, and advanced medical imaging at Manya Diagnostic Center, Bilaspur.',
        'keywords': 'CT scan services, digital X-ray, medical imaging Bilaspur, diagnostic tests',
    },
    'gallery': {
        'title': 'Gallery - Manya Imaging & Diagnostic Center Bilaspur',
        'description': 'Take a virtual tour of Manya Imaging & Diagnostic Point. View our state-of-the-art facilities, equipment, and patient care environment in Bilaspur.',
        'keywords': 'diagnostic center gallery Bilaspur, medical facility photos, imaging center tour',
    },
    'contact': {
        'title': 'Contact Us - Manya Imaging & Diagnostic Center Bilaspur',
        'description': 'Visit Manya Imaging & Diagnostic Point at R.K Plaza, Link Road, Bilaspur. Call 07752 403073 or 91310 53337 to book an appointment.',
        'keywords': 'contact diagnostic center Bilaspur, Manya Imaging address, diagnostic center phone number',
    },
    'book-test': {
        'title': 'Book a Test - Manya Imaging & Diagnostic Center Bilaspur',
        'description': 'Schedule your diagnostic tests online at Manya Imaging & Diagnostic Point in Bilaspur. Quick appointment booking for CT Scan, X-Ray and more.',
        'keywords': 'book diagnostic test Bilaspur, schedule CT scan, appointment Manya Imaging',
    },
    'chatbot': {
        'title': 'AI Chat Assistant - Manya Imaging & Diagnostic Center',
        'description': 'Chat with our AI assistant to get quick answers about diagnostic services, appointments, and healthcare information at Manya Diagnostic Center.',
        'keywords': 'AI chatbot diagnostic center, healthcare assistant, Manya Imaging chat',
    },
}

@app.context_processor
def inject_seo_data():
    endpoint = request.endpoint
    data = PAGE_DATA.get(endpoint, PAGE_DATA['index'])
    return dict(page_data=data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/book-test')
def book_test():
    return render_template('book-test.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chatbot')
def chatbot():
    return render_template('test_chat.html')

@app.route('/test')
def test():
    return render_template('test_chat.html')

@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap.xml'), 200, {'Content-Type': 'application/xml'}

@app.route('/robots.txt')
def robots():
    return render_template('robots.txt'), 200, {'Content-Type': 'text/plain'}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for Manya Diagnostic Center. Provide helpful, concise responses about medical services, appointments, and general healthcare information."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        
        response = completion.choices[0].message.content
        
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to generate response'}), 500

if __name__ == '__main__':
    app.run(debug=True)
