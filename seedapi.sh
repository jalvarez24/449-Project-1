
## This seedapi.sh gets called from the make file, by calling `make seedapi`.



#
## Start of the POST request scripts to populate the database with tracks, using the tracks microservice
#


track_titles=("Let Go Feat. Grabbitz" "Big Pimpin" "Slow dancing in the dark" "Led Spirals")
album_titles=("W:/2016ALBUM/" "Vol. 3... Life and Times of S. Carter" "Ballads 1" "John Wick: Original Motion Picture Soundtrack")
artists=("deadmau5" "Jay-Z" "Joji" "Le Castle Vania")
length_seconds=("120" "140" "120" "130")
media_urls=("https://www.youtube.com/watch?v=PKFcaXd5G8c&list=RDMMPKFcaXd5G8c&start_radio=1" "https://www.youtube.com/watch?v=9pX1Gn3rCPw" "https://www.youtube.com/watch?v=K3Qzzggn--s" "https://www.youtube.com/watch?v=7Pv0u7uMn-g")
len=${#track_titles[@]}


# for (( i = 0; i<$len; i++ )); do \
#   curl -X POST \
#   -H "Content-Type: application/json" \
#   --data '{"track_title":"'"${track_titles[i]}"'","album_title":"'"${album_titles[i]}"'","artist":"'"${artists[i]}"'","length_seconds":"'"${length_seconds[i]}"'","url_media":"'"${media_urls[i]}"'"}' \
#   http://127.0.0.1:5001/api/v1/resources/musicService/tracks
# done


#
## Start of the POST request scripts to populate the database with users, using the user microservice
#


users=("avery123" "stroustrup123" "lovelace123")
passwords=("password123" "goodpass" "badpass")
names=("kenytt" "bjorne" "ada")
emails=("avery@mail.com" "c++@mail.com" "programmerOG@mail.com")
len=${#users[@]}


# for (( i = 0; i<$len; i++ )); do \
#   curl -X POST \
#   -H "Content-Type: application/json" \
#   --data '{"username":"'"${users[i]}"'","password":"'"${passwords[i]}"'","display_name":"'"${names[i]}"'","email":"'" ${emails[i]} "'"}' \
#   http://127.0.0.1:5000/api/v1/resources/musicService/users
# done



#
## Start of the POST request scripts to add descriptions to the database, using the descriptions microservice
#


curl -d '{"username" : "lovelace123", "track_id" : "1", "description_text" : "This song cured my depression."}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5002/api/v1/resources/musicService/descriptions