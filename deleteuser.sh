echo "Attempting to delete user with name '$1'"

curl -X DELETE -H "Content-Type: application/json" --data '{"username":"'"$1"'"}' http://127.0.0.1:5000/api/v1/resources/musicService/users