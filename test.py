import scan as scan

ban = scan.grab("crypto_eh")
print(ban['exists'])
print(ban['sug_ban'] + ban['s_ban'] + ban['ghost'] + ban['deboost'])