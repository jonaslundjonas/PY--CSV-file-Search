import os
import csv
from collections import defaultdict
from datetime import datetime

def search_csv_files(search_value):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results = defaultdict(int)
    total_occurrences = 0
    total_files = 0
    processed_files = 0

    for filename in os.listdir(current_dir):
        if filename.endswith('.csv'):
            total_files += 1
            file_path = os.path.join(current_dir, filename)
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        for field in row:
                            if field == search_value:
                                results[filename] += 1
                                total_occurrences += 1
                processed_files += 1
                print(f"Processed {processed_files}/{total_files} files", end='\r')
            except Exception as e:
                print(f"\nEtt fel uppstod vid läsning av {filename}: {str(e)}")

    print(f"\nBearbetning slutförd. {processed_files} filer genomsökta.")
    return results, total_occurrences, total_files

def generate_report(search_value, results, total_occurrences, total_files):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"Sökrapport - {now}\n"
    report += f"Sökt värde: '{search_value}'\n\n"
    report += f"Totalt antal genomsökta filer: {total_files}\n"
    report += f"Totalt antal förekomster: {total_occurrences}\n\n"
    report += "Resultat per fil:\n"
    
    for filename, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
        report += f"{filename}: {count} förekomster\n"
    
    return report

def save_report(report):
    filename = f"search_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    return filename

def main():
    search_value = input("Ange värdet du vill söka efter i CSV-filerna: ")
    print(f"Söker efter '{search_value}' i CSV-filer...")

    results, total_occurrences, total_files = search_csv_files(search_value)
    
    report = generate_report(search_value, results, total_occurrences, total_files)
    print("\nRapport:")
    print(report)

    save_option = input("Vill du spara rapporten till en fil? (ja/nej): ").lower()
    if save_option == 'ja':
        filename = save_report(report)
        print(f"Rapporten har sparats till filen: {filename}")

if __name__ == "__main__":
    main()
