from src.utils import generate_holidays_dataset


def main():
    df_holidays = generate_holidays_dataset()
    df_holidays.to_csv("Turkey_official_and_religious_days.csv", index=False)


if __name__ == '__main__':
    main()
