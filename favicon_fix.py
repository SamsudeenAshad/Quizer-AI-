@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return empty response with "No Content" status
