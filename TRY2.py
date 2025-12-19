f = open("data.txt", "r+")
print(f.read())
f.write("\nNew content added")
f.close()
