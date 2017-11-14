deep_list = [
  [
    [
      47167667, 
      "answer", 
      "Randomly choose a word from text file Python"
    ], 
    "https://stackoverflow.com/a/47167667"
  ], 
  [
    [
      47103718, 
      "answer", 
      "AttributeError: &#39;Spotify&#39; object has no attribute &#39;current_user_saved_tracks&#39;"
    ], 
    "https://stackoverflow.com/a/47103718"
  ], 
  [
    [
      47101953, 
      "answer", 
      "python Split list based on delimiting list value"
    ], 
    "https://stackoverflow.com/a/47101953"
  ], 
  [
    [
      46935426, 
      "answer", 
      "boto3 S3: get_object error handling"
    ], 
    "https://stackoverflow.com/a/46935426"
  ]
]
#print(deep_list)
for deep in deep_list:
	deep[0].extend([deep[1]])
	del deep[1]


new_list = [d[0] for d in deep_list]
print(new_list)