def format_response(type, content=None, columns=None, rows=None, labels=None,data=None):
    if type == "text":
        return {"type": "text", "content": content}
    elif type == "table":
        return {"type": "table", "columns": columns, "rows": rows}
    elif type == "chart":
        return {"type": "chart", "labels": labels, "data": data}
    else:
        return { "type": "text", "content": "⚠️ Unknown response format." }
