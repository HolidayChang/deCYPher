import os
import sys
import json

def load_exclude_variants(vcf_path):
    
    exclude_set = set()
    if not os.path.exists(vcf_path):
        return exclude_set
    with open(vcf_path, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            cols = line.strip().split('\t')
            if len(cols) >= 5:
                variant_key = f"{cols[0]}\t{cols[1]}\t.\t{cols[3]}\t{cols[4]}"
                exclude_set.add(variant_key)
    return exclude_set

def check_vcf_for_special_gene(sample_vcf_path, exclude_vcf_path):
    if not os.path.exists(sample_vcf_path):
        return "VCF_NOT_FOUND"
    
    exclude_variants = load_exclude_variants(exclude_vcf_path)
    if not exclude_variants:
        return "Not_*13"
    
    with open(sample_vcf_path, 'r') as f:
        sample_content = f.read()
    
    for var in exclude_variants:
        if var in sample_content:
            return "Not_*13"
            
    return "*13"

def extract_matching_star_allele(txt_file, paf_file, gene_name, vcf_path=None, exclude_vcf=None):
    if gene_name == "CYP2D613":
        return check_vcf_for_special_gene(vcf_path, exclude_vcf)
    
    matching_variants = set()
    found_cyp2d6_4 = False
    hahaha_found = False 
    no_matching_variants = False

    if gene_name == "DPYD":
        allele_list = []
        if os.path.exists(txt_file):
            with open(txt_file, 'r') as f:
                parse_rs = False
                for line in f:
                    if "No files with 100% matching variants." in line: return "reference"
                    if "Files with 100% matching variants" in line:
                        parse_rs = True
                        continue
                    if parse_rs and line.startswith("-"):
                        rs_id = line.replace(".vcf", "").replace("-", "").strip()
                        allele_list.append(rs_id)
        return " ".join(allele_list) if allele_list else "reference"

    
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            lines = f.readlines()
            start_parsing = False
            for line in lines:
                line = line.strip()
                if "DETECT_STAR5" in line:
                    hahaha_found = True
                    break
                if "No files with 100% matching variants." in line:
                    no_matching_variants = True
                    break
                if "Files with 100% matching variants" in line:
                    start_parsing = True
                    continue
                if start_parsing and line.startswith("-"):
                    variant = "*" + line.replace(".vcf", "").split(".")[-1]
                    matching_variants.add(variant)
                    if "CYP2D6.4.vcf" in line: found_cyp2d6_4 = True

    if hahaha_found: return "*5"
    if no_matching_variants: return "*1"
    
    result = "No matching allele found"
    if os.path.exists(paf_file):
        with open(paf_file, 'r') as paf:
            for line in paf:
                cols = line.strip().split('\t')
                if len(cols) > 5 and "*" in cols[5]:
                    star = "*" + cols[5].split("*")[-1]
                    if star in matching_variants:
                        result = star
                        break
    
   
    if result in ["*10", "*185"] and found_cyp2d6_4:
        result = "*4"

    return result

if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit(1)

    result_dir, paf_dir, output_json, gene_name = sys.argv[1:5]
    result_dict = {}
    
    
    base_script_path = os.path.dirname(os.path.abspath(__file__))
    exclude_vcf_path = os.path.join(base_script_path, "ref", "CYP2D613", "RefSeqGene", "CYP2D613.vcf")
    
    
    vcf_dir = os.path.abspath(os.path.join(result_dir, "..", "extract"))

   
    if gene_name == "CYP2D613":
        vcf_files = sorted([f for f in os.listdir(vcf_dir) if f.endswith(".vcf")])
        for vcf_file in vcf_files:
            idx = f"allele{len(result_dict)+1}"
            result_dict[idx] = check_vcf_for_special_gene(os.path.join(vcf_dir, vcf_file), exclude_vcf_path)
    else:
        txt_files = sorted([f for f in os.listdir(result_dir) if f.endswith(".txt")])
        for txt_file in txt_files:
            idx = f"allele{len(result_dict)+1}"
            txt_path = os.path.join(result_dir, txt_file)
            paf_path = os.path.join(paf_dir, txt_file.replace(".txt", ".paf"))
            vcf_path = os.path.join(vcf_dir, txt_file.replace(".txt", ".vcf"))
            result_dict[idx] = extract_matching_star_allele(txt_path, paf_path, gene_name, vcf_path, exclude_vcf_path)

    if gene_name == "CYP2D613":
        final_alleles_13 = [v for v in result_dict.values() if v == "*13"]
        if not final_alleles_13:
            sys.exit(0) 
        gene_result_output = { "CYP2D6": { f"allele{i+1}": v for i, v in enumerate(final_alleles_13) } }
        
    elif gene_name == "CYP2D6" and "*5" in result_dict.values():
        gene_result_output = { gene_name: { "allele1": "*5" } }
        
    elif len(result_dict) > 5:
        gene_result_output = { gene_name: { "note": "Potential assembly artifact or SV detected." } }
        
    else:
        gene_result_output = { gene_name: result_dict }

    
    if os.path.exists(output_json):
        with open(output_json, 'r') as f:
            try: all_data = json.load(f)
            except: all_data = {}
    else:
        all_data = {}

    if gene_name == "CYP2D613":
        
        if "CYP2D6" in all_data:
            exist_num = len(all_data["CYP2D6"])
            for i, v in enumerate(final_alleles_13):
                all_data["CYP2D6"][f"allele{exist_num + i + 1}"] = v
        else:
            all_data.update(gene_result_output)
    else:
        all_data.update(gene_result_output)

    with open(output_json, 'w') as out:
        json.dump(all_data, out, indent=2)














