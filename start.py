from src.setup import modelsLoad, menu

def main():
    # Return model instances from data/stage with metadata
    models = modelsLoad()

    # Display menu to access model info and visualization
    menu(models)

if __name__ == "__main__":
    main()
