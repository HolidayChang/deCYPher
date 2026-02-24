import os
import sys
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GENES_CONFIG = {
    "CYP2D6":   {"ref": "CYP2D6.1.001.fa",    "special": False},
    "CYP2C19":  {"ref": "CYP2C19.1.001.fasta", "special": False},
    "CYP2B6":   {"ref": "CYP2B6.1.001.fasta", "special": False},
    "CYP2C9":   {"ref": "CYP2C9.1.001.fasta", "special": False},
    "CYP3A5":   {"ref": "CYP3A5.1.001.fasta", "special": False},
    "CYP4F2":   {"ref": "CYP4F2.1.001.fasta", "special": False},
    "NUDT15":   {"ref": "NUDT15.1.001.fasta", "special": False},
    "SLCO1B1":  {"ref": "SLCO1B1.1.001.fasta", "special": False},
    "DPYD":     {"ref": "DPYD.1.001.fasta",    "special": False},
    "CYP2D613": {"ref": "CYP2D6.13.001.fa",   "special": True},
}

def run_command(cmd, stdout_path=None):
    try:
        if stdout_path:
            with open(stdout_path, 'w') as f_out:
                subprocess.run(cmd, stdout=f_out, check=True)
        else:
            subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[Error] Command failed: {' '.join(cmd)}")
        raise e

def main():
    parser = argparse.ArgumentParser(
        description="deCYPher: A specialized genotyping tool for pharmacogenes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--input', required=True, help='Path to assembly fasta file')
    parser.add_argument('--name', required=True, help='Sample name')
    parser.add_argument('--outdir', required=True, help='Output directory')
    parser.add_argument('--threads', default="18", help='CPU threads')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    ref_root = os.path.join(BASE_DIR, 'ref')
    extract_script = os.path.join(BASE_DIR, 'extract_loci_from_paf.py')
    annotation_script = os.path.join(BASE_DIR, 'annotation.py')
    comparison_script = os.path.join(BASE_DIR, 'comparison.py')
    paftools_js = os.path.join(os.environ.get('CONDA_PREFIX', ''), 'bin/paftools.js')

    base_dir = os.path.join(args.outdir, args.name)
    final_json_path = os.path.join(base_dir, f"{args.name}.json")
    if os.path.exists(final_json_path): os.remove(final_json_path)

    for gene, config in GENES_CONFIG.items():
        print(f"\n>>>> Processing gene: {gene}")
        gene_dir = os.path.join(ref_root, gene)
        ref_fa = os.path.join(gene_dir, config['ref'])
        haplo_fa = os.path.join(gene_dir, f"{gene}.haplotypes.fasta")
        refseq_dir = os.path.join(gene_dir, "RefSeqGene")

        dirs = {k: os.path.join(base_dir, gene, k) for k in ['alignment', 'extract', 'result']}
        for d in dirs.values(): os.makedirs(d, exist_ok=True)

        # 1. Mapping & 2. Extract
        paf_path = os.path.join(dirs['alignment'], "mapping.paf")
        run_command(["minimap2", "-c", "-x", "map-hifi", "-y", "--cs", "-t", args.threads, "-2", args.input, ref_fa], stdout_path=paf_path)
        run_command(["python3", extract_script, args.input, paf_path, dirs['extract']])

        # 3. Calling variants
        fasta_files = sorted([f for f in os.listdir(dirs['extract']) if f.endswith(".fasta")])
        for fasta in fasta_files:
            fasta_path = os.path.join(dirs['extract'], fasta)
            base = os.path.splitext(fasta)[0]
            v_paf = os.path.join(dirs['extract'], f"{base}.paf")
            v_vcf = os.path.join(dirs['extract'], f"{base}.vcf")
            run_command(["minimap2", "-c", "-x", "map-hifi", "-y", "--cs", "-t", args.threads, "-2", ref_fa, fasta_path], stdout_path=v_paf)
            run_command(["k8", paftools_js, "call", "-L3", "-l3", "-f", ref_fa, v_paf], stdout_path=v_vcf)

        # 特殊流程：如果是 CYP2D613，直接進入判定，跳過 4 & 5
        if config['special']:
            print(f"Special mode: Direct VCF comparison for {gene}")
            run_command(["python3", comparison_script, dirs['result'], dirs['result'], final_json_path, gene])
            continue

        # 4. Haplotype Alignment
        for fasta in fasta_files:
            base = os.path.splitext(fasta)[0]
            c_paf = os.path.join(dirs['result'], f"comparison_{base}.paf")
            run_command(["minimap2", "-c", "-x", "map-hifi", "-y", "--cs", "-t", args.threads, "-2", haplo_fa, os.path.join(dirs['extract'], fasta)], stdout_path=c_paf)

        # 5. Annotating
        for fasta in fasta_files:
            base = os.path.splitext(fasta)[0]
            v_vcf = os.path.join(dirs['extract'], f"{base}.vcf")
            t_txt = os.path.join(dirs['result'], f"comparison_{base}.txt")
            run_command(["python3", annotation_script, v_vcf, refseq_dir, t_txt, gene])

        # 6. Summarizing
        run_command(["python3", comparison_script, dirs['result'], dirs['result'], final_json_path, gene])

    print(f"\n[Success] Analysis completed. Report: {final_json_path}")

if __name__ == "__main__":
    main()
