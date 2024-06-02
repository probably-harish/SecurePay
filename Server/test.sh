# display the users
curl localhost:7070/users | jq

# register users
curl -X POST -H "Content-type: application/json" -d '{"username":"harishthefirst", "password": "adithyan0914", "type" : "merchant"}' localhost:7070/signup
curl -X POST -H "Content-type: application/json" -d '{"username":"harishthesecond", "password": "adithyan0914", "type" : "merchant"}' localhost:7070/signup
curl -X POST -H "Content-type: application/json" -d '{"username":"harishthethird", "password": "adithyan0914", "type": "merchant"}' localhost:7070/signup

# generate qr codes for each user
curl -X POST -H "Content-Type: application/json" -d '{
    "username": "harishthefirst",
    "password": "adithyan0914",
    "current_location": {"latitude": 100, "longitude": 50}
}' http://localhost:7070/generate_qr

curl -X POST -H "Content-Type: application/json" -d '{
    "username": "harishthesecond",
    "password": "adithyan0914",
    "current_location": {"latitude": 10, "longitude": 50}
}' http://localhost:7070/generate_qr

curl -X POST -H "Content-Type: application/json" -d '{
    "username": "harishthethird",
    "password": "adithyan0914",
    "current_location": {"latitude": 10, "longitude": 500}
}' http://localhost:7070/generate_qr

# ^^^ the above should return a success message ^^^

curl -X POST -H "Content-Type: application/json" -d '{
    "username": "harishthethird",
    "password": "adithyan0914",
    "current_location": {"latitude": 10.005, "longitude": 500.08}
}' http://localhost:7070/generate_qr

# ^^^ this command must ideally return a failure message ^^^ 

curl localhost:7070/users | jq
