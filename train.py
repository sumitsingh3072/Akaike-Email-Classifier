from models import train_email_classifier

if __name__ == "__main__":
    csv_path = "data/dataset.csv"
    train_email_classifier(csv_path)
