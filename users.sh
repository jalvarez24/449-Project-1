users=("avery123" "stroustrup123" "lovelace123")
passwords=("password123" "goodpass" "badpass")
names=("kenytt" "bjorne" "ada")
emails=("avery@mail.com" "c++@mail.com" "programmerOG@mail.com")
len=${#users[@]}

for (( i = 0; i<$len; i++ )); do \
  #echo ${users[i]}
  curl -X POST \
  -H "Content-Type: application/json" \
  --data '{"username":"'"${users[i]}"'","password":"'"${passwords[i]}"'","display_name":"'"${names[i]}"'","email":"'" ${emails[i]} "'"}' \
  http://127.0.0.1:5000/api/v1/resources/musicService/users
done
