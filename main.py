from search import Search, Algorithm, SearchResult
from controller import Controller

if __name__ == "__main__":
    for i in range(1, 11):
        controller = Controller(str(i))
        controller.run()
