# marketing_agent.py
# Python microservice for Marketing Agent using Microsoft Agent Framework

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from kit_templates import load_example_kit

app = Flask(__name__)
CORS(app)


@app.route('/agent/marketing-kit', methods=['POST'])
def marketing_kit():
    try:
        # Accept both JSON and form-data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            # Handle files metadata if present
            if 'files' in request.files:
                data['files'] = [
                    {
                        'filename': f.filename,
                        'mimetype': f.mimetype,
                        'size': len(f.read())
                    }
                    for f in request.files.getlist('files')
                ]

        print(f"[DEBUG] Received /agent/marketing-kit request: {json.dumps(data, indent=2)}")
        kit = load_example_kit()
        # Update kit with form fields if present
        if 'clientName' in data:
            kit['client']['brand_name'] = data['clientName']
        if 'website' in data:
            kit['client']['brand_url'] = data['website']
        if 'offering' in data:
            kit['client']['offering'] = data['offering']
        if 'targetMarkets' in data:
            kit['client']['target_markets'] = data['targetMarkets']
        if 'competitors' in data:
            kit['client']['competitors'] = data['competitors']
        if 'additionalDetails' in data:
            kit['client']['additional_details'] = data['additionalDetails']
        if 'files' in data:
            kit['client']['uploaded_files'] = data['files']

        print(f"[DEBUG] Responding with kit: {json.dumps(kit, indent=2)[:1000]}... (truncated)")
        return jsonify(kit)
    except Exception as e:
        print(f"[ERROR] Exception in /agent/marketing-kit: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=7000, debug=True)
