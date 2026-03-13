from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Giả lập Database
locations_db = [
    {"id": 1, "name": "Hồ Gươm", "city": "Hà Nội"},
    {"id": 2, "name": "Phố Cổ", "city": "Hà Nội"}
]


@app.route('/api/v1/locations', methods=['GET'])
def get_locations_v1():
    return jsonify({
        "data": locations_db,
        "metadata": {
            "total": len(locations_db),
            "version": "1.0"
        }
    })


@app.route('/api/v1.1/locations', methods=['GET'])
def get_locations_v1_1():
    enriched_data = []
    for loc in locations_db:
        # Thêm dữ liệu mới vào mà không xóa dữ liệu cũ
        new_loc = loc.copy()
        new_loc["rating"] = 4.8
        new_loc["description"] = "Điểm đến hấp dẫn"
        enriched_data.append(new_loc)

    return jsonify({
        "data": enriched_data,
        "metadata": {
            "total": len(enriched_data),
            "next_page": "/api/v1.1/locations?page=2", # Bổ sung dễ dàng
            "version": "1.1"
        }
    })


@app.route('/api/v2/locations', methods=['GET'])
def get_locations_v2():
    v2_data = []
    for loc in locations_db:
        v2_data.append({
            "id": loc["id"],
            "location_name": loc["name"], # Đổi tên trường (Breaking Change)
            "city_code": "HN" if loc["city"] == "Hà Nội" else "OTH"
        })

    response = make_response(jsonify({
        "data": v2_data,
        "pagination": { # Đổi tên key từ metadata -> pagination
            "current_page": 1,
            "total_items": len(v2_data)
        }
    }))
    
    # Gửi Header để thông báo lộ trình gỡ bỏ bản cũ (Sunset)
    response.headers['X-API-Version'] = 'v2'
    response.headers['X-API-Sunset'] = '2027-01-01'
    return response

if __name__ == '__main__':
    print("(Flask) đang chạy...")
    app.run(debug=True, port=5000)