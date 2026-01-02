from flask import Flask, render_template, request, redirect, url_for, abort
import os
import secrets

# Explicitly define paths to ensure 'static' and 'templates' are found correctly
base_dir = os.path.abspath(os.path.dirname(__file__))
static_dir = os.path.join(base_dir, 'static')
template_dir = os.path.join(base_dir, 'templates')
paste_dir = os.path.join(base_dir, 'data', 'pastes')

app = Flask(__name__, 
            static_folder=static_dir, 
            template_folder=template_dir)

# Ensure data directory exists
if not os.path.exists(paste_dir):
    os.makedirs(paste_dir)

def save_paste(content, paste_id=None):
    """Saves paste content to a file. Generates a new ID if not provided."""
    if not paste_id:
        paste_id = secrets.token_urlsafe(8)
    file_path = os.path.join(paste_dir, f"{paste_id}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return paste_id

def delete_paste_file(paste_id):
    """Removes a paste file."""
    file_path = os.path.join(paste_dir, f"{paste_id}.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
def get_paste(paste_id):
    file_path = os.path.join(paste_dir, f"{paste_id}.txt")
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def list_pastes():
    """Returns a list of all paste IDs."""
    if not os.path.exists(paste_dir):
        return []
    files = [f for f in os.listdir(paste_dir) if f.endswith('.txt')]
    # Sort by modification time (most recent first)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(paste_dir, x)), reverse=True)
    return [f.replace('.txt', '') for f in files]

@app.route('/')
def index():
    pastes = list_pastes()
    return render_template('index.html', pastes=pastes)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    content = request.form.get('content')
    if not content:
        return redirect(url_for('index'))
    
    paste_id = save_paste(content)
    # Redirect to GET route to avoid form resubmission and 405s
    return redirect(url_for('view_paste', paste_id=paste_id))

@app.route('/view/<paste_id>', methods=['GET'])
def view_paste(paste_id):
    content = get_paste(paste_id)
    if content is None:
        abort(404)
    return render_template('view.html', content=content, paste_id=paste_id)

@app.route('/edit/<paste_id>')
def edit_paste(paste_id):
    content = get_paste(paste_id)
    if content is None:
        abort(404)
    return render_template('edit.html', content=content, paste_id=paste_id)

@app.route('/update/<paste_id>', methods=['POST'])
def update_paste(paste_id):
    content = request.form.get('content')
    if not content:
        return redirect(url_for('edit_paste', paste_id=paste_id))
    
    save_paste(content, paste_id=paste_id)
    return redirect(url_for('view_paste', paste_id=paste_id))

@app.route('/delete/<paste_id>')
def delete_paste(paste_id):
    delete_paste_file(paste_id)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Switching to 5001 to avoid conflicts with phantom processes on 5000
    print(f"Server starting on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)