from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
_groq_client = None

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client

BASE_URL = 'https://manyadiagonistic.in'

PAGE_DATA = {
    'index': {
        'title': 'Manya Imaging & Diagnostic Point - Best Diagnostic Center in Bilaspur',
        'description': "Bilaspur's trusted diagnostic center offering CT Scan, Digital X-Ray, MRI, Ultrasound and advanced imaging services with NABH-approved quality standards. Book your test today.",
        'keywords': 'diagnostic center Bilaspur, CT scan Bilaspur, X-ray Bilaspur, Manya Imaging, medical imaging Bilaspur, MRI Bilaspur, ultrasound Bilaspur',
        'og_title': 'Manya Imaging & Diagnostic Point - Bilaspur\'s Trusted Diagnostic Center',
        'og_image': f'{BASE_URL}/static/images/manyalogo.png',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}],
        'canonical_url': f'{BASE_URL}/',
        'priority': '1.0',
        'changefreq': 'weekly',
    },
    'about': {
        'title': 'About Us - Manya Imaging & Diagnostic Center Bilaspur | NABH Approved',
        'description': 'Learn about Manya Imaging & Diagnostic Point in Bilaspur. Led by Dr. Kumar Devashish with 20+ years of experience in radiology and diagnostic imaging. NABH approved diagnostic center.',
        'keywords': 'about Manya Imaging, Dr. Kumar Devashish, radiologist Bilaspur, diagnostic center team, NABH approved diagnostic center',
        'og_image': f'{BASE_URL}/static/images/devasish.jpeg',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'About', 'url': '/about'}],
        'canonical_url': f'{BASE_URL}/about',
        'priority': '0.8',
        'changefreq': 'monthly',
    },
    'services': {
        'title': 'Our Services - CT Scan, X-Ray, MRI & Imaging in Bilaspur',
        'description': 'Explore our comprehensive diagnostic services including CT Scan (160 Slice), Digital X-Ray, 1.5 Tesla MRI, Ultrasound, Color Doppler & more at Manya Diagnostic Center, Bilaspur.',
        'keywords': 'CT scan services, digital X-ray, medical imaging Bilaspur, diagnostic tests, MRI scan Bilaspur, ultrasound Bilaspur',
        'og_image': f'{BASE_URL}/static/images/equipment1.jpeg',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Services', 'url': '/services'}],
        'canonical_url': f'{BASE_URL}/services',
        'priority': '0.9',
        'changefreq': 'weekly',
    },
    'ct_scan': {
        'title': 'CT Scan in Bilaspur - 160 Slice Advanced CT Scan | Manya Imaging',
        'description': 'Advanced 160 Slice CT Scan at Manya Imaging in Bilaspur. Cardiac CT Angiography, head, chest, abdomen CT. NABH approved diagnostic center. Book your CT scan appointment today.',
        'keywords': 'CT scan Bilaspur, 160 slice CT scan, cardiac CT angiography Bilaspur, CT scan cost Bilaspur, Manya Imaging CT scan',
        'og_title': 'CT Scan - 160 Slice Advanced Cardiac CT | Manya Imaging Bilaspur',
        'og_image': f'{BASE_URL}/static/images/equipment1.jpeg',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Services', 'url': '/services'}, {'name': 'CT Scan', 'url': '/ct-scan'}],
        'canonical_url': f'{BASE_URL}/ct-scan',
        'priority': '0.9',
        'changefreq': 'monthly',
    },
    'digital_xray': {
        'title': 'Digital X-Ray in Bilaspur - Full Room DR | Manya Imaging',
        'description': 'Digital X-Ray services at Manya Imaging in Bilaspur. Full Room DR with Image Stitching. Chest X-Ray, bone imaging, and special procedures. NABH approved diagnostic center.',
        'keywords': 'digital X-ray Bilaspur, X-ray center Bilaspur, digital radiography, Manya Imaging X-ray, bone X-ray Bilaspur',
        'og_title': 'Digital X-Ray - Full Room DR with Image Stitching | Manya Imaging Bilaspur',
        'og_image': f'{BASE_URL}/static/images/equipment3.jpeg',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Services', 'url': '/services'}, {'name': 'Digital X-Ray', 'url': '/digital-xray'}],
        'canonical_url': f'{BASE_URL}/digital-xray',
        'priority': '0.9',
        'changefreq': 'monthly',
    },
    'mri': {
        'title': 'MRI Scan in Bilaspur - 1.5 Tesla Siemens MRI | Manya Imaging',
        'description': '1.5 Tesla Siemens Sempra MRI Scan at Manya Imaging in Bilaspur. Brain, spine, joint, abdominal, cardiac MRI. NABH approved diagnostic center. Book your MRI appointment.',
        'keywords': 'MRI scan Bilaspur, 1.5 Tesla MRI, Siemens Sempra MRI, brain MRI Bilaspur, spine MRI, Manya Imaging MRI',
        'og_title': 'MRI Scan - 1.5 Tesla Siemens Sempra | Manya Imaging Bilaspur',
        'og_image': f'{BASE_URL}/static/images/equipment6.jpg',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Services', 'url': '/services'}, {'name': 'MRI Scan', 'url': '/mri'}],
        'canonical_url': f'{BASE_URL}/mri',
        'priority': '0.9',
        'changefreq': 'monthly',
    },
    'ultrasound': {
        'title': 'Ultrasound in Bilaspur - 3D/4D USG & Color Doppler | Manya Imaging',
        'description': 'Advanced Ultrasound services at Manya Imaging in Bilaspur. Hitachi Arietta S60, 3D/4D imaging, Color Doppler, pregnancy scans. NABH approved diagnostic center.',
        'keywords': 'ultrasound Bilaspur, USG Bilaspur, 3D ultrasound, Color Doppler Bilaspur, pregnancy scan Bilaspur, Manya Imaging ultrasound',
        'og_title': 'Ultrasound & Color Doppler - Hitachi Arietta S60 | Manya Imaging Bilaspur',
        'og_image': f'{BASE_URL}/static/images/equipment5.jpeg',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Services', 'url': '/services'}, {'name': 'Ultrasound', 'url': '/ultrasound'}],
        'canonical_url': f'{BASE_URL}/ultrasound',
        'priority': '0.9',
        'changefreq': 'monthly',
    },
    'gallery': {
        'title': 'Photo Gallery - Manya Imaging & Diagnostic Center Bilaspur',
        'description': 'Take a virtual tour of Manya Imaging & Diagnostic Point. View our state-of-the-art facilities, equipment, and patient care environment in Bilaspur.',
        'keywords': 'diagnostic center gallery Bilaspur, medical facility photos, imaging center tour, Manya Imaging facilities',
        'og_image': f'{BASE_URL}/static/images/reception.jpeg',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Gallery', 'url': '/gallery'}],
        'canonical_url': f'{BASE_URL}/gallery',
        'priority': '0.6',
        'changefreq': 'monthly',
    },
    'contact': {
        'title': 'Contact Us - Manya Imaging & Diagnostic Center Bilaspur | 07752 403073',
        'description': 'Visit Manya Imaging & Diagnostic Point at R.K Plaza, Link Road, Bilaspur. Call 07752 403073 or 91310 53337. Open 24x7. NABH approved diagnostic center.',
        'keywords': 'contact diagnostic center Bilaspur, Manya Imaging address, diagnostic center phone number, Bilaspur diagnostic center location',
        'og_image': f'{BASE_URL}/static/images/manyalogo.png',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Contact', 'url': '/contact'}],
        'canonical_url': f'{BASE_URL}/contact',
        'priority': '0.7',
        'changefreq': 'monthly',
    },
    'book_test': {
        'title': 'Book a Test - Manya Imaging & Diagnostic Center Bilaspur',
        'description': 'Schedule your diagnostic tests online at Manya Imaging & Diagnostic Point in Bilaspur. Quick appointment booking for CT Scan, MRI, X-Ray, Ultrasound and more.',
        'keywords': 'book diagnostic test Bilaspur, schedule CT scan, appointment Manya Imaging, book MRI Bilaspur, online test booking',
        'og_image': f'{BASE_URL}/static/images/manyalogo.png',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'Book a Test', 'url': '/book-test'}],
        'canonical_url': f'{BASE_URL}/book-test',
        'priority': '0.8',
        'changefreq': 'monthly',
    },
    'chatbot': {
        'title': 'AI Chat Assistant - Manya Imaging & Diagnostic Center Bilaspur',
        'description': 'Chat with our AI assistant to get quick answers about diagnostic services, appointments, and healthcare information at Manya Diagnostic Center in Bilaspur.',
        'keywords': 'AI chatbot diagnostic center, healthcare assistant, Manya Imaging chat, Bilaspur diagnostic chat',
        'og_image': f'{BASE_URL}/static/images/manyalogo.png',
        'breadcrumbs': [{'name': 'Home', 'url': '/'}, {'name': 'AI Chat', 'url': '/chatbot'}],
        'canonical_url': f'{BASE_URL}/chatbot',
        'priority': '0.4',
        'changefreq': 'monthly',
    },
}

ENDPOINT_NAMES = {
    'index': 'Home',
    'about': 'About Us',
    'services': 'Our Services',
    'ct_scan': 'CT Scan',
    'digital_xray': 'Digital X-Ray',
    'mri': 'MRI Scan',
    'ultrasound': 'Ultrasound',
    'gallery': 'Gallery',
    'contact': 'Contact Us',
    'book_test': 'Book a Test',
    'chatbot': 'AI Chat Assistant',
}

@app.context_processor
def inject_globals():
    endpoint = request.endpoint
    data = PAGE_DATA.get(endpoint, PAGE_DATA['index'])
    return dict(page_data=data, endpoint_name=ENDPOINT_NAMES.get(endpoint, ''), base_url=BASE_URL)

# --- Page Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/ct-scan')
def ct_scan():
    return render_template('ct-scan.html')

@app.route('/digital-xray')
def digital_xray():
    return render_template('digital-xray.html')

@app.route('/mri')
def mri():
    return render_template('mri.html')

@app.route('/ultrasound')
def ultrasound():
    return render_template('ultrasound.html')

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

# --- SEO Routes ---

@app.route('/sitemap.xml')
def sitemap():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('sitemap.xml', pages=PAGE_DATA, today=today, base_url=BASE_URL), 200, {'Content-Type': 'application/xml'}

@app.route('/robots.txt')
def robots():
    return render_template('robots.txt', base_url=BASE_URL), 200, {'Content-Type': 'text/plain'}

# --- API Routes ---

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        groq_client = get_groq_client()
        completion = groq_client.chat.completions.create(
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
