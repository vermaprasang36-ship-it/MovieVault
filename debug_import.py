import tmdb_api

print("FILE:", tmdb_api.__file__)
print("HAS get_movies_by_genre:", hasattr(tmdb_api, "get_movies_by_genre"))

print("\nExports:")
for name in dir(tmdb_api):
    if name.startswith("get_"):
        print(name)


# .\.venv\Scripts\python.exe debug_import.py