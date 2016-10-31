SONG=$1
ARTIST=$2
TIME=$3

curl -X POST --data-urlencode 'payload={"channel": "#general", "username": "arash_ghost", "text": "'"$SONG"' by '"$ARTIST"' should play at around '"$TIME"'!", "icon_emoji": ":ghost:"}' https://hooks.slack.com/services/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

