track_titles=("Let Go Feat. Grabbitz" "Big Pimpin" "Slow dancing in the dark" "Led Spirals")
album_titles=("W:/2016ALBUM/" "Vol. 3... Life and Times of S. Carter" "Ballads 1" "John Wick: Original Motion Picture Soundtrack")
artists=("deadmau5" "Jay-Z" "Joji" "Le Castle Vania")
length_seconds=("120" "140" "120" "130")
media_urls=("https://www.youtube.com/watch?v=PKFcaXd5G8c&list=RDMMPKFcaXd5G8c&start_radio=1" "https://www.youtube.com/watch?v=9pX1Gn3rCPw" "https://www.youtube.com/watch?v=K3Qzzggn--s" "https://www.youtube.com/watch?v=7Pv0u7uMn-g")
len=${#track_titles[@]}


for (( i = 0; i<$len; i++ )); do \
  curl -X POST \
  -H "Content-Type: application/json" \
  --data '{"track_title":"'"${track_titles[i]}"'","album_title":"'"${album_titles[i]}"'","artist":"'"${artists[i]}"'","length_seconds":"'"${length_seconds[i]}"'","url_media":"'"${media_urls[i]}"'"}' \
  http://127.0.0.1:5001/api/v1/resources/musicService/tracks
done
