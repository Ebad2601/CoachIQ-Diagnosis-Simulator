#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║         CoachIQ — Sports Injury Diagnosis Simulator      ║
║         Built by Mark | OrthoAI Project                  ║
║         github.com/mark | Python 3 | Zero dependencies   ║
╚══════════════════════════════════════════════════════════╝

A clinical decision-making game for sports medicine education.
Work through real athlete cases, order investigations, and
make your diagnosis — just like a real sports physician.
"""

import time
import random
import os
import sys
import json
from datetime import datetime

# ─── ANSI COLOURS ────────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    BLACK   = "\033[30m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    BG_DARK = "\033[40m"
    BG_TEAL = "\033[46m"

    TEAL    = "\033[38;5;43m"
    ORANGE  = "\033[38;5;208m"
    MINT    = "\033[38;5;121m"
    CORAL   = "\033[38;5;203m"
    PURPLE  = "\033[38;5;141m"
    GOLD    = "\033[38;5;220m"


def supports_colour():
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

USE_COLOUR = supports_colour()

def col(colour, text):
    if USE_COLOUR:
        return f"{colour}{text}{C.RESET}"
    return text

def bold(text):   return col(C.BOLD, text)
def teal(text):   return col(C.TEAL, text)
def green(text):  return col(C.GREEN, text)
def red(text):    return col(C.RED, text)
def yellow(text): return col(C.YELLOW, text)
def cyan(text):   return col(C.CYAN, text)
def mint(text):   return col(C.MINT, text)
def gold(text):   return col(C.GOLD, text)
def coral(text):  return col(C.CORAL, text)
def purple(text): return col(C.PURPLE, text)
def dim(text):    return col(C.DIM, text)
def orange(text): return col(C.ORANGE, text)


# ─── CASE DATA ───────────────────────────────────────────────────────────────

CASES = [
    {
        "id": 1,
        "sport": "Cricket",
        "athlete": "Hamza, 22",
        "role": "Fast bowler — Club level",
        "presenting": (
            "Hamza presents with sharp anterior knee pain after landing\n"
            "  awkwardly on a delivery stride 3 days ago. Pain worsens on\n"
            "  stairs and when squatting. He reports a 'giving way' sensation\n"
            "  on one occasion but no acute swelling or locking."
        ),
        "vitals": [
            ("Mechanism",   "Landing impact during delivery"),
            ("Location",    "Anterior knee"),
            ("Duration",    "3 days"),
            ("VAS Pain",    "7 / 10"),
            ("Swelling",    "Mild periarticular"),
        ],
        "investigations": {
            "Ottawa knee rules": (
                "Ottawa criteria NEGATIVE for fracture. ROM limited 0–110°\n"
                "  due to pain. No bony tenderness at fibular head or\n"
                "  tibial tuberosity. Weight-bearing intact.",
                "No fracture. The absence of bony tenderness is reassuring."
            ),
            "Lachman test": (
                "Lachman: FIRM endpoint. No anterior tibial translation.\n"
                "  ACL structurally intact.",
                "ACL intact — rules out a major differential here."
            ),
            "McMurray test": (
                "McMurray: NEGATIVE medially and laterally. No click,\n"
                "  no pain arc through ROM.",
                "Meniscal tear less likely."
            ),
            "Clarke's test (patellar grind)": (
                "Clarke's: POSITIVE — patient grimaces on resisted quad\n"
                "  contraction with patella compressed. Crepitus noted.",
                "KEY FINDING. Think patellofemoral pathology."
            ),
        },
        "options": [
            "ACL tear",
            "Patellar tendinopathy",
            "Patellofemoral pain syndrome (PFPS)",
            "Medial meniscus tear",
        ],
        "correct": 2,
        "hint": (
            "Think about the mechanism — repetitive landing, anterior\n"
            "  knee pain worse on stairs/squatting, positive Clarke's test,\n"
            "  and the 'giving way' that's often reported in this condition.\n"
            "  No ligamentous or meniscal findings. What structure sits\n"
            "  between the femur and the tibial plateau?"
        ),
        "explanation": (
            "Patellofemoral Pain Syndrome (PFPS) is the diagnosis.\n\n"
            "  The anterior knee pain worsened by loading activities (stairs,\n"
            "  squatting), positive Clarke's test, and the complete absence of\n"
            "  ligamentous or meniscal findings all point here. PFPS is common\n"
            "  in fast bowlers due to repetitive high-impact landing forces on\n"
            "  the patellofemoral joint."
        ),
        "management": (
            "Physiotherapy: VMO strengthening, patellar taping, hip abductor\n"
            "  strengthening. NSAIDs 5–7 days. Activity modification — reduce\n"
            "  bowling load. Return to bowling 4–6 weeks with graduated load\n"
            "  progression. Reassess at 6 weeks; consider MRI if no improvement."
        ),
    },
    {
        "id": 2,
        "sport": "Football",
        "athlete": "Sofia, 19",
        "role": "Midfielder — Academy level",
        "presenting": (
            "Sofia twisted her ankle in a match 48 hours ago. Immediate\n"
            "  swelling and inability to weight-bear. She describes pain\n"
            "  lateral to the ankle. Now she can take a few steps but is\n"
            "  limping with significant pain."
        ),
        "vitals": [
            ("Mechanism",   "Inversion twist during tackle"),
            ("Location",    "Lateral ankle"),
            ("Duration",    "48 hours"),
            ("Weight-bear", "Partial — limping"),
            ("Swelling",    "Moderate, lateral"),
        ],
        "investigations": {
            "Ottawa ankle rules": (
                "Ottawa ankle rules: POSITIVE — bony tenderness at\n"
                "  posterior tip of lateral malleolus. Unable to take\n"
                "  4 full weight-bearing steps.",
                "Ottawa positive — imaging indicated."
            ),
            "X-ray ankle (AP + lateral)": (
                "X-ray: NO fracture visible. Soft tissue swelling noted\n"
                "  laterally. Intact bony cortex throughout.",
                "Fracture excluded. This is a soft tissue injury."
            ),
            "Anterior drawer test": (
                "Anterior drawer: INCREASED laxity vs contralateral.\n"
                "  Soft endpoint. ~8mm translation.",
                "ATFL likely disrupted. Quantifies ligament integrity."
            ),
            "Squeeze test (fibula)": (
                "Squeeze test: NEGATIVE. No proximal fibular pain.",
                "Maisonneuve fracture excluded."
            ),
        },
        "options": [
            "Maisonneuve fracture",
            "Lateral ankle ligament sprain (ATFL)",
            "Peroneal tendon rupture",
            "Talar dome osteochondral fracture",
        ],
        "correct": 1,
        "hint": (
            "Ottawa positive but X-ray clear. Positive anterior drawer\n"
            "  with a soft endpoint. Inversion mechanism. No proximal\n"
            "  fibular tenderness. This is the most common sports injury\n"
            "  in the world."
        ),
        "explanation": (
            "Lateral ankle ligament sprain — specifically ATFL involvement\n"
            "  — is the diagnosis.\n\n"
            "  Ottawa criteria indicated imaging which cleared fracture.\n"
            "  Positive anterior drawer with soft endpoint confirms ATFL\n"
            "  disruption. Given inability to weight-bear initially and\n"
            "  significant laxity, this is a Grade II–III sprain."
        ),
        "management": (
            "PRICE protocol immediately. Aircast brace 2–3 weeks.\n"
            "  Early proprioceptive physiotherapy — balance board work.\n"
            "  Grade I: return 1–2 weeks. Grade II: 3–6 weeks.\n"
            "  Grade III: up to 12 weeks. Functional rehabilitation\n"
            "  essential to prevent recurrence (40% re-sprain rate)."
        ),
    },
    {
        "id": 3,
        "sport": "Swimming",
        "athlete": "Tariq, 25",
        "role": "Competitive swimmer — National level",
        "presenting": (
            "Tariq reports a 4-week progressive worsening of shoulder pain,\n"
            "  worse with overhead strokes (freestyle, butterfly) and reaching\n"
            "  behind his back. No acute injury. Pain at the top of the shoulder.\n"
            "  Training 5 sessions per week, 4km per session."
        ),
        "vitals": [
            ("Mechanism",   "Overuse / overhead repetitive load"),
            ("Location",    "Superior / lateral shoulder"),
            ("Duration",    "4 weeks, progressive"),
            ("Training",    "5x/week — 4km per session"),
            ("Night pain",  "Occasional"),
        ],
        "investigations": {
            "Neer's impingement test": (
                "Neer's: POSITIVE — pain reproduced at 90–120° passive\n"
                "  forward flexion with shoulder internally rotated.",
                "Classic subacromial impingement sign."
            ),
            "Hawkins-Kennedy test": (
                "Hawkins-Kennedy: POSITIVE — pain with passive internal\n"
                "  rotation at 90° flexion.",
                "Second impingement test positive. Pattern establishing."
            ),
            "Empty can test (supraspinatus)": (
                "Empty can: POSITIVE — weakness AND pain with resisted\n"
                "  abduction in scapular plane, arm pronated.",
                "Supraspinatus weakness. Important differentiator."
            ),
            "Speed's test (biceps)": (
                "Speed's test: NEGATIVE — no pain with resisted forward\n"
                "  flexion, elbow extended, forearm supinated.",
                "Biceps tendinopathy less likely."
            ),
        },
        "options": [
            "Biceps long head tendinopathy",
            "AC joint arthritis",
            "Supraspinatus impingement syndrome",
            "Glenohumeral instability",
        ],
        "correct": 2,
        "hint": (
            "Overhead athlete, 5 sessions/week. Two impingement tests\n"
            "  both positive. Supraspinatus weak on empty can. What\n"
            "  structure passes through the subacromial space and is\n"
            "  repeatedly compressed with each stroke?"
        ),
        "explanation": (
            "Supraspinatus impingement syndrome is the diagnosis.\n\n"
            "  Positive Neer's and Hawkins-Kennedy with a weak empty can\n"
            "  in a high-volume overhead athlete is textbook presentation.\n"
            "  Chronic overuse has narrowed the subacromial space, causing\n"
            "  repetitive impingement of the supraspinatus tendon against\n"
            "  the coracoacromial arch with each stroke cycle."
        ),
        "management": (
            "Load management — reduce high-volume overhead sessions by 40%.\n"
            "  Rotator cuff strengthening programme (especially external\n"
            "  rotators). Scapular stabilisation physio. Consider subacromial\n"
            "  corticosteroid injection if no improvement at 6 weeks.\n"
            "  MRI if persistent. Return to full training 8–12 weeks."
        ),
    },
    {
        "id": 4,
        "sport": "Athletics",
        "athlete": "Aisha, 17",
        "role": "Sprinter — Regional level",
        "presenting": (
            "Aisha felt a sudden 'pop' in her posterior thigh mid-race\n"
            "  1 week ago and stopped immediately. She now has significant\n"
            "  bruising tracking down the posterior thigh and moderate\n"
            "  difficulty walking. Cannot jog."
        ),
        "vitals": [
            ("Mechanism",   "Explosive sprint — sudden onset"),
            ("Location",    "Posterior thigh, mid-belly"),
            ("Duration",    "1 week post-injury"),
            ("Bruising",    "Significant, tracking distally"),
            ("Walk",        "Possible — antalgic gait"),
        ],
        "investigations": {
            "Palpation": (
                "Tender palpable defect at mid-posterior thigh biceps femoris\n"
                "  belly. No bony tenderness. Significant ecchymosis extending\n"
                "  distally toward the popliteal fossa.",
                "Palpable defect suggests significant muscle disruption."
            ),
            "Single leg hamstring curl": (
                "Unable to perform without severe pain. Strength: 2/5\n"
                "  compared to 5/5 contralateral side.",
                "Major strength deficit confirms severity."
            ),
            "Slump / neural tension test": (
                "Slump test: NEGATIVE. No sciatic neural tension signs.\n"
                "  No paraesthesia or radicular symptoms.",
                "Sciatic nerve not involved — important to exclude."
            ),
            "MRI thigh": (
                "MRI: Grade III biceps femoris tear at myotendinous\n"
                "  junction. No proximal avulsion from ischial tuberosity.\n"
                "  Haematoma 4 x 2cm at tear site.",
                "Confirms Grade III. No avulsion = conservative Rx appropriate."
            ),
        },
        "options": [
            "Grade I hamstring strain",
            "Grade III biceps femoris tear",
            "Proximal hamstring avulsion fracture",
            "Sciatic nerve injury",
        ],
        "correct": 1,
        "hint": (
            "Sudden pop, immediate stop, posterior thigh bruising tracking\n"
            "  distally, palpable defect, 2/5 strength, MRI showing complete\n"
            "  disruption. The grade and specific muscle are both in the answer."
        ),
        "explanation": (
            "Grade III biceps femoris tear confirmed.\n\n"
            "  The mechanism (explosive sprint), immediate audible pop,\n"
            "  cessation of activity, significant tracking bruising, palpable\n"
            "  defect, and MRI showing complete myotendinous junction disruption\n"
            "  with haematoma are all consistent. No ischial avulsion = good\n"
            "  news for conservative management."
        ),
        "management": (
            "Week 0–2: PRICE, crutches, pain-free ROM only.\n"
            "  Week 2–6: Progressive hamstring strengthening (isometric → isotonic).\n"
            "  Week 6–12: Sports-specific running rehab, Nordic curls.\n"
            "  Return to sprint training: 12–16 weeks.\n"
            "  PRP injection may accelerate healing — refer sports medicine."
        ),
    },
    {
        "id": 5,
        "sport": "Basketball",
        "athlete": "Deven, 23",
        "role": "Power forward — Semi-professional",
        "presenting": (
            "Deven landed from a rebound and felt his knee 'buckle inward.'\n"
            "  Immediate large swelling within the hour. He heard a distinct\n"
            "  pop. Now cannot straighten his knee fully and reports major\n"
            "  instability — unable to trust the joint."
        ),
        "vitals": [
            ("Mechanism",   "Valgus landing from jump"),
            ("Swelling",    "Immediate, large haemarthrosis"),
            ("Pop heard",   "Yes — distinct"),
            ("Instability", "Significant — cannot weight trust"),
            ("ROM",         "Cannot fully extend"),
        ],
        "investigations": {
            "Lachman test": (
                "Lachman: POSITIVE — significant anterior tibial translation,\n"
                "  soft endpoint. Grade 2+ (>5mm).",
                "Primary ACL test. Significant finding."
            ),
            "Anterior drawer test": (
                "Anterior drawer at 90° flexion: POSITIVE.",
                "Confirms anterior instability."
            ),
            "Valgus stress test": (
                "Valgus stress at 30°: mild laxity. MCL Grade I involvement\n"
                "  possible but joint line intact.",
                "MCL involvement possible — common combined injury."
            ),
            "MRI knee": (
                "MRI: Complete ACL tear. Bone bruise lateral femoral condyle\n"
                "  + posterior tibial plateau (pivot shift pattern).\n"
                "  Intact MCL. No meniscal tear.",
                "Lateral 'kissing contusions' = classic pivot shift pattern."
            ),
        },
        "options": [
            "Grade III MCL tear",
            "Posterior cruciate ligament tear",
            "Anterior cruciate ligament rupture",
            "Patella dislocation",
        ],
        "correct": 2,
        "hint": (
            "Pop + immediate haemarthrosis + positive Lachman + valgus\n"
            "  landing + lateral bone bruise pattern on MRI. This is the\n"
            "  most feared knee injury in basketball and the most common\n"
            "  reason for surgical reconstruction in sports medicine."
        ),
        "explanation": (
            "ACL rupture — confirmed.\n\n"
            "  The classic triad: audible pop, immediate large haemarthrosis,\n"
            "  positive Lachman with soft endpoint. The valgus landing mechanism\n"
            "  and lateral 'kissing' bone bruise pattern (pivot shift injury) are\n"
            "  pathognomonic. MRI confirms complete tear. Immediate surgical\n"
            "  referral indicated."
        ),
        "management": (
            "Urgent orthopaedic referral — ACL reconstruction (BPTB or\n"
            "  hamstring autograft). Pre-op physio: reduce swelling, restore\n"
            "  quad activation. Post-op rehab: 9–12 months minimum.\n"
            "  Return to play based on functional criteria — hop tests,\n"
            "  quad symmetry index >90% — NOT time alone."
        ),
    },
    {
        "id": 6,
        "sport": "Tennis",
        "athlete": "Priya, 31",
        "role": "Amateur — Club level, 3x/week",
        "presenting": (
            "3-month history of lateral elbow pain, progressively worsening.\n"
            "  Worse with backhand strokes and gripping objects (coffee mug,\n"
            "  handshake). No trauma. Pain precisely at the lateral epicondyle.\n"
            "  Brief rest periods haven't helped."
        ),
        "vitals": [
            ("Mechanism",   "Overuse / repetitive wrist extension"),
            ("Location",    "Lateral epicondyle — precise"),
            ("Duration",    "3 months, progressive"),
            ("Activity",    "Tennis 3x/week + desk job"),
            ("Grip pain",   "Yes — daily activities affected"),
        ],
        "investigations": {
            "Cozen's test": (
                "Cozen's: POSITIVE — pain reproduced with resisted wrist\n"
                "  extension with elbow in full extension.",
                "Classic test for lateral epicondylalgia. Positive."
            ),
            "Mill's manoeuvre": (
                "Mill's: POSITIVE — pain with passive wrist flexion\n"
                "  with elbow extended.",
                "Second test positive. Pattern confirmed."
            ),
            "Grip dynamometer": (
                "Grip strength: 62% of contralateral side. Pain limiting\n"
                "  maximal effort.",
                "Significant functional deficit quantified."
            ),
            "Ultrasound elbow": (
                "USS: Hypoechoic area and neovascularity at ECRB tendon\n"
                "  origin. No complete tear.",
                "Degenerative tendinopathic changes confirmed — not 'itis'."
            ),
        },
        "options": [
            "Radial tunnel syndrome",
            "Lateral epicondyle stress fracture",
            "Lateral epicondylalgia (tennis elbow)",
            "Posterior interosseous nerve entrapment",
        ],
        "correct": 2,
        "hint": (
            "3 months, lateral elbow, two positive tests for wrist extension\n"
            "  resistance, grip weakness at 62%, degenerative USS changes at\n"
            "  ECRB origin. The sport she plays is literally in the name."
        ),
        "explanation": (
            "Lateral epicondylalgia — colloquially 'tennis elbow'.\n\n"
            "  Technically a tendinopathy (degenerative) of the ECRB origin,\n"
            "  NOT a true 'itis' (no inflammation on histology). Chronic\n"
            "  overload leads to failed healing response. Cozen's and Mill's\n"
            "  both positive with significant grip deficit confirms diagnosis."
        ),
        "management": (
            "Load management + eccentric wrist extension exercises (the\n"
            "  gold standard — Tyler Twist protocol). Physiotherapy.\n"
            "  Evidence does NOT support corticosteroid injection long-term\n"
            "  (worse outcomes at 1 year). PRP emerging as effective.\n"
            "  Rarely requires surgery (ECRB release). 80% resolve by 1 year."
        ),
    },
    {
        "id": 7,
        "sport": "Gymnastics",
        "athlete": "Zara, 15",
        "role": "Artistic gymnast — Regional squad",
        "presenting": (
            "6-week progressive low back pain, unilateral (left side), worse\n"
            "  with back extension movements and single-leg activities. No\n"
            "  acute trauma. Training 20+ hours per week. Pain reproduced\n"
            "  by standing on the left leg and arching back."
        ),
        "vitals": [
            ("Mechanism",   "Repetitive hyperextension loading"),
            ("Location",    "Lower back — left, paravertebral"),
            ("Duration",    "6 weeks, progressive"),
            ("Training",    "20+ hours/week gymnastics"),
            ("Age",         "15 years — skeletally immature"),
        ],
        "investigations": {
            "Single leg extension (stork) test": (
                "Stork test: POSITIVE on left — pain reproduced in lower\n"
                "  back with single-leg stance and extension. Negative right.",
                "Classic provocative test for pars interarticularis defect."
            ),
            "X-ray lumbosacral spine": (
                "X-ray lateral: subtle lucency at L4 pars interarticularis\n"
                "  region left side — 'Scotty dog sign' collar visible.",
                "Pars defect visible. X-ray may miss early stress reactions."
            ),
            "MRI spine": (
                "MRI: L4 pars stress reaction left side. Bone marrow oedema\n"
                "  on STIR sequence. No spondylolisthesis.",
                "Confirms active stress reaction — early/intermediate stage."
            ),
            "Neurological exam": (
                "Full neurological examination: INTACT. No motor weakness,\n"
                "  no radicular symptoms, no bowel/bladder involvement.",
                "No nerve root compromise — reassuring."
            ),
        },
        "options": [
            "L4/L5 disc herniation",
            "Spondylolysis (pars stress reaction)",
            "Sacroiliac joint dysfunction",
            "Scheuermann's kyphosis",
        ],
        "correct": 1,
        "hint": (
            "Young gymnast (skeletally immature), high-volume extension-\n"
            "  dominant sport, unilateral low back pain worse with extension,\n"
            "  positive stork test, pars region changes on imaging. This is\n"
            "  THE injury in young gymnasts worldwide."
        ),
        "explanation": (
            "Spondylolysis — pars interarticularis stress reaction.\n\n"
            "  Classic presentation: young athlete (<20 years), high-volume\n"
            "  hyperextension sport (gymnastics, cricket fast bowling, swimming\n"
            "  butterfly), unilateral low back pain worse with extension, positive\n"
            "  stork test, MRI showing pars oedema. No spondylolisthesis = good\n"
            "  prognosis with conservative management."
        ),
        "management": (
            "Activity restriction — stop gymnastics temporarily.\n"
            "  Rigid Boston brace 23 hours/day for 3–6 months (active\n"
            "  stress reaction). Core stability physiotherapy.\n"
            "  Serial imaging to confirm healing. Gradual return to\n"
            "  gymnastics at 3–6 months. Monitor for spondylolisthesis."
        ),
    },
    {
        "id": 8,
        "sport": "Rugby",
        "athlete": "Marcus, 28",
        "role": "Prop — Regional club",
        "presenting": (
            "Took a direct blow to the outer hip in a tackle 5 days ago.\n"
            "  Significant bruising developed over 48 hours. Walking with\n"
            "  an antalgic gait. Point tender over the iliac crest.\n"
            "  No neurology. No groin pain."
        ),
        "vitals": [
            ("Mechanism",   "Direct lateral blow in tackle"),
            ("Location",    "Iliac crest — anterosuperior"),
            ("Neurology",   "None"),
            ("Gait",        "Antalgic"),
            ("Bruising",    "Significant, well-demarcated"),
        ],
        "investigations": {
            "Palpation": (
                "Exquisite point tenderness at ASIS and anterosuperior\n"
                "  iliac crest. No crepitus. No step deformity palpable.",
                "Localised — not diffuse. Helps narrow injury."
            ),
            "X-ray pelvis": (
                "X-ray AP pelvis: NO fracture. NO avulsion. Intact bony\n"
                "  cortex throughout. Soft tissue swelling laterally.",
                "Fracture excluded. Soft tissue injury confirmed."
            ),
            "FABER test / hip ROM": (
                "FABER: mild discomfort at end range only. Full hip ROM\n"
                "  maintained in all planes.",
                "Hip joint not primarily affected."
            ),
            "Pelvic compression test": (
                "Pelvic compression: NO sacroiliac pain reproduced.\n"
                "  SI joint excluded from differential.",
                "Confirms injury localised to iliac crest / soft tissue."
            ),
        },
        "options": [
            "Iliac crest avulsion fracture",
            "Hip pointer (iliac crest contusion)",
            "Greater trochanteric bursitis",
            "Sacroiliac joint sprain",
        ],
        "correct": 1,
        "hint": (
            "Direct blow, iliac crest, significant bruising, no fracture\n"
            "  on X-ray, no hip joint involvement, contact sport.\n"
            "  This injury has a descriptive name that sounds like\n"
            "  something you'd get from a finger poking your hip."
        ),
        "explanation": (
            "Hip pointer — contusion of the iliac crest.\n\n"
            "  Direct trauma causes bruising of the iliac crest and\n"
            "  overlying soft tissues including the tensor fascia lata\n"
            "  origin. X-ray clears fracture. Point tenderness, ecchymosis,\n"
            "  antalgic gait without neurology or hip joint involvement\n"
            "  are all consistent."
        ),
        "management": (
            "PRICE protocol, NSAIDs, protected weight-bearing initially.\n"
            "  Padding on return to contact sport (essential — further\n"
            "  blows risk myositis ossificans). Graduated return 1–3 weeks\n"
            "  depending on severity. Physiotherapy for pain-free ROM."
        ),
    },
    {
        "id": 9,
        "sport": "Cycling",
        "athlete": "Alex, 34",
        "role": "Road cyclist — Sportive rider",
        "presenting": (
            "6 weeks of bilateral anterior knee pain, worst after long\n"
            "  rides and going downstairs. Aching pain just below the\n"
            "  kneecap (infrapatellar), not behind it. No swelling.\n"
            "  Rides 200+ km/week. Recently increased mileage by 30%."
        ),
        "vitals": [
            ("Mechanism",   "Overuse / repetitive knee extension"),
            ("Location",    "Infrapatellar — bilateral"),
            ("Duration",    "6 weeks"),
            ("Mileage",     "200+ km/week — recent ramp up"),
            ("Swelling",    "None"),
        ],
        "investigations": {
            "Patellar tendon palpation": (
                "Palpation: TENDER at patellar tendon origin — inferior\n"
                "  pole of patella bilaterally. Reproducible pain.",
                "Infrapatellar pole tenderness is the KEY location here."
            ),
            "Clarke's / grind test": (
                "Clarke's test: NEGATIVE. No patellofemoral crepitus\n"
                "  or retropatellar pain.",
                "Patellofemoral syndrome less likely."
            ),
            "VISA-P questionnaire": (
                "VISA-P score: 52/100 (normal = 100). Pain limits\n"
                "  ability to complete training and daily function.",
                "Confirms significant symptomatic tendinopathy."
            ),
            "Ultrasound patellar tendons": (
                "USS bilateral: hypoechoic region at tendon origin\n"
                "  with neovascularity. No tear.",
                "Tendinopathic changes confirmed bilaterally."
            ),
        },
        "options": [
            "Patellofemoral pain syndrome",
            "Hoffa's fat pad impingement",
            "Patellar tendinopathy (jumper's knee)",
            "Osgood-Schlatter disease",
        ],
        "correct": 2,
        "hint": (
            "Infrapatellar (below, not behind the kneecap), tender at\n"
            "  patellar tendon ORIGIN, tendinopathic USS changes bilaterally,\n"
            "  negative Clarke's, load-related pain from mileage ramp-up.\n"
            "  The colloquial name references a different jumping sport."
        ),
        "explanation": (
            "Patellar tendinopathy — 'jumper's knee' (despite this being a\n"
            "  cyclist!).\n\n"
            "  Key differentiator: pain is INFRAPATELLAR (below kneecap) not\n"
            "  retropatellar (behind kneecap — PFPS). Inferior patellar pole\n"
            "  tenderness and USS showing hypoechogenicity + neovascularisation\n"
            "  are diagnostic. Bilateral presentation common in cyclists\n"
            "  following rapid training load increases (too much, too soon)."
        ),
        "management": (
            "Load management — reduce mileage 30% immediately.\n"
            "  Saddle height assessment (too low = increased patellar tendon\n"
            "  load). Heavy slow resistance training: isometric loading first\n"
            "  (pain relief), then isotonic. VISA-P monitoring for progress.\n"
            "  DO NOT inject corticosteroid — weakens tendon structure."
        ),
    },
    {
        "id": 10,
        "sport": "Cricket",
        "athlete": "Bilal, 20",
        "role": "Wicketkeeper — Club level",
        "presenting": (
            "Bilal jammed his right thumb catching a fast delivery last week.\n"
            "  Swelling at the base of the thumb, bruising, and weakness of\n"
            "  pinch grip. He can move the thumb but it feels 'loose' and\n"
            "  he cannot grip the bat without pain."
        ),
        "vitals": [
            ("Mechanism",   "Forced thumb abduction — catching"),
            ("Location",    "Thumb MCP joint — ulnar side"),
            ("Instability", "Reported — 'loose' feeling"),
            ("Grip",        "Weak pinch — pain limiting"),
            ("Swelling",    "Present at MCP joint"),
        ],
        "investigations": {
            "Palpation": (
                "Tenderness localised to ULNAR aspect of thumb MCP\n"
                "  joint. Swelling present. No anatomical snuffbox\n"
                "  tenderness (scaphoid excluded).",
                "Ulnar-side location is critical in this mechanism."
            ),
            "Valgus (abduction) stress test": (
                "Valgus stress at 30° MCP flexion: POSITIVE — 30°\n"
                "  laxity vs 10° contralateral. SOFT endpoint (no firm stop).",
                "30° laxity + no firm endpoint = likely COMPLETE tear."
            ),
            "X-ray thumb": (
                "X-ray AP and lateral: NO fracture. No bony avulsion\n"
                "  fragment.",
                "Pure ligamentous injury confirmed."
            ),
            "Stener lesion assessment": (
                "Clinical palpation: firm palpable mass proximal to\n"
                "  joint line on ulnar side = Stener lesion present.",
                "CRITICAL: Stener lesion = adductor aponeurosis interposition = surgery."
            ),
        },
        "options": [
            "Scaphoid fracture",
            "Radial collateral ligament tear",
            "UCL rupture — Gamekeeper's / Skier's thumb",
            "Thumb metacarpal fracture",
        ],
        "correct": 2,
        "hint": (
            "Wicketkeeper, forced abduction on catching, ULNAR side\n"
            "  tenderness, valgus laxity with soft endpoint, likely Stener\n"
            "  lesion palpable. This injury has an eponym referencing\n"
            "  Scottish gamekeepers and is also common in skiers."
        ),
        "explanation": (
            "UCL rupture — Gamekeeper's thumb (also Skier's thumb).\n\n"
            "  Forced thumb abduction disrupts the ulnar collateral ligament\n"
            "  at the thumb MCP. Complete tear (soft endpoint, 30° laxity)\n"
            "  with Stener lesion (adductor aponeurosis folds over the torn\n"
            "  UCL, preventing healing) means this CANNOT heal conservatively\n"
            "  — surgical repair is mandatory."
        ),
        "management": (
            "URGENT hand surgery referral — Stener lesion requires\n"
            "  surgical UCL repair to restore proper anatomy.\n"
            "  Thumb spica splint while awaiting surgery.\n"
            "  Post-op: splint 6 weeks, hand therapy, return to\n"
            "  wicketkeeping 3–4 months. Without surgery: chronic\n"
            "  instability and grip weakness."
        ),
    },
]

# ─── UI HELPERS ──────────────────────────────────────────────────────────────

WIDTH = 68

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def line(char="─", colour=C.TEAL):
    print(col(colour, char * WIDTH))

def header_bar(text, colour=C.TEAL):
    pad = (WIDTH - len(text) - 2) // 2
    bar = "─" * pad + " " + text + " " + "─" * pad
    if len(bar) < WIDTH:
        bar += "─"
    print(col(colour, bar))

def box_line(text=""):
    print(col(C.DIM, "│") + " " + text)

def slow_print(text, delay=0.012, colour=None):
    full = col(colour, text) if colour else text
    for ch in full:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def pause(msg="Press ENTER to continue..."):
    print()
    input(dim(f"  {msg}"))

def get_input(prompt, valid_range):
    while True:
        try:
            raw = input(teal(f"\n  {prompt} ")).strip()
            val = int(raw)
            if val in valid_range:
                return val
        except (ValueError, KeyboardInterrupt):
            pass
        print(red(f"  Enter a number between {min(valid_range)} and {max(valid_range)}."))

def wrap_text(text, indent=4, width=WIDTH):
    words = text.replace("\n", " ").split()
    lines, current = [], ""
    for w in words:
        if len(current) + len(w) + 1 <= width - indent:
            current = (current + " " + w).strip()
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return (" " * indent + ("\n" + " " * indent).join(lines))


# ─── SCREENS ─────────────────────────────────────────────────────────────────

def splash_screen():
    clear()
    print()
    print(teal("  ╔══════════════════════════════════════════════════════════════╗"))
    print(teal("  ║") + bold(gold("          CoachIQ  ─  Sports Injury Diagnosis Simulator       ")) + teal("║"))
    print(teal("  ║") + dim("          Built under the OrthoAI Project  |  Python 3         ") + teal("║"))
    print(teal("  ╚══════════════════════════════════════════════════════════════╝"))
    print()
    slow_print("  Work through 10 real athlete cases.", colour=C.WHITE)
    slow_print("  Order investigations. Make your diagnosis.", colour=C.WHITE)
    slow_print("  Learn the evidence-based management.", colour=C.WHITE)
    print()
    print(dim("  ─ 10 cases  ─ 5 sports  ─ real clinical findings  ─ scoring  ─"))
    print()
    print(teal("  [1]") + "  Start simulation")
    print(teal("  [2]") + "  How to play")
    print(teal("  [3]") + "  High scores")
    print(teal("  [0]") + "  Exit")
    print()
    choice = get_input("→", [0, 1, 2, 3])
    return choice


def how_to_play():
    clear()
    header_bar("HOW TO PLAY", C.CYAN)
    print()
    sections = [
        ("OBJECTIVE",
         "Diagnose the athlete correctly across 10 sports injury cases.\n"
         "  Each case mimics a real clinical consultation."),
        ("PHASE 1 — HISTORY",
         "Read the athlete's presenting complaint and vital signs.\n"
         "  These are free — no cost to review."),
        ("PHASE 2 — INVESTIGATIONS",
         "You have 4 investigations available per case.\n"
         "  First 2 are FREE. Each additional costs 5 pts.\n"
         "  Choose wisely — a good clinician doesn't over-investigate."),
        ("PHASE 3 — DIAGNOSIS",
         "Select from 4 options. Correct = +20 pts.\n"
         "  Using the hint first = only +10 pts if correct.\n"
         "  Wrong = 0 pts for that case."),
        ("SCORING",
         "Max score: 200 pts (10 x 20 pts).\n"
         "  Grade A: 160+  |  B: 120–159  |  C: 80–119  |  D: <80"),
        ("TIP",
         "Read every investigation result carefully — the interpretation\n"
         "  note tells you what the finding means clinically."),
    ]
    for title, body in sections:
        print("  " + bold(teal(title)))
        print("  " + dim(body.replace("\n  ", "\n  ")))
        print()
    pause()


def show_high_scores():
    clear()
    header_bar("HIGH SCORES", C.GOLD)
    print()
    scores = load_scores()
    if not scores:
        print(dim("  No scores yet. Play a game first!"))
    else:
        print(f"  {'#':<4} {'Name':<20} {'Score':<10} {'Grade':<6} {'Date'}")
        line("─", C.DIM)
        for i, s in enumerate(scores[:10], 1):
            grade_col = green if s['grade'] == 'A' else (cyan if s['grade'] == 'B' else (yellow if s['grade'] == 'C' else red))
            print(f"  {i:<4} {s['name']:<20} {gold(str(s['score'])+' pts'):<18} {grade_col(s['grade']):<14} {dim(s['date'])}")
    print()
    pause()


SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coachiq_scores.json")

def load_scores():
    try:
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_score(name, score, grade):
    scores = load_scores()
    scores.append({
        "name": name,
        "score": score,
        "grade": grade,
        "date": datetime.now().strftime("%d %b %Y")
    })
    scores.sort(key=lambda x: x["score"], reverse=True)
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(scores[:20], f, indent=2)
    except Exception:
        pass


# ─── GAME LOGIC ──────────────────────────────────────────────────────────────

def render_athlete_card(case):
    line()
    print()
    sport_col = {
        "Cricket": teal, "Football": green, "Swimming": cyan,
        "Athletics": orange, "Basketball": coral, "Tennis": purple,
        "Rugby": orange, "Gymnastics": mint, "Cycling": gold,
    }.get(case["sport"], teal)

    print(f"  {bold(case['athlete']):<30} {sport_col('[ ' + case['sport'] + ' ]')}")
    print(f"  {dim(case['role'])}")
    print()
    print(f"  {bold('PRESENTING COMPLAINT')}")
    print(f"  {case['presenting']}")
    print()
    print(f"  {bold('VITALS & HISTORY')}")
    for k, v in case["vitals"]:
        print(f"  {teal(k+':'):<22} {v}")
    print()
    line()


def investigations_phase(case):
    invest_keys = list(case["investigations"].keys())
    selected = []
    invest_cost = 0

    while True:
        print()
        print(f"  {bold('INVESTIGATIONS')}  {dim('(first 2 free · +5 pts each after)')}")
        print()
        for i, key in enumerate(invest_keys, 1):
            done = i - 1 in selected
            status = green("✓") if done else dim("○")
            cost_note = "" if len(selected) < 2 or done else dim(" [−5 pts]")
            print(f"  {status} {teal(str(i)+')') if not done else dim(str(i)+')')} {dim(key) if done else key}{cost_note}")

        already_run = len(selected)
        print()
        print(f"  {teal('5)')} Proceed to diagnosis  {dim('→')}")
        print()

        if already_run == 0:
            prompt = "Select investigation (1–4) or 5 to diagnose:"
        else:
            prompt = "Another investigation (1–4) or 5 to diagnose:"

        available = [i for i in range(1, 5) if (i - 1) not in selected] + [5]
        choice = get_input(prompt, available)

        if choice == 5:
            break

        idx = choice - 1
        selected.append(idx)
        key = invest_keys[idx]
        result, interpretation = case["investigations"][key]

        if len(selected) > 2:
            invest_cost += 5
            print(yellow(f"\n  [−5 pts] Investigation cost applied."))

        print()
        header_bar(key.upper(), C.CYAN)
        print()
        print(f"  {result}")
        print()
        print(f"  {dim('Clinical note:')} {mint(interpretation)}")
        print()
        pause("Press ENTER to continue...")

    return invest_cost


def diagnosis_phase(case, hint_available=True):
    options = case["options"]
    hint_used = False

    while True:
        print()
        header_bar("MAKE YOUR DIAGNOSIS", C.GOLD)
        print()
        letters = ["A", "B", "C", "D"]
        for i, opt in enumerate(options):
            print(f"  {gold(letters[i]+')')} {opt}")
        print()
        if hint_available and not hint_used:
            print(f"  {teal('H)')} Show hint  {dim('(−10 pts · correct answer = +10 instead of +20)')}")
            print()
        print(f"  {dim('Enter A, B, C or D' + (' or H' if hint_available and not hint_used else '') + ':')}")
        print()

        valid = ["1", "2", "3", "4", "a", "b", "c", "d"]
        if hint_available and not hint_used:
            valid += ["h"]

        while True:
            try:
                raw = input(teal("  → ")).strip().lower()
                if raw in valid:
                    break
            except KeyboardInterrupt:
                sys.exit(0)
            print(red("  Invalid. Enter A, B, C, D" + (" or H." if hint_available and not hint_used else ".")))

        if raw == "h":
            hint_used = True
            print()
            header_bar("HINT", C.YELLOW)
            print()
            print(f"  {yellow(case['hint'])}")
            print()
            pause("Press ENTER to make your diagnosis...")
            continue

        answer_idx = ["a", "b", "c", "d"].index(raw) if raw in ["a", "b", "c", "d"] else int(raw) - 1
        return answer_idx, hint_used


def show_result(case, answer_idx, hint_used):
    correct_idx = case["correct"]
    is_correct = answer_idx == correct_idx
    pts = 0
    if is_correct:
        pts = 10 if hint_used else 20

    print()
    if is_correct:
        header_bar("✓  CORRECT DIAGNOSIS", C.GREEN)
        print()
        slow_print(f"  {'+'+str(pts)+' pts'}", colour=C.GREEN)
    else:
        header_bar("✗  INCORRECT", C.RED)
        print()
        print(red(f"  Your answer:   {case['options'][answer_idx]}"))
        print(green(f"  Correct:       {case['options'][correct_idx]}"))
        print(dim(f"  +0 pts"))

    print()
    print(f"  {bold('EXPLANATION')}")
    print()
    print(f"  {case['explanation']}")
    print()
    line("─", C.DIM)
    print()
    print(f"  {bold('MANAGEMENT')}")
    print()
    print(f"  {mint(case['management'])}")
    print()
    line()

    return pts


def run_game():
    clear()
    print()
    print(teal("  STARTING SIMULATION"))
    print()
    try:
        name = input(teal("  Enter your name: ")).strip() or "Player"
    except KeyboardInterrupt:
        return

    cases = CASES.copy()
    random.shuffle(cases)

    total_score = 0
    breakdown = []

    for case_num, case in enumerate(cases, 1):
        clear()
        print()
        print(f"  {dim('─' * 20)}  {bold(teal(f'CASE {case_num} OF {len(cases)}'))}  {dim('─' * 20)}")
        print(f"  {dim('Score: ')}{gold(str(total_score) + ' pts')}")
        print()

        render_athlete_card(case)
        pause("Press ENTER to proceed to investigations...")

        # Investigations
        invest_cost = investigations_phase(case)
        if invest_cost > 0:
            total_score = max(0, total_score - invest_cost)
            print(yellow(f"\n  Total investigation cost this case: −{invest_cost} pts"))
            print(dim(f"  Running score: {total_score} pts"))

        clear()
        print()
        print(f"  {dim('─' * 20)}  {bold(teal(f'CASE {case_num} — DIAGNOSIS'))}  {dim('─' * 20)}")
        print(f"  {bold(case['athlete'])} | {dim(case['sport'])}")
        print(f"  {dim('Score so far: ')}{gold(str(total_score) + ' pts')}")

        answer_idx, hint_used = diagnosis_phase(case)
        pts_earned = show_result(case, answer_idx, hint_used)
        total_score += pts_earned

        breakdown.append({
            "case": f"Case {case_num}",
            "sport": case["sport"],
            "correct_dx": case["options"][case["correct"]],
            "your_dx": case["options"][answer_idx],
            "correct": answer_idx == case["correct"],
            "pts": pts_earned,
            "invest_cost": invest_cost,
        })

        print(f"  {dim('Score: ')}{gold(str(total_score) + ' pts')}")
        print()
        if case_num < len(cases):
            pause(f"Press ENTER for Case {case_num + 1}...")
        else:
            pause("Press ENTER to see your final results...")

    show_final_results(name, total_score, breakdown)


def show_final_results(name, total_score, breakdown):
    clear()
    max_score = len(CASES) * 20
    pct = round((total_score / max_score) * 100)

    if pct >= 80:
        grade, trophy, grade_col = "A", "★★★", green
        message = "Outstanding clinician! Ready for sports medicine."
    elif pct >= 60:
        grade, trophy, grade_col = "B", "★★☆", cyan
        message = "Solid diagnostic reasoning. Keep studying."
    elif pct >= 40:
        grade, trophy, grade_col = "C", "★☆☆", yellow
        message = "Developing — review the cases you missed."
    else:
        grade, trophy, grade_col = "D", "☆☆☆", red
        message = "Back to the textbooks — anatomy and clinical tests."

    print()
    print(teal("  ╔══════════════════════════════════════════════════════════════╗"))
    print(teal("  ║") + bold("                    SIMULATION COMPLETE                       ") + teal("║"))
    print(teal("  ╚══════════════════════════════════════════════════════════════╝"))
    print()
    print(f"  {dim('Player:')} {bold(name)}")
    print(f"  {dim('Score: ')} {bold(gold(str(total_score) + ' / ' + str(max_score) + ' pts'))}  {dim('(' + str(pct) + '%)')}")
    print(f"  {dim('Grade: ')} {bold(grade_col(grade))}  {trophy}")
    print(f"  {dim(message)}")
    print()
    line("─", C.DIM)
    print()
    print(f"  {'CASE':<10} {'SPORT':<14} {'YOUR DIAGNOSIS':<32} {'PTS'}")
    line("─", C.DIM)
    for b in breakdown:
        pts_str = green(f"+{b['pts']}") if b["pts"] > 0 else red("+0")
        dx_str = (green("✓ ") if b["correct"] else red("✗ ")) + b["your_dx"][:28]
        print(f"  {dim(b['case']):<10} {b['sport']:<14} {dx_str:<40} {pts_str}")
        if b["invest_cost"] > 0:
            cost_note = f"  Investigation cost: −{b['invest_cost']} pts"
            print(dim(f"  {'':10} {'':14} {cost_note}"))

    line("─", C.DIM)
    print()

    correct_count = sum(1 for b in breakdown if b["correct"])
    print(f"  Correct diagnoses: {green(str(correct_count))} / {len(CASES)}")
    print()

    save_score(name, total_score, grade)
    print(dim("  Score saved to leaderboard."))
    print()
    pause("Press ENTER to return to main menu...")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    while True:
        choice = splash_screen()
        if choice == 1:
            run_game()
        elif choice == 2:
            how_to_play()
        elif choice == 3:
            show_high_scores()
        elif choice == 0:
            clear()
            print()
            print(teal("  CoachIQ — Sports Injury Diagnosis Simulator"))
            print(dim("  Built by Mark | OrthoAI Project"))
            print()
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(dim("\n  Exiting CoachIQ. Good luck with your studies."))
        sys.exit(0)
