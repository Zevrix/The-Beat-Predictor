SONG=$1
TIME=$2
PREDICT=$3

curl -X POST --data-urlencode 'payload={"channel": "#plays", "username": "arash_ghost", "text": "'"$SONG"' played at '"$TIME"' and was predicted to play at '"$PREDICT"'.", "icon_emoji": ":ghost:"}' https://hooks.slack.com/services/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

