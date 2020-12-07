import sqlite3
from sqlite3 import Error

"""
Example table data:

# Pill ID | Pill Name                     | Generic Name            | Drug Class
#----------------------------------------------------------------------------------------------
# 1       | LILLY 3228 25mg               | atomoxetine             | CNS stimulants
# 2       | LILLY 3229 40mg               | atomoxetine             | CNS stimulants
# 3       | LILLY 3238 18mg               | atomoxetine             | CNS stimulants
# 4       | LILLY 3239 60 mg              | atomoxetine             | CNS stimulants
# 5       | LILLY 3250 80 mg              | atomoxetine             | CNS stimulants
# 6       | LILLY 3251 100 mg             | atomoxetine             | CNS stimulants
# 7       | Cialis 10 mg                  | tadalafil               | Impotence agents
# 8       | Cialis 20 mg                  | tadalafil               | Impotence agents
# 9       | Kombiglyze XR 2.5/1000 4222   | metformin/saxagliptin   | Antidiabetic combinations
# 10      | Roche 75 mg                   | oseltamivir             | Neuraminidase inhibitors
"""
 
 # Connect to database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_pill(conn, pill):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO pills_tbl(id,name,generic_name,drug_class)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pill)
    return cur.lastrowid

def bulk_pills(conn):

    pills = [(1, "LILLY 3228 25 mg", "atomoxetine", "CNS stimulants"), 
             (2, "LILLY 3229 40 mg", "atomoxetine", "CNS stimulants"),
             (3, "LILLY 3238 18 mg", "atomoxetine", "CNS stimulants"),
             (4, "LILLY 3239 60 mg", "atomoxetine", "CNS stimulants"),
             (5, "LILLY 3250 80 mg", "atomoxetine", "CNS stimulants"),
             (6, "LILLY 3251 100 mg", "atomoxetine", "CNS stimulants"),
             (7, "Cialis 10 mg", "tadalafil", "Impotence agents"),
             (8, "Cialis 20 mg", "tadalafil", "Impotence agents"),
             (9, "Kombiglyze XR 2.5/1000 4222", "metformin/saxagliptin", "Antidiabetic combinations"),
             (10, "Tamiflu 75 mg", "oseltamivir", "Neuraminidase inhibitors"),
             (11, "Januvia 50 mg", "sitagliptin", "Dipeptidyl peptidase 4 inhibitors"),
             (12, "Januvia 100 mg", "sitagliptin", "Dipeptidyl peptidase 4 inhibitors"),
             (13, "Zocor 40 mg", "simvastatin", "Statins"),
             (14, "Parnate 10 mg", "tranylcypromine", "Monoamine oxidase inhibitors"),
             (15, "Promacta 75 mg", "eltrombopag", "Platelet-stimulating agents"),
             (16, "Requip XL 12 mg", "ropinirole", "Dopaminergic antiparkinsonism agents"),
             (17, "Requip 0.5 mg", "ropinirole", "Dopaminergic antiparkinsonism agents"),
             (18, "Requip 1 mg", "ropinirole", "Dopaminergic antiparkinsonism agents"),
             (19, "Requip 2 mg", "ropinirole", "Dopaminergic antiparkinsonism agents"),
             (20, "Requip 4 mg", "ropinirole", "Dopaminergic antiparkinsonism agents"),
             (21, "Xanax 0.5 mg", "alprazolam", "Benzodiazepines"),
             (22, "Aromasin 25 mg", "exemestane", "Aromatase inhibitors | Hormones/antineoplastics"),
             (23, "Mycobutin 150 mg", "rifabutin", "Rifamycin derivatives"),
             (24, "Sanctura XR 60 mg", "trospium", "Urinary antispasmodics"),
             (25, "Avandia 4 mg", "rosiglitazone", "Thiazolidinediones"),
             (26, "Soma 250 mg", "carisoprodol", "Skeletal muscle relaxants"),
             (27, "Zoloft 100 mg", "sertraline", "Selective serotonin reuptake inhibitors"),
             (28, "PredniSONE 10 mg", "prednisone", "Glucocorticoids"),
             (29, "Ramipril 10 mg", "ramipril", "Angiotensin Converting Enzyme Inhibitors"),
             (30, "Mycophenolate Mofetil 500 mg", "mycophenolate mofetil", "Selective immunosuppressants"),
             (31, "Lithium Carbonate 150 mg", "lithium carbonate", "Miscellaneous antipsychotic agents"),
             (32, "Dexamethasone 1.5 mg", "dexamethasone", "Glucocorticoids"),
             (33, "PredniSONE 5 mg", "prednisone", "Glucocorticoids"),
             (34, "Coumadin 2 mg", "warfarin", "Coumarins and indandiones"),
             (35, "Coumadin 2.5 mg", "warfarin", "Coumarins and indandiones"),
             (36, "Coumadin 3 mg", "warfarin", "Coumarins and indandiones"),
             (37, "Axert 12.5 mg", "almotriptan", "Antimigraine agents"),
             (38, "Norvasc 10 mg", "amlodipine", "Calcium channel blocking agents"),
             (39, "Procardia 10 mg", "nifedipine", "Calcium channel blocking agents"),
             (40, "Viagra 50 mg", "sildenafil", "Impotence agents"),
             (41, "Lipitor 10 mg", "atorvastatin", "Statins"),
             (42, "Lipitor 20 mg", "atorvastatin", "Statins"),
             (43, "Nitrostat 0.6 mg", "nitroglycerin", "Antianginal agents | Vasodilators"),
             (44, "Lyrica 100 mg", "pregabalin", "Gamma-aminobutyric acid analogs"),
             (45, "Lyrica 200 mg", "pregabalin", "Gamma-aminobutyric acid analogs"),
             (46, "Vicodin ES 7.5 mg", "acetaminophen/hydrocodone", "Narcotic analgesic combinations"),
             (47, "Teveten HCT 25 mg", "eprosartan/hydrochlorothiazide", "Angiotensin II inhibitors with thiazides"),
             (48, "Teveten 600 mg", "eprosartan", "Angiotensin receptor blockers"),
             (49, "Tarka 4 mg / 240 mg", "trandolapril/verapamil", "ACE inhibitors with calcium channel blocking agents"),
             (50, "SYNTHROID 75", "levothyroxine", "Thyroid drugs"),
             (51, "Tricor 48 mg", "fenofibrate", "Fibric acid derivatives"),
             (52, "Synthroid 88 mcg", "levothyroxine", "Thyroid drugs"),
             (53, "Synthroid 0.125 mg", "levothyroxine", "Thyroid drugs"),
             (54, "Synthroid 0.175 mg", "levothyroxine", "Thyroid drugs"),
             (55, "Synthroid 0.2 mg", "levothyroxine", "Thyroid drugs"),
             (56, "Trilipix 135 mg", "fenofibric acid", "Fibric acid derivatives"),
             (57, "Synthroid 112 mcg", "levothyroxine", "Thyroid drugs"),
             (58, "Rilutek 50 mg", "riluzole", "Miscellaneous central nervous system agents"),
             (59, "Diovan 80 mg", "valsartan", "Angiotensin receptor blockers"),
             (60, "Valsartan 160 mg", "valsartan", "Angiotensin receptor blockers"),
             (61, "Diovan 320 mg", "valsartan", "Angiotensin receptor blockers"),
             (62, "Tekturna 300 mg", "aliskiren", "Renin inhibitors"),
             (63, "Tekturna HCT 150 mg", "aliskiren", "Renin inhibitors"),
             (64, "Valturna aliskiren 150 mg", "aliskiren/valsartan", "Miscellaneous antihypertensive combinations"),
             (65, "Valturna aliskiren 300 mg", "aliskiren/valsartan", "Miscellaneous antihypertensive combinations"),
             (66, "Clarinex-D 12 Hour 2.5 mg", "desloratadine/pseudoephedrine", "Upper respiratory combinations"),
             (67, "Pantoprazole sodium delayed-release 20 mg", "pantoprazole sodium delayed-release", "Proton pump inhibitors"),
             (68, "Pantoprazole Sodium Delayed-Release 40 mg", "pantoprazole sodium delayed-release", "Proton pump inhibitors"),
             (69, "Moexipril Hydrochloride 7.5 mg", "moexipril hydrochloride", "Angiotensin Converting Enzyme Inhibitors"),
             (70, "Enalapril Maleate 2.5 mg", "enalapril maleate", "Angiotensin Converting Enzyme Inhibitors"),
             (71, "Enalapril Maleate 5 mg", "enalapril maleate", "Angiotensin Converting Enzyme Inhibitors"),
             (72, "Enalapril Maleate 10 mg", "enalapril maleate", "Angiotensin Converting Enzyme Inhibitors"),
             (73, "Enalapril Maleate 20 mg", "enalapril maleate", "Angiotensin Converting Enzyme Inhibitors"),
             (74, "Lamotrigine 25 mg", "lamotrigine", "Triazine anticonvulsants"),
             (75, "ClomiPHENE Citrate 50 mg", "clomiphene", "Synthetic ovulation stimulants"),
             (76, "Carvedilol 3.125 mg", "cardevilol", "Non-cardioselective beta blockers"),
             (77, "Carvedilol 3 mg", "cardevilol", "Non-cardioselective beta blockers"),
             (78, "Buspirone Hydrochloride 10 mg", "buspirone hydrochloride", "Miscellaneous anxiolytics, sedatives and hypnotics"),
             (79, "Tramadol Hydrochloride 50 mg", "tramadol hydrochloride", "Narcotic analgesics"),
             (80, "Tramadol", "tramadol hydrochloride", "Narcotic analgesics"),
             (81, "Isosorbide Mononitrate 20 mg", "isosorbide mononitrate", "Antianginal agents"),
             (82, "Amlodipine Besylate 2.5 mg", "amlodipine besylate", "Calcium channel blocking agents"),
             (83, "Epitol 200 mg", "carbamazepine", "Dibenzazepine anticonvulsants"),
             (84, "Carbamazepine 200 mg", "carbamazepine", "Dibenzazepine anticonvulsants"),
             (85, "Lamotrigine 25 mg", "lamotrigine", "Triazine anticonvulsants"),
             (86, "Carvedilol 6.25 mg", "carvedilol", "Non-cardioselective beta blockers"),
             (87, "93 135 Carvedilol 6.25 mg", "carvedilol", "Non-cardioselective beta blockers"),
             (88, "Naproxen 250 mg", "naproxen", "Nonsteroidal anti-inflammatory drugs"),
             (89, "Naproxen 375 mg", "naproxen", "Nonsteroidal anti-inflammatory drugs"),
             (90, "Naproxen 500 mg", "naproxen", "Nonsteroidal anti-inflammatory drugs"),
             (91, "93 Naproxen 500 mg", "naproxen", "Nonsteroidal anti-inflammatory drugs"),
             (92, "Ticlopidine Hydrochloride 250 mg", "ticlopidine hydrochloride", "Platelet aggregation inhibitors"),
             (93, "Topiramate 25 mg", "topiramate", "Platelet aggregation inhibitors"),
             (94, "Leflunomide 10 mg", "leflunomide", "Antirheumatics | Selective immunosuppressants"),
             (95, "Leflunomide 20 mg", "leflunomide", "Antirheumatics | Selective immunosuppressants"),
             (96, "Venlafaxine Hydrochloride 25 mg", "venlafaxine hydrochloride", "Serotonin-norepinephrine reuptake inhibitors"),
             (97, "Venlafaxine Hydrochloride", "venlafaxine hydrochloride", "Serotonin-norepinephrine reuptake inhibitors"),
             (98, "Bicalutamide 50 mg", "bicalutamide", "Antiandrogens | Hormones/antineoplastics"),
             (99, "Risperidone 0.25 mg", "risperidone", "Atypical antipsychotics"),
             (100, "Risperidone 93 225 0.5mg", "risperidone", "Atypical antipsychotics")]
    
    cur = conn.cursor()
    cur.executemany("""
        INSERT OR IGNORE INTO pills_tbl VALUES (?, ?, ?, ?)""", pills)

def main():
    database = "../pills_db.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        bulk_pills(conn)


if __name__ == '__main__':
    main()        