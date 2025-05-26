import requests

def create_google_doc(access_token: str, content: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Step 1: Create the blank doc
    doc_meta = {"title": "Generated SOP"}
    doc_res = requests.post("https://docs.googleapis.com/v1/documents", headers=headers, json=doc_meta)
    doc_id = doc_res.json().get("documentId")

    # Step 2: Insert the content
    update = {
        "requests": [
            {
                "insertText": {
                    "location": {"index": 1},
                    "text": content
                }
            }
        ]
    }

    requests.post(f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate", headers=headers, json=update)
    return doc_id
