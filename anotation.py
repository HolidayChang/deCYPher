import os
import sys

def load_variants(vcf_file):
    variants = set()
    line_count = 0
    import gzip
    open_func = gzip.open if vcf_file.endswith('.gz') else open
    mode = 'rt' if vcf_file.endswith('.gz') else 'r'
    
    try:
        with open_func(vcf_file, mode) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                parts = line.strip().split('\t', 5)
                try:
                    pos = int(parts[1])
                    ref = parts[3]
                    alt = parts[4]
                    variants.add((pos, ref, alt))
                    line_count += 1
                except (IndexError, ValueError):
                    continue
    except FileNotFoundError:
        print(f"Error: File {vcf_file} not found.")
        return set(), 0
        
    return variants, line_count

def compare_vcfs(reference_vcf, compare_dir, output_file, gene_name):
    reference_variants, line_count = load_variants(reference_vcf)

    if gene_name == "CYP2D6":
        threshold = 250
        if line_count > threshold:
            with open(output_file, 'w') as out_f:
                out_f.write("DETECT_STAR5\n")
            print(f"CYP2D6 DETECT_STAR5 written (line count = {line_count})")
            return

    similarities = {}

    for file in os.listdir(compare_dir):
        if not (file.endswith('.vcf') or file.endswith('.vcf.gz')):
            continue

        compare_vcf = os.path.join(compare_dir, file)
        compare_variants, _ = load_variants(compare_vcf)

        common = reference_variants & compare_variants
        matches = len(common)
        total_variants = len(compare_variants)

        percentage = (matches / total_variants * 100) if total_variants else 0
        similarities[file] = (matches, total_variants, percentage)

    with open(output_file, 'w') as out_f:
        perfect_matches = []
        for file, (matches, total, percentage) in similarities.items():
            out_f.write(f"VCF file: {file} - Matches: {matches}/{total} ({percentage:.2f}%)\n")
            if matches == total and total > 0:
                perfect_matches.append(file)

        if perfect_matches:
            out_f.write("\nFiles with 100% matching variants (POS, REF, ALT):\n")
            for file in perfect_matches:
                out_f.write(f" - {file}\n")
        else:
            out_f.write("\nNo files with 100% matching variants.\n")

    print(f"Comparison results written to {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python compare_vcfs.py <reference_vcf> <compare_dir> <output_file> <gene_name>")
        sys.exit(1)

    reference_vcf = sys.argv[1]
    compare_dir = sys.argv[2]
    output_file = sys.argv[3]
    gene_name = sys.argv[4]

    compare_vcfs(reference_vcf, compare_dir, output_file, gene_name)




