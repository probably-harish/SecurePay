from geopy.distance import vincenty

def calculate_distance(location1, location2):
    # Calculate distance using Vincenty formulae
    # try using other methods for variable accuracies... 
    # for our usecase, we are trying to achieve sub 10 meter accuraties 

    return vincenty(location1, location2).meters / 1000.0  

def find_users_in_vicinity(new_location, users, threshold_distance):
    nearby_users = []

    for user in users:
        for qrcode in user["qrcodes"]:
            qrcode_location = qrcode["location"]

            distance = calculate_distance(
                (new_location["latitude"], new_location["longitude"], new_location.get("altitude", 0)),
                (qrcode_location["latitude"], qrcode_location["longitude"], qrcode_location.get("altitude", 0))
            )

            if distance <= threshold_distance:
                nearby_users.append({
                    "user_id": user.get("user_id", "Unknown"),
                    "distance": distance,
                })
                break 

    return nearby_users
